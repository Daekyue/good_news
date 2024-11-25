from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time
import os
import json
import pandas as pd
from datetime import datetime
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

json_file_path = 'articles4.json'

START_PAGE = 401
END_PAGE = 500

data = []

for page_num in range(START_PAGE, END_PAGE+1):
    try:
        browser.get(f"https://www.indiewire.com/t/film/page/{page_num}/")

        for i in range(1, 13):
            path = f'/html/body/div[3]/div[2]/div/div/div/div[1]/div[1]/div/div/div/div[2]/div[{i}]/div/div[2]/div[2]/a'

            article = browser.find_element(By.XPATH, path)
            article.click()

            title_element = browser.find_element(By.TAG_NAME, 'h1')
            title = title_element.text

            content_elements = browser.find_elements(By.TAG_NAME, 'p')
            content = [element.text for element in content_elements if not element.get_attribute('class') and element.text.strip()]
            content = ''.join(content)

            date_element = browser.find_element(By.TAG_NAME, 'time')

            date_obj = datetime.strptime(date_element.text, "%B %d, %Y %I:%M %p")
            date = date_obj.strftime("%Y-%m-%d")

            url = browser.current_url

            new_data = {'title': title, 'content': content, 'category': '뉴스', 'date': date, 'url': url, 'keywords': ''}
            data.append(new_data)

            browser.back()
            print(len(data))
            time.sleep(0.5)


    except Exception as e:
        print(f"Error occurred on page {page_num} {title} : {e}")
        # 오류 발생 시에도 중간 데이터를 저장
        with open(json_file_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=4)
        continue


browser.quit()


with open(json_file_path, 'w', encoding='utf-8') as f:
    json.dump(data, f, ensure_ascii=False, indent=4)