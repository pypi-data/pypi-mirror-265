from __future__ import annotations

from logging import LoggerAdapter

from logs_ingestion.logs_record import LogsRecord


def add_record(extra, record):
    """
    put the record into the extra dict under the key 'record'
    """
    if extra is None:
        extra_new = {"record": record}
    else:
        extra_new = extra
        # extra_new.update(extra)
        extra_new["record"] = record
    return extra_new


class LoggerRecordAdapter(LoggerAdapter):
    def process(self, msg, kwargs):
        """
        move the 'record' argument from kwargs to the extra argument and delete the original entry; push the run_id and
        tag from the logger level to the record body.
        """
        kwargs['extra'] = add_record(kwargs.get('extra'), kwargs.get('record'))
        del kwargs['record']
        # if kwargs.get('extra') is None:
        #     raise ValueError("the extra argument is missing")
        # if kwargs['extra'].get('record') is None:
        #     raise ValueError("the extra argument is missing a record key and value")
        record = kwargs['extra']['record']
        # if we got a list of LogsRecord's, push the run_id and tag down into the list of records
        if isinstance(record, list):
            for body in record:
                if not isinstance(body, LogsRecord):
                    raise TypeError("the 'record' value in the logger line must be of type [LogsRecord]")
                body.run_id = self.extra.get('run_id')
                body.tag = self.extra.get('tag')
        else:
            if not isinstance(record, LogsRecord):
                raise TypeError("the 'record' value in the logger line must be of type LogsRecord")
            # the only thing we do here, is to add the run_id and tag in the record
            record.run_id = self.extra.get('run_id')
            record.tag = self.extra.get('tag')
        return msg, kwargs
