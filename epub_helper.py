from ebooklib import epub


def create_epub(title, description, url):
    """Creates an initial EPUB file with metadata."""
    book = epub.EpubBook()
    book.set_identifier(url)
    book.set_title(title)
    book.set_language("en")
    book.add_metadata("DC", "description", description)

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

    # Create a new chapter
    chapter = epub.EpubHtml(title=chapter_title, file_name=f"{chapter_title}.xhtml", lang="en")
    chapter.content = f"<h1>{chapter_title}</h1>\n{chapter_content}"

    # Add the chapter to the book
    book.add_item(chapter)

    # Add toc.ncx and nav.xhtml to ensure they are included in the spine and TOC
    if "nav" not in book.spine:
        book.spine = ["nav"]  # Ensure nav file is included in spine
    book.spine.append(chapter)  # Add the new chapter to the spine

    # Add the TOC file and update the spine
    book.add_item(epub.EpubNcx())  # You should always include a TOC file (toc.ncx)
    book.add_item(epub.EpubNav())  # Ensure nav.xhtml exists

    # Save the updated EPUB
    epub.write_epub(file, book, {})
