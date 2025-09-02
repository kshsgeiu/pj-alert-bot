# 📱 텔레그램 봇 설정 완벽 가이드

## 1단계: 텔레그램 봇 생성

### A. BotFather와 대화 시작
1. 텔레그램 앱에서 [@BotFather](https://t.me/botfather) 검색
2. **시작** 버튼 클릭
3. `/start` 명령어 입력

### B. 새 봇 생성
1. `/newbot` 명령어 입력
2. **봇 이름** 설정:
   ```
   예시: PJ Alert Bot
   ```
3. **봇 사용자명** 설정 (반드시 'bot'으로 끝나야 함):
   ```
   예시: pj_alert_myname_bot
   ```

### C. API 토큰 받기
BotFather가 다음과 같은 메시지를 보냅니다:
```
Done! Congratulations on your new bot. You will find it at t.me/pj_alert_myname_bot. 
You can now add a description, about section and profile picture for your bot, 
see /help for a list of commands. By the way, when you've finished creating your cool bot, 
ping our Bot Support if you want a better username.

Use this token to access the HTTP API:
123456789:AAHdqTcvCH1vGWJxfSeofSAs0K5PALDsaw

Keep your token secure and store it safely, it can be used by anyone to control your bot.
```

**🔑 API 토큰**: `123456789:AAHdqTcvCH1vGWJxfSeofSAs0K5PALDsaw`
**(이것을 복사해두세요!)**

## 2단계: 채팅 ID 확인

### A. 봇과 대화 시작
1. BotFather 메시지의 링크 클릭 (예: t.me/pj_alert_myname_bot)
2. **시작** 버튼 클릭
3. `/start` 메시지 입력

### B. 채팅 ID 가져오기
1. 브라우저(Safari/Chrome)에서 다음 URL 접속:
   ```
   https://api.telegram.org/bot123456789:AAHdqTcvCH1vGWJxfSeofSAs0K5PALDsaw/getUpdates
   ```
   *(여기서 `123456789:AAHdqTcvCH1vGWJxfSeofSAs0K5PALDsaw` 부분을 본인의 API 토큰으로 바꿔주세요)*

2. 다음과 같은 JSON 응답이 나타납니다:
   ```json
   {
     "ok": true,
     "result": [
       {
         "update_id": 123456789,
         "message": {
           "message_id": 1,
           "from": {
             "id": 987654321,
             "is_bot": false,
             "first_name": "Your Name"
           },
           "chat": {
             "id": 987654321,
             "first_name": "Your Name",
             "type": "private"
           },
           "date": 1234567890,
           "text": "/start"
         }
       }
     ]
   }
   ```

3. **채팅 ID 찾기**: `"chat": {"id": 987654321}` 부분의 숫자
   
   **🆔 채팅 ID**: `987654321`
   **(이것을 복사해두세요!)**

### C. 응답이 비어있는 경우
만약 `"result": []`라고 나온다면:
1. 봇에게 아무 메시지나 다시 보내기 (예: "안녕")
2. URL을 다시 새로고침
3. 최신 메시지의 `chat.id` 확인

## 3단계: GitHub Secrets 설정

### A. GitHub 저장소 접속
1. 본인의 PJ Alert Bot 저장소로 이동
2. **Settings** 탭 클릭

### B. Secrets 페이지 이동
1. 왼쪽 메뉴에서 **Secrets and variables** 클릭
2. **Actions** 선택

### C. 첫 번째 Secret 추가 (TG_TOKEN)
1. **New repository secret** 버튼 클릭
2. **Name**: `TG_TOKEN`
3. **Secret**: `123456789:AAHdqTcvCH1vGWJxfSeofSAs0K5PALDsaw` (본인 토큰)
4. **Add secret** 클릭

### D. 두 번째 Secret 추가 (TG_CHAT)
1. **New repository secret** 버튼 다시 클릭
2. **Name**: `TG_CHAT`
3. **Secret**: `987654321` (본인 채팅 ID, 숫자만)
4. **Add secret** 클릭

## 4단계: 설정 확인

### A. Secrets 목록 확인
다음 두 개가 보여야 합니다:
- `TG_TOKEN` (Updated X seconds ago)
- `TG_CHAT` (Updated X seconds ago)

### B. 테스트 메시지 발송
브라우저에서 다음 URL 접속해보세요:
```
https://api.telegram.org/bot123456789:AAHdqTcvCH1vGWJxfSeofSAs0K5PALDsaw/sendMessage?chat_id=987654321&text=Hello%20World
```
*(본인의 토큰과 채팅 ID로 바꿔서)*

텔레그램에서 "Hello World" 메시지를 받으면 설정 완료!

## 🚨 문제해결

### 1. "Chat not found" 오류
- 봇에게 `/start` 메시지를 보냈는지 확인
- 채팅 ID가 정확한지 재확인

### 2. "Unauthorized" 오류  
- API 토큰이 정확한지 확인
- 토큰에 공백이나 특수문자가 들어가지 않았는지 확인

### 3. "getUpdates" 결과가 빈 배열
- 봇에게 메시지를 새로 보낸 후 다시 시도
- 브라우저 캐시를 지우고 새로고침

### 4. GitHub Actions에서 알림 안됨
- Settings → Secrets에서 변수명 확인 (`TG_TOKEN`, `TG_CHAT`)
- 값에 따옴표나 공백이 들어가지 않았는지 확인

## 💡 추가 팁

### 봇 커스터마이징
BotFather에서 다음 명령어로 봇을 꾸밀 수 있습니다:
- `/setdescription`: 봇 설명 설정
- `/setuserpic`: 봇 프로필 사진 설정
- `/setcommands`: 봇 명령어 메뉴 설정

### 알림 소리 설정
텔레그램 → 봇과의 채팅 → 상단 클릭 → 알림에서 소리와 진동 설정 가능

### 그룹 채팅에서 사용
1. 봇을 그룹에 추가
2. `/getUpdates`에서 그룹의 `chat.id` 확인 (음수로 나타남)
3. 그 ID를 `TG_CHAT`에 설정

---

설정이 완료되면 GitHub Actions에서 15분마다 자동으로 모니터링하고 변화가 있을 때 알림을 보냅니다! 🎉