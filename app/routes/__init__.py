from app.routes.auth import router as auth_router
from app.routes.chef import router as chef_router
from app.routes.client import router as client_router
from app.routes.booking import router as booking_router

__all__ = ["auth_router", "chef_router", "client_router", "booking_router"]
