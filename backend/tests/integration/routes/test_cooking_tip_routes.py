from uuid import uuid4


def test_list_cooking_tips_delegates_to_service(full_api_client):
    response = full_api_client.get(
        "/api/cooking-tip",
        params={"limit": 5, "offset": 0, "title": "knife"},
    )

    assert response.status_code == 200
    assert response.json() == [{"id": "tip-1", "title": "knife"}]
    call = full_api_client.fake_cooking_tip_service.calls[-1]
    assert call[0] == "list_cooking_tips"
    assert call[1]["title"] == "knife"


def test_fetch_cooking_tips_via_recipe_service(full_api_client):
    response = full_api_client.get(
        "/api/cooking-tips",
        params={"limit": 3, "offset": 0},
    )

    assert response.status_code == 200
    assert response.json() == [{"id": "recipe-1", "name": None}]
    assert full_api_client.fake_recipe_service.calls[-1][0] == "list_recipes"


def test_fetch_cooking_tip_by_id(full_api_client):
    tip_id = uuid4()

    response = full_api_client.get(f"/api/cooking-tips/pilau/{tip_id}")

    assert response.status_code == 200
    body = response.json()
    assert body["cover"]["name"] == "pilau"
    assert body["steps"] == [{"no": 1}]


def test_like_cooking_tip(full_api_client):
    tip_id = uuid4()

    response = full_api_client.post(f"/api/cooking-tip/{tip_id}/like")

    assert response.status_code == 200
    assert response.json() == {"success": True}
    assert full_api_client.fake_recipe_service.calls[-1][0] == "like_unlike"
