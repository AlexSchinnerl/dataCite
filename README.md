# AlmaXml_2_dataCite
## Goal
We got a xml from an Alma export and want to transform it in a xml file suitable for uploading to the dataCite Website.

## How it works
The programm takes an Alma export file as input and searches for a specific field tag in the xml tree. Then take the information of the field (text, attributes, ...) an asign them to a xml tag corresponding to the template needed to upload at the dataCite website.

**Note!** Some Fields are filled with features, specially tailored to meet the needs of the JKU and would need adaptation if used in a different university.

# How to run
* Export bibliographic records from Alma (Admin > Run a Job > Export Bibliographic records)
* Replace the content of the `inputFile.xml` with your exported file
* Execute `main.py`.

The produced output and a logFile containing some caveats is stored in the output folder.

# Files
## xml Files
### Datacite Example
 The "dataciteExample.xml" contains the example structure, provided by the DataCite Website (https://schema.datacite.org/meta/kernel-4.4)

### Input File
The programm expects an input xml file which was exported from Alma via the "Export Bibliographic records" job.

The file should be named "inputFile.xml" and the structure should look as follows:
```
<collection>
    <record>
        <controlfield tag="009">AC16525066</controlfield>
        <datafield tag="024" ind1="7" ind2=" ">
            <subfield code="a">10.35011/risc.22-04</subfield>
            <subfield code="2">doi</subfield>
        </datafield>
    </record>
</collection>
```
## Python Files
### main
Contains the main method, where the input file is loaded and for each provided record a DataCite compatible xml file is created and saved in the output folder.

### map_functions
Stores all functionions needed to map a datafield from the input file to the output xml.

### testingRecord
Hold a function to test if mandatory fields are present in the input file and one to write caveats in the logfile