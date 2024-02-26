from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
from datetime import datetime
import time
import json

# 운영시간 가져오기
def extract_info_by_label(soup, label_text, default="정보 없음"):
    dt_element = soup.find('dt', string=lambda text: text and label_text in text)
    if dt_element:
        dd_element = dt_element.find_next_sibling('dd')
        if dd_element:
            return dd_element.get_text(strip=True)
    return default

# 상세정보 이미지 가져오기
def extract_images_by_label(soup, label_text):
    dt_element = soup.find('dt', string=lambda text: text and label_text in text)
    if dt_element:
        dd_element = dt_element.find_next_sibling('dd')
        if dd_element:
            images = dd_element.find_all('img')
            return ['https:' + img['src'] if not img['src'].startswith(('http:', 'https:')) else img['src'] for img in images]
    return []

# 브라우저 초기화 및 셋팅
browser = webdriver.Chrome()
wait = WebDriverWait(browser, 20)
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
    # 매장 이름과 주소 추출
    store_name = store.find_element(By.CSS_SELECTOR, "strong").text.strip()
    store_address = store.find_element(By.CSS_SELECTOR, ".result_details").text.strip()
    store_address = store_address.split('\n')[0]  # 주소에서 전화번호 제거

    # 매장 상세 정보 페이지로 이동
    browser.execute_script("arguments[0].click();", store)
    time.sleep(5)

    # 상세 정보 페이지의 HTML 가져오기
    detail_page_html = browser.page_source
    soup = BeautifulSoup(detail_page_html, 'html.parser')
    time.sleep(5)

    # 필요한 정보 가져오기
    operation_hours = extract_info_by_label(soup, "영업시간 보기", "영업시간 정보 없음")
    image_urls = ['https:' + img['src'] if not img['src'].startswith(('http:', 'https:')) else img['src'] for img in soup.select('.s_img img')]
    phone_number = extract_info_by_label(soup, "전화번호")
    parking_info = extract_info_by_label(soup, "주차정보")
    directions = extract_info_by_label(soup, "오시는 길")
    description = soup.select_one('.asm_stitle p').get_text(strip=True) if soup.select_one('.asm_stitle p') else "설명 없음"
    type_images = extract_images_by_label(soup, "타입")
    service_images = extract_images_by_label(soup, "서비스")

    # 매장 정보 저장
    store_info = {
        "name": store_name,
        "address": store_address,
        "image_urls": image_urls,
        "operation_hours": operation_hours,
        "phone_number": phone_number,
        "parking_info": parking_info,
        "directions": directions,
        "description": description,
        "type_images": type_images,
        "service_images": service_images
    }
    store_data_list.append(store_info)

    # 상세 페이지 닫기
    closeButton = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, ".btn_pop_close .isStoreViewClosePop")))
    closeButton.click()
    time.sleep(3)

# 문서 구조화
today = datetime.now().strftime('%Y%m%d')
final_data = {
    "kind": "한국스타벅스",
    "data": today,
    "etag": f"we820403{today}",
    "location": "제주특별자치도",
    "count": 1,
    "item": [store_info]
}

# JSON 파일로 저장
filename = f'starbucks_store_jeju_detail_{today}.json'
with open(filename, 'w', encoding='utf-8') as f:
    json.dump(final_data, f, ensure_ascii=False, indent=4)

print(f'JSON 파일 저장 완료: {filename}')

# 브라우저 닫기
browser.quit()