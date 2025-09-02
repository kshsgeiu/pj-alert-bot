# 🔥 Pointless Journey 재입고 알림 봇

**아이폰에서 Pointless Journey 신상품/재입고 알림을 받을 수 있는 GitHub Actions 기반 봇입니다!**

## ✨ 특징

- 🆓 **완전 무료** (GitHub Actions 무료 티어 사용)
- 📱 **아이폰 호환** (텔레그램을 통한 즉시 푸시 알림)
- ⏰ **24/7 자동 모니터링** (15분마다 체크)
- 🆕 **신상품 감지** (새로운 아이템 출시 시 알림)
- ✅ **재입고 알림** (품절 → 재고 있음 변화 감지)
- 🔄 **자동 캐시 관리** (중복 알림 방지)

## 🚀 빠른 시작

### 1단계: 저장소 복사하기

1. 이 저장소를 **Fork** 하거나 **Download ZIP**으로 다운로드
2. 본인의 GitHub 계정에 새 저장소로 업로드

### 2단계: 텔레그램 봇 만들기

#### A. 봇 생성
1. 텔레그램에서 [@BotFather](https://t.me/botfather) 검색
2. `/newbot` 명령어 입력
3. 봇 이름 설정 (예: PJ Alert Bot)
4. 봇 사용자명 설정 (예: pj_alert_123_bot)
5. **API 토큰 복사** (예: `123456789:AAHdqTcvCH1vGWJxfSeofSAs0K5PALDsaw`)

#### B. 채팅 ID 확인
1. 생성한 봇에게 `/start` 메시지 전송
2. 브라우저에서 다음 URL 접속:
   ```
   https://api.telegram.org/bot[여기에API토큰]/getUpdates
   ```
   예시: `https://api.telegram.org/bot123456789:AAHdqTcvCH1vGWJxfSeofSAs0K5PALDsaw/getUpdates`

3. 응답에서 `"chat":{"id":숫자}` 부분 찾기 (예: `987654321`)

### 3단계: GitHub Secrets 설정

1. GitHub 저장소 → **Settings** → **Secrets and variables** → **Actions**
2. **New repository secret** 클릭하여 다음 2개 추가:

#### TG_TOKEN
- **Name**: `TG_TOKEN`
- **Secret**: `123456789:AAHdqTcvCH1vGWJxfSeofSAs0K5PALDsaw` (실제 봇 토큰)

#### TG_CHAT
- **Name**: `TG_CHAT`  
- **Secret**: `987654321` (실제 채팅 ID, 숫자만)

### 4단계: GitHub Actions 활성화

1. 저장소 → **Actions** 탭
2. **I understand my workflows, enable them** 클릭
3. **PJ Alert Bot** 워크플로우 확인

### 5단계: 테스트 실행

1. **Actions** → **PJ Alert Bot** → **Run workflow** → **Run workflow**
2. 실행 로그에서 "총 XX개 상품 발견" 메시지 확인
3. 텔레그램에서 첫 알림 받기 (모든 상품이 "신상품"으로 표시됨)

## 📱 사용법

### 정상 작동 확인
- 첫 실행: 모든 상품을 "신상품"으로 알림 받음 (정상)
- 이후 실행: 변화가 있을 때만 알림 받음

### 알림 종류
- 🆕 **신상품**: 새로 출시된 아이템
- ✅ **재입고**: 품절에서 재고 있음으로 변화한 아이템

### 실행 주기
- **자동**: 15분마다 (GitHub Actions 스케줄)
- **수동**: Actions 탭에서 언제든지 실행 가능

## ⚙️ 설정 변경

### 모니터링 주기 변경
`.github/workflows/monitor.yml` 파일의 cron 값 수정:
```yaml
schedule:
  - cron: '*/10 * * * *'  # 10분마다
  - cron: '0 * * * *'     # 1시간마다  
  - cron: '0 */6 * * *'   # 6시간마다
```

### 알림 메시지 커스터마이징
`pj_monitor.py` 파일의 `create_alert_message` 함수에서 메시지 형식 변경 가능

## 🔧 문제해결

### 알림이 안 와요
1. GitHub Actions 로그 확인:
   - Actions → 최근 실행 → 로그 확인
   - "상품 발견" 메시지가 있는지 확인

2. 텔레그램 설정 확인:
   - Settings → Secrets에서 TG_TOKEN, TG_CHAT 값 재확인
   - 봇에게 `/start` 메시지를 다시 보냈는지 확인

3. 봇 권한 확인:
   - 봇과의 채팅에서 메시지 기록 확인
   - 봇을 차단하지 않았는지 확인

### GitHub Actions가 실행 안 됨
- 저장소 → Settings → Actions → **Allow all actions** 선택
- 무료 계정: 월 2000분 제한 확인 (이 봇은 월 100분 정도 사용)

### 너무 많은 알림
첫 실행 시 모든 상품이 "신상품"으로 알림되는 것은 정상입니다.
2번째 실행부터는 실제 변화가 있을 때만 알림됩니다.

## 📊 모니터링 현황

### 로그 확인
Actions → PJ Alert Bot → 최근 실행에서 다음 정보 확인 가능:
- 총 상품 수
- 신상품/재입고 현황  
- 실행 시간
- 오류 여부

### 캐시 파일
`cache.json` 파일에 이전 상품 정보가 저장됩니다.
변화 감지와 중복 알림 방지에 사용됩니다.

## 🎯 고급 사용법

### 다른 사이트 추가
`pj_monitor.py`에서 `TARGET_URL` 변경하고 파싱 로직 수정

### 여러 채널 알림
Discord, Slack 등 다른 메신저도 추가 가능:
```python
# Discord 웹훅 예시
def send_discord(message):
    webhook_url = "https://discord.com/api/webhooks/..."
    requests.post(webhook_url, json={"content": message})
```

### 이메일 알림 추가
Gmail SMTP를 통한 이메일 발송도 가능

## 📄 라이선스

MIT License - 자유롭게 사용하세요!

## 🤝 기여

버그 리포트나 기능 제안은 Issues에서 환영합니다!

---

**💡 팁**: 텔레그램 봇 토큰과 채팅 ID는 절대 공개하지 마세요!