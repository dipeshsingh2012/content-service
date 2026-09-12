from datetime import datetime
from typing import List, Optional
from pydantic import BaseModel, ConfigDict, Field


class LaneItem(BaseModel):
    id: str = Field(..., description="Unique ID for lane item")
    product_id: Optional[str] = Field(None, description="Linked catalog product ID if applicable")
    title: str = Field(..., description="Display title for circular card or item")
    subtitle: Optional[str] = Field(None, description="Taste notes, subtitle, or secondary label")
    image_url: str = Field(..., description="High-resolution image URL for card")
    target_url: str = Field(..., description="Storefront target link (e.g. #/coffees or #/product/xyz)")
    badge: Optional[str] = Field(None, description="Optional promotional badge e.g. POPULAR, NEW, SAVE 15%")
    price: Optional[str] = Field(None, description="Formatted price string if product card")
    sort_order: int = Field(0, description="Display order within lane")

    model_config = ConfigDict(from_attributes=True)


class LaneBase(BaseModel):
    title: str = Field(..., description="Public headline for lane (e.g. Explore by Category)")
    subtitle: Optional[str] = Field(None, description="Supporting subtitle copy")
    slug: str = Field(..., description="Unique URL/identifier handle")
    lane_type: str = Field("category_lane", description="Type: category_lane or product_lane")
    placement: str = Field("homepage", description="Target placement: homepage, discovery, all")
    card_style: str = Field("circular", description="Visual card style: circular or standard_card")
    has_navigation_arrows: bool = Field(True, description="Whether to show Prev/Next slider controls")
    status: str = Field("active", description="Lifecycle: active, draft, archived")
    sort_order: int = Field(0, description="Ordering of lane on page")
    items: List[LaneItem] = Field(default_factory=list, description="Ordered items in lane")

    model_config = ConfigDict(from_attributes=True)


class LaneCreate(LaneBase):
    id: Optional[str] = Field(None, description="Optional custom identifier (e.g. lane_homepage_categories)")


class LaneUpdate(BaseModel):
    title: Optional[str] = None
    subtitle: Optional[str] = None
    slug: Optional[str] = None
    lane_type: Optional[str] = None
    placement: Optional[str] = None
    card_style: Optional[str] = None
    has_navigation_arrows: Optional[bool] = None
    status: Optional[str] = None
    sort_order: Optional[int] = None
    items: Optional[List[LaneItem]] = None

    model_config = ConfigDict(from_attributes=True)


class LaneResponse(LaneBase):
    id: str
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    model_config = ConfigDict(from_attributes=True)


class LaneListResponse(BaseModel):
    items: List[LaneResponse]
    total: int

    model_config = ConfigDict(from_attributes=True)
