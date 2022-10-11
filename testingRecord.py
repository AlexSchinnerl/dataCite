def write_log(record, text):
    '''Append to logfile'''
    acNr = record.find(".//controlfield[@tag='009']").text
    with open("output/log.txt", "a") as logFile:
        logFile.write("{} - {}\n".format(acNr, text))


def subfield_check(datafield, subfieldCode, record):
    missingSubfield = False
    checkingSubfield = record.findall(f".//datafield[@tag='{datafield}']")
    # txtMsg = ""
    for item in checkingSubfield:
        if item.find(f"subfield[@code='{subfieldCode}']") is None:
            txtMsg = f"Missing Subfield '{subfieldCode}' in datafield {datafield}"
            write_log(record, txtMsg)
            missingSubfield = True
    return missingSubfield


# check 024



def check_for_doi(record):
    checkDOI = False
    for item in record.findall(".//datafield[@tag='024']"):
        if item.find("subfield[@code='2']").text == "doi":
                checkDOI = True
    if checkDOI == False:
        textMsg = "No DOI in record"
        # print(textMsg)
        write_log(record, textMsg)


def check_mandatory_fields(record):
    checkPass = False
    acNr = record.find(".//controlfield[@tag='009']").text
    print(f"Processing: {acNr}")
    # check for DOI:
    for item in record.findall(".//datafield[@tag='024']"):
        if subfield_check("024", "2", record) == False:
            check_for_doi(record)
        



    # check_for_doi = False
    # for item in record.findall(".//datafield[@tag='024']"):
    #     subfield_check, textMsg = check_subfields(datafield=item, subfieldcode="2", datafieldtag="024")
    #     if subfield_check == True:
    #         write_log(record, textMsg)    
    #     else:
    #         # checks if doi is in any 024
    #         if item.find("subfield[@code='2']").text == "doi":
    #             check_for_doi = True

    # if check_for_doi == False:
    #     textMsg = "No DOI in record"
    #     # print(textMsg)
    #     write_log(record, textMsg)



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