from fastapi import APIRouter, BackgroundTasks, status
from .schema import CctvAnalyzeRequest, CctvAnalyzeResponse
from .service import cctv_service

router = APIRouter(
    prefix="/cctv",
    tags=["cctv"],
)

@router.post("/analyze", response_model=CctvAnalyzeResponse, status_code=status.HTTP_202_ACCEPTED)
async def analyze_cctv(request: CctvAnalyzeRequest, background_tasks: BackgroundTasks):
    """
    CCTV 영상 분석 요청 접수 (비동기 처리)
    """
    # 백그라운드 작업 등록
    background_tasks.add_task(
        cctv_service.analyze_video_async,
        request
    )
    
    # 202 Accepted와 함께 현재 상태 PROCESSING 반환 (명세서 기준)
    return CctvAnalyzeResponse(
        job_id=request.job_id,
        status="PROCESSING"
    )

@router.post("/callback")
async def test_callback(payload: dict):
    print("테스트용 콜백")
    print(payload)

    return {"success": True}