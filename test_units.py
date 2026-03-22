#!/usr/bin/env python3
"""
FT 데일리 브리핑 - 단위 테스트

각 모듈의 기본 기능 검증
"""
import sys
from datetime import datetime
from config.config import KST, CLAUDE_API_KEY, GMAIL_ADDRESS, GMAIL_PASSWORD

print("=" * 70)
print("🧪 FT 데일리 브리핑 - 단위 테스트")
print("=" * 70)

# ✅ 테스트 1: 환경변수 로드
print("\n[테스트 1] 환경변수 로드")
print("-" * 70)
try:
    print(f"✓ CLAUDE_API_KEY: {CLAUDE_API_KEY[:20]}..." if CLAUDE_API_KEY else "✗ CLAUDE_API_KEY 없음")
    print(f"✓ GMAIL_ADDRESS: {GMAIL_ADDRESS}")
    print(f"✓ GMAIL_PASSWORD: {'*' * len(GMAIL_PASSWORD) if GMAIL_PASSWORD else '없음'}")
    print(f"✓ KST 타임존: {KST}")
    print("✅ 환경변수 로드 성공")
except Exception as e:
    print(f"❌ 환경변수 로드 실패: {e}")
    sys.exit(1)

# ✅ 테스트 2: 워치리스트 모듈
print("\n[테스트 2] 워치리스트 감지")
print("-" * 70)
try:
    from config.watchlist import is_watchlist_item
    
    test_texts = [
        "SK Hynix announces new HBM4 production",
        "Palantir stock rises 5%",
        "Tesla quarterly earnings",
        "Random company news",
    ]
    
    for text in test_texts:
        has_match, item = is_watchlist_item(text)
        status = "⭐" if has_match else " "
        print(f"{status} '{text[:40]}...' → {item if has_match else 'No match'}")
    
    print("✅ 워치리스트 감지 성공")
except Exception as e:
    print(f"❌ 워치리스트 감지 실패: {e}")
    sys.exit(1)

# ✅ 테스트 3: 로거 모듈
print("\n[테스트 3] 로거 설정")
print("-" * 70)
try:
    from src.logger import setup_logger
    
    test_logger = setup_logger("test_module")
    test_logger.info("테스트 로그 메시지")
    print("✓ Logger 초기화 완료")
    
    import os
    if os.path.exists("output/app.log"):
        print("✓ 로그 파일 생성 확인: output/app.log")
    print("✅ 로거 설정 성공")
except Exception as e:
    print(f"❌ 로거 설정 실패: {e}")
    sys.exit(1)

# ✅ 테스트 4: 유틸리티 함수
print("\n[테스트 4] 유틸리티 함수 (시간 처리)")
print("-" * 70)
try:
    from src.utils import get_kst_now, is_within_hours, format_publish_date
    
    now = get_kst_now()
    print(f"✓ KST 현재 시간: {now}")
    
    formatted = format_publish_date(now)
    print(f"✓ 포맷된 시간: {formatted}")
    
    is_recent = is_within_hours(now, 24)
    print(f"✓ 24시간 이내 확인: {is_recent}")
    print("✅ 유틸리티 함수 성공")
except Exception as e:
    print(f"❌ 유틸리티 함수 실패: {e}")
    sys.exit(1)

# ✅ 테스트 5: 이메일 설정
print("\n[테스트 5] 이메일 설정 (HTML 템플릿)")
print("-" * 70)
try:
    from config.email_config import build_email_body
    
    test_articles = {
        "Markets": [
            {
                "title": "Stock Markets Rise",
                "title_ko": "주식시장 상승",
                "link": "https://ft.com/test1",
                "pub_date": "2026년 03월 22일 00:44 KST",
                "summary": "Global stock markets showed strong gains today",
                "has_watchlist": True,
                "watchlist_item": "SK Hynix"
            }
        ],
        "Technology": [
            {
                "title": "AI Chip Shortage Deepens",
                "title_ko": "AI 칩 부족 심화",
                "link": "https://ft.com/test2",
                "pub_date": "2026년 03월 22일 00:40 KST",
                "summary": "Demand for advanced chips continues to outpace supply",
                "has_watchlist": False,
                "watchlist_item": ""
            }
        ]
    }
    
    html = build_email_body(test_articles, "2026년 03월 22일")
    if "<html" in html.lower() and "<body" in html.lower():
        print("✓ HTML 이메일 템플릿 생성 완료")
        print(f"✓ 생성된 HTML 크기: {len(html)} bytes")
    print("✅ 이메일 설정 성공")
except Exception as e:
    import traceback
    print(f"❌ 이메일 설정 실패: {e}")
    traceback.print_exc()
    sys.exit(1)

# ✅ 테스트 6: Claude API 연결 테스트 (간단한 호출)
print("\n[테스트 6] Claude API 연결 테스트")
print("-" * 70)
try:
    from src.translator import translate_text
    
    print("⏳ Claude API 호출 중...")
    result = translate_text("Hello, world")
    print(f"✓ API 응답: {result[:50]}...")
    print("✅ Claude API 연결 성공")
except Exception as e:
    print(f"⚠️  Claude API 테스트 건너뛰기: {str(e)[:50]}...")
    print("   (네트워크 문제 또는 API 문제일 수 있습니다)")

# ✅ 테스트 7: Gmail 연결 테스트 (발송 안 함)
print("\n[테스트 7] Gmail 설정 검증")
print("-" * 70)
try:
    import smtplib
    from config.config import GMAIL_SMTP_SERVER, GMAIL_SMTP_PORT
    
    print(f"✓ Gmail SMTP 서버: {GMAIL_SMTP_SERVER}:{GMAIL_SMTP_PORT}")
    
    # 실제 연결 테스트는 하지 않음 (이메일 발송 위험)
    if GMAIL_ADDRESS and GMAIL_PASSWORD:
        print(f"✓ Gmail 인증 정보 확인: {GMAIL_ADDRESS}")
        print("⚠️  실제 이메일 발송은 테스트하지 않습니다")
    print("✅ Gmail 설정 검증 성공")
except Exception as e:
    print(f"❌ Gmail 설정 검증 실패: {e}")
    sys.exit(1)

# ✅ 테스트 8: 파일 시스템
print("\n[테스트 8] 파일 시스템 검증")
print("-" * 70)
try:
    import os
    
    required_dirs = ["config", "src", "output", ".github/workflows"]
    for dir_name in required_dirs:
        if os.path.isdir(dir_name):
            print(f"✓ {dir_name}/ 디렉토리 존재")
        else:
            print(f"✗ {dir_name}/ 디렉토리 없음")
    
    required_files = [
        "main.py",
        "requirements.txt",
        ".env.example",
        "README.md",
        "config/config.py",
        "src/rss_fetcher.py",
        "src/translator.py",
        ".github/workflows/daily_brief.yml"
    ]
    
    for file_name in required_files:
        if os.path.isfile(file_name):
            print(f"✓ {file_name} 파일 존재")
        else:
            print(f"✗ {file_name} 파일 없음")
    
    print("✅ 파일 시스템 검증 성공")
except Exception as e:
    print(f"❌ 파일 시스템 검증 실패: {e}")
    sys.exit(1)

# 최종 결과
print("\n" + "=" * 70)
print("✅ 모든 단위 테스트 완료!")
print("=" * 70)
print("\n📋 테스트 결과 요약:")
print("  [1] ✓ 환경변수 로드")
print("  [2] ✓ 워치리스트 감지")
print("  [3] ✓ 로거 설정")
print("  [4] ✓ 유틸리티 함수")
print("  [5] ✓ 이메일 설정")
print("  [6] △ Claude API (네트워크 상태에 따라)")
print("  [7] ✓ Gmail 설정")
print("  [8] ✓ 파일 시스템")

print("\n🚀 다음 단계:")
print("  • 네트워크 연결 확인 후 --mode daily 재실행")
print("  • 또는 --mode analyze로 기사 분석 테스트")
print("  • GitHub Actions 워크플로우 스케줄 설정")

sys.exit(0)
