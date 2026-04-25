# 설정

MODEL_ID = "openai/clip-vit-base-patch32"
YOLO_MODEL_PATH = "yolo11s.pt"
VIDEO_PATH = "/Users/keonwoo/Documents/capstone_project/ai_prototype/video/test.mp4"
SHOW_UI = False  # UI 표시 여부 (성능 최대화를 위해 False로 설정 가능)
# YOLO 추적 대상 물체

VALID_LOST_ITEMS = {
    'backpack', 'umbrella', 'handbag', 
    'bottle', 'cup', 'cell phone', 'book'
}

# CLIP 분석 카테고리
ANALYSIS_CATEGORIES = [
    "smartphone", "earphones", "bag", "wallet", 
    "credit card", "student ID card", "textbook", "notebook", 
    "umbrella", "water bottle", "pencil case", "plush toy"
]

# CLIP 색상 프롬프트
ANALYSIS_COLORS = [
    "black", "white", "gray", "red", "blue", "green", 
    "yellow", "brown", "pink", "purple", "orange", "beige"
]

# --- 개선된 도난 탐지 설정 ---
THEFT_CONFIDENCE_THRESHOLD = 0.7  # 경고 발생을 위한 신뢰도 임계값
VERIFICATION_FRAMES = 30          # 경고 발생 전 물체가 사라져야 하는 연속 프레임 수
CONTACT_WEIGHT = 0.3              # 비소유자 접촉
OWNER_CLARITY_WEIGHT = 0.5        # 초기 소유자 지정의 명확성 (소유자 없을 시 0.0)
NO_OWNER_WEIGHT = 0.2             # 초기 소유자가 없을 때
STATIONARY_WEIGHT = 0.2           # 정지 상태의 확실성