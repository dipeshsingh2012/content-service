from typing import Optional
from fastapi import APIRouter, Depends, HTTPException, Query, Response, status
from sqlalchemy.ext.asyncio import AsyncSession

from src.db.database import get_db
from src.schemas.lane import LaneCreate, LaneListResponse, LaneResponse, LaneUpdate
from src.services.lane_service import LaneService

router = APIRouter(prefix="/api/v1")


@router.get("/health", tags=["Health"])
async def health_check():
    return {"status": "ok", "service": "content-service", "version": "0.1.0"}


@router.get(
    "/lanes",
    response_model=LaneListResponse,
    tags=["Content Lanes"],
    summary="List and filter content lanes",
)
async def list_lanes(
    response: Response,
    placement: Optional[str] = Query(None, description="Filter by placement (e.g. homepage, discovery, all)"),
    status: Optional[str] = Query(None, description="Filter by status (active, draft, archived)"),
    lane_type: Optional[str] = Query(None, description="Filter by lane type (category_lane, product_lane)"),
    q: Optional[str] = Query(None, description="Search query across title, slug, subtitle"),
    offset: int = Query(0, ge=0),
    limit: int = Query(50, ge=1, le=100),
    db: AsyncSession = Depends(get_db),
):
    service = LaneService(db)
    items, total = await service.list_lanes(
        placement=placement,
        status=status,
        lane_type=lane_type,
        q=q,
        offset=offset,
        limit=limit,
    )
    response.headers["X-Total-Count"] = str(total)
    return LaneListResponse(items=[LaneResponse.model_validate(item) for item in items], total=total)


@router.get(
    "/lanes/{lane_id}",
    response_model=LaneResponse,
    tags=["Content Lanes"],
    summary="Get single content lane by ID or slug",
)
async def get_lane(lane_id: str, db: AsyncSession = Depends(get_db)):
    service = LaneService(db)
    lane = await service.get_by_id(lane_id)
    if not lane:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Content lane '{lane_id}' not found",
        )
    return LaneResponse.model_validate(lane)


@router.post(
    "/lanes",
    response_model=LaneResponse,
    status_code=status.HTTP_201_CREATED,
    tags=["Content Lanes"],
    summary="Create a new content lane",
)
async def create_lane(payload: LaneCreate, db: AsyncSession = Depends(get_db)):
    service = LaneService(db)
    existing = await service.get_by_id(payload.slug)
    if existing:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=f"Content lane with slug '{payload.slug}' already exists",
        )
    lane = await service.create(payload)
    return LaneResponse.model_validate(lane)


@router.patch(
    "/lanes/{lane_id}",
    response_model=LaneResponse,
    tags=["Content Lanes"],
    summary="Update an existing content lane",
)
async def update_lane(
    lane_id: str,
    payload: LaneUpdate,
    db: AsyncSession = Depends(get_db),
):
    service = LaneService(db)
    lane = await service.update(lane_id, payload)
    if not lane:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Content lane '{lane_id}' not found",
        )
    return LaneResponse.model_validate(lane)


@router.delete(
    "/lanes/{lane_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    tags=["Content Lanes"],
    summary="Delete a content lane",
)
async def delete_lane(lane_id: str, db: AsyncSession = Depends(get_db)):
    service = LaneService(db)
    deleted = await service.delete(lane_id)
    if not deleted:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Content lane '{lane_id}' not found",
        )
    return Response(status_code=status.HTTP_204_NO_CONTENT)
