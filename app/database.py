from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from sqlalchemy.pool import QueuePool
from app.config import settings
import logging

logger = logging.getLogger(__name__)

engine_args = {
    "poolclass": QueuePool,
    "pool_size": settings.DB_POOL_SIZE,
    "max_overflow": settings.DB_MAX_OVERFLOW,
    "pool_timeout": 30,
    "pool_recycle": 1800,
}

if settings.ENVIRONMENT == "production":
    engine_args["echo"] = False
    if "postgresql" in settings.DATABASE_URL:
        engine_args["connect_args"] = {"sslmode": "require"}
else:
    engine_args["echo"] = True

engine = create_engine(settings.DATABASE_URL, **engine_args)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def health_check_db():
    """Проверка подключения к БД"""
    try:
        with engine.connect() as conn:
            conn.execute("SELECT 1")
        return True
    except Exception as e:
        logger.error(f"Database health check failed: {e}")
        return False