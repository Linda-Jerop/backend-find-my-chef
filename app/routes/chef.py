"""
Chef routes
"""

from fastapi import APIRouter

router = APIRouter()

# TODO: Implement chef routes
@router.get("/")
async def get_chefs():
    """Get all chefs"""
    return {"message": "Get all chefs endpoint"}
