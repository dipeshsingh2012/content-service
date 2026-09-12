import re
from typing import Optional, List, Tuple
from sqlalchemy import select, func, or_
from sqlalchemy.ext.asyncio import AsyncSession
from src.db.models import ContentLane
from src.schemas.lane import LaneCreate, LaneUpdate


class LaneService:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def list_lanes(
        self,
        placement: Optional[str] = None,
        status: Optional[str] = None,
        lane_type: Optional[str] = None,
        q: Optional[str] = None,
        offset: int = 0,
        limit: int = 50,
    ) -> Tuple[List[ContentLane], int]:
        stmt = select(ContentLane)
        count_stmt = select(func.count(ContentLane.id))

        filters = []
        if placement and placement != "all":
            filters.append(or_(ContentLane.placement == placement, ContentLane.placement == "all"))
        if status and status != "all":
            filters.append(ContentLane.status == status)
        if lane_type and lane_type != "all":
            filters.append(ContentLane.lane_type == lane_type)
        if q:
            term = f"%{q}%"
            filters.append(
                or_(
                    ContentLane.title.ilike(term),
                    ContentLane.slug.ilike(term),
                    ContentLane.subtitle.ilike(term),
                )
            )

        if filters:
            stmt = stmt.where(*filters)
            count_stmt = count_stmt.where(*filters)

        stmt = stmt.order_by(ContentLane.sort_order.asc(), ContentLane.created_at.desc())
        stmt = stmt.offset(offset).limit(limit)

        total_res = await self.db.execute(count_stmt)
        total = total_res.scalar() or 0

        res = await self.db.execute(stmt)
        items = list(res.scalars().all())

        return items, total

    async def get_by_id(self, lane_id: str) -> Optional[ContentLane]:
        stmt = select(ContentLane).where(or_(ContentLane.id == lane_id, ContentLane.slug == lane_id))
        res = await self.db.execute(stmt)
        return res.scalar_one_or_none()

    async def create(self, payload: LaneCreate) -> ContentLane:
        lane_id = payload.id
        if not lane_id:
            clean_slug = re.sub(r"[^a-zA-Z0-9_]", "_", payload.slug.lower())
            lane_id = f"lane_{clean_slug}"

        # Convert items to raw dicts for JSON storage
        items_dict = [item.model_dump() for item in payload.items] if payload.items else []

        lane = ContentLane(
            id=lane_id,
            title=payload.title,
            subtitle=payload.subtitle,
            slug=payload.slug,
            lane_type=payload.lane_type,
            placement=payload.placement,
            card_style=payload.card_style,
            has_navigation_arrows=payload.has_navigation_arrows,
            status=payload.status,
            sort_order=payload.sort_order,
            items=items_dict,
        )
        self.db.add(lane)
        await self.db.commit()
        await self.db.refresh(lane)
        return lane

    async def update(self, lane_id: str, payload: LaneUpdate) -> Optional[ContentLane]:
        lane = await self.get_by_id(lane_id)
        if not lane:
            return None

        update_data = payload.model_dump(exclude_unset=True)
        if "items" in update_data and update_data["items"] is not None:
            update_data["items"] = [
                item.model_dump() if hasattr(item, "model_dump") else item
                for item in update_data["items"]
            ]

        for field, value in update_data.items():
            setattr(lane, field, value)

        await self.db.commit()
        await self.db.refresh(lane)
        return lane

    async def delete(self, lane_id: str) -> bool:
        lane = await self.get_by_id(lane_id)
        if not lane:
            return False

        await self.db.delete(lane)
        await self.db.commit()
        return True
