####    기사를 중복으로 크롤링하는 문제가 있음
####    더보기 버튼을 다 누르고 한 번에 링크를 따오던가 
####    크롤링 하기 전에 중복 제거해야함


from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time
import pandas as pd
from bs4 import BeautifulSoup

from webdriver_manager.chrome import ChromeDriverManager
from openpyxl import Workbook, load_workbook

# Chrome 실행 옵션 설정
chrome_options = Options()
chrome_options.add_argument("--headless")
chrome_options.add_experimental_option("detach", True)
chrome_options.add_experimental_option("excludeSwitches", ["enable-logging"])

# ChromeDriverManager를 통해 크롬 드라이버의 최신 버전을 설치 및 실행
service = Service(executable_path=ChromeDriverManager().install())
browser = webdriver.Chrome(service=service, options=chrome_options)




def scrape_news_list(articles, data):

    for i in range(len(articles)):
        # 페이지 로드 후 다시 요소를 갱신해야 하므로 반복문에서 인덱스를 사용
        articles = browser.find_elements(By.CLASS_NAME, 'sa_text')  # 요소 갱신

        link = articles[i].find_element(By.TAG_NAME, 'a')  # 링크 요소 찾기
        article_url = link.get_attribute('href')  # 링크 URL 가져오기

        browser.get(article_url)  # 링크 열기


        # 제목, 본문 추출
        try:
            title_element = browser.find_element(By.CLASS_NAME, 'media_end_head_title')
            title = title_element.text

            content_element = browser.find_element(By.CLASS_NAME, 'go_trans._article_content')
            content = content_element.text

        except Exception as e:
            content = "본문을 가져올 수 없습니다."


        # 데이터 저장
        data.append({
            'title': title,
            'url': article_url,
            'content': content
        })

        print(len(data))
        browser.back()  # 이전 페이지로 돌아가기    




# 뉴스 페이지로 이동
browser.get("https://news.naver.com/section/100")

articles = browser.find_elements(By.CLASS_NAME, 'sa_text')
data = []

while True:
    # 페이지 크롤링
    scrape_news_list(articles, data)

    if len(data) > 50:
        break

    # 기사 더보기
    load_more_button = browser.find_element(By.CLASS_NAME, 'section_more_inner._CONTENT_LIST_LOAD_MORE_BUTTON')
    load_more_button.click()


browser.quit()


df = pd.DataFrame(data)
df.to_csv("test.csv", index=False)
