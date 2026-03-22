"""
Gmail SMTP를 통한 이메일 발송
"""
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from typing import Dict, List
from datetime import datetime
from config.config import GMAIL_ADDRESS, GMAIL_PASSWORD, GMAIL_SMTP_SERVER, GMAIL_SMTP_PORT, KST
from config.email_config import build_email_body
from src.logger import setup_logger

logger = setup_logger(__name__)

def send_daily_brief(articles_by_section: Dict[str, List[dict]], recipient: str = None) -> bool:
    """
    일일 브리핑 이메일 발송
    
    Args:
        articles_by_section: 번역된 기사
        recipient: 수신자 이메일
    
    Returns:
        성공 여부
    """
    try:
        if not GMAIL_ADDRESS or not GMAIL_PASSWORD:
            logger.error("Gmail 설정이 필요합니다. .env 파일을 확인하세요.")
            return False
        
        if not recipient:
            recipient = GMAIL_ADDRESS
        
        # HTML 본문 생성
        now = datetime.now(KST)
        date_str = now.strftime('%Y년 %m월 %d일')
        
        html_body = build_email_body(articles_by_section, date_str)
        
        # 이메일 생성
        message = MIMEMultipart('alternative')
        message['Subject'] = f"FT 데일리 브리핑 - {date_str}"
        message['From'] = GMAIL_ADDRESS
        message['To'] = recipient
        
        # HTML 부분 추가
        html_part = MIMEText(html_body, 'html', 'utf-8')
        message.attach(html_part)
        
        # 발송
        logger.info(f"이메일 발송 시작: {recipient}")
        with smtplib.SMTP(GMAIL_SMTP_SERVER, GMAIL_SMTP_PORT) as server:
            server.starttls()
            server.login(GMAIL_ADDRESS, GMAIL_PASSWORD)
            server.send_message(message)
        
        logger.info(f"이메일 발송 완료: {recipient}")
        return True
    
    except smtplib.SMTPAuthenticationError:
        logger.error("Gmail 인증 실패. App Password를 확인하세요.")
        return False
    except Exception as e:
        logger.error(f"이메일 발송 실패: {str(e)}", exc_info=True)
        return False
