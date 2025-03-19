from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup

# from fake_useragent import UserAgent 


# PATH ="C:/my/path/to/chromedriver.exe"

# ua = UserAgent()
# userAgent = ua.random
# print(userAgent)

options = Options()
# options.add_argument(f'user-agent={userAgent}')
options.add_experimental_option("detach", True)

driver = webdriver.Chrome(options=options) # , executable_path=PATH

driver.get("https://www.royalroad.com/fiction/26675/a-journey-of-black-and-red")

# Get Title and Description

title = driver.find_element(By.CSS_SELECTOR, "div>h1").text
# print(title)
description = []
description.append(driver.find_element(By.XPATH, "/html/body/div[3]/div/div/div/div[1]/div/div[2]/div/div[2]/div[1]/div[2]/div[3]/div/div/div/div/div/div[1]").text)
description.append(driver.find_element(By.XPATH, "/html/body/div[3]/div/div/div/div[1]/div/div[2]/div/div[2]/div[1]/div[2]/div[3]/div/div/div/div/div/div[4]").text)

# print(description)

# Select First Chapter
wait = WebDriverWait(driver, 10)
first_chapter = wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@id="chapters"]/tbody/tr[1]/td[1]')))
first_chapter.click()


chapter = driver.find_element(By.XPATH, '/html/body/div[3]/div/div/div/div/div[2]/div[2]/div[3]')
chapter = chapter.get_attribute("outerHTML")

soup = BeautifulSoup(chapter, 'html.parser')
print(soup)
filtered_paragraphs = []

for p in soup.find_all('p'):
    new_p = BeautifulSoup('<p></p>', 'html.parser').p
    new_p.extend(p.find_all(string=True, recursive=True))  # keeps bold and cursive
    p.replace_with(new_p)


print(soup)
# This gives the exact html. Needs to be cleaned so it will work for epub creation