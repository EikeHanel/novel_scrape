from ebooklib import epub


def create_epub(title, description, url):
    """Creates an initial EPUB file with metadata."""
    book = epub.EpubBook()
    book.set_identifier(url)
    book.set_title(title)
    book.set_language("en")
    book.add_metadata("DC", "description", description)

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

    # add css file
    nav_css = epub.EpubItem(uid="style_nav", file_name="style/nav.css", media_type="text/css", content=style)
    book.add_item(nav_css)

    # Initialize the spine with the nav file (toc.ncx and nav.xhtml should always be in the spine)
    book.spine = ["nav"]

    book.add_item(epub.EpubNcx())
    book.add_item(epub.EpubNav())
    # Save the empty book
    epub.write_epub(title + ".epub", book, {})
    return title + ".epub"


def add_chapter(file, chapter_title, chapter_content):
    """Adds a chapter to an existing EPUB file."""
    book = epub.read_epub(file)
    print(book)
    # Create a new chapter
    c1 = epub.EpubHtml(title=chapter_title, file_name=f"{chapter_title}.xhtml", lang="en")
    c1.content = f"<html><h1>{chapter_title}</h1>\n{chapter_content}</html>"

    # Add the chapter to the book
    book.add_item(c1)
    try:
        nav_len = len(book.toc)
        book.toc = (book.toc[0], c1)
    except TypeError:
        book.toc = (c1,)
    if not book.toc:
        print("ok")
    # Add the TOC file and update the spine
    # book.add_item(epub.EpubNcx())  # You should always include a TOC file (toc.ncx)
    # book.add_item(epub.EpubNav())  # Ensure nav.xhtml exists

    # Save the updated EPUB
    epub.write_epub(file, book, {})
