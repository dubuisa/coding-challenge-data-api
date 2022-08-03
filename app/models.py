from typing import Optional
from pydantic import BaseModel
from sqlmodel import SQLModel, Field


class DialogInput(BaseModel):
    text: str
    language: str


class Dialog(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    customerId: int
    dialogId: int
    consent: bool = False
    text: str
    language: str


class ConsentInput(BaseModel):
    is_accepted: bool
