import asyncio
from http import client
import pytest
from sqlalchemy import select
from starlette import status

from fastapi.testclient import TestClient
import os

from app.models import Dialog

os.environ["DATABASE_URL"] = "sqlite+aiosqlite:///:memory:"


async def create_test_client():
    """
    Creates a test application with in-memory database
    """

    from app.main import app

    test_client = TestClient(app)

    from app.db import engine
    from sqlalchemy import insert

    async with engine.begin() as conn:

        # create database table
        await conn.run_sync(Dialog.metadata.create_all)

        # add test_data
        await conn.execute(
            insert(Dialog).values(
                [
                    dict(
                        language="fr",
                        text="bonjour",
                        consent=False,
                        customerId=1,
                        dialogId=1,
                    ),
                    dict(
                        language="fr",
                        text="Hello",
                        consent=True,
                        customerId=2,
                        dialogId=1,
                    ),
                    dict(
                        language="en", text="Hi", consent=True, customerId=2, dialogId=1
                    ),
                    dict(
                        language="de",
                        text="Hallo",
                        consent=True,
                        customerId=3,
                        dialogId=2,
                    ),
                ]
            )
        )

    return test_client, engine


async def get_data_by_dialogId(db, dialogId):
    """
    Retrieves Dialogs by `dialogId`

    For test purpose only
    """
    async with db.begin() as conn:
        data = await conn.execute(select(Dialog).where(Dialog.dialogId == dialogId))
        return data.scalars().all()


client, db = asyncio.run(create_test_client())


def test_get_data_by_dialogId():
    data = asyncio.run(get_data_by_dialogId(db, 2))
    assert len(data) == 1


def test_status_up():
    response = client.get("/status")
    assert response.status_code == status.HTTP_200_OK
    assert response.json() == {"status": "up"}


def test_post_dialog_should_return_201():
    payload = {"text": "This is a test!", "language": "en"}
    customerId = 42
    dialogId = 1291
    response = client.post(f"/data/{customerId}/{dialogId}", json=payload)
    assert response.status_code == status.HTTP_201_CREATED


def test_post_empty_dialog_should_return_422():
    customerId = 42
    dialogId = 1291
    response = client.post(f"/data/{customerId}/{dialogId}", json={})
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY


@pytest.mark.parametrize(
    "customerId,dialogId",
    [
        (-1, 42),
        (42, -1),
    ],
)
def test_post_dialog_with_negative_id_should_return_422(customerId, dialogId):
    customerId = -1
    dialogId = 1291
    response = client.post(
        f"/data/{customerId}/{dialogId}",
        json={"text": "This is a test!", "language": "en"},
    )
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
    assert (
        response.json()["detail"][0]["msg"]
        == "ensure this value is greater than or equal to 0"
    )


@pytest.mark.parametrize(
    "language,customerId",
    [
        ("unkown", 2),
        ("fr", 404),
        (None, 404),
        ("unkown", None),
        (None, 1),
    ],
)
def test_empty_search_result_should_return_200(language, customerId):

    response = client.get(
        "/data",
        params={
            "language": language,
            "customerId": customerId,
        },
    )

    assert response.status_code == status.HTTP_200_OK
    assert response.json() == []


def test_get_data_should_return_only_consented_dialogs():
    response = client.get("/data")
    assert response.status_code == status.HTTP_200_OK
    assert len(response.json()) == 3


def test_get_data_should_be_sorted_by_id_descending():
    response = client.get("/data")
    data = response.json()

    assert response.status_code == status.HTTP_200_OK
    assert data[0]["id"] > data[1]["id"]
    assert data[1]["id"] > data[2]["id"]


def test_give_positive_consent_should_update_db_and_data_should_be_selectable():
    language = "it"
    customerId = 2048
    dialogId = 1024
    text = "This is a test!"
    payload = {"text": text, "language": language}

    # create dialog
    client.post(f"/data/{customerId}/{dialogId}", json=payload)

    # ensure that data is not visible
    data = client.get(
        "/data",
        params={
            "language": language,
            "customerId": customerId,
        },
    ).json()
    assert data == []

    # give positive consent
    reponse = client.post(f"/consents/{dialogId}", json={"is_accepted": True})
    assert reponse.status_code == status.HTTP_204_NO_CONTENT

    # retrieve data
    data = client.get(
        "/data",
        params={
            "language": language,
            "customerId": customerId,
        },
    ).json()
    assert len(data) == 1
    assert data[0]["customerId"] == customerId
    assert data[0]["dialogId"] == dialogId
    assert data[0]["language"] == language
    assert data[0]["text"] == text


def test_refuse_consent_should_return_204_and_delete_dialogs():
    language = "it"
    customerId = 123
    dialogId = 123
    text = "This is a test!"
    payload = {"text": text, "language": language}

    # create dialog
    client.post(f"/data/{customerId}/{dialogId}", json=payload)

    reponse = client.post(f"/consents/{dialogId}", json={"is_accepted": False})

    assert reponse.status_code == status.HTTP_204_NO_CONTENT

    data = asyncio.run(get_data_by_dialogId(db, dialogId))
    assert data == []
