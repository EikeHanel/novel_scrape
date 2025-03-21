from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
from epub_helper import create_epub, add_chapter


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
    
    # check with small novel first just a few chapters!!!
    
    while True:
        chapter_title, text = copy_chapter(driver)
        add_chapter(file=ebook_name, chapter_title=chapter_title, chapter_content=text)
        new_chapter = next_chapter()
        if not new_chapter:
            break


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
    # Does not keep <strong></strong> and <i></i> or <em></em>
    for p in soup.find_all('p'):
        new_p = BeautifulSoup('<p></p>', 'html.parser').p
        
        # NOT TESTED YET
        # different way to save <stong> etc.
        
        for content in p.contents:
            if content.name in ["strong", "i", "em"]:
                new_p.append(content)
            else:
                new_p.append(str(content))
        
        # new_p.extend(p.find_all(string=True, recursive=True))
        p.replace_with(new_p)
    return (chapter_title, str(soup))


def next_chapter(driver):
    """
        Clicks the 'Next Chapter' button to navigate to the next chapter.

    Args:
        driver (webdriver): The Selenium WebDriver instance.

    Returns:
        bool: True if navigation was successful, False if there are no more chapters.
    """
    wait = WebDriverWait(driver, 10)
    next_chapter = wait.until(EC.element_to_be_clickable((By.XPATH, '/html/body/div[3]/div/div/div/div/div[2]/div[2]/div[1]/div[2]/a')))
    if next_chapter.get_attribute("disabled") == "disabled":
        return False
    next_chapter.click()
    return True


if __name__ == "__main__":
    main()