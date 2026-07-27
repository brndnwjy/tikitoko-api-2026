from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from typing import List

from app.db.session import get_db
from app.models.item import ItemModel
from app.schemas.item import ItemCreate, ItemResponse

router = APIRouter()


# Add item
@router.post("/", response_model=ItemResponse, status_code=status.HTTP_201_CREATED)
async def create_item(
    item_in: ItemCreate,
    db: AsyncSession = Depends(get_db)
):
    db_item = ItemModel(**item_in.model_dump())

    db.add(db_item)
    await db.commit()
    await db.refresh(db_item)
    return db_item

# Get all items
@router.get("/", response_model=List[ItemResponse])
async def get_items(db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(ItemModel))
    items = result.scalars().all()
    return items

#Get item by ID
@router.get("/{item_id}", response_model=ItemResponse)
async def get_item(item_id: int, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(ItemModel).where(ItemModel.id == item_id))
    db_item = result.scalar_one_or_none()

    if db_item is None:
        raise HTTPException(status_code=404, detail="Item not found")

    return db_item