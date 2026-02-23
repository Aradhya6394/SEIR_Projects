import sys
import requests
import re
from bs4 import BeautifulSoup


# Function to get text from website body
def get_body(url):
    res = requests.get(url)                                        # send request to website
    page = BeautifulSoup(res.text, "html.parser")                  # parse HTML

    if page.body:                                                  # check if body exists
        return page.body.get_text().lower()                        # return body text in lowercase
    return ""


# Function to count frequency of words
def word_count(text):
    words = re.findall(r"[a-z0-9]+", text)                       # extract only alphanumeric words 
    data = {}

    for w in words:
        data[w] = data.get(w, 0) + 1                                

    return data


# Function to create 64-bit polynomial hash of a word
def poly_hash(word):
    p = 53
    mod = 2**64
    h = 0
    power = 1

    for ch in word:
        h = (h + ord(ch) * power) % mod                                # add character value
        power = (power * p) % mod                                      # increase power of p

    return h


# Function to build simhash from word frequencies
def make_hash(freq):
    vec = [0] * 64 

    for w, c in freq.items():
        h = poly_hash(w)                                                   # get hash of word

        for i in range(64):
            if (h >> i) & 1:
                vec[i] += c                                       # add frequency if bit is 1
            else:
                vec[i] -= c                                       # subtract frequency if bit is 0

    final = 0
    for i in range(64):
        if vec[i] > 0:
            final |= (1 << i)                                        # set bit to 1

    return final


# Function to count matching bits between two simhashes
def match_bits(h1, h2):
    x = h1 ^ h2  
    return 64 - bin(x).count("1")                                            

# Check if user gives two URLs
if len(sys.argv) != 3:
    print("Usage: python Assignment2.py <URL1> <URL2>")
    sys.exit()

u1 = sys.argv[1]
u2 = sys.argv[2]

# Get text from both websites
t1 = get_body(u1)
t2 = get_body(u2)

# Count word frequency
f1 = word_count(t1)
f2 = word_count(t2)

# Print word frequencies
print("\nWord Frequency for URL1:\n")
for w, c in f1.items():
    print(w, ":", c)

print("\nWord Frequency for URL2:\n")
for w, c in f2.items():
    print(w, ":", c)

# Create simhash for both
h1 = make_hash(f1)
h2 = make_hash(f2)

# Print simhash values
print("\nSimhash for URL1:", h1)
print("Simhash for URL2:", h2)

# Print number of common bits
print("\nCommon bits:", match_bits(h1, h2))