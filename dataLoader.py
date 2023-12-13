import keyring
import requests
import xml.etree.ElementTree as ET

def loader(acNr):
    """
    Takes an acNr and builds an api request. Then gives the response as xml and also saves the xml in a file (for later checkup)
    """
    key = keyring.get_password("alma_api", "alx_prod").rstrip()
    base = "https://api-eu.hosted.exlibrisgroup.com"
    url = f"{base}/almaws/v1/bibs?other_system_id=(AT-OBV){acNr}&apikey={key}"
    response = requests.get(url)
    root = ET.fromstring(response.content)
    # save response for checking
    with open(f"response_files/response_{acNr}.xml", "w", encoding="UTF-8") as f:
        f.write(response.text)
    return root