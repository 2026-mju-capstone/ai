import torch
from transformers import CLIPModel, CLIPProcessor
from ultralytics import YOLO
from config import config
import sys
from typing import Tuple

# 모델 캐싱을 위한 전역 변수
_cached_models = None

def load_models() -> Tuple[CLIPModel, CLIPProcessor, YOLO]:
    """
    CLIP 모델과 YOLO 모델을 메모리에 로드합니다. (싱글톤 방식)
    """
    global _cached_models
    
    # 이미 로드된 경우 캐시된 모델 반환
    if _cached_models is not None:
        return _cached_models

    print("[INFO]     Loading CLIP and YOLO models for the first time...")
    
    try:
        # 1. 장치(Device) 확인
        device = _get_device()
        print(f"[INFO]     Computing device: {device.upper()}")
    
        # 2. CLIP 모델 및 프로세서 로드
        clip_model = CLIPModel.from_pretrained(config.MODEL_ID)
        processor = CLIPProcessor.from_pretrained(config.MODEL_ID)
        
        # 3. YOLO 모델 로드 및 장치 이동
        yolo_model = YOLO(config.YOLO_MODEL_PATH)
        yolo_model.to(device)
        
        # 결과를 전역 변수에 저장
        _cached_models = (clip_model, processor, yolo_model)
        return _cached_models
        
    except Exception as e:
        print(f"[CRITICAL] Failed to load models: {e}")
        sys.exit(1)

def _get_device() -> str:
    """사용 가능한 최적의 장치로 반환합니다."""
    if torch.backends.mps.is_available():
        return "mps"
    elif torch.cuda.is_available():
        return "cuda"
    else:
        return "cpu"