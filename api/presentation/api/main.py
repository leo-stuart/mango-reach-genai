"""MangoAI API server — FastAPI wrapper around the ADK agent."""

import logging
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
load_dotenv()

from api.infrastructure.config.settings import settings
from api.presentation.api.routes import chat_routes

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)
logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Startup and shutdown events."""
    logger.info(f"🥭 {settings.app_name} Agent starting up...")
    yield
    logger.info(f"🥭 {settings.app_name} Agent shutting down...")


app = FastAPI(
    title="MangoAI Agent API",
    description="Sales Copilot Agent for Mango Reach — powered by Google ADK + GPT-4o",
    version="0.2.0",
    lifespan=lifespan,
)

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://127.0.0.1:5173",
        "http://localhost:8008",
        "https://cold-email-customization.vercel.app",
        "https://mangoreach.vercel.app",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(chat_routes.router)


@app.get("/")
async def root():
    return {
        "name": "MangoAI Agent API",
        "version": "0.2.0",
        "docs": "/docs",
        "agent": settings.app_name,
    }
