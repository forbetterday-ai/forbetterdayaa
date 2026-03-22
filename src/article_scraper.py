"""
FT.com 기사 원문 스크래핑
"""
import requests
from bs4 import BeautifulSoup
from typing import Tuple, Optional
from src.logger import setup_logger

logger = setup_logger(__name__)

HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36'
}

def scrape_article(url: str) -> Tuple[Optional[str], bool]:
    """
    FT.com 기사 원문 스크래핑
    
    Args:
        url: 기사 URL
    
    Returns:
        (원문_텍스트, 페이월_접근권)
    """
    try:
        logger.info(f"기사 스크래핑 시작: {url}")
        
        response = requests.get(url, headers=HEADERS, timeout=10)
        response.encoding = 'utf-8'
        
        if response.status_code != 200:
            logger.warning(f"HTTP {response.status_code}: {url}")
            return None, False
        
        soup = BeautifulSoup(response.content, 'html.parser')
        
        # 페이월 감지
        paywall_markers = [
            'paywall',
            'registration-prompt',
            'gate',
            'Subscribe to read',
        ]
        page_text = soup.get_text().lower()
        has_paywall = any(marker.lower() in page_text for marker in paywall_markers)
        
        # 기사 본문 추출
        article_text = ""
        
        # 시도 1: article 태그
        article = soup.find('article')
        if article:
            article_text = article.get_text(separator='\n', strip=True)
        
        # 시도 2: main 태그
        if not article_text:
            main = soup.find('main')
            if main:
                article_text = main.get_text(separator='\n', strip=True)
        
        # 시도 3: div.article-body
        if not article_text:
            div = soup.find('div', class_=lambda x: x and 'article' in x.lower())
            if div:
                article_text = div.get_text(separator='\n', strip=True)
        
        if article_text:
            logger.info(f"스크래핑 완료: {len(article_text)}자 (페이월: {has_paywall})")
            return article_text[:5000], has_paywall  # 5000자 제한
        else:
            logger.warning(f"기사 본문을 찾을 수 없음: {url}")
            return None, has_paywall
    
    except requests.Timeout:
        logger.error(f"타임아웃: {url}")
        return None, False
    except Exception as e:
        logger.error(f"스크래핑 실패: {str(e)}", exc_info=True)
        return None, False
