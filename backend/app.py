from fastapi import FastAPI
from fastapi import FastAPI, Request
from slowapi.errors import RateLimitExceeded
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from tortoise import Tortoise  # Needed for shutdown
import socketio
from fastapi.staticfiles import StaticFiles

from web_socket.main import MainNamespace
from config import init_db  # Your DB init logic
from routes.auth import auth_router,limiter
from routes.recipes import recipe_router
from utils.limiter import limiter  
from routes.user import user_router


ALLOWED_ORIGINS = [
    "http://localhost:5173",
    "http://localhost:8080",
    "https://yourfrontend.com",
    "https://the-food-lovers.netlify.app"
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
BASE_DIRECTORY = 'uploads'
app.mount("/uploads", StaticFiles(directory=BASE_DIRECTORY), name="uploads")


app.include_router(auth_router, prefix="/api")
app.include_router(recipe_router,prefix="/api")
app.include_router(user_router,prefix="/api")

socket_app = socketio.ASGIApp(
    sio,
    other_asgi_app=app,
    socketio_path="/ws/socket.io"  # Match frontend path
)


app.state.limiter = limiter  # for integration

@app.exception_handler(RateLimitExceeded)
async def rate_limit_handler(request: Request, exc: RateLimitExceeded):
    return JSONResponse(
        status_code=429,
        content={"detail": "Rate limit exceeded. Please wait."}
    )
    
@app.on_event("startup")
async def startup():
    print("🚀 Connecting to database...")
    await init_db(app)
    print("✅ DATABASE CONNECTED")

@app.on_event("shutdown")
async def shutdown():
    print("🛑 Closing DB connections...")
    await Tortoise.close_connections()


#uvicorn app:socket_app --reload
