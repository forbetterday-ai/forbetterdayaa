"""
Gmail SMTP 설정 및 이메일 템플릿
"""

HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="ko">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>FT 데일리 브리핑</title>
    <style>
        body {
            font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Helvetica Neue", Arial, sans-serif;
            line-height: 1.6;
            color: #333;
            background-color: #f5f5f5;
            margin: 0;
            padding: 20px;
        }
        .container {
            max-width: 900px;
            margin: 0 auto;
            background-color: white;
            border-radius: 8px;
            padding: 30px;
            box-shadow: 0 2px 8px rgba(0,0,0,0.1);
        }
        .header {
            border-bottom: 3px solid #0066cc;
            margin-bottom: 30px;
            padding-bottom: 20px;
        }
        .header h1 {
            margin: 0;
            color: #0066cc;
            font-size: 28px;
        }
        .header p {
            margin: 5px 0 0 0;
            color: #666;
            font-size: 14px;
        }
        .section {
            margin-bottom: 40px;
        }
        .section-title {
            font-size: 18px;
            font-weight: bold;
            color: white;
            background-color: #0066cc;
            padding: 12px 16px;
            border-radius: 4px;
            margin-bottom: 16px;
        }
        .article {
            border-left: 4px solid #0066cc;
            padding-left: 16px;
            margin-bottom: 20px;
            padding-bottom: 16px;
            border-bottom: 1px solid #eee;
        }
        .article:last-child {
            border-bottom: none;
            margin-bottom: 0;
            padding-bottom: 0;
        }
        .article-title {
            font-size: 16px;
            font-weight: bold;
            margin: 0 0 8px 0;
        }
        .article-title a {
            color: #0066cc;
            text-decoration: none;
        }
        .article-title a:hover {
            text-decoration: underline;
        }
        .article-meta {
            font-size: 12px;
            color: #999;
            margin-bottom: 8px;
        }
        .article-summary {
            font-size: 14px;
            color: #555;
            line-height: 1.6;
        }
        .watchlist-flag {
            display: inline-block;
            background-color: #ffcc00;
            color: #333;
            padding: 4px 8px;
            border-radius: 3px;
            font-size: 12px;
            font-weight: bold;
            margin-left: 8px;
        }
        .footer {
            border-top: 1px solid #eee;
            margin-top: 30px;
            padding-top: 20px;
            text-align: center;
            color: #999;
            font-size: 12px;
        }
        .footer a {
            color: #0066cc;
            text-decoration: none;
        }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>📰 FT 데일리 브리핑</h1>
            <p>{date_str}</p>
        </div>
        
        {sections_html}
        
        <div class="footer">
            <p>FT.com 최신 헤드라인을 매일 08:00 KST에 자동 수집합니다.</p>
            <p><a href="https://ft.com">Financial Times</a></p>
        </div>
    </div>
</body>
</html>
"""

def build_email_body(articles_by_section: dict, date_str: str) -> str:
    """
    섹션별 기사를 HTML 이메일로 조립
    
    Args:
        articles_by_section: {섹션명: [{title, title_ko, link, summary, pub_date, has_watchlist}]}
        date_str: 발송 날짜 문자열
    
    Returns:
        HTML 이메일 본문
    """
    sections_html = ""
    
    for section, articles in articles_by_section.items():
        if not articles:
            continue
        
        articles_html = ""
        for article in articles:
            watchlist_badge = ""
            if article.get('has_watchlist'):
                watchlist_badge = f'<span class="watchlist-flag">⭐ {article.get("watchlist_item", "모니터링")}</span>'
            
            articles_html += f"""
            <div class="article">
                <div class="article-title">
                    <a href="{article['link']}">{article.get('title_ko', article['title'])}</a>
                    {watchlist_badge}
                </div>
                <div class="article-meta">{article.get('pub_date', '')}</div>
                <div class="article-summary">{article.get('summary', '')}</div>
                <div style="font-size: 12px; color: #0066cc; margin-top: 8px;">
                    <a href="{article['link']}">원문 보기 →</a>
                </div>
            </div>
            """
        
        sections_html += f"""
        <div class="section">
            <div class="section-title">{section}</div>
            {articles_html}
        </div>
        """
    
    # .format() 대신 .replace() 사용 (CSS 스타일과의 충돌 방지)
    result = HTML_TEMPLATE.replace("{date_str}", date_str)
    result = result.replace("{sections_html}", sections_html)
    return result
