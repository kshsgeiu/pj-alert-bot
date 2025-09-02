#!/data/data/com.termux/files/usr/bin/bash

echo "🔥 Pointless Journey 알림봇 - Termux 설치 스크립트"
echo "=================================================="

# 1. 시스템 업데이트
echo "📦 시스템 업데이트 중..."
pkg update -y && pkg upgrade -y

# 2. 필수 패키지 설치
echo "🔧 필수 패키지 설치 중..."
pkg install -y python git curl jq cronie termux-api openssl

# 3. 저장소 접근 권한 설정
echo "📁 저장소 접근 권한 설정..."
termux-setup-storage

# 4. Python 가상환경 생성
echo "🐍 Python 가상환경 생성 중..."
python -m venv ~/venvs/pj-alert
source ~/venvs/pj-alert/bin/activate

# 5. Python 라이브러리 설치
echo "📚 필요한 라이브러리 설치 중..."
pip install --upgrade pip
pip install requests beautifulsoup4 cloudscraper

# 6. GitHub에서 최신 봇 다운로드
echo "🚀 최신 봇 코드 다운로드 중..."
mkdir -p ~/pj-alert
cd ~/pj-alert

# GitHub에서 스크립트 다운로드
curl -O https://raw.githubusercontent.com/hyoda/pj-alert-bot/main/pj_monitor.py
chmod +x pj_monitor.py

# 7. 실행 테스트
echo "🧪 봇 실행 테스트..."
source ~/venvs/pj-alert/bin/activate
python pj_monitor.py

# 8. 크론 스케줄 설정 (15분마다)
echo "⏰ 자동 실행 스케줄 설정 중..."
(crontab -l 2>/dev/null || echo "") | grep -v "pj_monitor.py" > /tmp/crontab_temp
echo "*/15 * * * * cd ~/pj-alert && source ~/venvs/pj-alert/bin/activate && python pj_monitor.py >> run.log 2>&1" >> /tmp/crontab_temp
crontab /tmp/crontab_temp
rm /tmp/crontab_temp

# 9. 크론 서비스 시작
echo "🔄 크론 서비스 시작..."
pkill crond 2>/dev/null || true
sleep 1
crond

# 크론 상태 확인
if pgrep crond > /dev/null; then
    echo "✅ 크론 서비스 시작 성공!"
else
    echo "⚠️  크론 서비스 시작 실패. 수동 시작: crond"
fi

echo ""
echo "🎉 설치 완료!"
echo ""
echo "📋 다음 단계:"
echo "1. 텔레그램 봇 생성 (@BotFather)"
echo "2. API 토큰과 채팅 ID 확인"
echo "3. 환경변수 설정:"
echo "   export TG_TOKEN=\"your-bot-token\""
echo "   export TG_CHAT=\"your-chat-id\""
echo "   echo 'export TG_TOKEN=\"your-bot-token\"' >> ~/.bashrc"
echo "   echo 'export TG_CHAT=\"your-chat-id\"' >> ~/.bashrc"
echo ""
echo "📊 상태 확인 명령어:"
echo "   tail -f ~/pj-alert/run.log     # 로그 실시간 확인"
echo "   crontab -l                      # 크론 작업 확인"
echo "   ps | grep crond                 # 크론 프로세스 확인"
echo ""
echo "🔥 15분마다 자동으로 Pointless Journey를 모니터링합니다!"