"""
FT.com RSS 수집 모듈 - 멀티 섹션 피드
"""
import feedparser
from datetime import datetime
from typing import Dict, List
from config.config import RSS_HOURS_LOOKBACK, KST
from src.logger import setup_logger
from src.utils import is_within_hours, format_publish_date

logger = setup_logger(__name__)

# FT 섹션별 RSS 피드
FT_SECTION_FEEDS = {
    'Markets': 'https://www.ft.com/markets?format=rss',
    'Companies': 'https://www.ft.com/companies?format=rss',
    'Technology': 'https://www.ft.com/technology?format=rss',
    'World': 'https://www.ft.com/world?format=rss',
    'US': 'https://www.ft.com/world/us?format=rss',
}


def fetch_ft_rss() -> Dict[str, List[dict]]:
    """
    FT RSS 피드 수집 - 복수 섹션 피드에서 수집 및 중복 제거

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
    articles_by_section = {}
    seen_links = set()  # 중복 제거용

    for section_name, feed_url in FT_SECTION_FEEDS.items():
        try:
            logger.info(f"FT RSS 수집: {section_name} ({feed_url})")
            feed = feedparser.parse(feed_url)

            if feed.bozo:
                logger.warning(f"RSS 파싱 경고 ({section_name}): {feed.bozo_exception}")

            section_articles = []

            for entry in feed.entries:
                # 중복 제거
                link = entry.get('link', '')
                if link in seen_links:
                    continue
                seen_links.add(link)

                # 발행 시간 확인 (24시간 이내)
                pub_date = entry.get('published', entry.get('updated', ''))
                if not is_within_hours(pub_date, RSS_HOURS_LOOKBACK):
                    continue

                # 기사 데이터 구성
                article = {
                    'title': entry.get('title', 'N/A'),
                    'link': link,
                    'pub_date': format_publish_date(pub_date),
                    'summary': entry.get('summary', '')[:300],
                    'section': section_name,
                }
                section_articles.append(article)

            if section_articles:
                articles_by_section[section_name] = section_articles
                logger.info(f"  → {section_name}: {len(section_articles)}개 기사")

        except Exception as e:
            logger.error(f"RSS 수집 실패 ({section_name}): {str(e)}", exc_info=True)

    total = sum(len(v) for v in articles_by_section.values())
    logger.info(f"수집 완료: 총 {total}개 기사 ({len(articles_by_section)}개 섹션)")
    return articles_by_section


def get_articles_summary(articles_by_section: Dict[str, List[dict]]) -> str:
    """기사 수집 요약"""
    total_articles = sum(len(v) for v in articles_by_section.values())
    summary = f"총 {total_articles}개 기사 수집\n\n"

    for section, articles in articles_by_section.items():
        summary += f"- {section}: {len(articles)}개\n"

    return summary
