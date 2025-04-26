from fastapi import APIRouter, File, HTTPException, UploadFile, status

from src.utils.s3 import upload_file

router = APIRouter(prefix="/uploads", tags=["Media"])


@router.post("/images", status_code=status.HTTP_201_CREATED)
async def upload_image(file: UploadFile = File(...)) -> dict[str, str]:
    if file.content_type not in {"image/jpeg", "image/png", "image/webp"}:
        raise HTTPException(
            status_code=status.HTTP_415_UNSUPPORTED_MEDIA_TYPE,
            detail="Unsupported image format",
        )
    data = await file.read()
    if len(data) > 5 * 1024 * 1024:
        raise HTTPException(
            status_code=status.HTTP_413_REQUEST_ENTITY_TOO_LARGE,
            detail="Image is too large",
        )
    url = upload_file(data, file.content_type)
    return {"url": url}
