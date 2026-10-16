from typing import Optional
from datetime import datetime
from pydantic import BaseModel, ConfigDict, Field
from decimal import Decimal



class ExpenseCreate(BaseModel):
    description: str = Field(..., min_length=1, max_length=255)
    category: str = Field(..., min_length=1, max_length=100)
    amount: Decimal = Field(..., gt=0, max_digits=12, decimal_places=2)
    

class ExpensesResponse(ExpenseCreate):
    id:int
    created_at:datetime
    updated_at:datetime

    model_config = ConfigDict(from_attributes=True)


class ExpensesUpdate(BaseModel):
    description: Optional[str] = Field(None, min_length=1, max_length=255)
    category: Optional[str] = Field(None, min_length=1, max_length=100)
    amount: Optional[Decimal] = Field(None, gt=0, max_digits=12, decimal_places=2)
