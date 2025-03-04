from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .routes import router as user_routes

app = FastAPI(
    title="User Management API",
    description="Rest Api for User Management",
    version="1.0.0",
)


origins = [
    "http://localhost",
    "http://localhost:4200",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(user_routes)
