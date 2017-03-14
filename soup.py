from urllib.request import urlopen
from urllib.request import HTTPError
from urllib.request import URLError
import re
import boto3
import botocore.exceptions

from bs4 import BeautifulSoup


#proxy_support = urllib.request.ProxyHandler({'http': '52.14.111.77:3128'})
#opener = urllib.request.build_opener(proxy_support)
#urllib.request.install_opener(opener)

dynamodb = boto3.resource('dynamodb', region_name='us-east-2')

try:
    table = dynamodb.create_table(
        TableName='AirfleetsUrl',
        KeySchema=[
            {
                'AttributeName': 'primkey',
                'KeyType': 'HASH'  # Partition key
            },
        ],
        AttributeDefinitions=[
            {
                'AttributeName': 'primkey',
                'AttributeType': 'S'
            },

        ],
        ProvisionedThroughput={
            'ReadCapacityUnits': 5,
            'WriteCapacityUnits': 5
        }
    )
except botocore.exceptions.ClientError as e:
    print(e.response['Error'])

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


planelinks = getplanes("http://www.airfleets.net/recherche/supported-plane.htm")

table = dynamodb.Table('AirfleetsUrl')

if planelinks is None:
    print("Error: The location could not be found")
else:
    for plane in planelinks:
        match = re.findall('.*listing/((?!list).*)', plane['href'])
        if match:
            response = table.put_item(
                Item={
                    'primkey': match[0],
                    'baseurl': "http://www.airfleets.net/listing/" + match[0],
                }
            )
            planes2 = getplanes("http://www.airfleets.net/listing/" + match[0])
            if planes2 is None:
                print("Error: The location could not be found")
            else:
                for plane in planes2:
                    match = re.findall('.*listing/((?!list).*)', plane['href'])
                    if match:
                        response = table.put_item(
                            Item={
                                'primkey': match[0],
                                'baseurl': "http://www.airfleets.net/listing/" + match[0],
                            }
                        )


# title = getitle("http://www.airfleets.net/listing/b787-2.htm")
# if title is None:
#     print("The title could not be found")
# else:
#     for name in title:
#         match = re.search('(^\w{6}$)|(^\w-\w{4})|(^\w{2}-\w{3})', name.get_text())
#         if match:
#             print(match.group())

