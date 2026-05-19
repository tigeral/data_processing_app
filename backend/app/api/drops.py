import logging
from fastapi import APIRouter
from app.schemas.drop import DropPayload

logger = logging.getLogger(__name__)
router = APIRouter()


@router.post("/drops", status_code=200)
async def receive_drops(payload: DropPayload) -> dict:
    for item in payload.items:
        details = f"type={item.type.value} name={item.name!r}"
        if item.mime_type:
            details += f" mime={item.mime_type}"
        if item.size is not None:
            details += f" size={item.size}B"
        if item.url:
            details += f" url={item.url}"
        if item.children:
            details += f" children={item.children}"
        logger.info("DROP %s", details)
    return {"received": len(payload.items)}
