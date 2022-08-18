import xml.etree.ElementTree as ET
import map_functions

def create_DCxml(record):
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
        "520":map_functions.create_descriptions,
        "536":map_functions.create_fundingReference
        }
    # if datafield is in Alma xml - run function
    for key in tagsDict:
        if record.find(".//datafield[@tag='{}']".format(key)) != None:
            tagsDict[key](output, record)

    # Functions with set values (Fields that are created with hard-coded value)
    map_functions.create_formats(output)
    map_functions.create_resourceType(output)
    map_functions.create_rights(output)

    return output

def write_log(record, text):
    acNr = record.find(".//controlfield[@tag='009']").text
    with open("log.txt", "a") as logFile:
        logFile.write("{} - {}\n".format(acNr, text))

def main():
    # Load Alma xml
    tree = ET.parse("inputFile.xml")
    collection = tree.getroot()
    counter = 0
    for record in collection:
        output = create_DCxml(record)
        # create tree ---------------------------------------------------
        outputTree = ET.ElementTree(output)
        # write output--------------------------------------------------------------
        acNr = record.find(".//controlfield[@tag='009']").text
        outputTree.write("output/output_{}.xml".format(acNr))
        print("created output_{}.xml".format(acNr))
        counter+=1
        print(counter)
    print("completed {} files".format(counter))

if __name__ == "__main__":
    main()