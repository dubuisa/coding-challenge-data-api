from typing import List

from fastapi import Depends, FastAPI, Path, Query
from fastapi.responses import Response
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from app.db import get_session
from app.dialog_repository import (delete_dialogs, save_dialog, select_dialogs,
                                   update_dialogs)
from app.models import ConsentInput, Dialog, DialogInput

app = FastAPI()

@app.get("/status")
async def get_service_status():
    """Retrieves API status"""
    return {"status": "up"}


@app.post(
    "/data/{customerId}/{dialogId}",
    status_code=status.HTTP_201_CREATED,
    response_class=Response,
)
async def add_dialog(
    dialog_input: DialogInput,
    customerId: int = Path(ge=0),
    dialogId: int = Path(ge=0),
    db: AsyncSession = Depends(get_session),
):
    """
    Saves a Dialog to the database.

    Dialog will not be selectable without customer consent.
    """

    await save_dialog(db, dialog=dialog_input, customerId=customerId, dialogId=dialogId)


@app.post(
    "/consents/{dialogId}",
    status_code=status.HTTP_204_NO_CONTENT,
    response_class=Response,
)
async def send_consent(
    consent: ConsentInput,
    dialogId: int = Path(title="The ID of the dialog", ge=0),
    db: AsyncSession = Depends(get_session),
):
    """
    Consent/Refuse to make the `dialogId` dialogs available to improve the model.

    - Giving consent makes the `dialogId` data accessible through GET /data endpoint
    - Refuse deletes Dialogs related to the given `dialogId`
    """

    if consent.is_accepted:
        await update_dialogs(db, dialogId=dialogId)
    else:
        await delete_dialogs(db, dialogId=dialogId)


@app.get("/data/", response_model=List[Dialog])
async def get_data(
    language: str = Query(default=None),
    customerId: int = Query(default=None, ge=0),
    db: AsyncSession = Depends(get_session),
):
    """
    Retrieves consented dialogs sorted by most recent with optional`language` and `customerId` filters.
    """
    
    dialogs = await select_dialogs(db, language=language, customerId=customerId)
    return dialogs
