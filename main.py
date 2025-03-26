from selenium import webdriver
from selenium.common import NoSuchElementException
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
from epub_helper import CreateEpub
import re
import os


def main():
    """
        Scrapes a novel from Royal Road and converts it into an EPUB file.
    """
    save_path = os.getcwd() + "/Novels"
    royal_road_novel = "https://www.royalroad.com/fiction/36735/the-perfect-run"

    options = Options()
    options.add_experimental_option("detach", True)

    # Connect to royal road webpage:
    driver = webdriver.Chrome(options=options)
    driver.get(royal_road_novel)

    # PopUp
    wait = WebDriverWait(driver, 10)
    pop_up = wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@id="ncmp__tool"]/div/div/div[3]/div[1]/button[2]')))
    pop_up.click()

    # Title & Author
    title = driver.find_element(By.CSS_SELECTOR, "div>h1").text
    title = re.sub(r'[^\w\s]', '', title)
    author = driver.find_element(By.CSS_SELECTOR, "div>h4>span>a").text

    # Cover
    cover_url = driver.find_element(By.CSS_SELECTOR, 'div>img').get_attribute("src")

    # Description
    description = driver.find_element(By.CLASS_NAME, "description")
    description = description.get_attribute("textContent")

    # Create epub with title and description:
    my_book = CreateEpub(title=title, author=author, cover_url=cover_url,
                         description=description, url=royal_road_novel, save_path=save_path)

    # Select First Chapter
    first_chapter = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, '.btn.btn-lg.btn-primary')))
    first_chapter.click()

    # # One Chapter - Use for Bug-tests
    # chapter_title, text = copy_chapter(driver)
    # print(text)
    # my_book.add_chapter(chapter_title, text)
    # driver.quit()
    # my_book.save()

    # ALL CHAPTERS
    while True:
        wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, 'div>.chapter-inner.chapter-content')))
        chapter_title, text = copy_chapter(driver)
        my_book.add_chapter(chapter_title, text)
        if not next_chapter(driver):
            break
    my_book.save()
    driver.quit()


def copy_chapter(driver):
    """
        Extracts the current chapter's title and content from the webpage.

    Args:
        driver (webdriver): The Selenium WebDriver instance.

    Returns:
        tuple: A tuple containing the chapter title (str) and cleaned HTML content (str).
    """
    chapter_title = driver.find_element(By.CSS_SELECTOR, "div>h1").text
    chapter_title = re.sub(r'[^\w\s]', '', chapter_title)
    chapter = driver.find_element(By.CSS_SELECTOR, 'div>.chapter-inner.chapter-content')
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

    try:
        btn_next_chapter = wait.until(EC.presence_of_element_located(
            (By.XPATH, "//a[contains(text(),'Next')] "
                       " | "
                       "/html/body/div[3]/div/div/div/div/div[2]/div[2]/div[1]/div[2]/button")
        ))
        if btn_next_chapter.tag_name == "button":
            print("Reached the last chapter.")
            return False
        btn_next_chapter.click()
        return True
    except NoSuchElementException:
        print("No more chapters")
        return False


if __name__ == "__main__":
    main()
