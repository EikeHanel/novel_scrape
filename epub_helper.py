from ebooklib import epub


class CreateEpub:
    def __init__(self, title, author, cover_path, description, url):
        """
        Initialize an EPUB book with metadata.
        """
        self.book = epub.EpubBook()
        self.book.set_identifier(url)
        self.book.set_title(title)
        self.book.set_language("en")
        if cover_path:
            self.add_cover_page(cover_path)
        self.book.add_author(author)
        self.book.add_metadata("DC", "description", description)

        self.title = title

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

    def add_cover_page(self, cover_path):
        with open(cover_path, "rb") as cover_file:
            self.book.set_cover(file_name="cover.jpg", content=cover_file.read())
        cover_page = epub.EpubHtml(title="Cover", file_name="cover.xhtml", lang="en")
        cover_page.content = f'''
            <html>
                <head>
                    <title>Cover</title>
                </head>
                <body>
                    <img src="cover.jpg" alt="Cover Image" style="width:100%;"/>
                </body>
            </html>
            '''
        self.book.add_item(cover_page)
        self.book.spine.insert(0, cover_page)

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

    def save(self, filename=None):
        """
        Saves the EPUB file to disk.
        """
        if filename is None:
            filename = self.title + ".epub"
        epub.write_epub(filename, self.book, {})
        return filename

