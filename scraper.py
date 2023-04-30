import re
from bs4 import BeautifulSoup
from urllib.parse import urlparse,urldefrag
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
file = open(FULL_FREQ_PATH, 'a')
file.close()

def scraper(url, resp):
    links = extract_next_links(url, resp)
    linkList = [link for link in links if is_valid(link)]
    if len(linkList) >0:
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
    if resp.status!=200:                                                    #checks for webpage errors
        return []
    if resp.raw_response == None:
        return []
    soup = BeautifulSoup(resp.raw_response.content, "html.parser")

    d = computeWordFrequencies(tokenize(soup.get_text()))
    new_D = {"url": resp.url, "dict": d}
    with open(FULL_FREQ_PATH, 'r') as fileFreq:                             #bad web pages are discontinued through comparing texts
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
    newUrl = urlparse(url)
    for line in soup.find_all():
        newL = line.get('href')
        if newL != None and newL != "":
            newL = newL.replace("\\", "").replace("\"", "")
            if type(newL) is not str or len(newL) == 0:
                pass
            elif "mailto:" in newL:
                pass
            elif len(newL)>2 and newL[:2] == "//":
                retList.append(newL)
                count+=1
            elif newL[0].isalnum() and "/" not in newL:
                index = resp.url.rfind("/")
                newL = resp.url[:index+1] + newL
                retList.append(newL)
                count+=1
            elif len(newL) >1 and newL[0] == "/" and newL[1].isalnum():
                newL = newUrl.scheme+"://"+newUrl.hostname + newL                                       #original was newL = resp.url + newL
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
        if url == None:
            return False
        url = urldefrag(url)[0]
        parsed = urlparse(url)
        with open(FULL_ALL_LINK_PATH, 'a') as file:
            if url !=None:
                file.write(f"{url}\n")
        if parsed.scheme not in set(["http", "https"]):
            return False
        if not containsHost(parsed.hostname):
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

def isSimilar(url):
    for link in already_visited:
        parsed1 = urlparse(url)
        parsed2 = urlparse(link)
        if parsed1.hostname == parsed2.hostname:
            path = SequenceMatcher(None, parsed1.path, parsed2.path).ratio()
            if path >.90:
                return True
    return False

def isTextSimilar(dict1, dict2):
    r = SequenceMatcher(None, str(dict1),str(dict2)).ratio()
    return r>.9

def containsHost(hostName):
    if hostName==None:
        return False
    compareSet = set(["www.ics.uci.edu", "www.cs.uci.edu", "www.informatics.uci.edu", "www.stat.uci.edu", "ics.uci.edu", "cs.uci.edu", "informatics.uci.edu", "stat.uci.edu"])
    for name in compareSet:
        if name in hostName:
            return True
    return False