# FT 데일리 브리핑 자동화

매일 한국시간 08:00에 Financial Times(FT.com)의 최신 뉴스를 자동으로 수집하여 한글 번역 후 Gmail로 발송하고, 사용자가 선택한 기사에 대해 전문 투자 분석 리포트를 자동 생성하는 Python 기반 자동화 시스템입니다.

## 🎯 주요 기능

### 1. 일일 자동 수집 및 발송 (`--mode daily`)
- **RSS 수집**: FT.com 홈페이지 RSS 피드에서 최근 24시간 기사 수집
- **섹션별 그룹핑**: Markets, Companies, Technology, World, Opinion 등으로 자동 분류
- **한글 번역**: Claude API를 사용하여 기사 제목 자동 번역
- **워치리스트 감지**: SK Hynix, 삼성전자, Palantir, RKLB 등 코어 워치리스트 종목 자동 감지 (⭐ 플래그)
- **HTML 이메일 발송**: 섹션별로 정리된 아름다운 HTML 이메일 발송

### 2. 기사 상세분석 (`--mode analyze`)
선택한 기사에 대해 아래 **4섹션 분석 양식**을 자동으로 적용하여 마크다운 리포트 생성:

**섹션 1: 제목번역 + 핵심내용 상세 재구성**
- 원문 제목 한글 번역
- 핵심 내용을 논리적 흐름으로 재구성
- 전문 용어 표기 및 핵심 수치 인용

**섹션 2: 행간읽기**
- 기사가 명시적으로 말하지 않은 함의 도출
- 근거 기반 추론 (추측 금지)

**섹션 3: 장기투자 인사이트**
- 메인 시나리오 + 대안 시나리오 (확률 할당)
- 외부 소스 링크 (뉴스, 리서치, IR 자료)

**섹션 4: X 게시글**
- 약 500자 한글 전문가 분석
- 구조적 함의 중심

**부록**
- 메타인지 A/B 테스트 (결론/프레이밍 분기)
- 베이즈 확률 트래커 (종목별 확률 변화)

## 🚀 설치 및 설정

### 환경 요구사항
- Python 3.11+
- pip

### 1단계: 저장소 클론
```bash
git clone https://github.com/your-repo/forbetterday.git
cd forbetterday
```

### 2단계: 의존성 설치
```bash
pip install -r requirements.txt
```

### 3단계: 환경 변수 설정
`.env.example`을 복사하여 `.env` 파일을 생성하고, 다음 정보를 입력하세요:

```bash
cp .env.example .env
```

#### Claude API Key 설정
1. [Anthropic 콘솔](https://console.anthropic.com)에 접속
2. API Key 생성 및 복사
3. `.env` 파일에 추가:
   ```
   CLAUDE_API_KEY=sk-ant-v1-xxxxxx...
   ```

#### Gmail 설정 (App Password)
1. Google 계정의 [보안 설정](https://myaccount.google.com/security)으로 이동
2. **두 단계 인증** 활성화 (필수)
3. [앱 비밀번호](https://myaccount.google.com/apppasswords) 생성
   - 앱: Mail
   - 기기: Windows PC (또는 기타)
   - 생성된 16자리 비밀번호 복사
4. `.env` 파일에 입력:
   ```
   GMAIL_ADDRESS=your_email@gmail.com
   GMAIL_PASSWORD=xxxx xxxx xxxx xxxx
   ```

#### 옵션: 분석 리포트 수신자 (다른 이메일로 발송)
```
ANALYSIS_RECIPIENT_EMAIL=recipient@example.com
```

### 4단계: .env 파일 확인
```bash
cat .env
```

예시:
```env
CLAUDE_API_KEY=sk-ant-v1-xxxxx
GMAIL_ADDRESS=myemail@gmail.com
GMAIL_PASSWORD=xxxx xxxx xxxx xxxx
FT_RSS_URL=https://feeds.ft.com/home/page/rss
LOG_LEVEL=INFO
```

## 📖 사용 방법

### 일일 브리핑 실행 (수동)
```bash
python main.py --mode daily
```

**결과:**
- `output/app.log`: 실행 로그
- 지정된 Gmail 주소로 HTML 이메일 발송

### 기사 상세분석 (대화형)
```bash
python main.py --mode analyze
```

**프롬프트:**
```
📰 분석할 기사 URL을 입력하세요:
URL: https://www.ft.com/content/xxxxx

📝 기사 제목을 입력하세요 (선택):
제목 (또는 Enter): AI 칩 수급 위기 심화
```

**결과:**
- `output/analysis_20240322_143022.md`: 마크다운 형식 분석 리포트

### 기사 URL 직접 지정
```bash
python main.py --mode analyze --url "https://www.ft.com/content/xxxxx"
```

## ⏰ 자동 스케줄링 (GitHub Actions)

### GitHub Secrets 설정
1. 저장소의 **Settings** → **Secrets and variables** → **Actions**로 이동
2. 다음 secrets 생성:
   - `CLAUDE_API_KEY`: Claude API 키
   - `GMAIL_ADDRESS`: Gmail 주소
   - `GMAIL_PASSWORD`: Gmail App Password

### 자동 실행
- **기본 스케줄**: 매일 KST 08:00 자동 실행
- **수동 트리거**: GitHub Actions에서 **Run workflow** 클릭

### 실행 현황 확인
1. 저장소의 **Actions** 탭 클릭
2. **FT 데일리 브리핑 자동화** 워크플로우 선택
3. 최근 실행 결과 확인

**성공 표시**: ✅ 초록색  
**실패 표시**: ❌ 빨간색 (클릭하여 로그 확인)

## 📊 프로젝트 구조

```
forbetterday/
├── config/                      # 설정 관련
│   ├── __init__.py
│   ├── config.py               # 환경변수 로드, 상수 정의
│   ├── watchlist.py            # 워치리스트 종목 (SK Hynix, 삼성 등)
│   └── email_config.py         # Gmail SMTP, HTML 템플릿
├── src/                         # 핵심 모듈
│   ├── __init__.py
│   ├── logger.py               # 로깅 설정
│   ├── utils.py                # 공용 유틸리티 (시간 포맷, KST 변환 등)
│   ├── rss_fetcher.py          # FT RSS 수집 + 섹션별 그룹핑
│   ├── translator.py           # Claude API 번역 + 워치리스트 감지
│   ├── email_sender.py         # Gmail SMTP 이메일 발송
│   ├── article_scraper.py      # FT.com 기사 원문 스크래핑
│   └── article_analyzer.py     # 4섹션 분석 양식 적용
├── .github/workflows/
│   └── daily_brief.yml         # GitHub Actions 자동화 (KST 08:00)
├── output/                      # 분석 결과 저장 (자동 생성)
│   ├── app.log                 # 실행 로그
│   └── analysis_YYYYMMDD_HHMMSS.md  # 분석 리포트
├── main.py                     # CLI 오케스트레이션 (진입점)
├── requirements.txt            # Python 의존성
├── .env.example                # 환경변수 템플릿
├── .gitignore
└── README.md
```

## 🔧 기술 스택

| 목적 | 라이브러리 | 버전 |
|------|----------|------|
| RSS 파싱 | feedparser | 6.0.10 |
| AI 번역 & 분석 | anthropic | 0.28.0 |
| HTTP 요청 | requests | 2.31.0 |
| 웹 스크래핑 | beautifulsoup4 | 4.12.2 |
| 환경변수 | python-dotenv | 1.0.0 |
| 타임존 | pytz | 2024.1 |

## ⚠️ 트러블슈팅

### 1. Gmail 발송 실패: "SMTPAuthenticationError"
```
❌ Gmail 인증 실패. App Password를 확인하세요.
```

**해결:**
- Gmail App Password가 공백/특수문자 없이 정확히 입력되었는가?
- 두 단계 인증이 활성화되어 있는가?
- 새로운 App Password를 생성하여 다시 시도

### 2. "CLAUDE_API_KEY 환경변수가 설정되지 않음"
```
❌ CLAUDE_API_KEY 환경변수가 설정되지 않았습니다.
```

**해결:**
- `.env` 파일이 프로젝트 루트에 있는가?
- `CLAUDE_API_KEY=sk-ant-v1-xxxxx` 형식이 올바른가?
- `python main.py` 실행 전 `.env` 생성 확인

### 3. RSS 기사 0개 수집
```
❌ 수집된 기사가 없습니다.
```

**원인:** FT RSS URL이 변경되었거나 24시간 이내 기사 없음

**해결:**
- `.env`의 `FT_RSS_URL` 확인: `https://feeds.ft.com/home/page/rss`
- `LOG_LEVEL=DEBUG`로 변경하여 상세 로그 확인
- FT.com 접속 가능 여부 확인

### 4. 번역/분석 실패: API 에러
```
Error: Connection error, Rate limit, Token limit exceeded
```

**해결:**
- Claude API 할당량 확인 ([Anthropic 콘솔](https://console.anthropic.com))
- 기사 길이가 너무 긴 경우: article_analyzer.py의 `max_tokens` 조정

## 📝 워치리스트 추가/수정

파일: `config/watchlist.py`

```python
WATCHLIST = {
    'SK Hynix': ['SK Hynix', 'SK하이닉스', 'HBM'],
    'Tesla': ['TSLA', 'Tesla', 'Elon Musk'],
    # 새 항목 추가
    'Apple': ['AAPL', 'Apple', 'iPhone'],
}
```

이후 `python main.py --mode daily` 실행하면 자동으로 적용됩니다.

## 🔐 보안 주의사항

⚠️ **프로덕션 배포 시:**
1. `.env` 파일을 `.gitignore`에 추가 (기본값: 적용됨)
2. GitHub Secrets를 사용하여 API 키 관리
3. Gmail App Password는 일반 비밀번호가 아님 (특수 앱용)
4. 주기적으로 App Password 재생성

## 📞 피드백 및 개선사항

- RSS 피드 오류: [FT.com 피드](https://feeds.ft.com/home/page/rss) 상태 확인
- Claude API 문제: [Anthropic 문서](https://docs.anthropic.com)
- 기타 버그: GitHub Issues 등록

## 📄 라이선스

MIT License

## 🙏 감사의 말

- Financial Times RSS Feed
- Anthropic Claude API
- Python 오픈소스 커뮤니티
