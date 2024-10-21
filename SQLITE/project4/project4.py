import pandas as pd
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
import time
import sqlite3
import re

# 0. Tạo cơ sở dữ liệu
conn = sqlite3.connect('musicians.db')
c = conn.cursor()
try:
    c.execute('''CREATE TABLE IF NOT EXISTS musician (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name_of_band TEXT,
                    year_active TEXT)''')
except Exception as e:
    print(e)

def them(name_of_band, year_active):
    conn = sqlite3.connect('musicians.db')
    c = conn.cursor()
    # Thêm vào cơ sở dữ liệu
    c.execute('''  
            INSERT INTO musician(name_of_band, year_active) 
            VALUES (:name, :year)
    ''',
              {'name' : name_of_band,
               'year_active' : year_active,
              })
    conn.commit()
    conn.close()

# Khởi tạo webdriver
chrome_path = r"C:/Users/Loc/Desktop/SQLITE/project3/chromedriver.exe"
ser = Service(chrome_path)
driver = webdriver.Chrome(service=ser)
options = webdriver.ChromeOptions()
options.headless = False

url = 'https://en.wikipedia.org/wiki/Lists_of_musicians#A'
driver.get(url)
time.sleep(2)

# Lấy ra tất cả các thẻ ul
ul_tag = driver.find_elements(By.TAG_NAME, 'ul')
ul_musicians = ul_tag[21]
li_tags = ul_musicians.find_elements(By.TAG_NAME, 'li')

link1 = []
link2 = []

# Lấy các đường dẫn từ các thẻ li
for tag in li_tags:
    try:
        link1.append(tag.find_element(By.TAG_NAME, 'a').get_attribute('href'))
    except Exception as e:
        print(f"Error getting link: {e}")

# Lấy danh sách ban nhạc từ trang đầu tiên
driver.get(link1[0])
time.sleep(2)

# Lấy list ban nhạc
ul_tag2 = driver.find_elements(By.TAG_NAME, 'ul')
ul_bannhac = ul_tag2[24]
li_tags2 = ul_bannhac.find_elements(By.TAG_NAME, 'li')

# Lấy các đường dẫn của các ban nhạc
for tag2 in li_tags2:
    try:
        link2.append(tag2.find_element(By.TAG_NAME, 'a').get_attribute('href'))
    except Exception as e:
        print(f"Error getting band link: {e}")

# Danh sách để lưu dữ liệu các ban nhạc
musicians_data = []

# Lấy thông tin từng ban nhạc
for l2 in link2:
    try:
        driver.get(l2)
        time.sleep(2)

        # Trích xuất tên ban nhạc
        try:
            name = driver.find_element(By.TAG_NAME, 'h1').text
        except Exception as e:
            name = ""
            print(f"Error getting band name: {e}")

        # Lấy năm hoạt động
        try:
            year_element = driver.find_element(By.XPATH, "//th[.//span[text()='Years active']]/following-sibling::td")
            year = year_element.text
        except Exception as e:
            year = ""
            print(f"Error getting year active: {e}")

        # Thêm thông tin vào danh sách và lưu vào cơ sở dữ liệu
        them(name, year)

    except Exception as e:
        print(f"Error processing {l2}: {e}")

# Đóng web driver
driver.quit()

# Truy vấn cơ bản
# Kết nối đến cơ sở dữ liệu
conn = sqlite3.connect('musicians.db')
c = conn.cursor()

# 1. Truy vấn để lấy tất cả các ban nhạc
print("Tất cả ban nhạc:")
try:
    c.execute("SELECT * FROM musician")
    rows = c.fetchall()  # Lấy tất cả các bản ghi
    for row in rows:
        print(row)
except sqlite3.OperationalError as e:
    print(f"Error querying table: {e}")

# Đóng kết nối
conn.close()
