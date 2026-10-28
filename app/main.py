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
    allow_origins=["*"],  # 👈 Open up for local development mapping tools
    allow_credentials=True, # 👈 Crucial if your routes_auth routes use Cookies/Bearer headers
    allow_methods=["*"],
    allow_headers=["*"],
)


app.include_router(routes_expenses.router)
app.include_router(routes_users.router)
app.include_router(routes_auth.router)


@app.get("/")
def index():
    return {"message": "Manage your finance"}