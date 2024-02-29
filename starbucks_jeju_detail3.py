from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
from datetime import datetime
import time
import json 
import re

# 브라우저 초기화 및 셋팅
browser = webdriver.Chrome()
wait = WebDriverWait(browser, 10)
browser.get("https://www.starbucks.co.kr/store/store_map.do")
time.sleep(10)

# 클릭 및 이동
browser.find_element(By.CSS_SELECTOR, "#container > div > form > fieldset > div > section > article.find_store_cont > article > header.loca_search > h3 > a").click()
time.sleep(5)
browser.find_element(By.CSS_SELECTOR, ".loca_step1_cont .sido_arae_box li:nth-child(16)").click()
time.sleep(5)
browser.find_element(By.CSS_SELECTOR, "#mCSB_2_container > ul > li:nth-child(1) > a").click()
time.sleep(5)

# 현재 페이지의 HTML 가져오기
html = browser.page_source

# BeautifulSoup을 사용하여 HTML 파싱
soup = BeautifulSoup(html, 'html.parser')

# 전체 점포 리스트 가져오기
stores = soup.select('.quickSearchResultBoxSidoGugun .quickResultLstCon')
store_data_list = []

for index, store in enumerate(stores):
    store_info = {}

    path = f"#mCSB_3_container > ul > li:nth-child({index + 1}) > strong"

    browser.find_element(By.CSS_SELECTOR, path).click()
    time.sleep(2)  # 페이지 로드를 기다립니다. 필요시 시간 조정

    # 각 점포의 정보 추출
    store_name = store.select_one('.quickResultLstCon > strong').text.strip()
    store_address = store.select_one('.result_details').text.strip()

    # 주소에서 해당 번호 제거
    store_address = re.sub(r'1522-3232', '', store_address)  # 번호 제거

    # store를 하나씩 클릭
    # 브라우저에서 li.quickResultLstCon를 가져와서 번호를 붙여줘야 함
    # quickResultLstCon:nth-child(num)
    # 클릭

    # 추출한 정보를 딕셔너리에 저장
    store_info['name'] = store_name
    store_info['address'] = store_address
    
    # store_data_list에 추가
    store_data_list.append(store_info)

# 결과 출력
for store_info in store_data_list:
    print(store_info)

# JSON 파일 구조화
today = datetime.now().strftime('%Y%m%d')
final_data = {
    "kind": "한국스타벅스",
    "data": today,
    "etag": f"we820403{today}",
    "location": "제주특별자치도",
    "count": len(store_data_list),
    "item": store_data_list
}

# JSON 파일로 저장
filename = f'starbucks_store_jeju_detail_{today}.json'
with open(filename, 'w', encoding='utf-8') as f:
    json.dump(final_data, f, ensure_ascii=False, indent=4)

print(f'JSON 파일 저장 완료: {filename}')

# 브라우저 닫기
browser.quit()