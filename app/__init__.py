from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from config.settings import settings

engine = create_engine(settings.DATABASE_URL, connect_args={"check_same_thread": False} if "sqlite" in settings.DATABASE_URL else {})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# Importing model modules to ensure declarative models are registered with Base.metadata
import app.models.user  # Registering User model
import app.models.chef  # Registering Chef model
import app.models.client  # Registering Client model
import app.models.booking  # Registering Booking model


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# Importing models to ensure they are registered on Base when the app package is imported  # Ensuring metadata is populated for tests
import app.models  # noqa: E402,F401


def create_app() -> FastAPI:
    app = FastAPI(title=settings.APP_NAME, version=settings.VERSION, docs_url="/api/docs", redoc_url="/api/redoc")
    
    cors_origins = settings.parsed_cors_origins if hasattr(settings, 'parsed_cors_origins') else settings.CORS_ORIGINS
    app.add_middleware(CORSMiddleware, allow_origins=cors_origins, allow_credentials=True, allow_methods=["*"], allow_headers=["*"])
    
    from app.routes.auth import router as auth_router
    from app.routes.chef import router as chef_router
    from app.routes.booking import router as booking_router
    from app.routes.client import router as client_router
    
    app.include_router(auth_router, prefix="/api/auth", tags=["Authentication"])
    app.include_router(chef_router, prefix="/api/chefs", tags=["Chefs"])
    app.include_router(booking_router, prefix="/api/bookings", tags=["Bookings"])
    app.include_router(client_router, prefix="/api/clients", tags=["Clients"])
    
    @app.get("/api/health", tags=["Health"])
    async def health_check():
        return {"status": "healthy", "message": "Find My Chef API is running"}
    
    return app
