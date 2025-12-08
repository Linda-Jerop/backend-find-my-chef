"""
Client routes
"""

from fastapi import APIRouter

router = APIRouter()

# TODO: Implement client routes
@router.get("/")
async def get_clients():
    """Get all clients"""
    return {"message": "Get all clients endpoint"}
# Minimal client router placeholder; not used heavily by booking tests.
