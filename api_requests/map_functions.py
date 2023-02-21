import xml.etree.ElementTree as ET
import re
from testingRecord import write_log

# Date -------------------------------------------------------------
def create_date(output, record):
    '''
    Takes controlfield 008 pos 0-5 (e.g. 220804) and builds a valid date (e.g. 2022-08-04)
    Creates element dates and subelement date
    Fills date text with created date
    '''
    dateMRC = record.find(".//controlfield[@tag='008']")
    date_alma = re.search("^\d{6}", dateMRC.text).group()
    date_alma = "20"+date_alma[:2]+"-"+date_alma[2:4]+"-"+date_alma[4:]
    dates_op = ET.Element("dates")
    date_op = ET.SubElement(dates_op, "date", attrib={"dateType":"Available"})
    date_op.text = date_alma

    output.append(dates_op)

# Identifier -------------------------------------------------------------
def create_identifier(output, record):
    '''
    Finds all (repeatable) datafield 024 elements
    If one of the fields contains a doi: element identifier is created and filled with the doi
    All other found identifiers (e.g. urn) are pasted in the alternateIdentifiers element        
    '''
    identifierMRC = record.findall(".//datafield[@tag='024']")
    for item in identifierMRC:
        if item.find("subfield[@code='2']") != None:
            if item.find("subfield[@code='2']").text == "doi":
                identifier = ET.Element("identifier", attrib={"identifierType":"DOI"})
                identifier.text = item.find("subfield[@code='a']").text
                output.append(identifier)
                
            else:
                altidentifiers = ET.Element("alternateIdentifiers")
                altidentifier = ET.SubElement(altidentifiers, "alternateIdentifier", attrib={"alternateIdentifierType":item.find("subfield[@code='2']").text})
                altidentifier.text = item.find("subfield[@code='a']").text

                output.append(altidentifiers)
    
# Language -------------------------------------------------------------
def create_language(output, record):
    '''
    Finds the datafield 041 element and pastes the language code (e.g. eng) in the language element    
    '''
    languageMRC = record.find(".//datafield[@tag='041']")
    language = ET.Element("language")
    language.text = languageMRC.find("subfield[@code='a']").text
    output.append(language)

# Creators -------------------------------------------------------------
def helper_create_creator(record, author, mainElement):
    '''
    Creates the single-creators to the creators element.
    For each creator additionally a creatorName, givenName and familyName element is created.
    Author Name is usually provided in datafield 100/700 subfield "a" (familyName, givenName)
    '''
    creator = ET.SubElement(mainElement, "creator")
    creatorName = ET.SubElement(creator, "creatorName", attrib={"nameType":"Personal"})
    creatorName.text = author.find("subfield[@code='a']").text

    if len(author.find("subfield[@code='a']").text.split(",")) > 1: # catch index error (if no split: len=1)
        givenName = ET.SubElement(creator, "givenName")
        givenName.text = author.find("subfield[@code='a']").text.split(",")[1]
        familyName = ET.SubElement(creator, "familyName")
        familyName.text = author.find("subfield[@code='a']").text.split(",")[0]
    else:
        # write log
        textMsg = "Author '{}' does not contain ','".format(author.find("subfield[@code='a']").text)
        write_log(record, textMsg)
        # continue with split at blank
        if len(author.find("subfield[@code='a']").text.split(" ")) == 2: # check if name contains 2 words sep. by blank (prevents wrong split in case of double name)
            givenName = ET.SubElement(creator, "givenName")
            givenName.text = author.find("subfield[@code='a']").text.split(" ")[1]
            familyName = ET.SubElement(creator, "familyName")
            familyName.text = author.find("subfield[@code='a']").text.split(" ")[0]
        else:
            textMsg = "Can not split '{}' no givenName and no familyName created".format(author.find("subfield[@code='a']").text)
            write_log(record, textMsg)

def create_creator(output, record):
    '''
    Creates the creators element and fills it with the authors provided by datafield 100 and/or all 700s.
    Uses the helper_create_creator function to create the creators subfields
    '''
    if output.find("creators") == None: # check if creators already exists (100 and 700 both call create_creators)
        creators = ET.Element("creators")
        if record.find(".//datafield[@tag='100']") != None: # if 100 contains text creeate main author and check for side authors
            # create main Author
            main_authorMRC = record.find(".//datafield[@tag='100']")
            helper_create_creator(record, main_authorMRC, creators)
        # create side-authors
        if record.findall(".//datafield[@tag='700']") != None:
            side_authorMRC = record.findall(".//datafield[@tag='700']")
            for author in side_authorMRC:
                helper_create_creator(record, author, creators)
        output.append(creators)

# Titles -------------------------------------------------------------
def create_title(output, record):
    '''
    Creates the titles element and its subelements title.
    Fills the Elements with datafield 245 subfield 'a' (title) and if existing subtitle from subfield 'b'
    '''
    titleMRC = record.find(".//datafield[@tag='245']")
    titles = ET.Element("titles")
    # ------------------------------ Main Title
    title = ET.SubElement(titles, "title")
    # check if '<<' OR '>>' are present in title and remove them
    titleText = titleMRC.find("subfield[@code='a']").text
    toCut = re.findall("<<|>>", titleText)
    for item in toCut:
            if item in titleText:
                    titleText = titleText.replace(item, "")
    title.text = titleText
    # ------------------------------ Subtitle
    if titleMRC.find("subfield[@code='b']") != None:
        subtitle = ET.SubElement(titles, "title", attrib={"titleType":"Subtitle"})
        subtitle.text = titleMRC.find("subfield[@code='b']").text
    output.append(titles)

# publisher/publicationYear -------------------------------------------------------------
def create_publisher(output, record):
    '''
    Creates the publisher and publicationYear element.
    Both are filled with datafield 264 (publisher with subfield 'b' and publicationYear with subfield 'c')
    '''
    # -------------publisher
    publisherMRC = record.find(".//datafield[@tag='264']")
    publisher = ET.Element("publisher")
    publisher.text = publisherMRC.find("subfield[@code='b']").text
    output.append(publisher)
    # -------------publication Year 
    publicationYear = ET.Element("publicationYear")
    pubDate = re.search("\d{4}", publisherMRC.find("subfield[@code='c']").text).group() # search for 4 digits in the "c" Subfield
    publicationYear.text = pubDate
    output.append(publicationYear)

# Size -------------------------------------------------------------
def create_size(output, record):
    '''
    Creates the sizes element and the size subelement.
    Fills size with pages from datafield 300 subfield 'a' (digits in parentheses)
    '''
    sizeMRC = record.find(".//datafield[@tag='300']")
    sizes = ET.Element("sizes")
    size = ET.SubElement(sizes, "size")
    if re.search("(?<=\()\d+", sizeMRC.find("subfield[@code='a']").text) != None:
        pageNr = re.search("(?<=\()\d+", sizeMRC.find("subfield[@code='a']").text).group() # match 1-n digits after ()
        size.text = str(pageNr + " pages")
    # else: # if no pages in () write full subfield text
        # size.text = record.find(".//datafield[@tag='300']").find("subfield[@code='a']").text
    output.append(sizes)

# Formats -------------------------------------------------------------
def create_formats(output, record):
    '''
    Creates formats element and subelement format.
    Fills element with default text "PDF" (alternatively datafield 347 subfield 'b' could be used)
    '''
    formatMRC = record.find(".//datafield[@tag='347']")
    formats = ET.Element("formats")
    formatDC = ET.SubElement(formats, "format")
    formatDC.text = formatMRC.find("subfield[@code='b']").text
    output.append(formats)

# Descriptions -------------------------------------------------------------
def create_descriptions(output, record):
    '''
    Creates the descriptions element and two subelements: SeriesInformation and Abstract
    SeriesInformation is filled with either datafield 773 subfield 't' and 'g' (if record is a journal) or datafield 490 subfield 'a' and 'v'
    Abstract is filled with all (repeatable) 520 datafields
    '''
    descriptions = ET.Element("descriptions")
    # ------------- Series Information
    description = ET.SubElement(descriptions, "description", attrib={"descriptionType":"SeriesInformation"})
    # field 490 is not present - .find() returns None
    check_for_490 = record.find(".//datafield[@tag='490']")
    if check_for_490 is None:
        seriesInformationMRC = record.find(".//datafield[@tag='773']")
        description.text = str(
            seriesInformationMRC.find("subfield[@code='t']").text 
            + ", "
            + seriesInformationMRC.find("subfield[@code='g']").text
            )
    else:
        seriesInformationMRC = record.find(".//datafield[@tag='490']")
        description.text = str(
            seriesInformationMRC.find("subfield[@code='a']").text 
            + ", "
            + seriesInformationMRC.find("subfield[@code='v']").text
            )
    # ------------- Abstract
    abstractMRC = record.findall(".//datafield[@tag='520']")
    for item in abstractMRC:
        description = ET.SubElement(descriptions, "description", attrib={"descriptionType":"Abstract"})
        # cut "eng: " or "ger: " from abstract text
        oldText = item.find("subfield[@code='a']").text
        toCut = re.search("^eng: |^ger: |^eng:|^ger:", oldText).group() # search for eng: and ger: with and without space
        abstractText = oldText.replace(toCut, "")
        description.text = abstractText
    output.append(descriptions)

# fundingReferences -------------------------------------------------------------
def create_fundingReference(output, record):
    '''
    Creates the fundingReferences element and its subelement fundingReference.
    Further the subelements of fundingReference: funderName, funderIdentifier and awardNumber
    awardNumber is filled with datafield 536 subfield 'f'
    funderName and funderIdentifier are a translation of the subfield 'a' text
    '''
    #Funder Dictionary for translation
    funderDict = {
        "Fonds zur Förderung der Wissenschaftlichen Forschung":["Austrian Science Fund", "https://doi.org/10.13039/501100002428"],
        "Österreichische Forschungsförderungsgesellschaft":["Österreichische Forschungsförderungsgesellschaft", "https://doi.org/10.13039/501100004955"],
        "Europäische Kommission":["European Commission", "https://doi.org/10.13039/501100000780"]
    }

    fundingMRC = record.findall(".//datafield[@tag='536']")
    fundingReferences = ET.Element("fundingReferences")
    for item in fundingMRC:
        fundingReference = ET.SubElement(fundingReferences, "fundingReference")
        funderName = ET.SubElement(fundingReference, "funderName")
        funderIdentifier = ET.SubElement(fundingReference, "funderIdentifier", attrib={"funderIdentifierType":"Crossref Funder ID"})
        awardNumber = ET.SubElement(fundingReference, "awardNumber")
        awardNumber.text = item.find(("subfield[@code='f']")).text
        # translation from funder in subfield 'a' to funderName and funderIdentifier
        if item.find(("subfield[@code='a']")).text in funderDict: # check if funder in funder Dictionary
            for funder in funderDict:
                if item.find(("subfield[@code='a']")).text == funder:
                    funderName.text = funderDict[funder][0]
                    funderIdentifier.text = funderDict[funder][1]
        else:
            textMsg = "Funder {} not in Funder Dictionary".format(item.find(("subfield[@code='a']")).text)
            write_log(record, textMsg)
    output.append(fundingReferences)

# Rights -------------------------------------------------------------
def create_rights(output, record):
    '''
    Creates rightsList element and subelement rights.
    Fills attributes with the data from datafield 540 subfield f and creates a fitting URL to the corresponding creativecommons.org/licenses site
    '''
    rightsList = ET.Element("rightsList")
    rights = ET.SubElement(rightsList, "rights")
    rightsMRC = record.find(".//datafield[@tag='540']")
    rightsIdentifier = rightsMRC.find("subfield[@code='f']").text
    rightsURL = rightsMRC.find("subfield[@code='u']").text
    rightsURL =  "https://creativecommons.org/licenses/{}/{}/legalcode".format(
        rightsIdentifier.split(" ")[1].lower(),
        rightsIdentifier.split(" ")[2]
        )
    rights.attrib = {
        "rightsIdentifier":rightsIdentifier,
        "rightsURI":rightsURL
        }
    output.append(rightsList)

# RecourceType -------------------------------------------------------------
def create_resourceType(output, record):
    '''
    Creates the resourceType and fills attribute resourceTypeGeneral with translated Information from datafield 970 ind1: 2 subfield d
    '''
    resTypeDict = {
        "OA-BOOKPART":"ConferencePaper",
        "OA-MONOGRAPH":"Report",
        "OA-ARTICLE":"JournalArticle"
    }
    resTypeMRC = record.find(".//datafield[@tag='970'][@ind1='2']")
    resourceType = ET.Element("resourceType")

    if resTypeMRC.find("subfield[@code='d']").text in resTypeDict:
        for resType in resTypeDict:
            if resTypeMRC.find("subfield[@code='d']").text == resType:
                resourceType.attrib = {"resourceTypeGeneral":resTypeDict[resType]}
    else:
        textMsg = "Resource Type {} not in Resource Type Dictionary".format(resTypeMRC.find("subfield[@code='d']").text)
        write_log(record, textMsg)    
    # resourceType.text = " "
    output.append(resourceType)