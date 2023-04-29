import re
from bs4 import BeautifulSoup
from urllib.parse import urlparse
import os
from tokenizer import tokenize,computeWordFrequencies
import json
from difflib import SequenceMatcher


absolute_path = os.path.dirname(__file__)
link_path = "Logs/links.txt"
wordFreq_path = "Logs/freq.txt"
all_link_path = "Logs/all_links.txt"
file4_path = "Logs/problem4.txt"
FULL_LINK_PATH = os.path.join(absolute_path, link_path)
FULL_FREQ_PATH = os.path.join(absolute_path, wordFreq_path)
FULL_ALL_LINK_PATH = os.path.join(absolute_path, all_link_path)
FULL_FILE4_PATH = os.path.join(absolute_path, file4_path)
already_visited = {}
#blacklist = {"http://www.ics.uci.edu/ugrad/courses/listing.php", "https://www.ics.uci.edu/privacy/index.php"}
file = open(FULL_FREQ_PATH, 'a')
file.close()

def scraper(url, resp):
    links = extract_next_links(url, resp)
    linkList = [link for link in links if is_valid(link)]
    file = open(FULL_LINK_PATH, 'a')
    for x in linkList:
        already_visited[x] = 1
        file.write(f"{x}\n")
    file.close()
    return linkList

def extract_next_links(url, resp):
    # Implementation required.
    # url: the URL that was used to get the page
    # resp.url: the actual url of the page
    # resp.status: the status code returned by the server. 200 is OK, you got the page. Other numbers mean that there was some kind of problem.
    # resp.error: when status is not 200, you can check the error here, if needed.
    # resp.raw_response: this is where the page actually is. More specifically, the raw_response has two parts:
    #         resp.raw_response.url: the url, again
    #         resp.raw_response.content: the content of the page!
    # Return a list with the hyperlinks (as strings) scrapped from resp.raw_response.content
    retList = []
    if resp.status!=200:
        return []
    soup = BeautifulSoup(resp.raw_response.content, "html.parser")

    d = computeWordFrequencies(tokenize(soup.get_text()))
    new_D = {"url": resp.url, "dict": d}
    with open(FULL_FREQ_PATH, 'r') as fileFreq:
        data = fileFreq.readline()
        while data:
            js = json.loads(data)
            if isTextSimilar(str(js["dict"]), str(new_D["dict"])):
                return []
            data = fileFreq.readline()
    file = open(FULL_FREQ_PATH, 'a')
    file.write(f"{json.dumps(new_D)}\n")
    file.close()
    count = 0
    for line in soup.find_all():
        newL = line.get('href')               #if url does not contain previous url or www then add line.get('href') to url and append
        if newL != None and newL != "":
            newL = newL.replace("\\", "").replace("\"", "")
            if newL[0] == "/":
                    newL = resp.url + newL
                    retList.append(newL)
                    count+=1
            else:
                retList.append(newL)
                count+=1
    newerD = {"url": resp.url, "unique": count}
    file4 = open(FULL_FILE4_PATH, 'a')
    if "ics.uci.edu" in resp.url:
        file4.write(f"{json.dumps(newerD)}\n")
    return retList

def is_valid(url):
    # Decide whether to crawl this url or not. 
    # If you decide to crawl it, return True; otherwise return False.
    # There are already some conditions that return False.
    try:
        with open(FULL_ALL_LINK_PATH, 'a') as file:
            if url !=None:
                file.write(f"{url}\n")
        parsed = urlparse(url)
        if parsed.scheme not in set(["http", "https"]):
            return False
        if parsed.hostname not in set(["www.ics.uci.edu", "www.cs.uci.edu", "www.informatics.uci.edu", "www.stat.uci.edu", "ics.uci.edu", "cs.uci.edu", "informatics.uci.edu", "stat.uci.edu"]):
            return False
        if isRepeating(parsed.path):
            return False
        if url in already_visited.keys():
            return False
        if isSimilar(url):
            return False
        return not re.match(
            r".*\.(css|js|bmp|gif|jpe?g|ico"
            + r"|png|tiff?|mid|mp2|mp3|mp4"
            + r"|wav|avi|mov|mpeg|ram|m4v|mkv|ogg|ogv|pdf"
            + r"|ps|eps|tex|ppt|pptx|doc|docx|xls|xlsx|names"
            + r"|data|dat|exe|bz2|tar|msi|bin|7z|psd|dmg|iso"
            + r"|epub|dll|cnf|tgz|sha1"
            + r"|thmx|mso|arff|rtf|jar|csv"
            + r"|rm|smil|wmv|swf|wma|zip|rar|gz)$", parsed.path.lower())

    except TypeError:
        print ("TypeError for ", parsed)
        raise

def isRepeating(path):
    arr = path.split("/")
    counter = 0
    while True:
        if counter>=len(arr):
            break
        for innerCounter, item in enumerate(arr):
            if counter!= innerCounter:
                if item == arr[counter]:
                    return True
        counter+=1

def isSimilar(url):
    for link in already_visited:
        parsed1 = urlparse(url)
        parsed2 = urlparse(link)
        if parsed1.hostname == parsed2.hostname:
            path = SequenceMatcher(None, parsed1.path, parsed2.path).ratio()
            if path >.9:
                return True
    return False

def isTextSimilar(dict1, dict2):
    r = SequenceMatcher(None, str(dict1),str(dict2)).ratio()
    return r>.9