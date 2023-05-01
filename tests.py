from difflib import SequenceMatcher
import os
from urllib.parse import urlparse,urldefrag
from tokenizer import tokenize,computeWordFrequencies
import json
from bs4 import BeautifulSoup
import requests

test = "http://www.ics.uci.edu/courses.html"
r = requests.get(test)
print(r.status_code)

    


