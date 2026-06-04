from uuid import uuid4


def test_follow_route_toggles_follow(api_client):
    chef_id = uuid4()

    response = api_client.post(f"/api/users/{chef_id}/follow")

    assert response.status_code == 200
    assert response.json() == {"success": True}
    assert api_client.fake_auth_service.calls[-1] == (
        "follow_unfollow",
        str(api_client.current_user.id),
        str(chef_id),
    )


def test_update_user_rejects_mismatched_identity(api_client):
    response = api_client.post(
        "/api/users/update/test_chef",
        json={
            "user_id": str(uuid4()),
            "email": "someone-else@example.com",
            "username": "new_name",
        },
    )

    assert response.status_code == 400
    assert response.json()["detail"] == "User ID or email does not match the authenticated user"


def test_update_user_accepts_authenticated_identity(api_client):
    response = api_client.post(
        "/api/users/update/test_chef",
        json={
            "user_id": str(api_client.current_user.id),
            "email": api_client.current_user.email,
            "username": "fresh_name",
        },
    )

    assert response.status_code == 200
    assert response.json()["success"] is True
    assert api_client.fake_auth_service.calls[-1][0] == "update_user"


def test_user_collection_routes_forward_query_params(api_client):
    target_id = uuid4()
    user_id = uuid4()

    followers = api_client.get(
        "/api/users/followers",
        params={"target_id": str(target_id), "user_id": str(user_id), "limit": 3, "offset": 6},
    )
    following = api_client.get(
        "/api/users/following",
        params={"target_id": str(target_id), "user_id": str(user_id)},
    )
    chefs = api_client.post("/api/users/get-chefs")
    stats = api_client.post("/api/users/get-chefs-stats")
    profile = api_client.post("/api/users/chef_nia")

    assert followers.json()["count"] == 0
    assert following.json()["count"] == 0
    assert chefs.json() == {"chefs": [], "total": 0}
    assert stats.json() == {"stats": [], "popular_chef": {}}
    assert profile.json()["user"]["username"] == "chef_nia"


def test_request_chef_delegates_to_auth_service(api_client):
    username = api_client.current_user.username

    response = api_client.post(f"/api/users/chef-request/{username}")

    assert response.status_code == 200
    assert response.json() is True
    assert api_client.fake_auth_service.calls[-1] == ("request_chef", str(api_client.current_user.id))


def test_request_chef_rejects_mismatched_username(api_client):
    response = api_client.post("/api/users/chef-request/other_user")

    assert response.status_code == 400
    assert "does not match" in response.json()["detail"]
