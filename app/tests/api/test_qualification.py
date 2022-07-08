from fastapi import status
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

from .base import get_valid_api_key, get_invalid_api_key


def test_get_all(client: TestClient, db: Session) -> None:
    headers = get_valid_api_key()
    response = client.get("/qualifications/", headers = headers)

    assert response.status_code == status.HTTP_200_OK
    assert type(response.json()) == list


def test_get_all_without_auth(client: TestClient, db: Session) -> None:
    response = client.get("/qualifications/")

    assert response.status_code == status.HTTP_401_UNAUTHORIZED


def test_get_all_invalid_api_key(client: TestClient, db: Session) -> None:
    headers = get_invalid_api_key()
    response = client.get("/qualifications/", headers = headers)

    assert response.status_code == status.HTTP_401_UNAUTHORIZED


def test_get_qualis_by_album(client: TestClient, db: Session) -> None:
    headers = get_valid_api_key()
    response = client.get("/qualifications/?album_id=1", headers = headers)

    assert response.status_code == status.HTTP_200_OK
    assert type(response.json()) == list


def test_get_inexistent_quali(client: TestClient, db: Session) -> None:
    headers = get_valid_api_key()
    response = client.get("/qualifications/40000", headers = headers)

    assert response.status_code == status.HTTP_404_NOT_FOUND


def test_create_quali(client: TestClient, db: Session) -> None:
    headers = get_valid_api_key()
    response = client.put("/qualifications/", headers = headers, json = {
        "user_id": "abc123",
        "album_id": 1,
        "value": 4
    })

    json = response.json()
    del json["id"]

    assert response.status_code == status.HTTP_201_CREATED
    assert json == {
        "user_id": "abc123",
        "album_id": 1,
        "value": 4
    }


def test_get_existing_quali(client: TestClient, db: Session) -> None:
    headers = get_valid_api_key()
    response = client.put("/qualifications/", headers = headers, json = {
        "user_id": "abc123",
        "album_id": 1,
        "value": 4
    })

    id = response.json()["id"]

    response = client.get("/qualifications/{}".format(id), headers = headers)

    assert response.status_code == status.HTTP_200_OK
    assert response.json() == {
        "id": id,
        "user_id": "abc123",
        "album_id": 1,
        "value": 4
    }


def test_remove_existing_quali(client: TestClient, db: Session) -> None:
    headers = get_valid_api_key()
    last_id = client.get("/qualifications/",
                         headers = headers).json()[-1]["id"]

    response = client.delete("/qualifications/{}".format(last_id),
                             headers = headers)

    assert response.status_code == status.HTTP_200_OK


def test_remove_inexisting_quali(client: TestClient, db: Session) -> None:
    headers = get_valid_api_key()
    response = client.delete("/qualifications/40000", headers = headers)

    assert response.status_code == status.HTTP_404_NOT_FOUND


def test_get_stats(client: TestClient, db: Session) -> None:
    headers = get_valid_api_key()
    response = client.get("/qualifications/stats/1",
                          headers = headers)

    assert response.status_code == status.HTTP_200_OK
    assert list(response.json().keys()) == ["count", "sum", "avg"]
