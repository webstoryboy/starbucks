# 파일 추가 모드로 열기
# f = open("test.txt", "a", encoding="utf8")  
# f.write("안녕하세요! 가자1")  # 파일에 텍스트 쓰기
# f.close()  # 파일 닫기

# 파일을 쓰기 모드로 열기
# f = open("test.txt", "w", encoding="utf8")  
# f.write("안녕하세요! 가자1 .\n안녕하세요! 가자1")  # 파일에 텍스트 쓰기
# f.close()  # 파일 닫기

# 파일 읽기 모드
# f = open("test.txt", "r", encoding="utf-8")  
# print(f.read())
# f.close()

# 파일 한줄씩 읽기 모드
# f = open("test.txt", "r", encoding="utf-8")  
# print(f.readline())
# print(f.readline())
# print(f.readline())
# print(f.readline())
# f.close()

# 파일 한줄씩 읽기 모드
# f = open("test.txt", "r", encoding="utf-8")  
# print(f.readlines())
# f.close()

# 파일 복사
# fr = open('test.txt', 'r', encoding="utf-8")
# fw = open('test_copy.txt', 'w', encoding="utf-8")
# fw.write(fr.read())
# fw.close()
# fr.close()

# 이미지 복사 
# fr = open('apple.png', 'rb')
# fw = open('apple_copy.png', 'wb')
# fw.write(fr.read())
# fw.close()
# fr.close()

# 이미지 복사 close 생략, with 메서드 사용
# with open('apple.png', 'rb') as fr:
#     with open('apple_copy.png', 'wb') as fw:
#         fw.write(fr.read())

# requests
# import requests
# res = requests.get("https://naver.com")
# # print(res.status_code) # 200
# # print(len(res.text)) # 글자수
# # print(res.text) # 

# with open("naver_text.html", "w", encoding="utf8") as f:
#     f.write(res.text)


# requests2
# import requests
# url = "https://webstoryboy.tistory.com/"
# headers = {'User-Agent': 'Mozilla/5.0'}
# res = requests.get(url, headers=headers)
# res.raise_for_status()
# with open("naver_text.html", "w", encoding="utf8") as f:
#     f.write(res.text)

# pip install beautifulsoup4
# pip install lxml
# import requests
# from bs4 import BeautifulSoup

# url = "https://www.naver.com"
# res = requests.get(url)
# res.raise_for_status()

# soup = BeautifulSoup(res.text, "lxml")
# # print(soup.title)
# # print(soup.title.get_text())
# # print(soup.a)
# # print(soup.a.attrs)
# # print(soup.a.attrs["href"])
# # print(soup.find("a"))
# # print(soup.find("a").text)
# # print(soup.find_all("div", attrs={"class": "atcmp_cue"}))
# print(soup.find("i", text="레이어 닫기"))



