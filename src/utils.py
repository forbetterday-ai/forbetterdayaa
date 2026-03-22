"""공용 유틸리티 함수"""
from datetime import datetime, timedelta
from config.config import KST

def get_kst_now() -> datetime:
    """현재 시간 KST로 반환"""
    return datetime.now(KST)

def is_within_hours(pub_date, hours: int = 24) -> bool:
    """발행 시간이 지정된 시간 내인지 확인"""
    try:
        # 텍스트 형식이면 파싱
        if isinstance(pub_date, str):
            from email.utils import parsedate_to_datetime
            pub_datetime = parsedate_to_datetime(pub_date)
        else:
            pub_datetime = pub_date
        
        # UTC로 변환
        if pub_datetime.tzinfo is None:
            pub_datetime = pub_datetime.replace(tzinfo=None)
        
        now = get_kst_now()
        cutoff = now - timedelta(hours=hours)
        
        return pub_datetime.replace(tzinfo=None) >= cutoff.replace(tzinfo=None)
    except Exception:
        return True  # 파싱 실패 시 포함

def format_publish_date(pub_date) -> str:
    """발행 시간 포맷"""
    try:
        if isinstance(pub_date, str):
            from email.utils import parsedate_to_datetime
            dt = parsedate_to_datetime(pub_date)
        else:
            dt = pub_date
        
        if dt.tzinfo is None:
            dt = KST.localize(dt)
        else:
            dt = dt.astimezone(KST)
        
        return dt.strftime('%Y년 %m월 %d일 %H:%M KST')
    except Exception:
        return str(pub_date)
