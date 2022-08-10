# AlmaXml_2_dataCite

Ziel ist es eine xml Datei, die aus Alma stammt, in eine xml Datei zu transformieren, die für DataCite hochgeladen werden kann.

## Libraries
xml.etree.ElementTree
re

## Files
* dataciteExample.xml - example xml provided by https://schema.datacite.org/meta/kernel-4.4
* exportExample - from Alma exported file - serves as input
* output.xml - transformed file - to direktly inport to dataCite

# Mapping
"What goes where"

# ToDo

* [x] ``<resourceType> <resourceTypeGeneral="Software">XML </resourceType>``
    * [x] resourceTypeGeneral soll "Text" sein~~
    * [x] kein text
* [] ``<formats>    <format>application/xml </format>   </formats>``
    [x]* befüllen mit "PDF" (wir haben nix anderes)
    * alternativ auch aus datafield tag="347" ind1=" " ind2=" "> subfield code="b">PDF /subfield>
* [] `` <descriptions> <description xml:lang="en-US" descriptionType="Abstract">XML example of all DataCite Metadata Schema v4.4 properties.</description>   </descriptions>``
    * [x] ---NB! 520 kann mehrmals vorkommen.
        * descriptionType="Abstract"
            * [x] befüllen mit ``<datafield tag="520" ind1=" " ind2=" "> <subfield code="a">``
            * Prefix Text "eng: " entfernen (ev. auch ger:)
        * descriptionType="SeriesInformation"
            * [x] `` <datafield tag="490" ind1="0" ind2=" "> <subfield code="a">RISC Report Series </subfield> <subfield code="v">22-04 </subfield> ``
                * [x] NB! subfielder mit "," getrennt
            * Bei ZS: 773 0 9 $t $g NB! $t und $g mit "," getrennt
                * z.B. AC16411195
* [x] `` <alternateIdentifiers> <alternateIdentifier alternateIdentifierType="URL"> </alternateIdentifier>  </alternateIdentifiers> ``
    * [x] befüllen mit URN
    * [x] alternateIdentifierType="URN"
    * [x] NB! Identifiers nur mit DOI
* [] ``<rightsList> <rights xml:lang="en-US" schemeURI="https://spdx.org/licenses/" rightsIdentifierScheme="SPDX" rightsIdentifier="CC0 1.0" rightsURI="https://creativecommons.org/publicdomain/zero/1.0/" /> </rightsList>``
    * [x] rightsIdentifier="CC BY 4.0 " standardmäßig einfügen
    * [x] Rights URI: https://creativecommons.org/licenses/by/4.0/legalcode
    * Felder im datafield tag="540" subfield code="f" subfield code="u" (hat leider eine andere URL)
