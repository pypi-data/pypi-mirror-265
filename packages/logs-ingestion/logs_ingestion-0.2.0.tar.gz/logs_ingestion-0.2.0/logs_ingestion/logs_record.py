import logging
from datetime import datetime, timezone
from typing import Union, Optional

from pydantic import BaseModel, ConfigDict, field_serializer, Field


class LogsRecord(BaseModel):
    model_config = ConfigDict(ser_json_timedelta='iso8601')

    @field_serializer('time_generated')
    def serialize_dt(self, dt: datetime, _info):
        return dt.isoformat()

    @field_serializer('duration')
    def serialize_float(self, value: float, _info):
        # try to get a sensible number of decimals into the duration
        return float(f'{value:.3f}') if value is not None else None

    @field_serializer('level')
    def serialize_level(self, value: int, _info):
        if isinstance(value, int):
            return logging.getLevelName(value)
        return value

    time_generated: datetime = Field(default=datetime.now(tz=timezone.utc),
                                     serialization_alias="TimeGenerated")
    # level will be overwritten in the actual logging line
    level: Union[int, str] = Field(default=logging.getLevelName(logging.INFO), serialization_alias="Level")
    # tag and run_id will be set later through the LoggerAdapter
    tag: str = Field(default=None, serialization_alias="Tag")
    run_id: str = Field(default=None, serialization_alias="RunId")

    status: Optional[str] = Field(default=None, serialization_alias="Status")
    message: Optional[str] = Field(default=None, serialization_alias="Message")
    duration: float = Field(default=None, serialization_alias="Duration")
