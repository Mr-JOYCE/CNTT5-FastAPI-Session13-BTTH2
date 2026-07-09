from datetime import datetime
from typing import Any, Optional

from pydantic import BaseModel, ConfigDict, field_validator


class BoardingSlotBase(BaseModel):
    slot_number: str
    room_size: str
    price_per_day: float
    status: str = "VACANT"

    @field_validator("slot_number")
    @classmethod
    def validate_slot_number(cls, v: str) -> str:
        if not v or not v.strip():
            raise ValueError("slot_number không được để trống")
        return v.strip()

    @field_validator("room_size")
    @classmethod
    def validate_room_size(cls, v: str) -> str:
        valid_sizes = {"SMALL", "MEDIUM", "LARGE"}
        if v not in valid_sizes:
            raise ValueError(f"room_size phải là một trong {sorted(valid_sizes)}")
        return v

    @field_validator("price_per_day")
    @classmethod
    def validate_price_per_day(cls, v: float) -> float:
        if v is None or v <= 0:
            raise ValueError("price_per_day phải lớn hơn 0")
        return v

    @field_validator("status")
    @classmethod
    def validate_status(cls, v: str) -> str:
        valid_status = {"VACANT", "OCCUPIED"}
        if v not in valid_status:
            raise ValueError(f"status phải là một trong {sorted(valid_status)}")
        return v


class BoardingSlotCreate(BoardingSlotBase):
    pass


class BoardingSlotUpdate(BaseModel):
    slot_number: Optional[str] = None
    room_size: Optional[str] = None
    price_per_day: Optional[float] = None
    status: Optional[str] = None

    @field_validator("slot_number")
    @classmethod
    def validate_slot_number(cls, v: Optional[str]) -> Optional[str]:
        if v is not None:
            if not v.strip():
                raise ValueError("slot_number không được để trống")
            return v.strip()
        return v

    @field_validator("room_size")
    @classmethod
    def validate_room_size(cls, v: Optional[str]) -> Optional[str]:
        if v is not None:
            valid_sizes = {"SMALL", "MEDIUM", "LARGE"}
            if v not in valid_sizes:
                raise ValueError(f"room_size phải là một trong {sorted(valid_sizes)}")
        return v

    @field_validator("price_per_day")
    @classmethod
    def validate_price_per_day(cls, v: Optional[float]) -> Optional[float]:
        if v is not None and v <= 0:
            raise ValueError("price_per_day phải lớn hơn 0")
        return v

    @field_validator("status")
    @classmethod
    def validate_status(cls, v: Optional[str]) -> Optional[str]:
        if v is not None:
            valid_status = {"VACANT", "OCCUPIED"}
            if v not in valid_status:
                raise ValueError(f"status phải là một trong {sorted(valid_status)}")
        return v


class BoardingSlotRead(BoardingSlotBase):
    id: int

    model_config = ConfigDict(from_attributes=True)


class APIResponse(BaseModel):
    statusCode: int
    message: str
    error: Optional[str] = None
    data: Optional[Any] = None
    path: str
    timestamp: str
