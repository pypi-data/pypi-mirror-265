from __future__ import annotations

import logging
import os
import pprint
from logging import Logger, getLogger, Handler

from azure.core.exceptions import HttpResponseError
from azure.identity import DefaultAzureCredential
from azure.monitor.ingestion import LogsIngestionClient

from logs_ingestion.logs_adapter import LoggerRecordAdapter


# noinspection PyTypeChecker
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
        if isinstance(record.record, list):
            log_body = []
            for body in record.record:
                body.level = record.levelname
                body.message = self.format(record)
                log_body.append(body.model_dump(exclude_none=True, by_alias=True))
        else:
            body = record.record
            body.level = record.levelname
            body.message = self.format(record)
            log_body = body.model_dump(exclude_none=True, by_alias=True)
        _upload_log_body(self._client, log_body)


def get_logger(name, run_id, tag, fmt=None):
    logger: Logger = getLogger(name)
    handler = _LogsIngestionHandler()
    handler.setFormatter(logging.Formatter(fmt, validate=False))
    logger.addHandler(handler)
    adapter = LoggerRecordAdapter(logger, {"run_id": run_id, "tag": tag})
    return adapter
