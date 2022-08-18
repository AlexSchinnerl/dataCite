# AlmaXml_2_dataCite
## Goal
We got a xml from an Alma export and want to transform it in a xml file suitable for uploading to the dataCite Website.

## How it works
The programm takes an Alma export file as input and it is basically searching for a specific datafield tag in the xml Tree. Then take the information of the field (text, attributes, ...) an asign them to a xml tag corresponding to the template needed to upload the xml at the dataCite website.

<u>Note!</u> Some Fields are filled with features, specially tailored to meet the needs of the JKU and would need adaptation if used in a different university.

## Libraries
* xml.etree.ElementTree
* re

# Files
## xml Files
### Datacite Example
 The "dataciteExample.xml" contains the example structure, provided by the DataCite Website (https://schema.datacite.org/meta/kernel-4.4)

### Input File
The programm expects an input xml file which was exported from Alma via the "Export Bibliographic records" job.

The file should be named "inputFile.xml" and the structure should look as follows:
<pre>
&lt;collection&gt;
    &lt;record&gt;
        &lt;controlfield tag="009"&gt;AC16525066&lt;/controlfield&gt;
        &lt;datafield tag="024" ind1="7" ind2=" "&gt;
            &lt;subfield code="a">10.35011/risc.22-04&gt;
            &lt;subfield code="2">doi&gt;
        &lt;/datafield&gt;
    &lt;/record&gt;
&lt;/collection&gt;
</pre> 

## Python Files
### main
Contains the main method, where the input file is loaded and for each provided record a DataCite compatible xml file is created and saved in the output folder.

### map_functions
Stores all functionions needed to map a datafield from the input file to the output xml.

# How to run
Replace the content of the inputFile.xml with your exported File and run the main.py file. The produced output is stored in the output folder.

# ToDo
* Finish readme
## NiceToHave
* ``formats > format``
    * Wird im Moment mit "PDF" befüllt. Alternativ auch aus 347er subfield "b"
* ``rightsList> rights ``
    * Wird standardmäßig mit "CC BY 4.0 " und fixer URL befüllt. Alternativ: 540er subfield "f" und subfield "u" (hat aber leider eine andere URL)
        
