import logging

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .models import model_expenses, users as model_users  # noqa: F401  (registers tables)
from .routes import routes_expenses, routes_users, routes_auth

logger = logging.getLogger(__name__)

app = FastAPI(
    title="Mimoni",
    version="0.0.1",
    description="Track your finance",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5500", "http://127.0.0.1:5500"],  # your frontend's origin
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(routes_expenses.router)
app.include_router(routes_users.router)
app.include_router(routes_auth.router)


@app.get("/")
def index():
    return {"message": "Manage your finance"}