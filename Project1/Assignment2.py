import sys   # for taking input from command line
import requests   # for opening website
from bs4 import BeautifulSoup   # for reading html
import re   # for finding words


# function for polynomial hash of word
def hash_word(word):
    p = 53   
    mod = 2**64  
    value = 0
    for i in range(len(word)):
        value = (value + ord(word[i]) * (p ** i)) % mod

    return value
# function to make simhash from url
def simhash_from_url(url):
    response = requests.get(url)   # get webpage
    soup = BeautifulSoup(response.text, "html.parser")   # parse html
    text = soup.body.get_text().lower()   # take body text and make lowercase
    words = re.findall(r"[a-z0-9]+", text)   # take only alphanumeric words
    freq = {}   # dictionary for word frequency
    # count words
    for w in words:
        if w in freq:
            freq[w] += 1
        else:
            freq[w] = 1
    bits = [0] * 64   # list for 64 bits
    # make vector
    for word in freq:
        h = hash_word(word)   # hash of word
        for i in range(64):
            if (h >> i) & 1:
                bits[i] += freq[word]   # add if bit is 1
            else:
                bits[i] -= freq[word]   # subtract if bit is 0

    final_hash = 0
    for i in range(64):
        if bits[i] > 0:
            final_hash += (1 << i)

    return final_hash
url1 = sys.argv[1]   # first website
url2 = sys.argv[2]   # second website

h1 = simhash_from_url(url1)   # simhash of first
h2 = simhash_from_url(url2)   # simhash of second
print("Simhash of URL1:", h1)
print("Simhash of URL2:", h2)

xor = h1 ^ h2   # xor for difference
different = bin(xor).count("1")   # count different bits

print("Common bits:", 64 - different)   # print common bits