import logging
from contextlib import asynccontextmanager

import dotenv

import uvicorn
from fastapi import FastAPI
from fastapi_pagination import add_pagination

dotenv.load_dotenv()
from app.database.engine import create_db_and_tables
from app.routers import status, users


@asynccontextmanager
async def lifespan(app: FastAPI):
    """FastAPI lifespan hook."""
    logging.warning("Pyfast in started")
    create_db_and_tables()
    yield
    logging.warning("Pyfast in stopped")


app = FastAPI(lifespan=lifespan)

app.include_router(status.router)
app.include_router(users.router)

add_pagination(app)

if __name__ == "__main__":
    """Create the database and tables and run the FastAPI server locally."""
    uvicorn.run(app, host="localhost", port=8000)
