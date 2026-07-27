from datetime import datetime
from pydantic import BaseModel, ConfigDict, Field


class ItemBase(BaseModel):
    name: str
    price: float = Field(..., gt=0)
    stock: int = Field(default=0, ge=0)
    cat_id: int | None = None
    description: str | None = None
    image_url: str | None = None


class ItemCreate(ItemBase):
    pass


class ItemResponse(ItemBase):
    id: int
    date_created: datetime
    last_updated: datetime

    model_config = ConfigDict(from_attributes=True)