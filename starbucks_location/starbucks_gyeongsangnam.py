from selenium import webdriver
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup as bs
from datetime import datetime 
import time
import json
import re

browser = webdriver.Chrome()
browser.get("https://www.starbucks.co.kr/store/store_map.do")
time.sleep(10)

# 지역검색 클릭
localSearch = browser.find_element(By.CSS_SELECTOR, "#container > div > form > fieldset > div > section > article.find_store_cont > article > header.loca_search > h3 > a")
localSearch.click()
time.sleep(5)

# 시/도 클릭
si = browser.find_element(By.CSS_SELECTOR, ".loca_step1_cont .sido_arae_box li:nth-child(10)")
si.click()
time.sleep(5)

# 전체를 클릭
gu = browser.find_element(By.CSS_SELECTOR, "#mCSB_2_container > ul > li:nth-child(1) > a")
gu.click()
time.sleep(5)

# html 파일 받아오기
html_source = browser.page_source
soup = bs(html_source, 'lxml')
titles = soup.select(".quickSearchResultBoxSidoGugun .quickResultLstCon strong")
addresses = soup.select(".quickSearchResultBoxSidoGugun .quickResultLstCon .result_details")

stores_data = []
for title, address in zip(titles, addresses):
    clean_title = title.text.strip()  # 제목의 불필요한 공백 제거
    clean_address = re.sub(r'\d{4}-\d{4}', '', address.text).strip()  # 전화번호 패턴을 찾아 제거
    stores_data.append({"name": clean_title, "address": clean_address})

# 오늘 날짜 가져오기
today = datetime.now().strftime('%Y%m%d')

# 최종 JSON 구조 정의
final_data = {
    "kind": "한국스타벅스",
    "data": today,
    "etag": f"we820403{today}",
    "location": "경상남도",
    "count": len(stores_data),
    "item": stores_data
}

# json 파일 추가하기
filename = f'starbucks_stores_gyeongsangnam_{today}.json'
with open(filename, 'w', encoding='utf-8') as f:
    json.dump(final_data, f, ensure_ascii=False, indent=4)

print(f'JSON 파일 저장 완료: {filename}')