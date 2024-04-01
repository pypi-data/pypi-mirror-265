import time
from functools import partial, wraps

from azure.monitor.ingestion import LogsIngestionClient

from logs_ingestion.logs_ingestion import _log_ingestion_client, _upload_log_body
from logs_ingestion.logs_adapter import LoggerRecordAdapter
from logs_ingestion.logs_record import LogsRecord


def time_and_log(method=None, *, logger: LoggerRecordAdapter,
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
                                            ).model_dump(exclude_none=True, by_alias=True))
        return result
    return wrapper
