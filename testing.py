import xml.etree.ElementTree as ET

def write_log(record, text):
    '''Append to logfile'''
    acNr = record.find(".//controlfield[@tag='009']").text
    with open("test_log.txt", "a") as logFile:
        logFile.write("{} - {}\n".format(acNr, text))

tree = ET.parse("inputFile.xml")
collection = tree.getroot()

checkTagsDict = {
    # keys: Datafields, Values: Subfields
    # "008":1,
    "024":["2","a"],
    "041":["a"],
    # "100":["a"], optional 100 or 700 or both
    "245":["a"], # b = optional
    "264":["b", "c"],
    "300":["a"],
    "347":["b"],
    # "490":["a", "v"], # optinal, 490 or 773
    "520":["a"],
    "536":["f", "a"],
    "540":["f", "u"],
    # "700":["a"],
    # "773":["t","g"], # optinal, 490 or 773
    "970":["d"]
    }


def checkDatafields(record):
    allDFs = True
    # acNr = record.find(".//controlfield[@tag='009']").text
    for key in checkTagsDict:
        if record.find(f".//datafield[@tag='{key}']") is None:
            txtMsg = f"No datafield {key}"
            print(txtMsg)
            write_log(record, txtMsg)
            allDFs = False
        else:
            # tagsDict[key](output, record) # run map function
            print(key, checkTagsDict[key])
            # print(record.find(f".//datafield[@tag='{key}']").text)
            # print(record.find(f".//datafield[@tag='{key}']").tag)
            # print(record.find(f".//datafield[@tag='{key}']").attrib)
            # for item in checkTagsDict[key]:
            #     print(item)
            #     for datafield in record.find(f".//datafield[@tag='{key}']"):
            #         if datafield.find(f"subfield[@code='{item}']") is None:
            #             print("No")
            #         else:
            #             print(datafield.find(f"subfield[@code='{item}']").text)
    return allDFs


    # # txtMsg = ""
    # for item in checkingSubfield:
    #     if item.find(f"subfield[@code='{subfieldCode}']") is None:
    #         txtMsg = f"Missing Subfield '{subfieldCode}' in datafield {datafield}"
    #         write_log(record, txtMsg)
    #         missingSubfield = True
    # return missingSubfield

def checkSubfields(record):
    allSubfields = True
    for key in checkTagsDict:
        datafields = record.findall(f".//datafield[@tag='{key}']")
        for datafield in datafields:
            for value in checkTagsDict[key]:
                if datafield.find(f"subfield[@code='{value}']") is None:
                    txtMsg = f"No subfied {value} in datafield {key}"
                    print(txtMsg)
                    write_log(record, txtMsg)
                    allSubfields = False
                # else:
                #     print(datafield.find(f"subfield[@code='{value}']").text)
    
    return allSubfields


for record in collection:
    print(record.find(".//controlfield[@tag='009']").text)
    print(checkDatafields(record))
    print(checkSubfields(record))