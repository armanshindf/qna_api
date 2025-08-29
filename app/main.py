from fastapi import FastAPI, Depends, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.trustedhost import TrustedHostMiddleware
from fastapi.middleware.gzip import GZipMiddleware
from fastapi.responses import JSONResponse
from contextlib import asynccontextmanager
import logging
from app.config import settings
from app.database import health_check_db, engine, Base
from app.routers import questions, answers
import time

logging.basicConfig(
    level=logging.INFO if settings.ENVIRONMENT == "production" else logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(),
        logging.FileHandler('app.log', encoding='utf-8') if settings.ENVIRONMENT == "production" else logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

@asynccontextmanager
async def lifespan(app: FastAPI):
    """Lifespan events для управления состоянием приложения"""
    startup_time = time.time()
    logger.info(f"Starting {settings.PROJECT_NAME} in {settings.ENVIRONMENT} mode...")
    
    if settings.ENVIRONMENT == "development":
        try:
            logger.info("Creating database tables...")
            Base.metadata.create_all(bind=engine)
            logger.info("Database tables created successfully")
        except Exception as e:
            logger.error(f"Error creating database tables: {e}")
    
    if health_check_db():
        logger.info("Database connection established")
    else:
        logger.error("Database connection failed")
    
    logger.info(f"Application started in {time.time() - startup_time:.2f} seconds")
    
    yield
    
    logger.info("Shutting down application...")

app = FastAPI(
    title=settings.PROJECT_NAME,
    description="API сервис для вопросов и ответов",
    version=settings.VERSION,
    docs_url="/docs" if settings.ENVIRONMENT != "production" else None,
    redoc_url="/redoc" if settings.ENVIRONMENT != "production" else None,
    openapi_url="/openapi.json" if settings.ENVIRONMENT != "production" else None,
    lifespan=lifespan
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS.split(","),
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.add_middleware(
    TrustedHostMiddleware,
    allowed_hosts=settings.ALLOWED_HOSTS.split(",")
)

if settings.ENVIRONMENT == "production":
    app.add_middleware(GZipMiddleware, minimum_size=1000)

app.include_router(questions.router, prefix="/api/v1")
app.include_router(answers.router, prefix="/api/v1")

@app.get("/")
async def root():
    return {
        "message": f"{settings.PROJECT_NAME} is running",
        "environment": settings.ENVIRONMENT,
        "version": settings.VERSION
    }

@app.get("/health")
async def health_check():
    """Health check endpoint для мониторинга"""
    db_status = health_check_db()
    status_code = 200 if db_status else 503
    
    return JSONResponse(
        status_code=status_code,
        content={
            "status": "healthy" if db_status else "unhealthy",
            "database": "connected" if db_status else "disconnected",
            "environment": settings.ENVIRONMENT,
            "timestamp": time.time()
        }
    )

@app.get("/api/v1/info")
async def app_info():
    """Информация о приложении"""
    return {
        "name": settings.PROJECT_NAME,
        "version": settings.VERSION,
        "environment": settings.ENVIRONMENT,
        "debug": settings.DEBUG
    }

@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    logger.error(f"Unhandled exception: {exc}", exc_info=True)
    return JSONResponse(
        status_code=500,
        content={
            "error": "Internal server error",
            "detail": str(exc) if settings.DEBUG else "Something went wrong"
        }
    )