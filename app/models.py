from sqlmodel import SQLModel, Field


class DialogInput(SQLModel):
    text : str
    language: str


class DialogBase(DialogInput):
    customerId: int
    dialogId: int

class Dialog(DialogBase, table=True):
    id: int = Field(default=None, primary_key=True)


