from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .api.v1.router import api_router
from .database.engine import create_db_and_tables
import asyncio
from contextlib import asynccontextmanager


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup: Create database tables
    await create_db_and_tables()
    yield
    # Shutdown: Cleanup operations can be added here


app = FastAPI(
    title="Task Management API",
    description="API for managing user tasks with CRUD operations",
    version="1.0.0",
    lifespan=lifespan
)

# CORS configuration for authentication
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # Frontend URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
    expose_headers=["*"],
)

# Include API routers
app.include_router(api_router)


@app.get("/")
async def root():
    return {"message": "Welcome to the Task Management API"}


@app.get("/health")
async def health_check():
    return {"status": "healthy"}