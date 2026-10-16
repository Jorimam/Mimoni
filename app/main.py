from fastapi import FastAPI
import logging

from .base import Base
from .database import engine
from .models import model_expenses  # noqa: F401  (needed so the table is registered on Base)
from .routes import routes_expenses

logger = logging.getLogger(__name__)

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Mimoni",
    version="0.0.1",
    description="Track your finance",
)

app.include_router(routes_expenses.router)


@app.get("/")
def index():
    return {"Message": "Manage your finance"}