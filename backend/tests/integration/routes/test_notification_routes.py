from uuid import uuid4


def test_fetch_notifications_for_authenticated_user(notification_api_client):
    client = notification_api_client
    username = client.current_user.username

    response = client.post(
        f"/api/notifications/{username}/fetch",
        json={"limit": 10, "offset": 0, "is_read": False},
    )

    assert response.status_code == 200
    body = response.json()
    assert body["count"] == 1
    assert client.fake_notification_service.calls[-1][0] == "get_notifications"


def test_fetch_notifications_rejects_wrong_username(notification_api_client):
    response = notification_api_client.post(
        "/api/notifications/other_user/fetch",
        json={"limit": 10},
    )

    assert response.status_code == 403
    assert "Not authorized" in response.json()["detail"]


def test_fetch_notification_counts(notification_api_client):
    response = notification_api_client.post(
        f"/api/notifications/{notification_api_client.current_user.username}/counts"
    )

    assert response.status_code == 200
    body = response.json()
    assert body["all"] == 6
    assert body["follows"] == 3


def test_mark_notification_as_read(notification_api_client):
    noty_id = uuid4()

    response = notification_api_client.post(
        f"/api/notifications/{noty_id}/read",
        json={"read": True},
    )

    assert response.status_code == 200
    assert response.json()["read"] is True
    assert notification_api_client.fake_notification_service.calls[-1][0] == "read_notification"


def test_mark_all_notifications_as_read(notification_api_client):
    response = notification_api_client.post(
        "/api/notifications/mark-all-read",
        json={"type": "like"},
    )

    assert response.status_code == 200
    assert response.json()["marked"] == "like"


def test_delete_notification(notification_api_client):
    noty_id = uuid4()

    response = notification_api_client.delete(f"/api/notifications/{noty_id}/delete")

    assert response.status_code == 200
    assert response.json()["success"] is True


def test_update_and_get_notification_settings(notification_api_client):
    update = notification_api_client.post(
        "/api/notifications/settings",
        json={
            "email_notifications": False,
            "push_notifications": True,
            "notificationTypes": {
                "like": True,
                "comment": False,
                "mention": True,
                "follow": True,
                "system": False,
            },
        },
    )
    get_settings = notification_api_client.post("/api/notifications/settings/get")

    assert update.status_code == 200
    assert update.json()["success"] is True
    assert get_settings.status_code == 200
    assert get_settings.json()["email_notifications"] is True
