from fastapi import FastAPI, HTTPException
from fastapi.staticfiles import StaticFiles
from starlette.responses import FileResponse
from fastapi import FastAPI, Request
from slowapi.errors import RateLimitExceeded
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from tortoise import Tortoise  # Needed for shutdown
import socketio
from fastapi.staticfiles import StaticFiles
from web_socket.main import (
    MainNamespace,
    RecipesNamespace,
    UsersNamespace,
    NotificationsNamespace,
)
from config import init_db  # Your DB init logic
from routes.auth import auth_router, limiter, AuthService
from routes.recipes import recipe_router, RecipeService
from routes.notifications import notification_router
from routes.cooking_tips import cooking_tip_router, RecipeService
from utils.limiter import limiter
from routes.user import user_router
import os
from config import Config, WEB_SERVER, BASE_SERVER

ALLOWED_ORIGINS = [
    "http://localhost:5173",
    "http://localhost:8080",
    "https://thefoodlovers.tera-in.top",
    "https://the-food-lovers.netlify.app",
    f"{WEB_SERVER}",
]


app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


sio = socketio.AsyncServer(
    async_mode="asgi",
    cors_allowed_origins=ALLOWED_ORIGINS,
)


sio.register_namespace(MainNamespace("/main"))
sio.register_namespace(RecipesNamespace("/recipes", RecipeService()))
sio.register_namespace(UsersNamespace("/users", AuthService()))
notifications_namespace = NotificationsNamespace("/notifications", AuthService())
sio.register_namespace(notifications_namespace)

socket_app = socketio.ASGIApp(
    sio,
    other_asgi_app=app,
    socketio_path="/ws/socket.io",  # Match frontend path
)


app.state.limiter = limiter  # for integration


@app.exception_handler(RateLimitExceeded)
async def rate_limit_handler(request: Request, exc: RateLimitExceeded):
    return JSONResponse(
        status_code=429, content={"detail": "Rate limit exceeded. Please wait."}
    )


app.include_router(auth_router, prefix="/api")
app.include_router(recipe_router, prefix="/api")
app.include_router(user_router, prefix="/api")
app.include_router(cooking_tip_router, prefix="/api")
app.include_router(notification_router, prefix="/api")


BASE_DIR = os.path.dirname(os.path.abspath(__file__))
VUE_DIST_DIR = os.path.abspath(os.path.join(BASE_DIR, "..", "dist"))
BASE_DIRECTORY = "uploads"
app.mount("/uploads", StaticFiles(directory=BASE_DIRECTORY), name="uploads")

@app.get("/", include_in_schema=False)
async def serve_root():
    return FileResponse(os.path.join(VUE_DIST_DIR, "index.html"))


@app.get("/{full_path:path}", include_in_schema=False)
async def serve_vue(full_path: str):
    file_path = os.path.join(VUE_DIST_DIR, full_path)

    if os.path.exists(file_path) and os.path.isfile(file_path):
        return FileResponse(file_path)

    return FileResponse(os.path.join(VUE_DIST_DIR, "index.html"))


app.mount(
    "/assets",
    StaticFiles(directory=os.path.join(VUE_DIST_DIR, "assets")),
    name="assets",
)


from utils.manual_email_send import trigger


@app.on_event("startup")
async def startup():
    print("🚀 Connecting to database...")
    await init_db(app)
    # print(await triger())

    print("✅ DATABASE CONNECTED")


@app.on_event("shutdown")
async def shutdown():
    print("🛑 Closing DB connections...")
    await Tortoise.close_connections()


# uvicorn app:socket_app --reload
# cloudflared tunnel --url http://localhost:8000
