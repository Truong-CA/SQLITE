
import pandas as pd
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.common.by import By
import time
import re
import sqlite3



######################
# tạo cơ sở dữ liệu
conn = sqlite3.connect('musicians.db')
c = conn.cursor()
try:
    c.execute('''
        CREATE TABLE musicians (
            id integer primary key autoincrement,
            name text,
            year_element text,
        )
    ''')
except Exception as e:
    print(e)

def them(name,year_element):
    conn = sqlite3.connect('musicians.db')
    c = conn.cursor()
    # Them vao co so du lieu
    c.execute('''
        INSERT INTO musicians (name, year_element)
        VALUE (:name, : year_element)
        ''',
        {
             'name':name,
             'year_element': year_element
        })
    conn.commit()
    conn.close()

#########################
# Khởi tạo webdriver
# tạo đường dẫn file thực thi geckodriver
gecko_path = r"C:/Users/Loc/Desktop/SQL_Lite/project4/geckodriver.exe"

# Khởi tạo đối tượng dịch vụ
ser = Service(gecko_path)

# Tạo tùy chọn option
options = Options()
options.binary_location ="C:/Program Files/Mozilla Firefox/firefox.exe"
# Thiết lập firefox chỉ hiện thị giao diện
options.headless = False

driver = webdriver.Firefox()

url = 'https://en.wikipedia.org/wiki/Lists_of_musicians#A'
driver.get(url)
time.sleep(2)

# Lấy ra tất cả các thẻ ul
ul_tag = driver.find_elements(By.TAG_NAME, 'ul')
# Chọn thẻ ul thứ 21
ul_musicians = ul_tag[21]

li_tags = ul_musicians.find_elements(By.TAG_NAME, 'li')

link1 = []
link2 = []

# Lấy các đường dẫn từ các thẻ li
for tag in li_tags:
    try:
        link1.append(tag.find_element(By.TAG_NAME, 'a').get_attribute('href'))
    except:
        pass

# In ra các đường dẫn
for l in link1:
    print(l)

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
    except:
        pass

# Danh sách để lưu dữ liệu các ban nhạc
musicians_data = []

# Lấy thông tin từng ban nhạc
count =0;
for l2 in link2:
    if (count >50):
        break
    count = count+1;

    print(link1)
    try:
        driver.get(l2)
        time.sleep(2)

        # Trích xuất tên ban nhạc
        try:
            name = driver.find_element(By.TAG_NAME, 'h1').text
        except:
            name = ""

        # Lấy năm hoạt động
        try:
            year_element = driver.find_element(By.XPATH, "//th[.//span[text()='Years active']]/following-sibling::td")
            year = year_element.text
        except:
            year = ""

        # tham tt vaào hàm def them

        them(name, year)

        # đóng web driver
        driver.quit()



    except Exception as e:
        print(f"Error processing {l2}: {e}")





