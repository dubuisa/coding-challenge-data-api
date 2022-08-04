from sqlalchemy import delete, insert, select, update
from sqlalchemy.ext.asyncio import AsyncSession

from app.models import Dialog, DialogInput


async def delete_dialogs(db: AsyncSession, dialogId: int):
    query = delete(Dialog).where(Dialog.dialogId == dialogId)
    await db.execute(query)


async def update_dialogs(db: AsyncSession, dialogId: int):
    query = update(Dialog).values(consent=True).where(Dialog.dialogId == dialogId)
    await db.execute(query)


async def save_dialog(
    db: AsyncSession, dialog: DialogInput, customerId: int, dialogId: int
):
    query = insert(Dialog).values(
        customerId=customerId,
        dialogId=dialogId,
        text=dialog.text,
        language=dialog.language,
    )
    await db.execute(query)


async def select_dialogs(db: AsyncSession, customerId: int, language: str):
    filters = [Dialog.consent == True]
    if customerId is not None:
        filters.append(Dialog.customerId == customerId)
    if language is not None:
        filters.append(Dialog.language == language)

    query = select(Dialog).where(*filters).order_by(Dialog.id.desc())
    result = await db.execute(query)
    return result.scalars().all()
