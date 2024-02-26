from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
from datetime import datetime
import time
import json

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

# 전체 점포 리스트
stores = browser.find_elements(By.CSS_SELECTOR, ".quickSearchResultBoxSidoGugun .quickResultLstCon")
store_data_list = []

for store in stores:
    # 매장 이름 추출
    store_name = store.find_element(By.CSS_SELECTOR, ".quickResultLstCon strong").text.strip()
    store_address = store.find_element(By.CSS_SELECTOR, ".result_details").text.strip()
    store_address = store_address.split('\n')[0]  # 주소에서 전화번호 제거

    # 매장 리스트 클릭
    browser.execute_script("arguments[0].click();", store)
    wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, ".map_marker_pop")))

    # 상세 정보 보기 버튼 클릭
    detail_button = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, ".btn_marker_detail")))
    detail_button.click()
    time.sleep(5)
    print("상세 정보 보기 버튼 클릭")

    # 상세 정보 페이지의 HTML 가져오기
    detail_page_html = browser.page_source
    soup = BeautifulSoup(detail_page_html, 'html.parser')
    time.sleep(5)

    # 추출한 정보를 저장
    store_info = {
        "name": store_name,
        "address": store_address,
    }

    # 전체 점포 리스트에 추가
    store_data_list.append(store_info)

    # 닫기 버튼 클릭하기
    close_button = browser.find_element(By.CSS_SELECTOR, ".btn_pop_close > a")
    close_button.click()
    time.sleep(5)

# 문서 구조화
today = datetime.now().strftime('%Y%m%d')
final_data = {
    "kind": "한국스타벅스",
    "data": today,
    "etag": f"we820403{today}",
    "location": "제주특별자치도",
    "count": 1,
    "item": store_data_list
}

# JSON 파일로 저장
filename = f'starbucks_store_jeju_detail_{today}.json'
with open(filename, 'w', encoding='utf-8') as f:
    json.dump(final_data, f, ensure_ascii=False, indent=4)

print(f'JSON 파일 저장 완료: {filename}')

# 브라우저 닫기
browser.quit()