"""
FT.com RSS 수집 모듈
"""
import feedparser
from datetime import datetime
from typing import Dict, List
from config.config import FT_RSS_URL, RSS_HOURS_LOOKBACK, KST
from src.logger import setup_logger
from src.utils import is_within_hours, format_publish_date

logger = setup_logger(__name__)

SECTION_MAPPING = {
    'markets': 'Markets',
    'companies': 'Companies',
    'technology': 'Technology',
    'world': 'World',
    'opinion': 'Opinion',
    'home': 'Home',
}

def fetch_ft_rss() -> Dict[str, List[dict]]:
    """
    FT RSS 피드 수집 및 섹션별 그룹핑
    
    Returns:
        {
            '섹션명': [
                {
                    'title': '원제목',
                    'link': 'URL',
                    'pub_date': '발행일',
                    'summary': '요약',
                    'section': '섹션'
                }
            ]
        }
    """
    try:
        logger.info(f"FT RSS 수집 시작: {FT_RSS_URL}")
        feed = feedparser.parse(FT_RSS_URL)
        
        if feed.bozo:
            logger.warning(f"RSS 파싱 경고: {feed.bozo_exception}")
        
        articles_by_section = {}
        
        for entry in feed.entries:
            # 발행 시간 확인 (24시간 이내)
            pub_date = entry.get('published', entry.get('updated', ''))
            if not is_within_hours(pub_date, RSS_HOURS_LOOKBACK):
                logger.debug(f"시간 범위 외 기사 제외: {entry.get('title', 'N/A')}")
                continue
            
            # 섹션 추출
            section = 'Home'
            if 'tags' in entry:
                for tag in entry.tags:
                    tag_term = tag.get('term', '').lower()
                    if tag_term in SECTION_MAPPING:
                        section = SECTION_MAPPING[tag_term]
                        break
            
            # 기사 데이터 구성
            article = {
                'title': entry.get('title', 'N/A'),
                'link': entry.get('link', ''),
                'pub_date': format_publish_date(pub_date),
                'summary': entry.get('summary', '')[:300],  # 300자 제한
                'section': section,
            }
            
            # 섹션별 그룹핑
            if section not in articles_by_section:
                articles_by_section[section] = []
            articles_by_section[section].append(article)
        
        logger.info(f"수집 완료: {sum(len(v) for v in articles_by_section.values())}개 기사")
        return articles_by_section
    
    except Exception as e:
        logger.error(f"RSS 수집 실패: {str(e)}", exc_info=True)
        return {}

def get_articles_summary(articles_by_section: Dict[str, List[dict]]) -> str:
    """기사 수집 요약"""
    total_articles = sum(len(v) for v in articles_by_section.values())
    summary = f"총 {total_articles}개 기사 수집\n\n"
    
    for section, articles in articles_by_section.items():
        summary += f"- {section}: {len(articles)}개\n"
    
    return summary
