import torch
from transformers import CLIPProcessor, CLIPModel
from ultralytics import YOLO
from typing import Tuple, Any
import config
import sys

def load_models() -> Tuple[Any, Any, Any]:
    """
    CLIP 모델과 YOLO 모델을 로드하여 반환합니다.
    
    Returns:
        Tuple[CLIPModel, CLIPProcessor, YOLO]: 로드된 모델 및 프로세서
    """
    print("[INFO]     Loading CLIP and YOLO models...")
    
    try:
        # 1. 계산 장치(Device) 확인
        device = _get_device()
        print(f"[INFO]     Computing device: {device.upper()}")
    
        # 2. CLIP 모델 및 프로세서 로드
        clip_model = CLIPModel.from_pretrained(config.MODEL_ID)
        processor = CLIPProcessor.from_pretrained(config.MODEL_ID)
        
        # 3. YOLO 모델 로드 및 장치 이동
        yolo_model = YOLO(config.YOLO_MODEL_PATH)
        yolo_model.to(device)
        
        return clip_model, processor, yolo_model
        
    except Exception as e:
        print(f"[CRITICAL] Failed to load models: {e}")
        sys.exit(1)

def _get_device() -> str:
    """사용 가능한 최적의 계산 장치를 반환합니다."""
    if torch.backends.mps.is_available():
        return "mps"
    elif torch.cuda.is_available():
        return "cuda"
    else:
        return "cpu"