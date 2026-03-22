"""
FT 기사 4섹션 분석 양식
"""
import os
from typing import Optional
import json
from datetime import datetime
from config.config import KST, OUTPUT_DIR, CLAUDE_API_KEY
from src.logger import setup_logger
from src.translator import translate_for_analysis
from src.article_scraper import scrape_article
from anthropic import Anthropic

logger = setup_logger(__name__)

# 환경변수에 API 키 설정 (Anthropic이 자동으로 읽도록)
if CLAUDE_API_KEY:
    os.environ['ANTHROPIC_API_KEY'] = CLAUDE_API_KEY

def _get_client():
    """Anthropic 클라이언트 지연 초기화"""
    return Anthropic()

def analyze_article(url: str, title: str, summary: str) -> Optional[str]:
    """
    기사를 claude.md 4섹션 분석 양식으로 분석
    
    Args:
        url: 기사 URL
        title: 기사 제목 (원문)
        summary: 기사 요약
    
    Returns:
        마크다운 형식 분석 리포트 (또는 None)
    """
    try:
        logger.info(f"기사 분석 시작: {title[:50]}")
        
        # 원문 스크래핑
        article_text, has_paywall = scrape_article(url)
        if not article_text:
            article_text = summary
            logger.warning(f"원문 스크래핑 실패, 요약 사용")
        
        # Section 1: 제목번역 + 핵심내용
        section1 = _generate_section1(title, article_text)
        
        # Section 2: 행간읽기
        section2 = _generate_section2(article_text)
        
        # Section 3: 장기투자 인사이트
        section3 = _generate_section3(article_text)
        
        # Section 4: X 게시글
        section4 = _generate_section4(section1, section3)
        
        # 부록 1: 메타인지 A/B 테스트
        appendix1 = _generate_appendix1(section3)
        
        # 부록 2: 베이즈 확률 트래커
        appendix2 = _generate_appendix2(section3)
        
        # 최종 리포트 조립
        report = f"""# {title}

[원문 링크]({url})

---

## 📰 섹션 1: 제목번역 + 핵심내용 상세 재구성

{section1}

---

## 🔍 섹션 2: 행간읽기

{section2}

---

## 💡 섹션 3: 장기투자 인사이트

{section3}

---

## 𝕏 섹션 4: X 게시글

{section4}

---

## 📊 부록 1: 메타인지 A/B 테스트

{appendix1}

---

## 📈 부록 2: 베이즈 확률 트래커

{appendix2}

---

**분석 일시**: {datetime.now(KST).strftime('%Y년 %m월 %d일 %H:%M:%S KST')}
"""
        
        # 리포트 저장
        timestamp = datetime.now(KST).strftime('%Y%m%d_%H%M%S')
        filename = f"{OUTPUT_DIR}/analysis_{timestamp}.md"
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(report)
        
        logger.info(f"분석 완료: {filename}")
        return report
    
    except Exception as e:
        logger.error(f"분석 실패: {str(e)}", exc_info=True)
        return None

def _generate_section1(title: str, article_text: str) -> str:
    """섹션 1: 제목번역 + 핵심내용"""
    try:
        message = _get_client().messages.create(
            model="claude-3-5-sonnet-20241022",
            max_tokens=2000,
            messages=[
                {
                    "role": "user",
                    "content": f"""다음 FT 뉴스 기사에 대해 [섹션 1] 분석을 작성하세요.

**FT 기사 제목**
{title}

**기사 본문**
{article_text}

**섹션 1 작성 가이드:**
1. 원문 제목의 한글 번역 (명확하고 자연스러운 번역)
2. 핵심 내용을 논리적 흐름으로 재구성 (단순 요약 아님)
3. 객관적 사실 기반 상세 서술
4. 전문 용어는 [한글 풀이] (영문원어) 괄호 병기
5. 핵심 수치, 인용문은 원문 그대로 인용
6. 투자 관련 팩트(밸류에이션, 정책, 수급, 경쟁구도, 타임라인)는 본문 흐름 안에 자연스럽게 삽입

제목의 한글 번역만 **제목 (한글)** 형식으로 먼저 제시하고, 그 다음 핵심내용 상세 재구성을 작성하세요."""
                }
            ]
        )
        return message.content[0].text.strip()
    except Exception as e:
        logger.error(f"섹션1 생성 실패: {str(e)}")
        return "분석 실패"

def _generate_section2(article_text: str) -> str:
    """섹션 2: 행간읽기"""
    try:
        message = _get_client().messages.create(
            model="claude-3-5-sonnet-20241022",
            max_tokens=1500,
            messages=[
                {
                    "role": "user",
                    "content": f"""다음 FT 뉴스 기사에 대해 [섹션 2] 행간읽기 분석을 작성하세요.

**기사 본문**
{article_text[:3000]}

**섹션 2 작성 가이드:**
1. 기사가 명시적으로 말하지 않았지만 암시하는 내용 도출
2. 반드시 기사 본문의 구체적 근거를 인용하여 추론 전개
3. 근거 없는 추측 금지
4. 시장 환경, 산업 구조, 경쟁 역학 관점의 함의 발굴

구체적 근거와 함께 명시적으로 도출하세요."""
                }
            ]
        )
        return message.content[0].text.strip()
    except Exception as e:
        logger.error(f"섹션2 생성 실패: {str(e)}")
        return "분석 실패"

def _generate_section3(article_text: str) -> str:
    """섹션 3: 장기투자 인사이트"""
    try:
        message = _get_client().messages.create(
            model="claude-3-5-sonnet-20241022",
            max_tokens=2000,
            messages=[
                {
                    "role": "user",
                    "content": f"""다음 FT 뉴스 기사에 대해 [섹션 3] 장기투자 인사이트 분석을 작성하세요.

**기사 본문**
{article_text[:3000]}

**섹션 3 작성 가이드:**
1. 메인 시나리오 1개 + 대안 시나리오 1~2개 제시
2. 각 시나리오에 확률 부여 (메인 시나리오는 필수)
3. 외부 소스 링크 포함 (뉴스, 리서치, 공식 자료 등)
4. 확률 >55:45 → 한쪽 방향 결론 명시
5. 확률 45:55~55:45 → 양쪽 병렬 결론

# 메인 시나리오
[시나리오명]: [확률]% - [설명]

# 대안 시나리오
[시나리오명]: [확률]% - [설명]

# 외부 소스
- [링크 제목](URL)

형식으로 작성하세요."""
                }
            ]
        )
        return message.content[0].text.strip()
    except Exception as e:
        logger.error(f"섹션3 생성 실패: {str(e)}")
        return "분석 실패"

def _generate_section4(section1: str, section3: str) -> str:
    """섹션 4: X 게시글 (500자 한글)"""
    try:
        message = _get_client().messages.create(
            model="claude-3-5-sonnet-20241022",
            max_tokens=800,
            messages=[
                {
                    "role": "user",
                    "content": f"""다음 분석에 기반하여 X(구 Twitter) 게시글을 작성하세요.

**섹션 1 (핵심내용)**
{section1[:500]}

**섹션 3 (투자인사이트)**
{section3[:500]}

**X 게시글 작성 가이드:**
1. 약 500자 한글 (줄글/prose paragraph 형식)
2. 전문가 분석 톤
3. 이모지는 문단 서두에만 사용 (최대 2-3개)
4. 구조적 함의와 패러다임 전환 중심 (직접적 종목 나열 지양)
5. 해시태그 2~3개
6. 실제 X에 게재 가능한 가독성

**작성 예시 구조:**
[이모지] 유도 문장...

본론 (3-4문장):
- 배경 팩트
- 구조적 함의
- 시장 영향

해시태그: #해시1 #해시2

500자 이상 600자 이하로 작성하세요."""
                }
            ]
        )
        return message.content[0].text.strip()
    except Exception as e:
        logger.error(f"섹션4 생성 실패: {str(e)}")
        return "분석 실패"

def _generate_appendix1(section3: str) -> str:
    """부록 1: 메타인지 A/B 테스트"""
    try:
        message = _get_client().messages.create(
            model="claude-3-5-sonnet-20241022",
            max_tokens=800,
            messages=[
                {
                    "role": "user",
                    "content": f"""섹션 3의 다음 분석에 기반하여 [부록 1] 메타인지 A/B 테스트를 작성하세요.

**섹션 3**
{section3}

**메타인지 A/B 테스트 가이드:**
1. 결론 분기형 또는 프레이밍 분기형 선택 (유동적)
2. 각 옵션에 확률 % 표시
3. 섹션 3의 방향성 확률과 일관성 유지

**형식 예시:**
# 결론 분기형
**Option A**: [결론A] ([확률]%)
이유: [근거]

**Option B**: [결론B] ([확률]%)
이유: [근거]

또는 프레이밍 분기형으로 구성하세요."""
                }
            ]
        )
        return message.content[0].text.strip()
    except Exception as e:
        logger.error(f"부록1 생성 실패: {str(e)}")
        return "생성 실패"

def _generate_appendix2(section3: str) -> str:
    """부록 2: 베이즈 확률 트래커"""
    try:
        message = _get_client().messages.create(
            model="claude-3-5-sonnet-20241022",
            max_tokens=600,
            messages=[
                {
                    "role": "user",
                    "content": f"""섹션 3의 다음 분석에 기반하여 [부록 2] 베이즈 확률 트래커를 작성하세요.

**섹션 3**
{section3}

**베이즈 확률 트래커 형식:**
- 형식: `종목/테마명: 현재확률% (↑/↓/→) [변동사유 한줄]`
- ↑/↓ = ±1%p (일반 시그널)
- ↑↑/↓↓ = ±2%p (산업구조 수준 시그널만)
- → = 변동 없음

섹션 3에서 언급된 종목이나 테마의 확률을 추출하여 트래커 형식으로 작성하세요."""
                }
            ]
        )
        return message.content[0].text.strip()
    except Exception as e:
        logger.error(f"부록2 생성 실패: {str(e)}")
        return "생성 실패"
