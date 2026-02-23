import sys
import requests
import re
from bs4 import BeautifulSoup

# Get page body text
def get_body(url):
    try:
        res = requests.get(url)
        res.raise_for_status()   # check if request successful
        page = BeautifulSoup(res.text, "html.parser")

        if page.body:
            return page.body.get_text().lower()
        return ""
    except requests.exceptions.RequestException as e:
        print("Error fetching URL:", e)
        sys.exit(1)

# Count words
def word_count(text):
    words = re.findall(r"[a-z0-9]+", text)
    data = {}

    for w in words:
        data[w] = data.get(w, 0) + 1

    return data

# 64-bit hash
def poly_hash(word):
    p = 53
    mod = 2**64
    h = 0
    power = 1

    for ch in word:
        h = (h + ord(ch) * power) % mod
        power = (power * p) % mod

    return h

if len(sys.argv) != 2:
    print("Usage: python script.py <url>")
    sys.exit(1)

url = sys.argv[1]

text = get_body(url)
freq = word_count(text)

# Print word frequencies
for word, count in freq.items():
    print(word, ":", count)

'''At this stage, I have not been able to complete the remaining sections:
- Generating the Simhash for the document.
- Comparing the Simhash values of two different URLs.
- Calculating how many bits are common between them.'''
