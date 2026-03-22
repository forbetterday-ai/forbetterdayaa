# 🚀 FT 데일리 브리핑 - 배포 완벽 가이드

**작성일**: 2026년 3월 22일  
**상태**: ✅ 배포 준비 완료

---

## 📋 배포 전 체크리스트

- [x] 프로젝트 구조 생성
- [x] 모든 모듈 작성
- [x] 단위 테스트 통과 (8/8)
- [x] Claude API 연결 확인
- [x] .env 설정 완료
- [x] GitHub Actions 워크플로우 작성
- [x] README.md 작성

**현재 상태**: 배포 준비 완료 🎉

---

## 🔑 필수 정보 확인

배포 전에 다음 정보를 준비하세요:

### 1. GitHub 계정
- 웹사이트: https://github.com
- 로그인 확인 필수

### 2. Claude API 키
- 웹사이트: https://console.anthropic.com
- 위치: API Keys 섹션
- 형식: `sk-ant-v1-xxxxx...`

### 3. Gmail 설정
- **Gmail 주소**: forbetterday@gmail.com (현재 설정)
- **App Password**: `zbvx ikeu ezts qlls` (현재 설정)
  - 📌 **생성 방법**: Google 계정 → 보안 → [앱 비밀번호](https://myaccount.google.com/apppasswords)
  - 📌 **주의**: 공백 포함하여 정확히 복사

---

## 🎯 배포 방법 (2가지)

### ✅ **방법 A: GitHub Web UI (추천 - 가장 간단!)**

#### **Step 1: GitHub 저장소 생성** (5분)

1. https://github.com/new 접속
2. 저장소 설정:
   ```
   Repository name: forbetterday
   Description: FT Daily Brief Automation - 매일 FT.com 뉴스 자동 수집 & 분석
   Visibility: Public (또는 Private)
   Initialize this repository with: README (체크 안 함)
   ```
3. **Create repository** 클릭

**예상 화면**:
```
✓ gangseong-gu/forbetterday
  Public · 0 commits
  
  It's easier to work together on github.com
  ...two ways to get started below.
```

---

#### **Step 2: 로컬 Git 설정 & Push** (5분)

터미널을 열고 다음 명령어를 실행하세요:

```bash
cd /Users/gangseong-gu/Desktop/forbetterday

# Git 초기화 (Xcode 도구 문제 시 Skip - 다른 방법 사용)
git init

# Git 사용자 설정
git config user.email "forbetterday@gmail.com"
git config user.name "FT Automation"

# 모든 파일 추가
git add .

# 커밋
git commit -m "Initial commit: FT Daily Brief Automation v1.0"

# main 브랜치로 변경
git branch -M main

# GitHub 저장소 연결 (YOUR-USERNAME을 본인 GitHub 계정명으로 변경)
git remote add origin https://github.com/YOUR-USERNAME/forbetterday.git

# Push
git push -u origin main
```

**실행 예시**:
```
$ git init
Initialized empty Git repository in /Users/gangseong-gu/Desktop/forbetterday/.git/

$ git add .
$ git commit -m "Initial commit: FT Daily Brief Automation v1.0"
main (root-commit) abc1234] Initial commit: FT Daily Brief Automation v1.0
 17 files changed, 3500 insertions(+)
 create mode 100644 README.md
 ...

$ git push -u origin main
Enumerating objects: 20, done.
Counting objects: 100% (20/20), done.
...
To https://github.com/YOUR-USERNAME/forbetterday.git
 * [new branch]      main -> main
Branch 'main' set up to track remote branch 'main' from 'origin'.

✅ Push 완료!
```

**🚨 Xcode 도구 문제 시**:
```
xcode-select: note: No developer tools were found...
```

→ 다음 코드 블록 실행:
```bash
# GitHub Desktop 설치 후 사용하거나
# 또는 SSH 키 설정 후 재시도
git push -u origin main
```

---

#### **Step 3: GitHub Secrets 설정** (5분)

이 단계에서 API 키와 비밀번호를 GitHub에 안전하게 저장합니다.

1. GitHub 저장소 접속 (https://github.com/YOUR-USERNAME/forbetterday)

2. **Settings** → **Security** → **Secrets and variables** → **Actions** 클릭

3. **New repository secret** 클릭

4. **첫 번째 Secret: CLAUDE_API_KEY**
   ```
   Name: CLAUDE_API_KEY
   Value: sk-ant-v1-xxxxx... (Anthropic 콘솔에서 복사)
   ```
   → **Add secret** 클릭

5. **두 번째 Secret: GMAIL_ADDRESS**
   ```
   Name: GMAIL_ADDRESS
   Value: forbetterday@gmail.com
   ```
   → **Add secret** 클릭

6. **세 번째 Secret: GMAIL_PASSWORD**
   ```
   Name: GMAIL_PASSWORD
   Value: zbvx ikeu ezts qlls (Gmail App Password - 공백 포함)
   ```
   → **Add secret** 클릭

**완료 후 화면**:
```
✓ CLAUDE_API_KEY
✓ GMAIL_ADDRESS
✓ GMAIL_PASSWORD
```

---

#### **Step 4: GitHub Actions 확인** (2분)

1. 저장소 → **Actions** 탭 클릭

2. **FT 데일리 브리핑 자동화** 워크플로우 표시

3. **Run workflow** 클릭하여 수동 실행 테스트

**예상 결과**:
```
✅ Run FT 데일리 브리핑 자동화 started...
```

4. 실행 완료 대기 (2-3분)

**성공 표시**:
```
✅ Action succeeded
  Step 1: Checkout repository ✓
  Step 2: Set up Python ✓
  Step 3: Install dependencies ✓
  Step 4: Run daily brief ✓
  Step 5: Upload logs ✓
```

---

### ⚙️ **방법 B: GitHub CLI (고급)**

GitHub CLI가 설치되어 있다면:

```bash
# GitHub CLI 설치 (필요시)
brew install gh

# GitHub 로그인
gh auth login

# 저장소 생성 & Push
cd /Users/gangseong-gu/Desktop/forbetterday
gh repo create forbetterday --public --source=. --remote=origin --push

# Secrets 설정
gh secret set CLAUDE_API_KEY --body 'sk-ant-v1-xxxxx...'
gh secret set GMAIL_ADDRESS --body 'forbetterday@gmail.com'
gh secret set GMAIL_PASSWORD --body 'zbvx ikeu ezts qlls'
```

---

## ✨ 배포 완료 확인

### 1️⃣ GitHub 저장소 확인
```
https://github.com/YOUR-USERNAME/forbetterday
├─ Code 탭: 모든 파일 업로드됨
├─ Actions 탭: 워크플로우 실행 로그
└─ Settings: Secrets 설정됨
```

### 2️⃣ GitHub Actions 자동 실행 확인
```
매일 KST 08:00에 자동 실행됨
├─ UTC 기준: 전일 23:00 (Cron: 0 23 * * *)
└─ 수동 실행: Actions → "FT 데일리 브리핑 자동화" → Run workflow
```

### 3️⃣ 이메일 수신 확인
```
첫 번째 자동 실행 후:
📧 Gmail (forbetterday@gmail.com) 수신함에 메일 도착
└─ 제목: "FT 데일리 브리핑 - 2026년 03월 22일"
```

### 4️⃣ 로그 확인
```
GitHub Actions
├─ Run 로그 확인: Actions → 최신 실행 클릭
└─ Artifacts 다운로드: 로그 파일 (7일 보관)
```

---

## 🔍 배포 후 모니터링

### **매일 체크**
```
☐ GitHub Actions 탭에서 "Success" 표시 확인
☐ Gmail 수신함에서 FT 브리핑 메일 도착 확인
```

### **주 1회 점검**
```
☐ GitHub Artifacts에서 app.log 다운로드 후 에러 확인
☐ Claude API 할당량 확인 (console.anthropic.com)
```

### **에러 발생 시**
```
1. GitHub Actions 탭에서 빨간 X 클릭
2. "Run daily brief" 단계의 에러 메시지 확인
3. output/app.log 에러 메시지 별 해결:
   
   ❌ "CLAUDE_API_KEY 환경변수가 설정되지 않음"
   → GitHub Secrets CLAUDE_API_KEY 확인
   
   ❌ "Gmail 인증 실패"
   → GitHub Secrets GMAIL_PASSWORD 확인
   
   ❌ "수집된 기사가 없습니다"
   → FT RSS URL 상태 확인 (네트워크 문제일 수 있음)
```

---

## 📊 배포 후 사용 흐름

### **매일 아침 (08:00 KST)**
```
1️⃣ Gmail에서 FT 브리핑 메일 확인
   ├─ 새 기사 35~40개 수집
   ├─ 한글 번역 적용
   └─ 워치리스트 항목 ⭐ 표시 (SK Hynix, Palantir 등)

2️⃣ 관심 기사 선택
   └─ 클릭하여 원문 FT.com으로 이동

3️⃣ 상세 분석 필요시 (선택)
   python3 main.py --mode analyze --url "https://ft.com/..."
   └─ 4섹션 분석 리포트 생성 (2분)
```

---

## 🛠️ 배포 후 커스터마이징

### **워치리스트 추가**
```bash
# config/watchlist.py 편집
vi config/watchlist.py

# 새 항목 추가
'Apple': ['AAPL', 'Apple', 'iPhone'],
'Microsoft': ['MSFT', 'Microsoft'],

# Commit & Push
git add config/watchlist.py
git commit -m "Add Apple & Microsoft to watchlist"
git push
```

### **일정 변경**
```bash
# .github/workflows/daily_brief.yml 편집
vi .github/workflows/daily_brief.yml

# Cron 일정 변경 (기본: KST 08:00)
# 예: KST 09:00 → UTC 00:00
on:
  schedule:
    - cron: '0 0 * * *'

# Commit & Push
git add .github/workflows/daily_brief.yml
git commit -m "Change schedule to 9:00 KST"
git push
```

---

## 🎉 배포 완료!

축하합니다! 🎊

이제 **매일 자동으로 FT 뉴스를 수집하고 분석하는 시스템**이 준비되었습니다.

```
✅ 배포 상태: 활성화
✅ 자동 실행: 매일 KST 08:00
✅ 이메일 발송: forbetterday@gmail.com
✅ 분석 리포트: 필요시 생성

🚀 프로덕션 운영 중!
```

---

## 📞 문제해결

### **자주 묻는 질문**

**Q: GitHub Push 실패 - "fatal: could not read Username"**
```
A: GitHub Desktop 설치 또는 SSH 키 설정 후 재시도
```

**Q: 이메일 수신 안 됨**
```
A: 
1. GitHub Secrets GMAIL_PASSWORD 확인 (공백 포함)
2. 두 단계 인증 활성화 확인
3. Gmail App Password 재생성 후 업데이트
```

**Q: 워크플로우 자동 실행 안 됨**
```
A:
1. Actions 탭: 워크플로우 활성화 여부 확인
2. .github/workflows/daily_brief.yml 파일 존재 확인
3. 저장소 Settings → Actions 권한 확인
```

**Q: API 할당량 초과**
```
A: Claude API 사용량 모니터링
   https://console.anthropic.com → Usage
   월 비용 예상: ~$0.50 (매우 저렴함)
```

---

**배포 성공을 기원합니다!** 🚀
