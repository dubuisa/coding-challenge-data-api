from typing import List
from fastapi import Depends, FastAPI
from fastapi.responses import Response
from sqlalchemy.ext.asyncio import AsyncSession

from app.db import get_session, init_db
from app.dialog_repository import (
    select_dialogs,
    save_dialog,
    delete_dialogs,
    update_dialogs,
)
from app.models import ConsentInput, Dialog, DialogInput

from starlette import status

app = FastAPI()

cache = dict()


@app.on_event("startup")
async def on_startup():
    init_db()


@app.get("/status")
async def get_service_status():
    return {"status": "up"}


@app.post(
    "/data/{customerId}/{dialogId}",
    status_code=status.HTTP_201_CREATED,
    response_class=Response,
)
async def add_dialog(
    customerId: int,
    dialogId: int,
    dialog_input: DialogInput,
    db: AsyncSession = Depends(get_session),
):

    await save_dialog(db, dialog=dialog_input, customerId=customerId, dialogId=dialogId)


@app.post(
    "/consents/{dialogId}",
    status_code=status.HTTP_204_NO_CONTENT,
    response_class=Response,
)
async def send_consent(
    dialogId: int, consent: ConsentInput, db: AsyncSession = Depends(get_session)
):

    if consent.is_accepted:
        await update_dialogs(db, dialogId=dialogId)
    else:
        await delete_dialogs(db, dialogId=dialogId)


@app.get("/data/", response_model=List[Dialog])
async def get_data(
    language: str = None,
    customerId: int = None,
    db: AsyncSession = Depends(get_session),
):
    dialogs = await select_dialogs(db, language=language, customerId=customerId)
    return dialogs
