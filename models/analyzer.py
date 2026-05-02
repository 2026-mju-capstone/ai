import torch
import torch.nn.functional as F
from PIL import Image
from typing import Tuple, List, Optional, Any
from config import config

class ImageAnalyzer:
    """CLIP 모델을 사용하여 이미지의 카테고리, 색상 및 특징 벡터를 분석하는 클래스"""
    
    def __init__(self, clip_model, processor):
        self.model = clip_model
        self.processor = processor

    def _get_best_match(self, outputs: Any, labels: List[str]) -> Tuple[str, float]:
        """모델 출력에서 가장 확률이 높은 라벨과 그 확률을 반환합니다."""
        probs = outputs.logits_per_image.softmax(dim=1).squeeze().tolist()
        # 단일 라벨인 경우 리스트로 변환
        if isinstance(probs, float):
            probs = [probs]
        sorted_output = sorted(zip(labels, probs), key=lambda x: x[1], reverse=True)
        return sorted_output[0]

    def _load_image(self, img_path: str) -> Image.Image:
        """로컬 경로 또는 URL에서 이미지를 로드합니다."""
        import requests
        from io import BytesIO
        
        if img_path.startswith(('http://', 'https://')):
            response = requests.get(img_path, timeout=10)
            return Image.open(BytesIO(response.content)).convert("RGB")
        else:
            return Image.open(img_path).convert("RGB")

    def analyze_item(self, img_path: str) -> Optional[Tuple[str, str]]:
        """이미지를 분석하여 카테고리와 색상을 반환합니다."""
        if not img_path:
            return None

        try:
            image = self._load_image(img_path)
            
            # 1. 카테고리 분석
            category, prob_item = self._analyze_category(image)
            print(f"\n[ANALYSIS] Category : {category} ({prob_item*100:.1f}%)")
    
            # 2. 색상 분석
            color, prob_color = self._analyze_color(image, category)
            print(f"[ANALYSIS] Color    : {color} ({prob_color*100:.1f}%)")
    
            return category, color
        except Exception as e:
            print(f"[ERROR]    Failed to analyze image: {e}")
            return None

    def _analyze_category(self, image: Image.Image) -> Tuple[str, float]:
        """이미지의 물체 카테고리를 추론합니다."""
        inputs = self.processor(
            text=config.ANALYSIS_CATEGORIES, 
            images=image, 
            return_tensors="pt", 
            padding=True
        )
        with torch.no_grad():
            outputs = self.model(**inputs)
        return self._get_best_match(outputs, config.ANALYSIS_CATEGORIES)

    def _analyze_color(self, image: Image.Image, category: str) -> Tuple[str, float]:
        """물체의 색상을 추론합니다."""
        color_prompts = [f"{c} {category}" for c in config.ANALYSIS_COLORS]
        inputs_color = self.processor(
            text=color_prompts, 
            images=image, 
            return_tensors="pt", 
            padding=True
        )
        with torch.no_grad():
            outputs_color = self.model(**inputs_color)
        best_prompt, prob = self._get_best_match(outputs_color, color_prompts)
        return best_prompt.split()[0], prob

    def extract_vector(self, image_path: str) -> Optional[List[float]]:
        """이미지에서 특징 벡터를 추출합니다."""
        if not image_path:
            return None
            
        try:
            image = self._load_image(image_path)
            inputs = self.processor(images=image, return_tensors="pt")
    
            with torch.no_grad():
                outputs = self.model.get_image_features(**inputs)
                features = self._normalize_features(outputs)
                
            return features.squeeze().cpu().numpy().tolist()
        except Exception as e:
            print(f"[ERROR]    Failed to extract vector: {e}")
            return None

    def _normalize_features(self, outputs: Any) -> torch.Tensor:
        """모델 출력에서 특징을 추출하고 정규화합니다."""
        if hasattr(outputs, 'image_embeds'):
            features = outputs.image_embeds
        elif hasattr(outputs, 'pooler_output'):
            features = outputs.pooler_output
        elif isinstance(outputs, torch.Tensor):
            features = outputs
        else:
            features = outputs[0]
            
        return F.normalize(features, p=2, dim=-1)
