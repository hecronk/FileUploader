from src.tests.utils import client


def test_register(test_db):
    response = client.post(
        url="/auth/register",
        headers={
            "Content-Type": "application/json"
        },
        json={
            "username": "my_username",
            "password": "mypassword"
        }
    )

    assert response.status_code == 200


def test_login(test_db):
    response = client.post(
        url="/auth/login",
        headers={
            "Content-Type": "application/json"
        },
        json={
            "username": "my_username",
            "password": "mypassword"
        }
    )

    assert response.status_code == 200
