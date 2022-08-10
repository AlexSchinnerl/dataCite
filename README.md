# AlmaXml_2_dataCite

Ziel ist es eine xml Datei, die aus Alma stammt, in eine xml Datei zu transformieren, die für DataCite hochgeladen werden kann.

## Libraries
xml.etree.ElementTree
re

## Files
* dataciteExample.xml - example xml provided by https://schema.datacite.org/meta/kernel-4.4
* exportExample - from Alma exported file - serves as input
* output.xml - transformed file - to direktly inport to dataCite

# How it works
The programm takes an Alma export file as input and it is basically searching for a specific datafield tag in the xml Tree. Then take the information of the field (text, attributes, ...) an asign them to a xml tag corresponding to the template needed to upload the xml at the dataCite Website.

# ToDo
Offene Frage: Welches Datafield, bzw. Subfield kann einmal nicht vorhanden sein, welches ist immer da?

Subfelder ´, die nicht vorhanden sein können abfangen...

## NiceToHave
* ``formats > format``
    * Wird im Moment mit "PDF" befüllt. Alternativ auch aus 347er subfield "b"
* ``rightsList> rights ``
    * Wird standardmäßig mit "CC BY 4.0 " und fixer URL befüllt. Alternativ: 540er subfield "f" und subfield "u" (hat aber leider eine andere URL)
        
