from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
import re
import time
import sqlite3

######################################################
# 0. Tạo cơ sở dữ liệu
conn = sqlite3.connect('painters.db')
c = conn.cursor()
try:
    c.execute('''
        CREATE TABLE painter (
            id integer primary key autoincrement,
            name text,
            birth text,
            death text,
            nationality text
        )
    ''')
except Exception as e:
    print(e)

def them(name, birth, death, nationality):
    conn = sqlite3.connect('painters.db')
    c = conn.cursor()
    # Thêm vào cơ sở dữ liệu
    c.execute('''
        INSERT INTO painter(name, birth, death, nationality)
        VALUES (:name, :birth, :death, :nationality)
    ''',
      {
          'name': name,
          'birth': birth,
          'death': death,
          'nationality': nationality,
      })
    conn.commit()
    conn.close()

######################################################
# I. Tạo danh sách chứa links
all_links = []

######################################################
# II. Lấy ra tất cả đường dẫn để truy cập đến các họa sĩ
# Khởi tạo Webdriver

# Đường dẫn đến file thực thi chromedriver
chrome_path = r"C:/Users/Loc/Desktop/SQLITE/project3/chromedriver.exe"

# Khởi tạo đối tượng dịch vụ với đường dẫn đến chromedriver
ser = Service(chrome_path)

# Tạo tùy chọn cho Chrome
options = webdriver.ChromeOptions()
options.headless = False  # Thiết lập để hiện thị giao diện

for i in range(70, 71):
    # Khởi tạo driver
    driver = webdriver.Chrome(service=ser, options=options)
    url = "https://en.wikipedia.org/wiki/List_of_painters_by_name_beginning_with_%22" + chr(i) + "%22"
    try:
        # Mở trang
        driver.get(url)

        # Đợi một chút để trang tải
        time.sleep(3)

        # Lấy ra tất cả các thẻ ul
        ul_tags = driver.find_elements(By.TAG_NAME, "ul")
        print(len(ul_tags))

        # Chọn thẻ ul thứ 21
        ul_painters = ul_tags[20]  # list start with index=0

        # Lấy ra tất cả các thẻ <li> thuộc ul_painters
        li_tags = ul_painters.find_elements(By.TAG_NAME, "li")

        # Tạo danh sách các URL
        links = [tag.find_element(By.TAG_NAME, "a").get_attribute("href") for tag in li_tags]
        for x in links:
            all_links.append(x)
    except Exception as e:
        print(f"Error while getting links: {e}")

    # Đóng web driver
    driver.quit()

######################################################
# III. Lấy thông tin của từng họa sĩ
count = 0
for link in all_links:
    if count > 3:  # Giới hạn lấy thông tin của 4 họa sĩ
        break
    count += 1

    print(link)
    try:
        # Khởi tạo webdriver
        driver = webdriver.Chrome(service=ser, options=options)
        # Mở trang
        url = link
        driver.get(url)

        # Đợi 2 giây
        time.sleep(2)

        # Lấy tên họa sĩ
        try:
            name = driver.find_element(By.TAG_NAME, "h1").text
        except:
            name = ""

        # Lấy ngày sinh
        try:
            birth_element = driver.find_element(By.XPATH, "//th[text()='Born']/following-sibling::td")
            birth = birth_element.text
            birth = re.findall(r'[0-9]{1,2} +\s+[A-Za-z]+ +[0-9]{4}', birth)
            birth = birth[0] if birth else ""  # Lấy kết quả đầu tiên nếu có
        except:
            birth = ""

        # Lấy ngày mất
        try:
            death_element = driver.find_element(By.XPATH, "//th[text()='Died']/following-sibling::td")
            death = death_element.text
            death = re.findall(r'[0-9]{1,2} +\s+[A-Za-z]+ +[0-9]{4}', death)
            death = death[0] if death else ""  # Lấy kết quả đầu tiên nếu có
        except:
            death = ""

        # Lấy quốc tịch
        try:
            nationality_element = driver.find_element(By.XPATH, "//th[text()='Nationality']/following-sibling::td")
            nationality = nationality_element.text
        except:
            nationality = ""

        # Thêm thông tin vào cơ sở dữ liệu
        them(name, birth, death, nationality)

        # Đóng web driver
        driver.quit()
    except Exception as e:
        print(f"Error processing {link}: {e}")

# truy vấn cơ bản
# Kết nối đến cơ sở dữ liệu
conn = sqlite3.connect('painters.db')
c = conn.cursor()

# 1. Truy vấn để lấy tất cả các họa sĩ
print("Tất cả họa sĩ:")
c.execute("SELECT * FROM painter")
rows = c.fetchall()  # Lấy tất cả các bản ghi
for row in rows:
    print(row)
#2


# Đóng kết nối cơ sở dữ liệu
conn.close()


