from uuid import uuid4


def valid_recipe_payload(recipe_id=None):
    recipe_id = recipe_id or uuid4()
    return {
        "isPublic": True,
        "allowComments": True,
        "copyProtection": "allow",
        "recipeCover": {
            "id": str(recipe_id),
            "recipeName": "Pilau",
            "repiceColor": "#4CAF50",
            "image": "data:image/png;base64,abc",
            "tags": ["rice", "dinner"],
            "cookTime": {"hr": 1, "min": 15},
            "description": "Spiced rice",
            "cuisine": {"name": "Kenyan", "region": "East Africa"},
            "complexityLevel": {"name": "Easy", "value": "1"},
            "category": ["Dinner"],
        },
        "recipeSteps": {
            "id": str(recipe_id),
            "name": "Pilau",
            "description": "Cook pilau",
            "category": ["Dinner"],
            "ingredients": [{"name": "Rice", "amount": "2", "unit": "cups"}],
            "steps": [
                {
                    "no": 1,
                    "timeRequired": {"hr": 0, "min": 30},
                    "tempRequired": 100,
                    "ingredientsUsed": [{"name": "Rice", "amount": "2", "unit": "cups"}],
                    "instructions": "Boil rice",
                    "image": "data:image/png;base64,abc",
                    "videoUrl": "",
                }
            ],
            "tags": ["rice"],
        },
    }


def test_create_recipe_requires_chef(api_client, non_chef_user):
    from routes.recipes import get_current_user

    api_client.app.dependency_overrides[get_current_user] = lambda: non_chef_user

    response = api_client.post("/api/recipes", json=valid_recipe_payload())

    assert response.status_code == 403
    assert response.json()["detail"] == "Only chefs can submit recipes"


def test_create_recipe_returns_recipe_metadata(api_client):
    response = api_client.post("/api/recipes", json=valid_recipe_payload())

    assert response.status_code == 200
    body = response.json()
    assert body["message"] == "Recipe processed successfully"
    assert body["recipeName"] == "Pilau"
    assert api_client.fake_recipe_service.calls[-1][0] == "create_or_update_recipe"


def test_fetch_recipes_forwards_filters_to_service(api_client):
    response = api_client.post(
        "/api/recipes/get",
        json={"limit": 5, "offset": 10, "recipe_name": "pilau", "category": ["Dinner"]},
    )

    assert response.status_code == 200
    assert response.json() == [{"id": "recipe-1", "name": "pilau"}]
    call = api_client.fake_recipe_service.calls[-1]
    assert call[0] == "list_recipes"
    assert call[1]["limit"] == 5
    assert call[1]["offset"] == 10
    assert call[1]["name"] == "pilau"


def test_get_recipe_by_id_returns_cover_and_steps(api_client):
    recipe_id = uuid4()

    response = api_client.get(f"/api/recipes/pilau/{recipe_id}")

    assert response.status_code == 200
    body = response.json()
    assert body["cover"]["name"] == "pilau"
    assert body["steps"] == [{"no": 1}]


def test_recipe_suggestions_delegates_to_service(api_client):
    response = api_client.post("/api/recipes/pilau/suggestions")

    assert response.status_code == 200
    assert response.json() == [{"name": "pilau"}]
    assert api_client.fake_recipe_service.calls[-1][0] == "get_recipes_suggestions"


def test_comment_routes_cover_create_reply_edit_delete(api_client):
    recipe_id = uuid4()

    created = api_client.post(
        f"/api/recipes/{recipe_id}/comments",
        json={"content": "Looks delicious"},
    )
    replied = api_client.post(
        f"/api/recipes/{recipe_id}/comments",
        json={"content": "Agreed", "parent": 1},
    )
    edited = api_client.post(
        f"/api/recipes/{recipe_id}/comments",
        json={"content": "Updated", "comment_id": 1},
    )
    deleted = api_client.delete(f"/api/recipes/{recipe_id}/comments/1")

    assert created.json()["content"] == "Looks delicious"
    assert replied.json()["parent"] == 1
    assert edited.json()["content"] == "Updated"
    assert deleted.json() == {"success": True}
    assert [call[0] for call in api_client.fake_recipe_service.calls[-4:]] == [
        "post_comment",
        "reply_to_comment",
        "edit_comment",
        "delete_comment",
    ]


def test_recipe_meta_batch_rejects_empty_id_list(api_client):
    response = api_client.post("/api/recipes/meta", json={"recipe_ids": []})

    assert response.status_code == 400
    assert response.json()["detail"] == "No recipe IDs provided."


def test_get_comments_and_likes_forward_params(api_client):
    recipe_id = uuid4()

    comments = api_client.get(
        "/api/recipes/comments",
        params={"recipe_id": str(recipe_id), "limit": 5, "offset": 0},
    )
    likes = api_client.get(
        "/api/recipes/likes",
        params={"recipe_id": str(recipe_id), "limit": 10},
    )
    views = api_client.get(
        "/api/recipes/views",
        params={"recipe_id": str(recipe_id)},
    )

    assert comments.json()["count"] == 0
    assert likes.json() == {"likes": []}
    assert views.json() == {"views": []}


def test_like_favourite_comment_like_and_delete_recipe(api_client):
    recipe_id = uuid4()

    like = api_client.post(f"/api/recipes/{recipe_id}/like")
    favourite = api_client.post(f"/api/recipes/{recipe_id}/favourite-recipe")
    comment_like = api_client.post(
        "/api/recipes/comments/likes",
        json={"id": 1, "reaction": {"name": "heart"}, "recipe_id": str(recipe_id), "is_liked": True},
    )
    deleted = api_client.post(f"/api/recipes/{recipe_id}/delete")

    assert like.json() == {"success": True}
    assert favourite.json() == {"success": True}
    assert comment_like.json() == {"success": True}
    assert deleted.json() == {"success": True}
