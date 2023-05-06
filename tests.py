from difflib import SequenceMatcher
import os
from urllib.parse import urlparse,urldefrag
from tokenizer import tokenize,computeWordFrequencies
import json
from bs4 import BeautifulSoup
import requests

absolute_path = os.path.dirname(__file__)
link_path = "Logs/links.txt"
all_links = "Logs/all_links.txt"
file4_path = "Logs/problem4.txt"
problem3_path = "Logs/problem3.txt"
stop_word_path = "Logs/stop_words.txt"
write_file = "Logs/report.txt"
ALL_LINKS_PATH = os.path.join(absolute_path, all_links)
FULL_LINK_PATH = os.path.join(absolute_path, link_path)
FULL_PROBLEM3_PATH = os.path.join(absolute_path, problem3_path)
FULL_FILE4_PATH = os.path.join(absolute_path, file4_path)
FULL_REPORT_FILE = os.path.join(absolute_path, write_file)
FULL_STOP_WORDS_FILE = os.path.join(absolute_path, stop_word_path)
already_seen = set()
seen_words = set()
stop_word = set()
with open(FULL_STOP_WORDS_FILE,'r') as stop_word_file:
    word = stop_word_file.readline()
    while word:
        word = word.strip()
        stop_word.add(word)
        word = stop_word_file.readline()
report_file = open(FULL_REPORT_FILE, "a")

link_count = 0
with open(FULL_LINK_PATH, 'r') as fileFreq:                             
    data = fileFreq.readline()
    while data:
        link_count+=1
        data = fileFreq.readline()
report_file.write(f"{str(link_count)}\n")

with open(FULL_PROBLEM3_PATH, 'r') as fileFreq:                             
    data = fileFreq.readline()
    url = ""
    word_count = 0
    while data:
        js = json.loads(data)
        temp_count = 0
        for words in js["dict"].values():
            temp_count+=words
        if temp_count>word_count and "~wjohnson" not in js["url"] and "ics.uci.edu/~cs224" not in js["url"]:
            word_count = temp_count
            url = js["url"]
        data = fileFreq.readline()
report_file.write(f"{url}\n")

with open(FULL_PROBLEM3_PATH, 'r') as fileFreq:                             
    data = fileFreq.readline()
    d = {}
    while data:
        js = json.loads(data.strip())
        word_dict = js["dict"]
        for word, count in word_dict.items():
            if not word.isalpha() or word in set(["t", "e", "P", "s", "n", "o", "l", "p", "i","r", "c","m","d","f", "b", "div", "w", "h", "wp", "ph", "j"]) or word in stop_word:
                pass
            elif word in seen_words:
                d[word] += count
            else:
                d[word] = count
                seen_words.add(word)
        data = fileFreq.readline()
    d = sorted(d.items(), key=lambda x:x[1], reverse=True)
    d = d[:50]
    l = [x[0] for x in d]
report_file.write(f"{str(l)}\n")

with open(ALL_LINKS_PATH, 'r') as fileFreq:                             
    data = fileFreq.readline()
    l = []
    while data:
        try:
            parsed = urlparse(data)
            if data is str:
                if data[0] == " ":
                    data = data[1:]
                parsed = urlparse(data.strip())
            if data == None or parsed.hostname == None:
                pass
            elif parsed.hostname == "www.ics.uci.edu":
                pass
            elif parsed.hostname in already_seen:
                for count, d in enumerate(l):
                    if d["url"] == parsed.hostname:
                        d["unique"] +=1
            elif ".ics.uci.edu" in parsed.hostname:
                l.append({"url": str(parsed.hostname), "unique": 1})
                already_seen.add(str(parsed.hostname))
            data = fileFreq.readline()
        except:
            pass
    l = sorted(l, key= lambda d : d["url"])
report_file.write(f"total: {len(l)}\n")
report_file.write(str(l))


report_file.close()
