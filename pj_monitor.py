#!/usr/bin/env python3
"""
Pointless Journey 재입고 알림 봇
GitHub Actions에서 실행되는 모니터링 스크립트
"""

import os
import json
import requests
import time
from datetime import datetime, timezone
from pathlib import Path
import sys

try:
    import cloudscraper
    from bs4 import BeautifulSoup
except ImportError as e:
    print(f"필요한 라이브러리가 없습니다: {e}")
    sys.exit(1)

# 설정
TARGET_URL = "https://pointlessjourney.jp"
CACHE_FILE = "cache.json"
ALERT_FILE = "alert.txt"

# 환경변수에서 텔레그램 설정 읽기
TG_TOKEN = os.getenv("TG_TOKEN")
TG_CHAT = os.getenv("TG_CHAT")

def load_cache():
    """이전 상품 정보 로드"""
    if Path(CACHE_FILE).exists():
        with open(CACHE_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    return {}

def save_cache(data):
    """상품 정보 저장"""
    with open(CACHE_FILE, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

def scrape_products():
    """Pointless Journey 상품 정보 수집"""
    scraper = cloudscraper.create_scraper()
    
    try:
        response = scraper.get(TARGET_URL, timeout=30)
        response.raise_for_status()
    except Exception as e:
        print(f"사이트 접근 실패: {e}")
        return []
    
    soup = BeautifulSoup(response.text, 'html.parser')
    products = []
    
    # 상품 링크 찾기 (Pointless Journey 구조에 맞춤)
    for link in soup.find_all('a', href=True):
        href = link.get('href')
        if not href or '/products/' not in href:
            continue
            
        # 절대 URL로 변환
        if href.startswith('/'):
            href = TARGET_URL.rstrip('/') + href
        
        # 상품명 추출
        title = link.get_text(strip=True)
        if not title or len(title) < 2:
            # 이미지 alt 속성에서 제목 찾기
            img = link.find('img')
            if img and img.get('alt'):
                title = img.get('alt').strip()
        
        if not title or len(title) < 2:
            continue
        
        # 품절 상태 확인
        parent = link.parent
        if parent:
            parent_text = parent.get_text(' ', strip=True).lower()
        else:
            parent_text = link.get_text(' ', strip=True).lower()
        
        # 품절 키워드 체크
        sold_out_keywords = ['sold out', 'soldout', '품절', '在庫なし', 'out of stock']
        is_sold_out = any(keyword in parent_text for keyword in sold_out_keywords)
        
        product_id = href.split('/')[-1] or href
        products.append({
            'id': product_id,
            'title': title,
            'url': href,
            'in_stock': not is_sold_out,
            'last_seen': datetime.now(timezone.utc).isoformat()
        })
    
    # 중복 제거
    unique_products = {}
    for product in products:
        unique_products[product['id']] = product
    
    print(f"총 {len(unique_products)}개 상품 발견")
    return list(unique_products.values())

def check_changes(current_products, cached_products):
    """변화 감지: 신상품, 재입고"""
    new_products = []
    restocked_products = []
    
    for product in current_products:
        product_id = product['id']
        cached = cached_products.get(product_id)
        
        if not cached:
            # 새 상품
            new_products.append(product)
        elif not cached.get('in_stock', False) and product['in_stock']:
            # 재입고 (품절 → 재고 있음)
            restocked_products.append(product)
    
    return new_products, restocked_products

def create_alert_message(new_products, restocked_products):
    """알림 메시지 생성"""
    messages = []
    
    if new_products:
        messages.append(f"🆕 **신상품 {len(new_products)}개 발견!**")
        for product in new_products[:5]:  # 최대 5개만
            messages.append(f"• {product['title']}")
            messages.append(f"  {product['url']}")
        if len(new_products) > 5:
            messages.append(f"... 외 {len(new_products) - 5}개 더")
    
    if restocked_products:
        if messages:
            messages.append("")
        messages.append(f"✅ **재입고 {len(restocked_products)}개!**")
        for product in restocked_products[:5]:  # 최대 5개만
            messages.append(f"• {product['title']}")
            messages.append(f"  {product['url']}")
        if len(restocked_products) > 5:
            messages.append(f"... 외 {len(restocked_products) - 5}개 더")
    
    if messages:
        messages.insert(0, "🔥 **Pointless Journey 알림**")
        messages.append("")
        messages.append(f"⏰ {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        return "\n".join(messages)
    
    return None

def send_telegram_message(message):
    """텔레그램 메시지 발송"""
    if not TG_TOKEN or not TG_CHAT:
        print("텔레그램 설정이 없습니다. (TG_TOKEN, TG_CHAT)")
        return False
    
    url = f"https://api.telegram.org/bot{TG_TOKEN}/sendMessage"
    data = {
        'chat_id': TG_CHAT,
        'text': message,
        'parse_mode': 'Markdown',
        'disable_web_page_preview': True
    }
    
    try:
        response = requests.post(url, data=data, timeout=10)
        response.raise_for_status()
        print("텔레그램 메시지 발송 성공!")
        return True
    except Exception as e:
        print(f"텔레그램 발송 실패: {e}")
        return False

def main():
    """메인 실행 함수"""
    print(f"[{datetime.now()}] Pointless Journey 모니터링 시작...")
    
    # 현재 상품 정보 수집
    current_products = scrape_products()
    if not current_products:
        print("상품 정보를 가져올 수 없습니다.")
        return
    
    # 이전 캐시 로드
    cached_products = load_cache()
    
    # 변화 감지
    new_products, restocked_products = check_changes(current_products, cached_products)
    
    # 알림 메시지 생성
    alert_message = create_alert_message(new_products, restocked_products)
    
    if alert_message:
        print("변화 감지! 알림 발송...")
        print(alert_message)
        
        # 알림 파일 생성 (GitHub Actions에서 사용)
        with open(ALERT_FILE, 'w', encoding='utf-8') as f:
            f.write(alert_message)
        
        # 텔레그램 발송
        send_telegram_message(alert_message)
        
        # 환경변수로 GitHub Actions에 알림
        with open(os.environ.get('GITHUB_OUTPUT', '/dev/null'), 'a') as f:
            f.write('has_changes=true\n')
    else:
        print("변화 없음")
        # 알림 파일 삭제
        if Path(ALERT_FILE).exists():
            Path(ALERT_FILE).unlink()
        
        with open(os.environ.get('GITHUB_OUTPUT', '/dev/null'), 'a') as f:
            f.write('has_changes=false\n')
    
    # 캐시 업데이트
    updated_cache = {}
    for product in current_products:
        updated_cache[product['id']] = product
    
    save_cache(updated_cache)
    print(f"캐시 업데이트 완료: {len(updated_cache)}개 상품")

if __name__ == "__main__":
    main()