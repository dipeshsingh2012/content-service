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
    created_at = Column(DateTime(timezone=True), default=lambda: datetime.datetime.now(datetime.timezone.utc))
    updated_at = Column(DateTime(timezone=True), default=lambda: datetime.datetime.now(datetime.timezone.utc), onupdate=lambda: datetime.datetime.now(datetime.timezone.utc))


class CMSPage(Base):
    __tablename__ = "cms_pages"

    id = Column(String, primary_key=True, index=True)
    page_type = Column(String, nullable=False, default="static", index=True)  # home, collection, discovery, static
    title = Column(String, nullable=False, index=True)
    slug = Column(String, unique=True, nullable=False, index=True)
    description = Column(Text, nullable=True)
    is_published = Column(Boolean, nullable=False, default=True, index=True)
    sections = Column(JSON_TYPE, nullable=False, default=list)  # list of section dicts
    created_at = Column(DateTime(timezone=True), default=lambda: datetime.datetime.now(datetime.timezone.utc))
    updated_at = Column(DateTime(timezone=True), default=lambda: datetime.datetime.now(datetime.timezone.utc), onupdate=lambda: datetime.datetime.now(datetime.timezone.utc))


class CMSSiteShell(Base):
    __tablename__ = "cms_site_shell"

    id = Column(String, primary_key=True, default="default")  # Singleton key 'default'
    promo_bar = Column(JSON_TYPE, nullable=False, default=dict)
    header = Column(JSON_TYPE, nullable=False, default=dict)
    footer = Column(JSON_TYPE, nullable=False, default=dict)
    theme = Column(JSON_TYPE, nullable=False, default=dict)
    created_at = Column(DateTime(timezone=True), default=lambda: datetime.datetime.now(datetime.timezone.utc))
    updated_at = Column(DateTime(timezone=True), default=lambda: datetime.datetime.now(datetime.timezone.utc), onupdate=lambda: datetime.datetime.now(datetime.timezone.utc))


class CMSThemePreset(Base):
    __tablename__ = "cms_theme_presets"

    id = Column(String, primary_key=True, index=True)
    name = Column(String, nullable=False)
    preset = Column(String, unique=True, nullable=False, index=True)
    mode = Column(String, nullable=False, default="light")
    primary_color = Column(String, nullable=False)
    accent_color = Column(String, nullable=False)
    surface_color = Column(String, nullable=False)
    background_color = Column(String, nullable=False)
    text_color = Column(String, nullable=False)
    font_family = Column(String, nullable=False, default="sans")
    border_radius = Column(String, nullable=False, default="rounded-2xl")
    badge_text = Column(String, nullable=True)
    is_active = Column(Boolean, nullable=False, default=False)
    sort_order = Column(Integer, default=0)
    created_at = Column(DateTime(timezone=True), default=lambda: datetime.datetime.now(datetime.timezone.utc))
    updated_at = Column(DateTime(timezone=True), default=lambda: datetime.datetime.now(datetime.timezone.utc), onupdate=lambda: datetime.datetime.now(datetime.timezone.utc))

