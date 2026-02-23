import sys
import requests
from bs4 import BeautifulSoup


def find_page(url):
    try:
        response = requests.get(url)
    except:
        print("Unable to open the page")
        return

    soup = BeautifulSoup(response.text, "html.parser")

    # Print title
    print("Title:")
    if soup.title:
        print(soup.title.string)
    else:
        print("No title found")
    print()

    # Print body text
    print("Body:")
    if soup.body:
        print(soup.body.get_text())
    else:
        print("No body found")
    print()

    # Print all links
    print("Links:")
    links = soup.find_all("a")
    for link in links:
        href = link.get("href")
        if href:
            print(href)


if len(sys.argv) < 2:
    print("Usage: python Assignment1.py <URL>")
else:
    find_page(sys.argv[1])