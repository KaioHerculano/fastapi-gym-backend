from datetime import datetime
from decimal import Decimal
from typing import List, Optional
from uuid import UUID

from pydantic import BaseModel, ConfigDict, field_validator


class PlanCreateSchema(BaseModel):
    name: str
    description: Optional[str] = None
    price: Decimal
    duration_months: int
    is_active: bool = True

    @field_validator('name')
    def validate_name(cls, value: str) -> str:
        if len(value.strip()) < 3:
            raise ValueError('O nome do plano deve ter no mínimo 3 caracteres')
        return value.strip()

    @field_validator('price')
    def validate_price(cls, value: Decimal) -> Decimal:
        if value <= 0:
            raise ValueError('O preço deve ser maior que zero')
        return value

    @field_validator('duration_months')
    def validate_duration_months(cls, value: int) -> int:
        if value <= 0:
            raise ValueError('A duração em meses deve ser maior que zero')
        return value


class PlanUpdateSchema(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    price: Optional[Decimal] = None
    duration_months: Optional[int] = None
    is_active: Optional[bool] = None

    @field_validator('name')
    def validate_name(cls, value: str) -> str:
        if value is not None and len(value) < 3:
            raise ValueError('O nome do plano deve ter no mínimo 3 caracteres')
        return value

    @field_validator('price')
    def validate_price(cls, value: Decimal) -> Decimal:
        if value is not None and value <= 0:
            raise ValueError('O preço deve ser maior que zero')
        return value

    @field_validator('duration_months')
    def validate_duration_months(cls, value: int) -> int:
        if value is not None and value <= 0:
            raise ValueError('A duração em meses deve ser maior que zero')
        return value


class PlanPublicSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    name: str
    description: Optional[str] = None
    price: Decimal
    duration_months: int
    is_active: bool
    created_at: datetime
    updated_at: datetime


class PlanListPublicSchema(BaseModel):
    plans: List[PlanPublicSchema]
    offset: int
    limit: int
