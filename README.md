# RoyalRoad Scraper to EPUB Converter

## Overview
This script scrapes a novel from [Royal Road](https://www.royalroad.com/) and converts it into an **EPUB** file for offline reading. Using **Selenium** and **BeautifulSoup**, the script extracts chapter content, metadata (title, author, cover, description), and compiles them into a structured eBook format using **EbookLib**.

## Features
- **Scrapes novels from Royal Road** and extracts all chapters.
- **Creates an EPUB file** with metadata, a cover, and formatted content.
- **Automatically navigates** through chapters.
- **Saves EPUB in a structured format** under a specified directory.

## Installation
### Prerequisites
Ensure you have the following installed:
- **Python 3.8+**
- **Google Chrome** (for Selenium WebDriver)
- **ChromeDriver** (Ensure it matches your Chrome version)

### Install Dependencies
```bash
pip install -r requirements.txt
```

## Usage
1. **Run the script:**
   ```bash
   python main.py
   ```
2. The EPUB file will be saved in the `Novels` directory within the current working directory.

## Project Structure
```
📂 Your Repository
│── main.py              # Main script for scraping and EPUB creation
│── epub_helper.py       # Helper module for EPUB creation
│── requirements.txt     # Dependencies list
│── README.md            # Documentation
```

## Configuration
- The script currently scrapes **"The Perfect Run"** from Royal Road.
- To scrape a different novel, update the **`royal_road_novel`** variable in `main.py` with the desired URL.

## Dependencies
The script uses the following Python libraries:
- `selenium` – For browser automation
- `beautifulsoup4` – For parsing HTML content
- `EbookLib` – For EPUB creation
- `requests` – For fetching cover images

## Legal & Ethical Considerations
⚠ **Web Scraping for Personal Use Only!**
- This script is intended for **personal use only**.
- Do **not** redistribute or use scraped content for commercial purposes.
- Scraping should be performed **ethically**, respecting Royal Road's **terms of service**.
- The script may stop working if Royal Road updates its website structure.

## Disclaimer
By using this script, you **assume full responsibility** for compliance with applicable laws and terms of service. The author is **not liable** for any misuse or legal consequences.

---

### Contributions
Feel free to **fork and modify** the script. Pull requests are welcome for improvements and bug fixes!

### License
This project is licensed under the **MIT License**. See `LICENSE` for details.

