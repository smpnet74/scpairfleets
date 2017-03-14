from urllib.request import urlopen
from urllib.request import HTTPError
from urllib.request import URLError
import boto3
import botocore.exceptions
import json
from bs4 import BeautifulSoup

def getplanes(url: object) -> object:
    try:
        html = urlopen(url)
    except HTTPError as e:
        return None
    except URLError as e:
        return None
    try:
        bsObj = BeautifulSoup(html.read(), "html.parser")
        planeslinks = bsObj.find_all("a", href=True)
    except AttributeError as e:
        return None
    return planeslinks

dynamodb = boto3.resource('dynamodb', region_name='us-east-2')

table = dynamodb.Table('AirfleetsUrl')

response = table.scan()

for i in response['Items']:
    urlcheck = (json.dumps(i['baseurl']))
    print(urlcheck)
    planelinks = getplanes(urlcheck)


