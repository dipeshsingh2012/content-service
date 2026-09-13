from datetime import datetime
from typing import Any, Dict, List, Literal, Optional
from pydantic import BaseModel, ConfigDict, Field

# ==========================================
# Global Site Shell Schemas
# ==========================================

ThemeColor = Literal["amber", "espresso", "emerald", "crimson", "slate"]


class PromoBarConfig(BaseModel):
    enabled: bool = True
    text: str
    cta_text: Optional[str] = None
    cta_url: Optional[str] = None
    theme: str = "amber"
    badge: Optional[str] = None
    dismissible: Optional[bool] = True

    model_config = ConfigDict(from_attributes=True)


class NavNode(BaseModel):
    id: str
    label: str
    url: str
    badge: Optional[str] = None
    is_external: Optional[bool] = False
    children: Optional[List["NavNode"]] = None

    model_config = ConfigDict(from_attributes=True)


class HeaderConfig(BaseModel):
    brand_name: str
    brand_tagline: Optional[str] = None
    brand_badge: Optional[str] = None
    logo_url: Optional[str] = "/logo.jpg"
    nodes: List[NavNode] = Field(default_factory=list)
    show_search: bool = True
    show_cart: bool = True
    show_spatial_finder: bool = True
    sticky: bool = True

    model_config = ConfigDict(from_attributes=True)


class FooterLink(BaseModel):
    label: str
    url: str
    is_external: Optional[bool] = False

    model_config = ConfigDict(from_attributes=True)


class FooterColumn(BaseModel):
    id: str
    title: str
    links: List[FooterLink] = Field(default_factory=list)

    model_config = ConfigDict(from_attributes=True)


class SocialLink(BaseModel):
    platform: str
    url: str

    model_config = ConfigDict(from_attributes=True)


class FooterConfig(BaseModel):
    brand_name: str
    brand_description: str
    columns: List[FooterColumn] = Field(default_factory=list)
    show_newsletter: bool = True
    newsletter_title: Optional[str] = None
    newsletter_placeholder: Optional[str] = None
    social_links: List[SocialLink] = Field(default_factory=list)
    copyright: str

    model_config = ConfigDict(from_attributes=True)


ThemePreset = Literal["alpine", "amber", "espresso", "emerald", "crimson", "slate"]
ThemeMode = Literal["light", "dark", "system"]
FontFamily = Literal["sans", "serif", "mono"]
BorderRadius = Literal["rounded-none", "rounded-lg", "rounded-xl", "rounded-2xl", "rounded-full"]


class ThemeConfig(BaseModel):
    id: str = "theme_hill_jhil_alpine"
    name: str = "Hill Jhil Alpine Tarn"
    preset: ThemePreset = "alpine"
    mode: ThemeMode = "light"
    primary_color: str = "#085454"
    accent_color: str = "#0d9488"
    surface_color: str = "#ffffff"
    background_color: str = "#f0fdfa"
    text_color: str = "#042f2e"
    font_family: FontFamily = "serif"
    border_radius: BorderRadius = "rounded-2xl"
    badge_text: Optional[str] = "ALPINE ESTATE HARVEST"
    is_active: bool = True
    updated_at: Optional[str] = None

    model_config = ConfigDict(from_attributes=True)


class ThemeConfigUpdate(BaseModel):
    id: Optional[str] = None
    name: Optional[str] = None
    preset: Optional[ThemePreset] = None
    mode: Optional[ThemeMode] = None
    primary_color: Optional[str] = None
    accent_color: Optional[str] = None
    surface_color: Optional[str] = None
    background_color: Optional[str] = None
    text_color: Optional[str] = None
    font_family: Optional[FontFamily] = None
    border_radius: Optional[BorderRadius] = None
    badge_text: Optional[str] = None
    is_active: Optional[bool] = None

    model_config = ConfigDict(from_attributes=True)


class GlobalShellConfig(BaseModel):
    promo_bar: PromoBarConfig
    header: HeaderConfig
    footer: FooterConfig
    theme: Optional[ThemeConfig] = Field(default_factory=ThemeConfig)

    model_config = ConfigDict(from_attributes=True)


class GlobalShellResponse(GlobalShellConfig):
    id: str = "default"
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    model_config = ConfigDict(from_attributes=True)


class GlobalShellUpdate(BaseModel):
    promo_bar: Optional[PromoBarConfig] = None
    header: Optional[HeaderConfig] = None
    footer: Optional[FooterConfig] = None
    theme: Optional[ThemeConfig] = None

    model_config = ConfigDict(from_attributes=True)


# ==========================================
# CMS Page & Section Schemas
# ==========================================

PageType = Literal["home", "product", "collection", "discovery", "static"]

SectionType = Literal[
    "hero_banner",
    "category_lane",
    "category_grid",
    "product_lane",
    "product_grid",
    "testimonials",
    "promo_callout",
]


class PageSection(BaseModel):
    id: str
    type: str
    title: str
    subtitle: Optional[str] = None
    is_active: bool = True
    sort_order: int = 1
    config: Dict[str, Any] = Field(default_factory=dict)

    model_config = ConfigDict(from_attributes=True)


class CMSPageBase(BaseModel):
    page_type: str = "static"
    title: str
    slug: str
    description: Optional[str] = None
    is_published: bool = True
    sections: List[PageSection] = Field(default_factory=list)

    model_config = ConfigDict(from_attributes=True)


class CMSPageCreate(CMSPageBase):
    id: Optional[str] = None


class CMSPageUpdate(BaseModel):
    page_type: Optional[str] = None
    title: Optional[str] = None
    slug: Optional[str] = None
    description: Optional[str] = None
    is_published: Optional[bool] = None
    sections: Optional[List[PageSection]] = None

    model_config = ConfigDict(from_attributes=True)


class CMSPageResponse(CMSPageBase):
    id: str
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    model_config = ConfigDict(from_attributes=True)


class CMSPageListResponse(BaseModel):
    items: List[CMSPageResponse]
    total: int

    model_config = ConfigDict(from_attributes=True)


class CMSResetResponse(BaseModel):
    message: str
    shell: GlobalShellConfig
    pages: List[CMSPageResponse]

    model_config = ConfigDict(from_attributes=True)

