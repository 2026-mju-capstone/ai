import cv2
import platform
from config import config

class Visualizer:
    """탐지 결과를 화면에 시각화하는 클래스"""
    
    def __init__(self, window_name="Theft Detection System"):
        self.window_name = window_name
        self.font = cv2.FONT_HERSHEY_SIMPLEX

    def render(self, frame, detection_result, frame_count, total_frames, avg_fps):
        """프레임에 탐지 정보와 상태를 그려 화면에 표시합니다."""
        # 1. YOLO 기본 어노테이션 (박스, 라벨)
        annotated_frame = detection_result.plot()
        
        # 2. UI 오버레이 (반투명 배경)
        overlay = annotated_frame.copy()
        cv2.rectangle(overlay, (10, 10), (320, 90), (0, 0, 0), -1)
        cv2.addWeighted(overlay, 0.4, annotated_frame, 0.6, 0, annotated_frame)
        
        # 3. 상태 정보 텍스트 표시 (프레임 진행도 및 FPS)
        cv2.putText(annotated_frame, f"Frame: {frame_count} / {total_frames}", 
                    (20, 40), self.font, 0.7, (255, 255, 255), 2)
        cv2.putText(annotated_frame, f"Avg FPS: {avg_fps:.2f}", 
                    (20, 75), self.font, 0.7, (0, 255, 0), 2)

        # 4. 화면 출력
        cv2.imshow(self.window_name, annotated_frame)

    def close(self):
        """윈도우 리소스 해제"""
        cv2.destroyAllWindows()
        # macOS 환경에서의 윈도우 닫기 이슈 대응
        if platform.system() == 'Darwin':
            cv2.waitKey(1)
