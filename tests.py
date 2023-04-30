from difflib import SequenceMatcher
import os
from urllib.parse import urlparse,urldefrag

r = SequenceMatcher(None, "https://www.ics.uci.edu/community/news/spotlight/spotlight_russell.php/about/search/search_graduate_all.php/ugrad/QA_Graduation","https://www.ics.uci.edu/community/news/spotlight/spotlight_russell.php/about/search/search_graduate_all.php/ugrad/resources/index").ratio()
print(r)
parsed = urlparse("https://www.ics.uci.edu/community/news/spotlight/spotlight_russell.php/about/search/search_graduate_all.php/ugrad/QA_Graduation")
s = "https://www.ics.uci.edu/community/news/spotlight/spotlight_russell.php/about/search/search_graduate_all.php/ugrad/QA_Graduation"
print(parsed.hostname)
print(parsed.scheme)
print(".".isalnum())
print(s[:3])
    


