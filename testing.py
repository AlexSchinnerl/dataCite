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
    "024":["2","a"],
    "041":["a"],
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
    # "100":["a"], optional 100 or 700 or both
    }

cfList = ["008", "009"]



def checkControlfields(record):
    allCFs = True
    for item in cfList:
        if record.find(f".//controlfield[@tag='{item}']") is None:
            txtMsg = f"No controlfield {item}"
            print(txtMsg)
            write_log(record, txtMsg)
            allCFs = False
        # else:
        #     print(record.find(f".//controlfield[@tag='{item}']").text)
    return allCFs

def checkDatafields(record):
    allDFs = True
    # acNr = record.find(".//controlfield[@tag='009']").text
    for key in checkTagsDict:
        if record.find(f".//datafield[@tag='{key}']") is None:
            txtMsg = f"No datafield {key}"
            print(txtMsg)
            write_log(record, txtMsg)
            allDFs = False
        # else:
            # tagsDict[key](output, record) # run map function
            # print(key, checkTagsDict[key])

    return allDFs

def checkSubfields(record):
    allSubfields = True
    for key in checkTagsDict:
        datafields = record.findall(f".//datafield[@tag='{key}']")
        for datafield in datafields:
            for value in checkTagsDict[key]:
                if datafield.find(f"subfield[@code='{value}']") is None:
                    txtMsg = f"No subfield {value} in datafield {key}"
                    print(txtMsg)
                    write_log(record, txtMsg)
                    allSubfields = False
                # else:
                #     print(datafield.find(f"subfield[@code='{value}']").text)
    
    return allSubfields

def runTests(record):
    print("Testing: ", record.find(".//controlfield[@tag='009']").text)
    controlSum = 0
    if checkControlfields(record):
        print("Controlfields clear")
        controlSum +=1
    if checkDatafields(record):
        print("Datafields clear")
        controlSum +=1
    if checkSubfields(record):
        print("Subfields clear")
        controlSum +=1
    if controlSum == 3:
        print("All clear")

def check_for_doi(record):
    checkDOI = False
    for item in record.findall(".//datafield[@tag='024']"):
        if item.find("subfield[@code='2']").text == "doi":
                checkDOI = True
    if checkDOI == False:
        textMsg = "No DOI in record"
        # print(textMsg)
        write_log(record, textMsg)


# 1. All DFS
# 2. All SFs
# 3. Check for SF content

for record in collection:
    runTests(record)
    # checkControlfields(record)
    # print(checkDatafields(record))
    # print(checkSubfields(record))
