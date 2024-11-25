from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time
import os
import json
import pandas as pd
from bs4 import BeautifulSoup

from webdriver_manager.chrome import ChromeDriverManager
from openpyxl import Workbook, load_workbook

# Chrome 실행 옵션 설정
chrome_options = Options()
#chrome_options.add_argument("--headless")
chrome_options.add_experimental_option("detach", True)
chrome_options.add_experimental_option("excludeSwitches", ["enable-logging"])

# ChromeDriverManager를 통해 크롬 드라이버의 최신 버전을 설치 및 실행
service = Service(executable_path=ChromeDriverManager().install())
browser = webdriver.Chrome(service=service, options=chrome_options)

json_file_path = 'articles.json'

START_PAGE = 1
END_PAGE = 2

data = []


for page_num in range(START_PAGE, END_PAGE+1):
    try:
        for i in range(1, 12):

            path = f'//*[@id="content"]/div/ul/li[{i}]/a'
            goto = browser.find_element(By.XPATH, path)
            goto.click()
            
            articles = browser.find_elements(By.TAG_NAME, 'li')
            for article in articles:
                url = article.find_element(By.TAG_NAME, 'a')  # 링크 요소 찾기
                article_url = url.get_attribute('href')  # 링크 URL 가져오기

                if "mag_id" in article_url:
                    # 기사 페이지 접근
                    browser.get(article_url)

                    # 제목 추출
                    title_element = browser.find_element(By.CLASS_NAME, 'news_tit')
                    title = title_element.text

                    # 내용 추출
                    # wait.until(EC.presence_of_element_located((By.TAG_NAME, 'p')))
                    content_elements = browser.find_elements(By.TAG_NAME, 'p')
                    content = [element.text for element in content_elements 
                        if 'number' not in element.get_attribute('class') and element.text.strip()
                    ]
                    content = ''.join(content)

                    # 날짜 추출
                    date_element = browser.find_element(By.CSS_SELECTOR, 'div.by')

                    date = date_element.get_attribute('innerText')
                    date = date.split()[-1]


                    new_data = {'title': title, 'content': content, 'category': '뉴스', 'date': date, 'url': article_url, 'keywords': ''}
                    data.append(new_data)

                    browser.back()
                    print(len(data))
                    time.sleep(2)


    except Exception as e:
        print(f"Error occurred on page {page_num}: {e}")
        # 오류 발생 시에도 중간 데이터를 저장
        with open(json_file_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=4)


browser.quit()


with open(json_file_path, 'w', encoding='utf-8') as f:
    json.dump(data, f, ensure_ascii=False, indent=4)