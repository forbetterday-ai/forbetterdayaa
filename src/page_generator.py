"""
데일리 뉴스 브리핑 웹페이지 생성 모듈
"""
import os
import re
from datetime import datetime, timedelta
from config.config import KST
from src.logger import setup_logger
from src.rss_fetcher import get_feed_status

logger = setup_logger(__name__)

# 소스 그룹 매핑
SOURCE_GROUPS = {
    'FT': ['FT Markets', 'FT Companies', 'FT Technology', 'FT World', 'FT US', 'FT Opinion', 'FT Global Economy'],
    'Bloomberg': ['BBG Markets', 'BBG Technology', 'BBG Politics', 'BBG Economics', 'BBG Industries'],
    'Reuters': ['Reuters Business', 'Reuters Markets'],
    'TechCrunch': ['TechCrunch', 'TC Startups', 'TC AI', 'TC Venture'],
    'Space': ['SpaceNews', 'Space.com', 'Payload Space', 'Satellite Today'],
    'Defense': ['Breaking Defense', 'Defense News', 'Defense One', 'DefenseScoop', 'Air & Space Forces', 'Space & Defense'],
    'Ars Technica': ['Ars Technica'],
    '매경': ['MK 헤드라인', 'MK 경제', 'MK 금융', 'MK 기업', 'MK 증권', 'MK IT'],
    '한경': ['HK 경제', 'HK 산업', 'HK 금융', 'HK IT', 'HK 전체'],
    '조선': ['조선 헤드라인', '조선 정치', '조선 사회'],
}


def _extract_date_str(pub_date: str) -> str:
    """pub_date 문자열에서 날짜(YYYY년 MM월 DD일) 추출"""
    match = re.search(r'(\d{4})년\s*(\d{2})월\s*(\d{2})일', pub_date)
    if match:
        return f"{match.group(1)}년 {match.group(2)}월 {match.group(3)}일"
    return ""


def _get_source_group(section_name: str) -> str:
    """섹션 이름으로 소스 그룹 반환"""
    for group, sections in SOURCE_GROUPS.items():
        if section_name in sections:
            return group
    return "기타"


def generate_briefing_page(articles_by_section: dict):
    now = datetime.now(KST)
    date_str = now.strftime('%Y년 %m월 %d일')
    time_str = now.strftime('%H:%M')
    weekday_map = {0: '월', 1: '화', 2: '수', 3: '목', 4: '금', 5: '토', 6: '일'}
    weekday = weekday_map[now.weekday()]

    total_articles = sum(len(v) for v in articles_by_section.values())

    # 피드 상태
    status = get_feed_status()
    unavailable_feeds = [k for k, v in status.items() if v in ('unavailable', 'error')]
    status_html = ""
    if unavailable_feeds:
        feeds_list = ", ".join(unavailable_feeds)
        status_html = f'<div class="status-alert">⚠️ RSS 피드 접속 불가: {feeds_list} — 해당 소스의 RSS 서비스가 중단되었거나 접속이 차단된 상태입니다.</div>'

    # 날짜 목록 수집
    all_dates = set()
    for section, articles in articles_by_section.items():
        for article in articles:
            d = _extract_date_str(article.get('pub_date', ''))
            if d:
                all_dates.add(d)
    sorted_dates = sorted(all_dates, reverse=True)

    # 날짜 필터 버튼
    date_buttons = '<button class="filter-btn date-btn active" onclick="filterDate(\'all\')">전체</button>'
    for d in sorted_dates:
        date_buttons += f'<button class="filter-btn date-btn" onclick="filterDate(\'{d}\')">{d}</button>'

    # 소스 그룹 필터 버튼 + 기사 수 계산
    source_buttons = '<button class="filter-btn source-btn active" onclick="filterSource(\'all\')">Show All</button>'
    for group_name, section_list in SOURCE_GROUPS.items():
        count = 0
        for s in section_list:
            if s in articles_by_section:
                count += len(articles_by_section[s])
        if count > 0:
            source_buttons += f'<button class="filter-btn source-btn" onclick="filterSource(\'{group_name}\')">{group_name} <strong>{count}</strong></button>'

    # 섹션별 통계 pill
    section_stats = ""
    for section, articles in articles_by_section.items():
        section_stats += f'<span class="stat-pill">{section} <strong>{len(articles)}</strong></span>'

    # 기사 HTML 생성
    articles_html = ""
    for section, articles in articles_by_section.items():
        source_group = _get_source_group(section)
        articles_html += f'<div class="section-group" data-source="{source_group}">'
        articles_html += f'<div class="section-label">{section}</div>'

        for article in articles:
            title = article.get('title', 'N/A')
            title_ko = article.get('title_ko', '')
            link = article.get('link', '#')
            pub_date = article.get('pub_date', '')
            has_watchlist = article.get('has_watchlist', False)
            watchlist_item = article.get('watchlist_item', '')
            article_date = _extract_date_str(pub_date)

            watchlist_badge = f'<span class="watchlist-badge">★ {watchlist_item}</span>' if has_watchlist else ''

            if title_ko and title_ko != title:
                main_title = title_ko
                sub_html = f'<div class="article-original">{title}</div>'
            else:
                main_title = title
                sub_html = ''

            articles_html += f'''
            <a href="{link}" target="_blank" class="article-card {"watchlist" if has_watchlist else ""}" data-date="{article_date}" data-source="{source_group}">
                <div class="article-header">
                    <div class="article-title">{main_title}</div>
                    {watchlist_badge}
                </div>
                {sub_html}
                <div class="article-meta">
                    <span class="article-date">{pub_date}</span>
                </div>
            </a>
            '''

        articles_html += '</div>'

    html = f'''<!DOCTYPE html>
<html lang="ko">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Daily News Brief - {date_str}</title>
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link href="https://fonts.googleapis.com/css2?family=Noto+Sans+KR:wght@300;400;500;700;900&family=Playfair+Display:wght@700;900&family=JetBrains+Mono:wght@400;500&display=swap" rel="stylesheet">
    <style>
        :root {{
            --bg-primary: #0a0a0a;
            --bg-card: #141414;
            --bg-card-hover: #1a1a1a;
            --border: #222;
            --text-primary: #e8e8e8;
            --text-secondary: #888;
            --text-muted: #555;
            --accent: #c9a94e;
            --accent-dim: #6b5a2a;
            --watchlist: #d4442a;
            --watchlist-bg: rgba(212, 68, 42, 0.08);
        }}
        * {{ margin: 0; padding: 0; box-sizing: border-box; }}
        body {{
            font-family: 'Noto Sans KR', sans-serif;
            background: var(--bg-primary);
            color: var(--text-primary);
            line-height: 1.7;
            min-height: 100vh;
        }}
        .header {{
            border-bottom: 1px solid var(--border);
            padding: 2rem 0;
            background: linear-gradient(180deg, #111 0%, var(--bg-primary) 100%);
            position: sticky;
            top: 0;
            z-index: 100;
        }}
        .container {{
            max-width: 900px;
            margin: 0 auto;
            padding: 0 1.5rem;
        }}
        .header-top {{
            display: flex;
            justify-content: space-between;
            align-items: flex-start;
            margin-bottom: 1rem;
        }}
        .brand {{
            font-family: 'Playfair Display', serif;
            font-size: 2rem;
            font-weight: 900;
            color: var(--accent);
            letter-spacing: -0.02em;
        }}
        .brand-sub {{
            font-size: 0.75rem;
            font-weight: 300;
            color: var(--text-muted);
            letter-spacing: 0.15em;
            text-transform: uppercase;
            margin-top: 0.3rem;
        }}
        .date-block {{ text-align: right; }}
        .date-main {{
            font-family: 'JetBrains Mono', monospace;
            font-size: 0.85rem;
            color: var(--text-secondary);
        }}
        .date-weekday {{
            font-size: 1.8rem;
            font-weight: 900;
            color: var(--text-primary);
            line-height: 1;
        }}
        .update-time {{
            font-family: 'JetBrains Mono', monospace;
            font-size: 0.7rem;
            color: var(--text-muted);
            margin-top: 0.25rem;
        }}
        .total-count {{
            font-family: 'JetBrains Mono', monospace;
            font-size: 0.8rem;
            color: var(--accent);
            background: var(--accent-dim);
            padding: 0.25rem 0.75rem;
            border-radius: 100px;
            margin-bottom: 0.5rem;
            display: inline-block;
        }}
        .filter-row {{
            display: flex;
            gap: 0.4rem;
            flex-wrap: wrap;
            align-items: center;
            margin-bottom: 0.5rem;
        }}
        .filter-label {{
            font-family: 'JetBrains Mono', monospace;
            font-size: 0.65rem;
            color: var(--text-muted);
            text-transform: uppercase;
            letter-spacing: 0.1em;
            margin-right: 0.3rem;
            flex-shrink: 0;
        }}
        .filter-btn {{
            font-family: 'JetBrains Mono', monospace;
            font-size: 0.7rem;
            padding: 0.35rem 0.7rem;
            border: 1px solid var(--border);
            border-radius: 6px;
            background: var(--bg-card);
            color: var(--text-secondary);
            cursor: pointer;
            transition: all 0.2s ease;
        }}
        .filter-btn:hover {{
            border-color: var(--accent-dim);
            color: var(--text-primary);
        }}
        .filter-btn.active {{
            background: var(--accent-dim);
            border-color: var(--accent);
            color: var(--accent);
            font-weight: 500;
        }}
        .filter-btn strong {{
            color: var(--accent);
            margin-left: 0.2rem;
        }}
        .stats-row {{
            display: flex;
            gap: 0.4rem;
            flex-wrap: wrap;
            margin-top: 0.5rem;
        }}
        .stat-pill {{
            font-size: 0.65rem;
            color: var(--text-muted);
            background: transparent;
            border: 1px solid var(--border);
            padding: 0.2rem 0.5rem;
            border-radius: 100px;
        }}
        .stat-pill strong {{
            color: var(--text-secondary);
            margin-left: 0.15rem;
        }}
        .filter-count {{
            font-family: 'JetBrains Mono', monospace;
            font-size: 0.75rem;
            color: var(--accent);
            margin-top: 0.5rem;
        }}
        .status-alert {{
            margin-top: 0.75rem;
            padding: 0.6rem 0.8rem;
            background: rgba(212, 68, 42, 0.08);
            border: 1px solid rgba(212, 68, 42, 0.2);
            border-radius: 8px;
            font-size: 0.75rem;
            color: var(--watchlist);
            line-height: 1.4;
        }}
        .main {{ padding: 1.5rem 0 4rem; }}
        .section-group {{ margin-bottom: 2rem; }}
        .section-group.hidden {{ display: none; }}
        .section-label {{
            font-family: 'JetBrains Mono', monospace;
            font-size: 0.7rem;
            font-weight: 500;
            color: var(--accent);
            text-transform: uppercase;
            letter-spacing: 0.2em;
            padding: 0.5rem 0;
            border-bottom: 1px solid var(--border);
            margin-bottom: 0.5rem;
        }}
        .article-card {{
            display: block;
            text-decoration: none;
            color: inherit;
            padding: 0.8rem 1rem;
            margin-bottom: 0.15rem;
            border-radius: 8px;
            transition: all 0.2s ease;
            border: 1px solid transparent;
        }}
        .article-card:hover {{
            background: var(--bg-card-hover);
            border-color: var(--border);
            transform: translateX(4px);
        }}
        .article-card.watchlist {{
            background: var(--watchlist-bg);
            border-left: 3px solid var(--watchlist);
        }}
        .article-card.hidden {{ display: none; }}
        .article-header {{
            display: flex;
            justify-content: space-between;
            align-items: flex-start;
            gap: 0.75rem;
        }}
        .article-title {{
            font-size: 0.9rem;
            font-weight: 500;
            line-height: 1.5;
        }}
        .article-original {{
            font-size: 0.78rem;
            color: var(--text-muted);
            margin-top: 0.25rem;
            padding-left: 0.75rem;
            border-left: 2px solid var(--border);
            font-style: italic;
        }}
        .watchlist-badge {{
            flex-shrink: 0;
            font-size: 0.6rem;
            font-weight: 500;
            color: var(--watchlist);
            background: rgba(212, 68, 42, 0.15);
            padding: 0.15rem 0.5rem;
            border-radius: 4px;
            white-space: nowrap;
        }}
        .article-date {{
            font-family: 'JetBrains Mono', monospace;
            font-size: 0.65rem;
            color: var(--text-muted);
        }}
        .footer {{
            border-top: 1px solid var(--border);
            padding: 2rem 0;
            text-align: center;
        }}
        .footer-text {{
            font-size: 0.7rem;
            color: var(--text-muted);
        }}
        .footer-text a {{
            color: var(--accent-dim);
            text-decoration: none;
        }}
        .empty-state {{
            text-align: center;
            padding: 4rem 0;
            color: var(--text-muted);
        }}
        @media (max-width: 640px) {{
            .brand {{ font-size: 1.5rem; }}
            .date-weekday {{ font-size: 1.3rem; }}
            .header-top {{ flex-direction: column; gap: 0.75rem; }}
            .date-block {{ text-align: left; }}
            .article-header {{ flex-direction: column; gap: 0.25rem; }}
            .header {{ position: static; }}
        }}
    </style>
</head>
<body>
    <header class="header">
        <div class="container">
            <div class="header-top">
                <div>
                    <div class="brand">Daily News Brief</div>
                    <div class="brand-sub">FT · Bloomberg · Reuters · TechCrunch · Space · Defense · 매경 · 한경 · 조선</div>
                </div>
                <div class="date-block">
                    <div class="date-weekday">{weekday}요일</div>
                    <div class="date-main">{date_str}</div>
                    <div class="update-time">업데이트 {time_str} KST</div>
                </div>
            </div>
            <span class="total-count">총 {total_articles}개 기사</span>
            <div class="filter-row">
                <span class="filter-label">날짜</span>
                {date_buttons}
            </div>
            <div class="filter-row">
                <span class="filter-label">소스</span>
                {source_buttons}
            </div>
            <div class="filter-count" id="filterCount"></div>
            {status_html}
        </div>
    </header>
    <main class="main">
        <div class="container">
            {articles_html if total_articles > 0 else '<div class="empty-state">📭 수집된 기사가 없습니다.</div>'}
        </div>
    </main>
    <footer class="footer">
        <div class="container">
            <div class="footer-text">
                Daily News Brief · KST 07:00 / 12:00 / 20:00 / 21:00 자동 업데이트<br>
                Powered by FT · Bloomberg · Reuters · TechCrunch · Space · Defense · 매경 · 한경 · 조선
            </div>
        </div>
    </footer>
    <script>
        let currentDate = 'all';
        let currentSource = 'all';

        function filterDate(date) {{
            currentDate = date;
            document.querySelectorAll('.date-btn').forEach(b => b.classList.remove('active'));
            event.target.classList.add('active');
            applyFilters();
        }}

        function filterSource(source) {{
            currentSource = source;
            document.querySelectorAll('.source-btn').forEach(b => b.classList.remove('active'));
            event.target.classList.add('active');
            applyFilters();
        }}

        function applyFilters() {{
            let visibleCount = 0;

            document.querySelectorAll('.article-card').forEach(card => {{
                const matchDate = (currentDate === 'all' || card.getAttribute('data-date') === currentDate);
                const matchSource = (currentSource === 'all' || card.getAttribute('data-source') === currentSource);

                if (matchDate && matchSource) {{
                    card.classList.remove('hidden');
                    visibleCount++;
                }} else {{
                    card.classList.add('hidden');
                }}
            }});

            document.querySelectorAll('.section-group').forEach(group => {{
                const matchSource = (currentSource === 'all' || group.getAttribute('data-source') === currentSource);
                const hasVisible = group.querySelectorAll('.article-card:not(.hidden)').length > 0;

                if (matchSource && hasVisible) {{
                    group.classList.remove('hidden');
                }} else {{
                    group.classList.add('hidden');
                }}
            }});

            const countEl = document.getElementById('filterCount');
            if (currentDate === 'all' && currentSource === 'all') {{
                countEl.textContent = '';
            }} else {{
                countEl.textContent = visibleCount + '개 기사 표시 중';
            }}
        }}
    </script>
</body>
</html>'''

    docs_dir = 'docs'
    os.makedirs(docs_dir, exist_ok=True)
    output_path = os.path.join(docs_dir, 'index.html')
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(html)
    logger.info(f"브리핑 웹페이지 생성 완료: {output_path}")
    return output_path
