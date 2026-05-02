from contextlib import asynccontextmanager
import uvicorn
import asyncio
from fastapi import FastAPI

from api.vision import vision
from api.cctv import cctv, service, test_callback # service, test_callback 추가
from models.loader import load_models

@asynccontextmanager
async def lifespan(app: FastAPI):
    # 서버 시작 시 모델 로드
    load_models()
    # 서버 시작 시 백그라운드 워커 실행
    asyncio.create_task(service.cctv_service.run_worker())
    yield

app = FastAPI(
    title="2026 Myongji Capstone AI Server",
    description="CCTV Theft Detection System - AI Worker Server",
    version="1.0.0",
    lifespan=lifespan
)

# 라우터 등록
app.include_router(vision.router)
app.include_router(cctv.router)
app.include_router(test_callback.router) # 테스트 콜백 라우터 등록

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)