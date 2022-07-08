from fastapi import status
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

from .base import get_valid_api_key, get_invalid_api_key


def test_get_all(client: TestClient, db: Session) -> None:
    headers = get_valid_api_key()
    response = client.get("/comments/", headers = headers)
    assert response.status_code == status.HTTP_200_OK
    assert type(response.json()) == list


def test_get_all_without_auth(client: TestClient, db: Session) -> None:
    response = client.get("/comments/")
    assert response.status_code == status.HTTP_401_UNAUTHORIZED


def test_get_all_invalid_api_key(client: TestClient, db: Session) -> None:
    headers = get_invalid_api_key()
    response = client.get("/comments/", headers = headers)
    assert response.status_code == status.HTTP_401_UNAUTHORIZED


def test_get_inexistent_comment(client: TestClient, db: Session) -> None:
    headers = get_valid_api_key()
    response = client.get("/comments/40000", headers = headers)

    assert response.status_code == status.HTTP_404_NOT_FOUND


def test_create_comment(client: TestClient, db: Session) -> None:
    headers = get_valid_api_key()
    response = client.put("/comments/", headers = headers, json = {
        "user_id": "abc123",
        "album_id": 1,
        "comment": "Very good!"
    })

    json = response.json()
    del json["id"]

    assert response.status_code == status.HTTP_201_CREATED or \
           response.status_code == status.HTTP_200_OK
    assert json == {
        "user_id": "abc123",
        "album_id": 1,
        "comment": "Very good!"
    }


def test_get_existing_comment(client: TestClient, db: Session) -> None:
    headers = get_valid_api_key()
    response = client.put("/comments/", headers = headers, json = {
        "user_id": "abc1234",
        "album_id": 1,
        "comment": "Very good!"
    })

    id = response.json()["id"]

    response = client.get("/comments/{}".format(id), headers = headers)

    assert response.status_code == status.HTTP_200_OK
    assert response.json() == {
        "id": id,
        "user_id": "abc1234",
        "album_id": 1,
        "comment": "Very good!"
    }


def test_remove_existing_comment(client: TestClient, db: Session) -> None:
    headers = get_valid_api_key()
    last_id = client.get("/comments/", headers = headers).json()[-1]["id"]

    response = client.delete("/comments/{}".format(last_id), headers = headers)

    assert response.status_code == status.HTTP_200_OK


def test_remove_inexisting_comment(client: TestClient, db: Session) -> None:
    headers = get_valid_api_key()
    response = client.delete("/comments/40000", headers = headers)

    assert response.status_code == status.HTTP_404_NOT_FOUND
