from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from typing import Optional, List
from app import get_db
from app.models.chef import Chef
from app.models.user import User
from app.schemas.chef import ChefUpdate, ChefResponse
from app.utils.auth import get_current_user

router = APIRouter()


@router.get("", response_model=List[ChefResponse])
def list_chefs(
    cuisine: Optional[str] = Query(None),
    location: Optional[str] = Query(None),
    max_price: Optional[float] = Query(None),
    search: Optional[str] = Query(None),
    db: Session = Depends(get_db)
):
    query = db.query(Chef).filter(Chef.is_available == 1)
    
    if cuisine:
        query = query.filter(Chef.cuisines.contains(cuisine))
    if location:
        query = query.filter(Chef.location.ilike(f"%{location}%"))
    if max_price:
        query = query.filter(Chef.hourly_rate <= max_price)
    if search:
        query = query.join(User).filter(User.name.ilike(f"%{search}%"))
    
    chefs = query.all()
    return [chef.to_dict() for chef in chefs]


@router.get("/{chef_id}", response_model=ChefResponse)
def get_chef(chef_id: int, db: Session = Depends(get_db)):
    chef = db.query(Chef).filter(Chef.id == chef_id).first()
    if not chef:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Chef not found")
    return chef.to_dict()


@router.put("/{chef_id}", response_model=ChefResponse)
def update_chef(chef_id: int, chef_data: ChefUpdate, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    chef = db.query(Chef).filter(Chef.id == chef_id).first()
    
    if not chef:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Chef not found")
    
    if chef.user_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized to update this profile")
    
    update_data = chef_data.dict(exclude_unset=True)
    for key, value in update_data.items():
        if key == "is_available" and value is not None:
            setattr(chef, key, 1 if value else 0)
        else:
            setattr(chef, key, value)
    
    db.commit()
    db.refresh(chef)
    
    return chef.to_dict()
