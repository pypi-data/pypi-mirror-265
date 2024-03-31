import os
import pprint
from logging import Logger, getLogger, Handler, LoggerAdapter

from azure.core.exceptions import HttpResponseError
from azure.identity import DefaultAzureCredential
from azure.monitor.ingestion import LogsIngestionClient

from logs_ingestion.logs_record import LogsRecord


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


class _LogsIngestionHandler(Handler):

    def __init__(self, *args, **kwargs):
        super(_LogsIngestionHandler, self).__init__(*args, **kwargs)
        self._client: LogsIngestionClient = _log_ingestion_client()

    def emit(self, record):
        body = record.record
        body.level = record.levelname
        body.message = record.msg
        _upload_log_body(self._client, body.model_dump(by_alias=True))


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
