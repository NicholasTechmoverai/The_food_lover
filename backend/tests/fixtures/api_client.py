from types import SimpleNamespace
from uuid import uuid4

import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient

from tests.fixtures.fake_services import (
    FakeAuthService,
    FakeCookingTipService,
    FakeNotificationService,
    FakeRecipeService,
)


@pytest.fixture
def current_user():
    return SimpleNamespace(
        id=uuid4(),
        name="Test Chef",
        username="test_chef",
        email="chef@example.com",
        is_chef=True,
    )


@pytest.fixture
def non_chef_user(current_user):
    return SimpleNamespace(**{**current_user.__dict__, "is_chef": False})


def _build_api(
    current_user,
    *,
    include_notifications=False,
    include_cooking_tips=False,
):
    from routes.auth import AuthService, auth_router
    from routes.recipes import RecipeService, get_current_user as recipe_current_user, recipe_router
    from routes.user import get_current_user as user_current_user, user_router
    from utils.limiter import limiter

    auth_service = FakeAuthService()
    recipe_service = FakeRecipeService()
    notification_service = FakeNotificationService()
    cooking_tip_service = FakeCookingTipService()

    api = FastAPI()
    api.state.limiter = limiter
    api.include_router(auth_router, prefix="/api")
    api.include_router(recipe_router, prefix="/api")
    api.include_router(user_router, prefix="/api")

    api.dependency_overrides[AuthService] = lambda: auth_service
    api.dependency_overrides[RecipeService] = lambda: recipe_service
    api.dependency_overrides[recipe_current_user] = lambda: current_user
    api.dependency_overrides[user_current_user] = lambda: current_user

    if include_notifications:
        from routes.auth import get_current_user as notification_current_user
        from routes.notifications import NotificationService, notification_router

        api.include_router(notification_router, prefix="/api")
        api.dependency_overrides[NotificationService] = lambda: notification_service
        api.dependency_overrides[notification_current_user] = lambda: current_user

    if include_cooking_tips:
        from routes.auth import get_current_user as cooking_tip_current_user
        from routes.cooking_tips import CookingTipService, cooking_tip_router

        api.include_router(cooking_tip_router, prefix="/api")
        api.dependency_overrides[CookingTipService] = lambda: cooking_tip_service
        api.dependency_overrides[cooking_tip_current_user] = lambda: current_user

    return api, auth_service, recipe_service, notification_service, cooking_tip_service


@pytest.fixture
def api_client(current_user):
    api, auth_service, recipe_service, *_ = _build_api(current_user)

    with TestClient(api) as client:
        client.fake_auth_service = auth_service
        client.fake_recipe_service = recipe_service
        client.current_user = current_user
        client.app = api
        yield client


@pytest.fixture
def notification_api_client(current_user):
    api, auth_service, recipe_service, notification_service, _ = _build_api(
        current_user, include_notifications=True
    )

    with TestClient(api) as client:
        client.fake_auth_service = auth_service
        client.fake_recipe_service = recipe_service
        client.fake_notification_service = notification_service
        client.current_user = current_user
        client.app = api
        yield client


@pytest.fixture
def full_api_client(current_user):
    api, auth_service, recipe_service, notification_service, cooking_tip_service = _build_api(
        current_user, include_notifications=True, include_cooking_tips=True
    )

    with TestClient(api) as client:
        client.fake_auth_service = auth_service
        client.fake_recipe_service = recipe_service
        client.fake_notification_service = notification_service
        client.fake_cooking_tip_service = cooking_tip_service
        client.current_user = current_user
        client.app = api
        yield client
