import logging
import os
from config.config import LOG_LEVEL, LOG_FORMAT, OUTPUT_DIR

# output 디렉토리 생성
os.makedirs(OUTPUT_DIR, exist_ok=True)

def setup_logger(name: str) -> logging.Logger:
    """로깅 설정"""
    logger = logging.getLogger(name)
    logger.setLevel(LOG_LEVEL)
    
    # 파일 핸들러
    file_handler = logging.FileHandler(f'{OUTPUT_DIR}/app.log')
    file_handler.setLevel(LOG_LEVEL)
    file_handler.setFormatter(logging.Formatter(LOG_FORMAT))
    
    # 콘솔 핸들러
    console_handler = logging.StreamHandler()
    console_handler.setLevel(LOG_LEVEL)
    console_handler.setFormatter(logging.Formatter(LOG_FORMAT))
    
    if not logger.handlers:
        logger.addHandler(file_handler)
        logger.addHandler(console_handler)
    
    return logger

logger = setup_logger(__name__)
