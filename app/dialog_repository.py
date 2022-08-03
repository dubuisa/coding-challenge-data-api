from sqlalchemy import update, delete, insert, select
from app.models import Dialog
from sqlalchemy.ext.asyncio import AsyncSession


async def delete_dialogs(db: AsyncSession, dialogId: int):
    query = (
        delete(Dialog)
            .where(Dialog.dialogId == dialogId)
    )
    await db.execute(query)


async def update_dialogs(db: AsyncSession, dialogId: int):
    query = (
        update(Dialog)
         .values(consent=True)
         .where(Dialog.dialogId == dialogId)        
    )
    await db.execute(query)


async def save_dialog(db: AsyncSession, dialog: Dialog):
    query = insert(Dialog).values(dialog.dict())
    await db.execute(query)

async def select_dialogs(db: AsyncSession, customerId: int, language: str):
    filters = [Dialog.consent == True]
    if customerId is not None:
        filters.append(Dialog.customerId == customerId)
    if language is not None:
        filters.append(Dialog.language == language)

    print(filters)
    query = (
        select(Dialog)
            .where(*filters)
            .order_by(Dialog.id.desc())
    )
    print(query)
    result = await db.execute(query)
    return result.all()