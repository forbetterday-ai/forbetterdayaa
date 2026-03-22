# 📋 FT 데일리 브리핑 - 배포 체크리스트

**목표**: GitHub에 배포하고 자동화 설정 완료

---

## ✅ 배포 전 확인 (지금 완료)

- [x] 프로젝트 구조 생성
- [x] 모든 Python 모듈 작성
- [x] 단위 테스트 통과 (8/8)
- [x] .env 파일 설정 (CLAUDE_API_KEY, Gmail)
- [x] requirements.txt 준비 (anthropic 0.25.0)
- [x] GitHub Actions 워크플로우 생성
- [x] README.md 작성
- [x] .gitignore 설정

✅ **현재 상태**: **배포 준비 100% 완료** 🎉

---

## 🚀 배포 단계별 체크리스트

### **Step 1: GitHub 저장소 생성** (⏱️ 5분)

**수행자**: 사용자 (Web UI)

```
□ https://github.com/new 접속
□ Repository name: forbetterday
□ Description: FT Daily Brief Automation
□ Visibility: Public 선택
□ 'Create repository' 클릭
```

**예상 결과**:
```
✅ gangseong-gu/forbetterday (또는 YOUR-USERNAME/forbetterday)
   Public repository 생성됨
```

---

### **Step 2: Git 초기화 & Push** (⏱️ 5분)

**수행자**: 사용자 (Terminal)

```bash
# 터미널에서 다음 명령어 실행:
cd /Users/gangseong-gu/Desktop/forbetterday

# Git 초기화
git init

# 사용자 설정
git config user.email "forbetterday@gmail.com"
git config user.name "FT Automation"

# 파일 추가
git add .

# 커밋
git commit -m "Initial commit: FT Daily Brief Automation v1.0"

# 브랜치 변경
git branch -M main

# Remote 추가 (YOUR-USERNAME을 본인 GitHub 계정명으로 변경)
git remote add origin https://github.com/YOUR-USERNAME/forbetterday.git

# Push
git push -u origin main
```

**체크**:
```
□ git init 성공
□ git add . 완료
□ git commit 완료
□ git push 완료
✅ GitHub 저장소에 모든 파일 업로드됨
```

**🚨 문제 발생 시**:
- Xcode 도구 문제: GitHub Desktop 설치 후 재시도
- SSH 키 문제: HTTPS 방식으로 재시도

---

### **Step 3: GitHub Secrets 설정** (⏱️ 5분)

**수행자**: 사용자 (Web UI)

**위치**: GitHub 저장소 → Settings → Security → Secrets and variables → Actions

```
□ 'New repository secret' 클릭
  
  Secret 1:
  □ Name: CLAUDE_API_KEY
  □ Value: sk-ant-v1-xxxxx... (Anthropic 콘솔 복사)
  □ 'Add secret' 클릭
  
  Secret 2:
  □ Name: GMAIL_ADDRESS
  □ Value: forbetterday@gmail.com
  □ 'Add secret' 클릭
  
  Secret 3:
  □ Name: GMAIL_PASSWORD
  □ Value: zbvx ikeu ezts qlls (Gmail App Password)
  □ 'Add secret' 클릭
```

**완료 확인**:
```
✅ CLAUDE_API_KEY (숨겨짐)
✅ GMAIL_ADDRESS (공개)
✅ GMAIL_PASSWORD (숨겨짐)
```

---

### **Step 4: GitHub Actions 테스트** (⏱️ 3분)

**수행자**: 사용자 (Web UI)

**위치**: GitHub 저장소 → Actions

```
□ 'FT 데일리 브리핑 자동화' 워크플로우 확인
□ 'Run workflow' 드롭다운 클릭
□ 'Run workflow' 버튼 클릭
```

**실행 대기** (2-3분):
```
⏳ Run #1 - FT 데일리 브리핑 자동화
   ├─ Status: In Progress...
   └─ 완료 대기
```

**완료 확인**:
```
✅ Status: Success (또는 Failed)

성공한 경우:
□ Step 1 ✓ Checkout repository
□ Step 2 ✓ Set up Python
□ Step 3 ✓ Install dependencies
□ Step 4 ✓ Run daily brief
□ Step 5 ✓ Upload logs

실패한 경우:
□ 'Run daily brief' 단계 에러 메시지 확인
□ DEPLOYMENT.md의 "문제해결" 섹션 참고
```

---

### **Step 5: 이메일 수신 확인** (⏱️ 2분)

**수행자**: 사용자 (Gmail)

```
□ forbetterday@gmail.com 수신함 확인
□ "FT 데일리 브리핑 - 2026년 03월 22일" 메일 확인
□ HTML 이메일이 제대로 표시되는지 확인
```

**예상 이메일 구조**:
```
Title: FT 데일리 브리핑 - 2026년 03월 22일

Header:
📰 FT 데일리 브리핑
2026년 03월 22일

Sections:
[Markets] - 8개 기사
  ✓ 글로벌 주식시장 강세
  ✓ SK Hynix HBM 계약 ⭐
  ...

[Technology] - 6개 기사
  ✓ AI 칩 수급 현황
  ✓ Palantir 계약 수주 ⭐
  ...

[Companies] - 7개 기사
  ...

Footer:
Financial Times (원문 링크)
```

**완료 확인**:
```
✅ 이메일 받음
✅ HTML 렌더링 정상
✅ 섹션별 정보 표시됨
✅ 워치리스트 항목 ⭐ 표시됨
```

---

## 🎯 배포 완료 확인

모든 Step이 완료되었을 때:

```
✅ GitHub 저장소 생성 (https://github.com/YOUR-USERNAME/forbetterday)
✅ 코드 Push 완료
✅ GitHub Secrets 3개 설정 완료
✅ GitHub Actions 수동 실행 성공
✅ 이메일 수신 확인
```

**배포 상태**: 🟢 **ACTIVE** (활성화)

---

## 📅 자동 실행 확인

배포 후 매일 자동으로 실행됨:

```
시간: 매일 KST 08:00 (UTC 23:00 전일)

자동 실행 확인:
□ 매일 아침 08:00에 GitHub Actions 워크플로우 실행
□ Gmail에 이메일 도착
□ Actions 탭에서 실행 로그 확인

수동 실행 (필요시):
□ Actions 탭 → 'Run workflow' → 'Run workflow' 클릭
→ 즉시 실행됨
```

---

## 🔍 배포 후 모니터링

### **매일 (아침 5분)**
```
☐ GitHub Actions: 최신 워크플로우 "Success" 확인
☐ Gmail: "FT 데일리 브리핑" 메일 도착 확인
```

### **주 1회 (금요일)**
```
☐ GitHub Artifacts: app.log 다운로드 후 에러 확인
☐ Claude API: console.anthropic.com → Usage 확인
☐ GitHub: 워크플로우 실행 이력 5~7개 표시 확인
```

### **월 1회 (월요일)**
```
☐ GitHub Secrets 유효성 확인
☐ Gmail App Password 갱신 예정 체크
☐ API 할당량 및 사용량 분석
```

---

## ⚠️ 에러 발생 시 대응

| 에러 | 원인 | 해결 |
|------|------|------|
| `fatal: could not read Username` | Git 인증 문제 | GitHub Desktop 사용 또는 SSH 키 설정 |
| 이메일 수신 안 됨 | Gmail 인증 실패 | Secrets에서 GMAIL_PASSWORD 확인 |
| `수집된 기사가 없습니다` | 네트워크/FT RSS 문제 | 재실행 또는 FT.com 상태 확인 |
| `CLAUDE_API_KEY 없음` | Secrets 설정 오류 | Secrets 재설정 후 워크플로우 재실행 |

---

## ✨ 배포 성공!

```
┌─────────────────────────────────────┐
│                                     │
│  🎉 배포 완료!                      │
│                                     │
│  매일 KST 08:00 자동 실행됨        │
│  Gmail로 FT 브리핑 수신 중          │
│                                     │
│  다음: 매일 이메일 확인 & 분석      │
│                                     │
└─────────────────────────────────────┘
```

---

**마지막 확인**: 모든 체크박스 완료하면 배포 완료! ✅
