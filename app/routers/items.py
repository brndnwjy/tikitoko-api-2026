from fastapi import APIRouter, HTTPException, status
from pydantic import BaseModel, Field
from typing import List, Optional

router = APIRouter()

# Data models
class Item(BaseModel):
    id: int
    name: str
    description: Optional[str] = None
    price: float = Field(..., gt=0, description="Price must be greater than zero")

class ItemCreate(BaseModel):
    name: str
    description: Optional[str] = None
    price: float = Field(..., gt=0)

# In-memory storage for items
# Stored some dummy items for demonstration purposes
items_db: List[Item] = [
    {"id": 1, "name": "Dummy 1", "description": "Description for Dummy 1", "price": 10.0},
    {"id": 2, "name": "Dummy 2", "description": "Description for Dummy 2", "price": 15.0},
    {"id": 3, "name": "Dummy 3", "description": "Description for Dummy 3", "price": 22.50},
]

# API endpoints
@router.get("/", response_model=List[Item])
async def get_items():
    return items_db

@router.post("/", response_model=Item, status_code=status.HTTP_201_CREATED)
async def create_item(item_in: ItemCreate):
    new_item = Item(id=len(items_db) + 1, **item_in.model_dump())
    items_db.append(new_item)
    return new_item

@router.get("/{item_id}", response_model=Item)
async def get_item(item_id: int):
    for item in items_db:
        if item.id == item_id:
            return item
        
    raise HTTPException(
        status_code=404, 
        detail="Item not found"
    )

