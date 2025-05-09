from ebooklib import epub
import re
import os
import requests
import time


class CreateEpub:
    def __init__(self, title, author, cover_url, description, url, save_path):
        """
        Initialize an EPUB book with metadata.
        """
        self.book = epub.EpubBook()
        self.book.set_identifier(url)
        self.book.set_title(title)
        self.book.set_language("en")
        self.book.add_author(author)
        self.book.add_metadata("DC", "description", description)
        self.title = title

        safe_title = re.sub(r'[^\w\s-]', '', title).strip().replace(" ", "_")
        self.save_path = os.path.join(save_path, safe_title)
        os.makedirs(self.save_path, exist_ok=True)
        if cover_url:
            self.add_cover_page(cover_url)

        # Default CSS
        style = '''
        @namespace epub "http://www.idpf.org/2007/ops";
        body {
            font-family: Cambria, Liberation Serif, Bitstream Vera Serif, Georgia, Times, Times New Roman, serif;
        }
        h2 {
             text-align: left;
             text-transform: uppercase;
             font-weight: 200;     
        }
        ol {
                list-style-type: none;
        }
        ol > li:first-child {
                margin-top: 0.3em;
        }
        nav[epub|type~='toc'] > ol > li > ol  {
            list-style-type:square;
        }
        nav[epub|type~='toc'] > ol > li > ol > li {
                margin-top: 0.3em;
        }
        '''

        nav_css = epub.EpubItem(uid="style_nav", file_name="style/nav.css", media_type="text/css", content=style)
        self.book.add_item(nav_css)

        # Initialize spine and TOC
        self.book.spine = ["nav"]
        self.book.toc = []

        self.book.add_item(epub.EpubNcx())
        self.book.add_item(epub.EpubNav())

    def add_cover_page(self, cover_url):
        response = requests.get(cover_url)
        time.sleep(2)
        if response.status_code == 200:
            cover_path = os.path.join(self.save_path, "cover.jpg")
            with open(cover_path, "wb") as file:
                file.write(response.content)
        else:
            return

        with open(cover_path, "rb") as cover_file:
            self.book.set_cover(file_name="cover.jpg", content=cover_file.read())

    def add_chapter(self, chapter_title, chapter_content):
        """
        Adds a chapter to the EPUB book.
        """
        chapter = epub.EpubHtml(title=chapter_title, file_name=f"{chapter_title}.xhtml", lang="en")
        chapter.content = f"""
        <html>
            <head>
                <title>{chapter_title}</title>
            </head>
            <body>
                <h2>{chapter_title}</h2>
                {chapter_content}
            </body>
        </html>
        """

        self.book.add_item(chapter)
        self.book.toc.append(chapter)
        self.book.spine.append(chapter)

    def save(self):
        """
        Saves the EPUB file to disk.
        """
        filename = self.title
        filename = re.sub(r'[^\w\s-]', '', filename).strip().replace(" ", "_")
        full_path = os.path.join(self.save_path, filename + ".epub")
        epub.write_epub(full_path, self.book, {})

