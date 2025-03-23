from selenium import webdriver
from selenium.common import NoSuchElementException
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
import requests
from epub_helper import CreateEpub
import re
import time


def main():
    """
        Scrapes a novel from Royal Road and converts it into an EPUB file.
    """
    options = Options()
    options.add_experimental_option("detach", True)

    # Connect to royal road webpage:
    # Replace royal_road_novel with the novel you want to "download" and convert to epub
    royal_road_novel = "https://www.royalroad.com/fiction/26675/a-journey-of-black-and-red"
    driver = webdriver.Chrome(options=options)
    driver.get(royal_road_novel)

    # Title & Author
    title = driver.find_element(By.CSS_SELECTOR, "div>h1").text
    title = re.sub(r'[^\w\s]', '', title)
    author = driver.find_element(By.CSS_SELECTOR, "div>h4>span>a").text

    # Cover
    cover_url = driver.find_element(By.CSS_SELECTOR, 'div>img').get_attribute("src")
    response = requests.get(cover_url)
    time.sleep(2)
    if response.status_code == 200:
        cover_path = f"{title}.jpg"
        with open(cover_path, "wb") as file:
            file.write(response.content)
    else:
        cover_path = False

    # Description
    description = driver.find_element(By.CLASS_NAME, "description")
    description = description.get_attribute("textContent")

    # Create epub with title and description:
    my_book = CreateEpub(title=title, author=author, cover_path=cover_path,
                         description=description, url=royal_road_novel)

    # Select First Chapter
    wait = WebDriverWait(driver, 10)
    first_chapter = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, '.btn.btn-lg.btn-primary')))
    first_chapter.click()

    # One Chapter
    chapter_title, text = copy_chapter(driver)
    my_book.add_chapter(chapter_title, text)
    driver.quit()
    my_book.save()

    # ALL CHAPTERS
    # while True:
    #     time.sleep(2)
    #     chapter_title, text = copy_chapter(driver)
    #     my_book.add_chapter(chapter_title, text)
    #     # add_chapter(file=ebook_name, chapter_title=chapter_title, chapter_content=text)
    #     if not next_chapter(driver):
    #         break
    # my_book.save()
    # driver.quit()


def copy_chapter(driver):
    """
        Extracts the current chapter's title and content from the webpage.

    Args:
        driver (webdriver): The Selenium WebDriver instance.

    Returns:
        tuple: A tuple containing the chapter title (str) and cleaned HTML content (str).
    """
    chapter_title = driver.find_element(By.CSS_SELECTOR, "div>h1").text
    chapter = driver.find_element(By.XPATH, '/html/body/div[3]/div/div/div/div/div[2]/div[2]/div[3]')
    chapter = chapter.get_attribute("outerHTML")

    soup = BeautifulSoup(chapter, 'html.parser')
    chapter_content = []
    for p in soup.find_all('p'):
        chapter_content.append("<p>" + "".join(str(item) for item in p.contents) + "</p>")

    return chapter_title, " ".join(chapter_content)


def next_chapter(driver):
    """
        Clicks the 'Next Chapter' button to navigate to the next chapter.

    Args:
        driver (webdriver): The Selenium WebDriver instance.

    Returns:
        bool: True if navigation was successful, False if there are no more chapters.
    """
    wait = WebDriverWait(driver, 10)
    btn_next_chapter = wait.until(EC.presence_of_element_located((By.XPATH, '/html/body/div[3]/div/div/div/div/div['
                                                                            '2]/div[2]/div[1]/div[2]')))
    try:
        btn_next_chapter = btn_next_chapter.find_element(By.TAG_NAME, "a")
        btn_next_chapter.click()
        return True
    except NoSuchElementException:
        print("No more chapters")
        return False


if __name__ == "__main__":
    main()
