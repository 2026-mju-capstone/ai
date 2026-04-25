from fastapi import APIRouter
from .schema import VisionRequest, VisionResponse
from .service import vision_service


router = APIRouter(
    prefix="/vision",
    tags=["vision"],
)

@router.post("/analyze", response_model=VisionResponse)
async def analyze_vision(request: VisionRequest):
    """
    단일 비전 이미지 분석 (동기 처리)
    """
    # 서비스 호출
    result = await vision_service.analyze_image(request.image_url)

    # result를 VisionResponse 형태로 변환
    return VisionResponse(**result)