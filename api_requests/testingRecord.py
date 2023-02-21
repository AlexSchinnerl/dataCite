def write_log(record, text):
    '''Append to logfile'''
    acNr = record.find(".//controlfield[@tag='009']").text
    with open("output/log.txt", "a") as logFile:
        logFile.write("{} - {}\n".format(acNr, text))


def check_subfields(datafield, subfieldcode, datafieldtag):
    missingSubfield = False
    textMsg = ""
    if datafield.find(f"subfield[@code='{subfieldcode}']") == None:
        textMsg = f"Missing Subfield '{subfieldcode}' in {datafieldtag}"
        missingSubfield = True
    return missingSubfield, textMsg

def check_mandatory_fields(record):
    acNr = record.find(".//controlfield[@tag='009']").text
    print(f"Processing: {acNr}")
    # check for DOI:
    check_for_doi = False
    for item in record.findall(".//datafield[@tag='024']"):
        subfield_check, textMsg = check_subfields(datafield=item, subfieldcode="2", datafieldtag="024")
        if subfield_check == True:
            write_log(record, textMsg)    
        else:
            # checks if doi is in any 024
            if item.find("subfield[@code='2']").text == "doi":
                check_for_doi = True

    if check_for_doi == False:
        textMsg = "No DOI in record"
        # print(textMsg)
        write_log(record, textMsg)
    # check if author in 100 and/or 700
    if record.find(".//datafield[@tag='100']") == None and record.find(".//datafield[@tag='700']") == None:
        textMsg = "No author (datafield 100 or datafield 700) in record"
        # print(textMsg)
        write_log(record, textMsg)
    # check for title (245 10 $$a)
    if record.find(".//datafield[@tag='245']") == None:
        textMsg = "No Title (datafield 245) in record"
        #print(textMsg)
        write_log(record, textMsg)
    if record.find(".//datafield[@tag='264']") == None:
        textMsg = "No Publication Data (datafield 264) in record"
        #print(textMsg)
        write_log(record, textMsg)
    elif record.find(".//datafield[@tag='264']").find("subfield[@code='b']") == None:
        textMsg = "No Publisher (datafield 264 #1 $$b) in record"
        # print(textMsg)
        write_log(record, textMsg)
    elif record.find(".//datafield[@tag='264']").find("subfield[@code='c']") == None:
        textMsg = "No Publisher (datafield 264 #1 $$c) in record"
        # print(textMsg)
        write_log(record, textMsg)