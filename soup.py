from urllib.request import urlopen
from urllib.request import HTTPError
import re
import sys

from bs4 import BeautifulSoup


def getitle(url: object) -> object:
    try:
        html = urlopen(url)
    except HTTPError as e:
        return None
    try:
        bsObj = BeautifulSoup(html.read(), "html.parser")
        title = bsObj.find_all("a", {"class": "lien"})
    except AttributeError as e:
        return None
    return title

def getplanes(url: object) -> object:
    try:
        html = urlopen(url)
    except HTTPError as e:
        return None
    try:
        bsObj = BeautifulSoup(html.read(), "html.parser")
        planeslinks = bsObj.find_all("a", href=True)
    except AttributeError as e:
        return None
    return planeslinks

planelinks = getplanes("http://www.airfleets.net/recherche/supported-plane.htm")
size = sys.getsizeof(planelinks)
print(size)

if planelinks is None:
    print("Error: The location could not be found")
else:
    for plane in planelinks:
        match = re.findall('.*listing/(.*)', plane['href'])
        if match:
            print(match[0])

# title = getitle("http://www.airfleets.net/listing/b787-2.htm")
# if title is None:
#     print("The title could not be found")
# else:
#     for name in title:
#         match = re.search('(^\w{6}$)|(^\w-\w{4})|(^\w{2}-\w{3})', name.get_text())
#         if match:
#             print(match.group())