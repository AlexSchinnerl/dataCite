import xml.etree.ElementTree as ET
import map_functions
from testingRecord import check_mandatory_fields

def create_DCxml(record):
    '''
    Creates output root element 'resource'
    Goes through a Dictionary of datafield tags and starts the corresponding function
    Afterwards the functions not associated with a specific datafield are executed
    '''
    # create output root
    output = ET.Element("resource")
    output.attrib = {
        "xmlns:xsi":"http://www.w3.org/2001/XMLSchema-instance",
        "xsi:schemaLocation": "http://datacite.org/schema/kernel-4 https://schema.datacite.org/meta/kernel-4.4/metadata.xsd",
        "xmlns":"http://datacite.org/schema/kernel-4"
        }
    # Dictionary to map functions to Alma Datafield
    tagsDict = {
        "008":map_functions.create_date,
        "024":map_functions.create_identifier,
        "041":map_functions.create_language,
        "100":map_functions.create_creator,
        "245":map_functions.create_title,
        "264":map_functions.create_publisher,
        "300":map_functions.create_size,
        "347":map_functions.create_formats,
        "520":map_functions.create_descriptions,
        "536":map_functions.create_fundingReference,
        "540":map_functions.create_rights,
        "700":map_functions.create_creator,
        "970":map_functions.create_resourceType
        }
    # if datafield is in Alma xml - run function
    for key in tagsDict:
        if record.find(".//controlfield[@tag='{}']".format(key)) != None:
            tagsDict[key](output, record)
        elif record.find(".//datafield[@tag='{}']".format(key)) != None:
            tagsDict[key](output, record)
    return output

def main():
    '''
    Loads the input xml file (Alma export), checks if mandatory fields are present and starts for each record in collection the create_DCxml function.
    '''
    # Load Alma xml
    tree = ET.parse("inputFile.xml")
    collection = tree.getroot()
    #clear log file
    open("output/log.txt", "w").close()
    # go through all records in collection    
    counter = 0
    for record in collection:
        check_mandatory_fields(record)
        output = create_DCxml(record)
        # create tree
        outputTree = ET.ElementTree(output)
        # write output
        acNr = record.find(".//controlfield[@tag='009']").text
        outputTree.write("output/output_{}.xml".format(acNr))
        print("created output_{}.xml".format(acNr))
        counter+=1
        # print(counter)
    
    print("completed {} files".format(counter))
    # count content in log file
    errorCount = 0
    with open("output/log.txt") as log:
        errorCount = len(log.readlines())
    print("{} caveats - see log file".format(errorCount))

if __name__ == "__main__":
    main()