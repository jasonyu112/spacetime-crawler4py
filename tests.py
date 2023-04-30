from difflib import SequenceMatcher
import os
from urllib.parse import urlparse,urldefrag

r = SequenceMatcher(None, "https://www.ics.uci.edu/about/about_meet_the_dean.php/grad/about_safety.php,","https://www.ics.uci.edu/about/about_meet_the_dean.php/grad/about_contact.php").ratio()
print(r)
parsed = urlparse("https://www.ics.uci.edu/community/news/spotlight/spotlight_russell.php/about/search/search_graduate_all.php/ugrad/QA_Graduation")
s = "https://www.ics.uci.edu/community/news/spotlight/spotlight_russell.php/about/search/search_graduate_all.php/ugrad/QA_Graduation"
print(parsed.hostname)
print(parsed.scheme)
print(".".isalnum())
print(s[:3])
    


