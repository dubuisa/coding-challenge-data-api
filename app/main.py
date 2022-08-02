from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy.future import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.db import get_session
from app.models import Dialog, DialogBase, DialogInput

app = FastAPI()

cache = dict()

@app.get("/status")
async def pong():
    return {"status": "up"}



@app.post("/data/{customerId}/{dialogId}")
async def add_dialog(customerId: int,
                     dialogId: int,
                     dialog_input: DialogInput):

    dialog = Dialog(
        customerId = customerId,
        dialogId=dialogId,
        text = dialog_input.text,
        language = dialog_input.language
    )
    dialogs = cache.get(dialogId)
    if dialogs:
        dialogs.append(dialog)
    else:
        cache[dialogId] = [dialog]
    print(cache[dialogId])



@app.post("/consents/{dialogId}")
async def send_consent(dialogId: int,
                      accepted: bool,
                      session: AsyncSession = Depends(get_session)
                      ):
    dialogs = cache.pop(dialogId, None)

    if not dialogs:
        raise HTTPException(status_code=400, detail=f"The {dialogId = } does not exists")
    
    if accepted:
        session.add_all(dialogs)
        await session.commit()
    

@app.get('/data/')
async def get_data(language: str = None,
          customerId: int = None,
          session: AsyncSession = Depends(get_session)):
    
    select_statement = select(Dialog).where(
        (Dialog.customerId == customerId or customerId is None)
        and
        (Dialog.language == language or language is None)
    ).order_by(Dialog.id.desc())
    
    result = await session.execute(select_statement)
    return result


# @app.get("/songs", response_model=list[Song])
# async def get_songs(session: AsyncSession = Depends(get_session)):
#     result = await session.execute(select(Song))
#     songs = result.scalars().all()
#     return [Song(name=song.name, artist=song.artist, year=song.year, id=song.id) for song in songs]


# @app.post("/songs")
# async def add_song(song: SongCreate, session: AsyncSession = Depends(get_session)):
#     song = Song(name=song.name, artist=song.artist, year=song.year)
#     session.add(song)
#     await session.commit()
#     await session.refresh(song)
#     return song
