import os

from sqlalchemy import create_engine
from sqlalchemy.engine import URL
from sqlalchemy.orm import sessionmaker
from sqlalchemy_utils import create_database, database_exists

REQUIRED_VARS = ["DB_USER", "DB_PASSWORD", "DB_HOST", "DB_PORT", "DB_DATABASE"]
missing = [name for name in REQUIRED_VARS if not os.getenv(name)]
if missing:
    raise RuntimeError(f"Missing environment variables: {', '.join(missing)}")

SQLALCHEMY_DB_URL = URL.create(
    drivername="mysql+pymysql",
    username=os.environ["DB_USER"],
    password=os.environ["DB_PASSWORD"],
    host=os.environ["DB_HOST"],
    port=int(os.environ["DB_PORT"]),
    database=os.environ["DB_DATABASE"],
)

if not database_exists(SQLALCHEMY_DB_URL):
    create_database(SQLALCHEMY_DB_URL)

engine = create_engine(
    SQLALCHEMY_DB_URL,
    echo=os.getenv("DB_ECHO", "false").lower() == "true",
    pool_pre_ping=True,
    pool_recycle=1800,
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()