import time
import os
from functools import partial, wraps
from enum import Enum
from logging import Logger, getLogger, Handler, LoggerAdapter
from datetime import datetime, timezone
from pydantic import BaseModel, Field, ConfigDict, field_serializer
import pprint

from azure.core.exceptions import HttpResponseError
from azure.identity import DefaultAzureCredential
from azure.monitor.ingestion import LogsIngestionClient


class Level(Enum):
    """
    INFO: informational messages, no action required
    ERROR: error messages, action and/or alerting is dependent on separate configuration
    CRITICAL: critical messages, action and/or alerting is mandatory
    """
    INFO = 'INFO'
    ERROR = 'ERROR'
    CRITICAL = 'CRITICAL'

    def __str__(self):
        """output the value when string context is needed"""
        return str(self.value)
    

def _log_ingestion_client():
    credential = DefaultAzureCredential()
    endpoint = os.environ["DATA_COLLECTION_ENDPOINT"]
    client = LogsIngestionClient(endpoint=endpoint,
                                 credential=credential,
                                 logging_enable=True)
    return client


def _upload_log_body(client, body):
    rule_id = os.environ["LOGS_DCR_RULE_ID"]
    stream_name = os.environ["LOGS_DCR_STREAM_NAME"]
    try:
        # if is not an array or a string, encapsulate body as an array
        if not isinstance(body, list):
            body = [body]
        pprint.pp(body)
        client.upload(rule_id=rule_id,
                      stream_name=stream_name,
                      logs=body)
    except HttpResponseError as e:
        print(f"Upload to DCR failed: {e}")


def time_and_log(method=None, *, logger: Logger,
                 message=None, status=None):
    if method is None:
        return partial(time_and_log, logger=logger,
                       message=message,
                       status=status)
    client: LogsIngestionClient = _log_ingestion_client()
    tag = logger.extra['tag']
    run_id = logger.extra['run_id']
    log_tag = tag if tag else method.__module__
    log_message = message if message else method.__name__
    @wraps(method)
    def wrapper(*args, **kwargs):
        ts = time.perf_counter()
        result = method(*args, **kwargs)
        te = time.perf_counter()
        _upload_log_body(client, LogsRecord(tag=log_tag, run_id=run_id,
                                            status=status,
                                            message=log_message,
                                            duration=te-ts
                                 ).model_dump(by_alias=True))
        return result
    return wrapper


class _LogsIngestionHandler(Handler):

    def __init__(self, *args, **kwargs):
        super(_LogsIngestionHandler, self).__init__(*args, **kwargs)
        self._client: LogsIngestionClient = _log_ingestion_client()

    def emit(self, record):
        body = record.record
        body.level = record.levelname
        body.message = record.msg
        _upload_log_body(self._client, body.model_dump(by_alias=True))


class LogsRecord(BaseModel):
    model_config = ConfigDict(ser_json_timedelta='iso8601')

    @field_serializer('time_generated')
    def serialize_dt(self, dt: datetime, _info):
        return dt.isoformat()

    @field_serializer('duration')
    def serialize_float(self, value: float, _info):
        # try to get a sensible number of decimals into the duration
        return float(f'{value:.3f}')

    time_generated: datetime = Field(default=datetime.now(tz=timezone.utc),
                                     serialization_alias="TimeGenerated")
    # level will be overwritten in the actual logging line
    level: str = Field(default=str(Level.INFO), serialization_alias="Level")
    # tag and run_id will be set later through the LoggerAdapter
    tag: str = Field(default=None, serialization_alias="Tag")
    run_id: str = Field(default=None, serialization_alias="RunId")

    status: str = Field(default=None, serialization_alias="Status")
    message: str = Field(serialization_alias="Message")
    duration: float = Field(default=None, serialization_alias="Duration")


class _BodyAdapter(LoggerAdapter):
    def process(self, msg, kwargs):
        if kwargs.get('extra') is None:
            raise ValueError("the extra argument is missing")
        if kwargs['extra'].get('record') is None:
            raise ValueError("the extra argument is missing a record key and value")
        record = kwargs['extra']['record']
        if not(isinstance(record, LogsRecord)):
            raise TypeError("the extra 'record' value in the logger line must be of type LogsRecord")
        # the only thing we do here, is to add the run_id and tag in the record
        record.run_id = self.extra.get('run_id')
        record.tag = self.extra.get('tag')
        return msg, kwargs


def get_logger(name, run_id, tag):
    logger: Logger = getLogger(name)
    logger.addHandler(_LogsIngestionHandler())
    adapter = _BodyAdapter(logger, {"run_id": run_id, "tag": tag})
    return adapter


if __name__ == "__main__":
    logger: Logger = get_logger(__name__, run_id="42", tag="logger1")
    logger.warning('testing azure logging', extra={"record": LogsRecord(
                   status="OK",
                   message="message",
                   duration=1.23)})

    logger: Logger = get_logger(__name__, run_id="666", tag="logger2")

    @time_and_log(logger=logger, message="bla", status="timed")
    def test():
        pass

    logger: Logger = get_logger(__name__, run_id="667", tag="logger3")

    @time_and_log(logger=logger, message="bla", status="timed")
    def test2():
        time.sleep(1)
        pass

    test()
    test2()
