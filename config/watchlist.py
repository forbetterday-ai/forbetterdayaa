"""
claude.md에서 추출한 코어 워치리스트
"""

WATCHLIST = {
    # 미국/글로벌
    'Palantir': ['PLTR', 'Palantir', 'palantir'],
    'Rocket Lab': ['RKLB', 'Rocket Lab', 'rocket lab'],
    'Bloom Energy': ['BE', 'Bloom Energy', 'bloom energy'],
    'Planet Labs': ['PL', 'Planet Labs', 'planet labs'],
    'Cheniere Energy': ['LNG', 'Cheniere', 'cheniere'],
    'Anduril': ['Anduril', 'anduril'],
    'SpaceX': ['SpaceX', 'spacex', 'Starshield'],
    'Robinhood': ['HOOD', 'Robinhood', 'robinhood'],
    'Tesla': ['TSLA', 'Tesla', 'tesla', 'Elon Musk'],
    'Google': ['GOOGL', 'GOOG', 'Google', 'Alphabet'],
    
    # 한국
    'SK Hynix': ['SK Hynix', 'SK하이닉스', 'SKH', '하이닉스', 'Hynix', 'HBM'],
    'Samsung Electronics': ['Samsung', '삼성전자', 'SSNLF', 'Samsung Foundry'],
    'Hanwha Aerospace': ['Hanwha Aerospace', '한화에어로스페이스', 'HanwhaAerotech'],
    'LIG Nex1': ['LIG Nex1', 'LIG Nex1', '천궁'],
    
    # 테마 키워드
    'HBM': ['HBM', 'HBM4', 'HBM3E', 'AI 메모리'],
    'AI Inference': ['AI inference', 'inference', 'LLM', 'NVIDIA'],
    'Space': ['space', 'satellite', 'SpaceX'],
    'Defense': ['defense', 'military', '방위사업', '방산'],
    'Energy': ['energy', 'LNG', 'power'],
}

def is_watchlist_item(text: str) -> tuple:
    """
    텍스트에서 워치리스트 종목 감지
    
    Returns:
        (감지_여부, 종목명)
    """
    if not text:
        return False, ""
    
    text_lower = text.lower()
    
    for item_name, keywords in WATCHLIST.items():
        for keyword in keywords:
            if keyword.lower() in text_lower:
                return True, item_name
    
    return False, ""
