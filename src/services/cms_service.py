import datetime
import re
from typing import List, Optional, Tuple
from sqlalchemy import func, or_, select
from sqlalchemy.ext.asyncio import AsyncSession

from src.db.models import CMSPage, CMSSiteShell, CMSThemePreset
from src.db.seed import DEFAULT_GLOBAL_SHELL, DEFAULT_THEME_PRESETS_LIST, seed_cms_data
from src.schemas.cms import CMSPageCreate, CMSPageUpdate, GlobalShellUpdate


class CMSService:
    def __init__(self, db: AsyncSession):
        self.db = db

    # ----------------------------------------------------
    # Global Site Shell Operations
    # ----------------------------------------------------
    async def get_shell(self) -> CMSSiteShell:
        stmt = select(CMSSiteShell).where(CMSSiteShell.id == "default")
        res = await self.db.execute(stmt)
        shell = res.scalar_one_or_none()
        if not shell:
            shell = CMSSiteShell(
                id="default",
                promo_bar=DEFAULT_GLOBAL_SHELL["promo_bar"],
                header=DEFAULT_GLOBAL_SHELL["header"],
                footer=DEFAULT_GLOBAL_SHELL["footer"],
                theme=DEFAULT_GLOBAL_SHELL["theme"],
            )
            self.db.add(shell)
            await self.db.commit()
            await self.db.refresh(shell)
        elif not shell.theme:
            shell.theme = DEFAULT_GLOBAL_SHELL["theme"]
            await self.db.commit()
            await self.db.refresh(shell)
        return shell

    async def update_shell(self, payload: GlobalShellUpdate) -> CMSSiteShell:
        shell = await self.get_shell()
        update_data = payload.model_dump(exclude_unset=True)

        for field in ["promo_bar", "header", "footer", "theme"]:
            if field in update_data and update_data[field] is not None:
                val = update_data[field]
                setattr(shell, field, val.model_dump() if hasattr(val, "model_dump") else val)

        await self.db.commit()
        await self.db.refresh(shell)
        return shell

    # ----------------------------------------------------
    # Theme Presets Operations (PostgreSQL-backed)
    # ----------------------------------------------------
    async def get_theme_presets(self) -> List[CMSThemePreset]:
        stmt = select(CMSThemePreset).order_by(CMSThemePreset.sort_order.asc())
        res = await self.db.execute(stmt)
        presets = res.scalars().all()
        if not presets:
            for preset_data in DEFAULT_THEME_PRESETS_LIST:
                preset = CMSThemePreset(**preset_data)
                self.db.add(preset)
            await self.db.commit()
            res = await self.db.execute(stmt)
            presets = res.scalars().all()
        return list(presets)

    async def get_theme_preset(self, preset_key: str) -> Optional[CMSThemePreset]:
        stmt = select(CMSThemePreset).where(CMSThemePreset.preset == preset_key)
        res = await self.db.execute(stmt)
        return res.scalar_one_or_none()

    # ----------------------------------------------------
    # CMS Pages Operations
    # ----------------------------------------------------
    async def list_pages(
        self,
        page_type: Optional[str] = None,
        is_published: Optional[bool] = None,
        q: Optional[str] = None,
        offset: int = 0,
        limit: int = 50,
    ) -> Tuple[List[CMSPage], int]:
        stmt = select(CMSPage)
        count_stmt = select(func.count(CMSPage.id))

        filters = []
        if page_type and page_type != "all":
            filters.append(CMSPage.page_type == page_type)
        if is_published is not None:
            filters.append(CMSPage.is_published == is_published)
        if q:
            term = f"%{q}%"
            filters.append(
                or_(
                    CMSPage.title.ilike(term),
                    CMSPage.slug.ilike(term),
                    CMSPage.description.ilike(term),
                )
            )

        if filters:
            stmt = stmt.where(*filters)
            count_stmt = count_stmt.where(*filters)

        stmt = stmt.order_by(CMSPage.created_at.asc()).offset(offset).limit(limit)

        total_res = await self.db.execute(count_stmt)
        total = total_res.scalar() or 0

        res = await self.db.execute(stmt)
        items = list(res.scalars().all())

        return items, total

    async def get_page_by_id_or_slug(self, page_id: str) -> Optional[CMSPage]:
        clean_id = page_id.strip()
        with_slash = "/" + clean_id.lstrip("/")
        without_slash = clean_id.lstrip("/")
        stmt = select(CMSPage).where(
            or_(
                CMSPage.id == clean_id,
                CMSPage.slug == clean_id,
                CMSPage.slug == with_slash,
                CMSPage.slug == without_slash,
            )
        )
        res = await self.db.execute(stmt)
        return res.scalar_one_or_none()

    async def create_page(self, payload: CMSPageCreate) -> CMSPage:
        # Check slug uniqueness
        existing = await self.get_page_by_id_or_slug(payload.slug)
        if existing:
            raise ValueError(f"CMS Page with slug '{payload.slug}' already exists")

        page_id = payload.id
        if not page_id:
            clean_slug = re.sub(r"[^a-zA-Z0-9_]", "_", payload.slug.strip("/"))
            suffix = clean_slug if clean_slug else "home"
            page_id = f"page_{suffix}_{int(datetime.datetime.now(datetime.timezone.utc).timestamp())}"

        sections_dict = [
            sec.model_dump() if hasattr(sec, "model_dump") else sec
            for sec in payload.sections
        ] if payload.sections else []

        page = CMSPage(
            id=page_id,
            page_type=payload.page_type,
            title=payload.title,
            slug=payload.slug,
            description=payload.description,
            is_published=payload.is_published,
            sections=sections_dict,
        )
        self.db.add(page)
        await self.db.commit()
        await self.db.refresh(page)
        return page

    async def update_page(self, page_id: str, payload: CMSPageUpdate) -> Optional[CMSPage]:
        page = await self.get_page_by_id_or_slug(page_id)
        if not page:
            return None

        update_data = payload.model_dump(exclude_unset=True)

        if "slug" in update_data and update_data["slug"] != page.slug:
            existing_slug = await self.get_page_by_id_or_slug(update_data["slug"])
            if existing_slug and existing_slug.id != page.id:
                raise ValueError(f"CMS Page with slug '{update_data['slug']}' already exists")

        if "sections" in update_data and update_data["sections"] is not None:
            update_data["sections"] = [
                sec.model_dump() if hasattr(sec, "model_dump") else sec
                for sec in update_data["sections"]
            ]

        for field, value in update_data.items():
            setattr(page, field, value)

        await self.db.commit()
        await self.db.refresh(page)
        return page

    async def delete_page(self, page_id: str) -> bool:
        page = await self.get_page_by_id_or_slug(page_id)
        if not page:
            return False

        await self.db.delete(page)
        await self.db.commit()
        return True

    # ----------------------------------------------------
    # Reset Defaults
    # ----------------------------------------------------
    async def reset_defaults(self) -> Tuple[CMSSiteShell, List[CMSPage]]:
        await seed_cms_data(self.db, force_reset=True)
        shell = await self.get_shell()
        pages_res = await self.db.execute(select(CMSPage).order_by(CMSPage.created_at.asc()))
        pages = list(pages_res.scalars().all())
        return shell, pages
