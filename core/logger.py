import json
import os
from datetime import datetime
from typing import Dict, List, Any

class TheftLogger:
    """도난 의심 이벤트를 JSON 파일로 기록하고 관리하는 클래스"""
    
    def __init__(self, log_file: str = "output/theft_log.json"):
        self.log_file = log_file
        self.events: List[Dict[str, Any]] = []
        self._ensure_output_dir()
        self._load_existing()

    def _ensure_output_dir(self):
        """로그 파일이 저장될 디렉토리가 존재하는지 확인하고 없으면 생성합니다."""
        output_dir = os.path.dirname(self.log_file)
        if output_dir and not os.path.exists(output_dir):
            try:
                os.makedirs(output_dir)
            except OSError as e:
                print(f"[ERROR]    Could not create log directory: {e}")

    def _load_existing(self):
        """기존 로그 파일이 있으면 데이터를 로드합니다."""
        if os.path.exists(self.log_file):
            try:
                with open(self.log_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    if isinstance(data, list):
                        self.events = data
            except (json.JSONDecodeError, IOError) as e:
                print(f"[WARN]     Existing log file corrupted or unreadable: {e}")
                self.events = []

    def log_event(self, event_type: str, data: Dict[str, Any]):
        """
        일반적인 이벤트를 기록합니다.
        """
        entry = {
            'timestamp': datetime.now().isoformat(),
            'event_type': event_type,
            'details': data
        }
        self.events.append(entry)
        self._save()
        print(f"[LOGGER]   Event recorded: {event_type}")

    def log_callback(self, data: Dict[str, Any]):
        """
        콜백 데이터 형식을 그대로 유지하면서 타임스탬프만 추가하여 기록합니다.
        
        Args:
            data: CctvCallbackRequest의 model_dump() 결과 데이터
        """
        entry = data.copy()
        # 콜백 데이터와 겹치지 않는 필드명 사용
        entry['logged_at'] = datetime.now().isoformat()
        
        self.events.append(entry)
        self._save()
        print(f"[LOGGER]   Callback data logged (Job ID: {entry.get('job_id')})")

    def _save(self):
        """현재까지의 모든 이벤트를 JSON 파일로 저장합니다."""
        try:
            # 원자적 저장을 위해 임시 파일 사용 후 교체하는 방식도 고려할 수 있으나,
            # 현재는 단순 쓰기로 구현합니다.
            with open(self.log_file, 'w', encoding='utf-8') as f:
                json.dump(self.events, f, indent=2, ensure_ascii=False)
        except IOError as e:
            print(f"[ERROR]    Failed to save log to {self.log_file}: {e}")
