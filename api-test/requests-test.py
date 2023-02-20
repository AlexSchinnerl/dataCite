import requests
import keyring
from xml.etree import ElementTree as ET

key = keyring.get_password("alma_api", "alx_prod").rstrip()
base = "https://api-eu.hosted.exlibrisgroup.com"
inputList = ["AC16712579","AC16712576"]
# bibs = f"/almaws/v1/bibs?other_system_id=(AT-OBV){acNr}&apikey={key}"



for acNr in inputList:
    url = f"https://api-eu.hosted.exlibrisgroup.com/almaws/v1/bibs?other_system_id=(AT-OBV){acNr}&apikey={key}"
    response = requests.get(url)
    # print(response.text)
    with open(f"response_{acNr}.xml", "w", encoding="UTF-8") as f:
        f.write(response.text)

# with open("response2.xml", "w") as f:
#     f.write(response.content)

# tree = ET.fromstring(response.content)
# print(tree)

