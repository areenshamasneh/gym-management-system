from pydantic import BaseModel, Field, field_validator
from typing import Optional
from enum import Enum


class HallTypeName(str, Enum):
    SAUNA = "Sauna"
    TRAINING = "Training"
    YOGA = "Yoga"
    SWIMMING = "Swimming"


class HallTypeCode(str, Enum):
    SAUNA = "SAUNA"
    TRAINING = "TRAINING"
    YOGA = "YOGA"
    SWIMMING = "SWIMMING"


class HallTypeModel(BaseModel):
    name: HallTypeName
    code: HallTypeCode
    type_description: Optional[str] = Field(None, max_length=255)

    @field_validator('name', mode='before')
    def normalize_name(cls, value):
        normalized_value = value.capitalize()
        if normalized_value not in HallTypeName._value2member_map_:
            raise ValueError(f'Invalid value for name: {value}')
        return normalized_value

    @field_validator('code', mode='before')
    def normalize_code(cls, value):
        normalized_value = value.upper()
        if normalized_value not in HallTypeCode._value2member_map_:
            raise ValueError(f'Invalid value for code: {value}')
        return normalized_value

    @field_validator('code', mode='before')
    def validate_code(cls, value):
        normalized_value = value.upper()
        if normalized_value not in HallTypeCode._value2member_map_:
            raise ValueError(f'Invalid value for code: {value}')
        return normalized_value
