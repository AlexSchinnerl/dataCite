# Alma_2_dataCite

## Goal
The goal of this program is to get a Bibliographic Record via the ALMA API ([Retrieve Bib](https://developers.exlibrisgroup.com/console/?url=/wp-content/uploads/alma/openapi/bibs.json#/)) and transform it into a suitable XMl for uploading to the dataCite Website.

## How it works

The programm searches the `input.txt` file for AC-numbers, and then uses its `loader` function to load a bibliographic record from Alma.

> **NB!** make sure to change the credentials in the loader function to match those of your institution.

The `loader` produces an XML which can be used to:
* Search for a specific field tag in the xml tree
* Take the information of the field (text, attributes, ...)
* And asign them to a XML tag corresponding to the template needed to upload at the dataCite website

# Preperation (Keyring)

In the program we use the *keyring* library to safely store the API-Key, so that you don't have it to appear in your script.  
https://pypi.org/project/keyring/

After installing keyring, the library supplies a `keyring` command which is installed with the package. Which would be available for setting, getting, and deleting passwords.  

## Store API-Key

Open Command-Line:
```py
python
import keyring
keyring.set_password(service_name="<<YourServiceName>>", username="<<YourUserName>>", password="<<YourApiLKey>>")
```
## Retrieve API-Key

In your python file:
```py
import keyring
print(keyring.get_password(service_name="<<YourServiceName>>", username="<<YourUserName>>"))
# or store the api key in a variable - for later use
var = keyring.get_password(service_name="<<YourServiceName>>", username="<<YourUserName>>")
```

## Delete API-Key

If you want to delete your Password run:
```py
import keyring
keyring.delete_password(service_name="<<YourServiceName>>", username="<<YourUserName>>")
```

# How to run

* Store API-Key in keyring (see Preperation)
* Insert AC-Numbers in the `input.txt` file
* Execute `main.py`

The produced output and a logFile containing some caveats is stored in the output folder. Additionally the program stores the responses files for reference.

Note that the `response_files` and `output` folders are are cleared from old files as the program starts. If you don't want that behaviour, comment out those lines in the `main.py` file:
```py
dir_list = ["response_files", "output"] # list of folders to clear before program starts
for directory in dir_list:
    clear_directory(directory)
```

# Files

## Datacite Example

The `dataciteExample.xml` contains the example structure, provided by the [DataCite Website](https://schema.datacite.org/meta/kernel-4.4)

## Input File

A textfile containing the AC-numbers of the records you want to process.

## Response XML Files

The XML files from the API should look like this:

```xml
<bibs total_record_count="1">
    <bib>
        <mms_id>...</mms_id>
        .
        .
        <record>
            <controlfield tag="009">AC16525066</controlfield>
            <datafield tag="024" ind1="7" ind2=" ">
                <subfield code="a">10.35011/risc.22-04</subfield>
                <subfield code="2">doi</subfield>
            </datafield>
            .
            .
        </record>
    </bib>
</bibs>
```

## Python Files

### main

Contains the `main` method, along with the helper functions: `clear_directory` and `create_DCxml`. For each record the Alma XML is loaded and a DataCite compatible XML file is created and saved in the output folder.

### dataLoader

A simple function for accessing the ALMA API to get the user Data. The response is stored as `response_{AC Number}.xml`

### map_functions

Stores all functionions needed to map a datafield from the input file to the output xml.

### testingRecord

Hold a function to test if mandatory fields are present in the input file and one to write caveats in the logfile