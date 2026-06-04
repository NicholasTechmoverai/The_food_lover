from uuid import uuid4


def test_login_returns_token_and_calls_auth_service(api_client):
    response = api_client.post(
        "/api/auth/login",
        json={"email": "chef@example.com", "password": "secret123"},
    )

    assert response.status_code == 200
    assert response.json()["access_token"] == "token"
    assert api_client.fake_auth_service.calls[-1] == ("login", "chef@example.com", "secret123")


def test_signup_validates_payload_and_returns_verification(api_client):
    response = api_client.post(
        "/api/auth/sign-up",
        json={
            "email": "new@example.com",
            "name": "New Chef",
            "password": "secret123",
            "confirm_password": "secret123",
            "terms": True,
        },
    )

    assert response.status_code == 200
    assert response.json() == {"id": "verification-id", "type": "email"}


def test_refresh_passes_user_id_to_auth_service(api_client):
    user_id = uuid4()

    response = api_client.post("/api/auth/refresh", json={"user_id": str(user_id)})

    assert response.status_code == 200
    assert response.json() == {"access_token": "fresh-token"}
    assert api_client.fake_auth_service.calls[-1] == ("renew_token", str(user_id))


def test_is_user_exists_returns_404_for_missing_user(api_client):
    response = api_client.post(
        "/api/auth/is-user-exists",
        params={"verifier": "missing@example.com"},
    )

    assert response.status_code == 404
    assert response.json()["detail"] == "User not found."


def test_is_user_exists_returns_true_for_existing_user(api_client):
    response = api_client.post(
        "/api/auth/is-user-exists",
        params={"verifier": "chef@example.com"},
    )

    assert response.status_code == 200
    assert response.json() is True


def test_verify_code_delegates_to_auth_service(api_client):
    code_id = uuid4()

    response = api_client.post(
        "/api/auth/verify",
        params={"code_id": str(code_id), "code": "123456", "type": "email"},
    )

    assert response.status_code == 200
    assert response.json() == {"verified": True}
    assert api_client.fake_auth_service.calls[-1][0] == "verify_code"


def test_send_verification_with_code_id(api_client):
    code_id = uuid4()

    response = api_client.post(
        "/api/auth/send-verification",
        params={"code_id": str(code_id), "type": "email", "method": "link"},
    )

    assert response.status_code == 200
    assert response.json() == {"sent": True}


def test_send_verification_rejects_taken_email(api_client):
    response = api_client.post(
        "/api/auth/send-verification",
        params={
            "new_email": "taken@example.com",
            "u_id": "user-1",
            "type": "email",
            "method": "link",
        },
    )

    assert response.status_code == 400
    assert response.json()["detail"] == "Email already registered!"


def test_reset_password_delegates_to_auth_service(api_client):
    response = api_client.post(
        "/api/auth/reset-password",
        params={
            "verifier": "chef@example.com",
            "password": "newpass1",
            "confirmPassword": "newpass1",
        },
    )

    assert response.status_code == 200
    assert response.json() == {"reset": True}
    assert api_client.fake_auth_service.calls[-1][0] == "change_password"


def test_logout_returns_success(api_client):
    response = api_client.post("/api/auth/logout", params={"token": "some-token"})

    assert response.status_code == 200
    assert response.json() is True
