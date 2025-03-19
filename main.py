from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
from epub_helper import create_epub, add_chapter

options = Options()
options.add_experimental_option("detach", True)

# Connect to royal road webpage:
royal_road_novel = "https://www.royalroad.com/fiction/26675/a-journey-of-black-and-red"
driver = webdriver.Chrome(options=options)
driver.get(royal_road_novel)

# Get Title and Description
title = driver.find_element(By.CSS_SELECTOR, "div>h1").text
description_lst = [driver.find_element(By.XPATH,
                                       "/html/body/div[3]/div/div/div/div[1]/div/div[2]/div/div[2]/div[1]/div[2]/div["
                                       "3]/div/div/div/div/div/div[1]").text,
                   driver.find_element(By.XPATH,
                                       "/html/body/div[3]/div/div/div/div[1]/div/div[2]/div/div[2]/div[1]/div[2]/div["
                                       "3]/div/div/div/div/div/div[4]").text]
description = " ".join(description_lst)

# Create epub with title and description:
ebook_name = create_epub(title=title, description=description, url=royal_road_novel)

# Select First Chapter
wait = WebDriverWait(driver, 10)
first_chapter = wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@id="chapters"]/tbody/tr[1]/td[1]')))
first_chapter.click()

chapter_title = driver.find_element(By.CSS_SELECTOR, "div>h1").text
chapter = driver.find_element(By.XPATH, '/html/body/div[3]/div/div/div/div/div[2]/div[2]/div[3]')
chapter = chapter.get_attribute("outerHTML")

soup = BeautifulSoup(chapter, 'html.parser')
for p in soup.find_all('p'):
    new_p = BeautifulSoup('<p></p>', 'html.parser').p
    new_p.extend(p.find_all(string=True, recursive=True))  # keeps bold and cursive
    p.replace_with(new_p)
# Adding chapter to ebook
add_chapter(file=ebook_name, chapter_title=chapter_title, chapter_content=str(soup))


#   prints the <div> with cleaned <p>
#   get all chapters?
#   get structure of epub and make it so i can add content!
#       add all chapters in one operation
#   OR
#       add chapter per chapter to the epub
#   save or look into converting the epub into mobi
