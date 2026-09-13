from typing import Optional
from fastapi import APIRouter, Depends, HTTPException, Query, Response, status
from sqlalchemy.ext.asyncio import AsyncSession

from src.db.database import get_db
from src.schemas.lane import LaneCreate, LaneListResponse, LaneResponse, LaneUpdate
from src.services.lane_service import LaneService
from src.schemas.cms import (
    CMSPageCreate,
    CMSPageListResponse,
    CMSPageResponse,
    CMSPageUpdate,
    CMSResetResponse,
    FooterConfig,
    GlobalShellResponse,
    GlobalShellUpdate,
    HeaderConfig,
    PromoBarConfig,
)
from src.services.cms_service import CMSService

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


# ====================================================
# CMS Global Site Shell Endpoints
# ====================================================

@router.get(
    "/cms/shell",
    response_model=GlobalShellResponse,
    tags=["CMS Global Shell"],
    summary="Get active global site shell configuration (promo bar, header, footer)",
)
async def get_cms_shell(db: AsyncSession = Depends(get_db)):
    service = CMSService(db)
    shell = await service.get_shell()
    return GlobalShellResponse.model_validate(shell)


@router.put(
    "/cms/shell",
    response_model=GlobalShellResponse,
    tags=["CMS Global Shell"],
    summary="Update or upsert global site shell configuration",
)
async def update_cms_shell(payload: GlobalShellUpdate, db: AsyncSession = Depends(get_db)):
    service = CMSService(db)
    shell = await service.update_shell(payload)
    return GlobalShellResponse.model_validate(shell)


@router.get(
    "/cms/shell/promo-bar",
    response_model=PromoBarConfig,
    tags=["CMS Global Shell"],
    summary="Get active promo bar configuration",
)
async def get_cms_promo_bar(db: AsyncSession = Depends(get_db)):
    service = CMSService(db)
    shell = await service.get_shell()
    return PromoBarConfig.model_validate(shell.promo_bar)


@router.put(
    "/cms/shell/promo-bar",
    response_model=PromoBarConfig,
    tags=["CMS Global Shell"],
    summary="Update active promo bar configuration",
)
async def update_cms_promo_bar(payload: PromoBarConfig, db: AsyncSession = Depends(get_db)):
    service = CMSService(db)
    shell = await service.update_shell(GlobalShellUpdate(promo_bar=payload))
    return PromoBarConfig.model_validate(shell.promo_bar)


@router.get(
    "/cms/shell/header",
    response_model=HeaderConfig,
    tags=["CMS Global Shell"],
    summary="Get active header navigation configuration",
)
async def get_cms_header(db: AsyncSession = Depends(get_db)):
    service = CMSService(db)
    shell = await service.get_shell()
    return HeaderConfig.model_validate(shell.header)


@router.put(
    "/cms/shell/header",
    response_model=HeaderConfig,
    tags=["CMS Global Shell"],
    summary="Update active header navigation configuration",
)
async def update_cms_header(payload: HeaderConfig, db: AsyncSession = Depends(get_db)):
    service = CMSService(db)
    shell = await service.update_shell(GlobalShellUpdate(header=payload))
    return HeaderConfig.model_validate(shell.header)


@router.get(
    "/cms/shell/footer",
    response_model=FooterConfig,
    tags=["CMS Global Shell"],
    summary="Get active footer configuration",
)
async def get_cms_footer(db: AsyncSession = Depends(get_db)):
    service = CMSService(db)
    shell = await service.get_shell()
    return FooterConfig.model_validate(shell.footer)


@router.put(
    "/cms/shell/footer",
    response_model=FooterConfig,
    tags=["CMS Global Shell"],
    summary="Update active footer configuration",
)
async def update_cms_footer(payload: FooterConfig, db: AsyncSession = Depends(get_db)):
    service = CMSService(db)
    shell = await service.update_shell(GlobalShellUpdate(footer=payload))
    return FooterConfig.model_validate(shell.footer)


# ====================================================
# CMS Pages Endpoints
# ====================================================

@router.get(
    "/cms/pages",
    response_model=CMSPageListResponse,
    tags=["CMS Pages"],
    summary="List and filter CMS pages",
)
async def list_cms_pages(
    response: Response,
    page_type: Optional[str] = Query(None, description="Filter by page type (home, collection, discovery, static)"),
    is_published: Optional[bool] = Query(None, description="Filter by published status"),
    q: Optional[str] = Query(None, description="Search across title, slug, description"),
    offset: int = Query(0, ge=0),
    limit: int = Query(50, ge=1, le=100),
    db: AsyncSession = Depends(get_db),
):
    service = CMSService(db)
    items, total = await service.list_pages(
        page_type=page_type,
        is_published=is_published,
        q=q,
        offset=offset,
        limit=limit,
    )
    response.headers["X-Total-Count"] = str(total)
    return CMSPageListResponse(
        items=[CMSPageResponse.model_validate(item) for item in items],
        total=total,
    )


@router.get(
    "/cms/pages/{page_id}",
    response_model=CMSPageResponse,
    tags=["CMS Pages"],
    summary="Get single CMS page by ID or slug",
)
async def get_cms_page(page_id: str, db: AsyncSession = Depends(get_db)):
    service = CMSService(db)
    page = await service.get_page_by_id_or_slug(page_id)
    if not page:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"CMS page '{page_id}' not found",
        )
    return CMSPageResponse.model_validate(page)


@router.post(
    "/cms/pages",
    response_model=CMSPageResponse,
    status_code=status.HTTP_201_CREATED,
    tags=["CMS Pages"],
    summary="Create a new CMS page",
)
async def create_cms_page(payload: CMSPageCreate, db: AsyncSession = Depends(get_db)):
    service = CMSService(db)
    try:
        page = await service.create_page(payload)
        return CMSPageResponse.model_validate(page)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=str(e))


@router.patch(
    "/cms/pages/{page_id}",
    response_model=CMSPageResponse,
    tags=["CMS Pages"],
    summary="Update an existing CMS page",
)
async def update_cms_page(
    page_id: str,
    payload: CMSPageUpdate,
    db: AsyncSession = Depends(get_db),
):
    service = CMSService(db)
    try:
        page = await service.update_page(page_id, payload)
        if not page:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"CMS page '{page_id}' not found",
            )
        return CMSPageResponse.model_validate(page)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=str(e))


@router.delete(
    "/cms/pages/{page_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    tags=["CMS Pages"],
    summary="Delete a CMS page",
)
async def delete_cms_page(page_id: str, db: AsyncSession = Depends(get_db)):
    service = CMSService(db)
    deleted = await service.delete_page(page_id)
    if not deleted:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"CMS page '{page_id}' not found",
        )
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.post(
    "/cms/reset-defaults",
    response_model=CMSResetResponse,
    tags=["CMS Pages"],
    summary="Reset CMS pages, layouts, and site shell to default showcase state",
)
async def reset_cms_defaults(db: AsyncSession = Depends(get_db)):
    service = CMSService(db)
    shell, pages = await service.reset_defaults()
    return CMSResetResponse(
        message="CMS layouts and site shell successfully reset to defaults",
        shell=GlobalShellResponse.model_validate(shell),
        pages=[CMSPageResponse.model_validate(p) for p in pages],
    )

