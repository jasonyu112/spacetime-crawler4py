from difflib import SequenceMatcher
import os
from urllib.parse import urlparse,urldefrag
from tokenizer import tokenize,computeWordFrequencies
import json
from bs4 import BeautifulSoup

def isTextSimilar(dict1, dict2):
    r = SequenceMatcher(None, str(dict1),str(dict2)).ratio()
    return r>.9

absolute_path = os.path.dirname(__file__)
wordFreq_path = "Logs/tests.txt"
FULL_FREQ_PATH = os.path.join(absolute_path, wordFreq_path)
og_d = {"url": "https://ngs.ics.uci.edu/smart-traffic", "dict": {"smart": 3, "traffic": 3, "ramesh": 5, "jain": 3, "search": 1, "entrepreneur": 1, "researcher": 1, "and": 2, "teacher": 1, "about": 1, "news": 1, "events": 1, "blogs": 1, "research": 2, "books": 2, "patents": 1, "presentations": 1, "projects": 1, "papers": 1, "computer": 1, "vision": 1, "experiential": 2, "computing": 2, "multimedia": 1, "information": 1, "management": 1, "teaching": 1, "current": 4, "courses": 2, "past": 3, "entrepreneurship": 1, "companies": 2, "partners": 1, "students": 2, "collaborators": 1, "professional": 1, "social": 1, "services": 1, "recognitions": 1, "interviews": 1, "personal": 1, "affiliations": 1, "education": 1, "favorite": 2, "quotes": 1, "navigation": 1, "wall": 1, "street": 1, "has": 1, "an": 1, "article": 1, "on": 1, "how": 1, "is": 2, "becoming": 1, "increasingly": 1, "many": 1, "such": 1, "articles": 1, "exist": 1, "this": 2, "one": 1, "a": 2, "good": 2, "summary": 1, "of": 2, "state": 1, "art": 1, "in": 1, "area": 1, "by": 3, "november": 1, "17": 1, "2008": 1, "no": 1, "comments": 1, "friends": 1, "technology": 1, "auto": 1, "industry": 1, "leave": 1, "replyyour": 1, "email": 2, "address": 1, "will": 1, "not": 1, "be": 1, "published": 1, "required": 1, "fields": 1, "are": 1, "marked": 1, "comment": 1, "name": 1, "website": 1, "copyright": 1, "2022": 1, "theme": 2, "horse": 1, "powered": 1, "wordpress": 1, "back": 1, "to": 1, "top": 1}}
d = og_d["dict"]
new_D = {"url": "https://ngs.ics.uci.edu/smart-traffic", "dict": d}
with open(FULL_FREQ_PATH, 'r') as fileFreq:                             #bad web pages are discontinued through comparing texts
    data = fileFreq.readline()
    while data:
        js = json.loads(data)
        if isTextSimilar(str(js["dict"]), str(new_D["dict"])):
            break
        data = fileFreq.readline()

    


