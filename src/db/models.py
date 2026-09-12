import datetime
from sqlalchemy import Boolean, Column, DateTime, Integer, JSON, String, Text
from sqlalchemy.dialects.postgresql import JSONB
from src.db.database import Base

JSON_TYPE = JSON().with_variant(JSONB, "postgresql")


class ContentLane(Base):
    __tablename__ = "content_lanes"

    id = Column(String, primary_key=True, index=True)
    title = Column(String, nullable=False, index=True)
    subtitle = Column(String, nullable=True)
    slug = Column(String, unique=True, nullable=False, index=True)
    lane_type = Column(String, nullable=False, default="category_lane")  # category_lane, product_lane
    placement = Column(String, nullable=False, default="homepage", index=True)  # homepage, discovery, all
    card_style = Column(String, nullable=False, default="circular")  # circular, standard_card
    has_navigation_arrows = Column(Boolean, default=True)
    status = Column(String, nullable=False, default="active", index=True)  # active, draft, archived
    sort_order = Column(Integer, default=0)
    items = Column(JSON_TYPE, nullable=False, default=list)  # list of item dicts
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.datetime.utcnow, onupdate=datetime.datetime.utcnow)
    created_at = Column(DateTime(timezone=True), default=lambda: datetime.datetime.now(datetime.timezone.utc))
    updated_at = Column(DateTime(timezone=True), default=lambda: datetime.datetime.now(datetime.timezone.utc), onupdate=lambda: datetime.datetime.now(datetime.timezone.utc))
