import logging
from datetime import datetime, timezone

from pydantic import BaseModel, ConfigDict, field_serializer, Field


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
    level: str = Field(default=str(logging.INFO), serialization_alias="Level")
    # tag and run_id will be set later through the LoggerAdapter
    tag: str = Field(default=None, serialization_alias="Tag")
    run_id: str = Field(default=None, serialization_alias="RunId")

    status: str = Field(default=None, serialization_alias="Status")
    message: str = Field(serialization_alias="Message")
    duration: float = Field(default=None, serialization_alias="Duration")
