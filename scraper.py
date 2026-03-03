import sys
import requests
from bs4 import BeautifulSoup

def open_website(link):
    try:
        my_header = {
            "User-Agent": "Mozilla/5.0"
        }
        page_data = requests.get(link, headers=my_header, timeout=5)
        if page_data.status_code != 200:
            print("Website could not be opened.")
            print("Status Code:", page_data.status_code)
            return
    except Exception as error:
        print("Something went wrong:", error)
        return
    parsed_page = BeautifulSoup(page_data.text, "html.parser")

    print("\nPAGE TITLE")
    if parsed_page.title:
        print(parsed_page.title.text.strip())
    else:
        print("Title not available")

    print("\nPAGE CONTENT")
    if parsed_page.body:
        print(parsed_page.body.get_text().strip())
    else:
        print("No content found")

    print("\nALL LINKS")
    all_links = parsed_page.find_all("a")

    if len(all_links) > 0:
        for item in all_links:
            url_link = item.get("href")
            if url_link:
                print(url_link)
    else:
        print("No links found on this page")
if len(sys.argv) < 2:
    print("Please provide a URL.")
    print("Example: python scraper.py https://example.com")
else:
    user_link = sys.argv[1]
    open_website(user_link)