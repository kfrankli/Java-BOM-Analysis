#!/usr/bin/env python3
import sys
import argparse
from lxml import etree
from os.path import exists

# Delete the namespace from the tags
def del_namespace_etree_tags(etree_root):
    for elem in etree_root.getiterator():
        # Skip comments and processing instructions,
        # because they do not have names
        if not (
            isinstance(elem, etree._Comment)
            or isinstance(elem, etree._ProcessingInstruction)
        ):
            # Remove a namespace URI in the element's name
            elem.tag = etree.QName(elem).localname
    # Remove unused namespace declarations
    etree.cleanup_namespaces(etree_root)

def process_dependancies(etree_root):
    dependanciesDict = dict()
    for dependency in etree_root.findall('./dependencies/') + etree_root.findall('./dependencyManagement/dependencies/'):
        groupId = ""
        artifactId = ""
        version = ""
        for child in dependency:
            if(child.tag == "groupId"):
                groupId = child.text
            elif(child.tag == "artifactId"):
                artifactId = child.text
            elif(child.tag == "version"):
                # Using this to look up often variablized artifact versions
                if "${" in child.text:
                    for property in etree_root.findall('./properties/'):
                        if property.tag == child.text[2:-1]:
                            version = property.text
                else:
                    version = child.text
            elif(child.tag in ["exclusions","scope","classifier","type","optional"]):
                continue
            elif(isinstance(child,etree._Comment)):
                continue
            else:
                print(child, child.tag)
                print("ERROR")
                exit(1)
        dependanciesDict[(groupId, artifactId)] = version
    return dependanciesDict

def compare_poms(appPom, bomPom):
    bomPomTree = etree.parse(bomPom)
    bomPomRoot = bomPomTree.getroot()
    del_namespace_etree_tags(bomPomRoot)
    bomDepdanciesDict = process_dependancies(bomPomRoot)

    appPomTree = etree.parse(appPom)
    appPomRoot = appPomTree.getroot()
    del_namespace_etree_tags(appPomRoot)
    pomDepdanciesDict = process_dependancies(appPomRoot)

    print("| groupId | artifactId | pom.xml version | BOM version |")
    print("|---|---|---|---|")
    for dependency in pomDepdanciesDict:
        if dependency in bomDepdanciesDict:
            groupId, artifactId = dependency
            print("| " + groupId + " | " + artifactId + " | " + pomDepdanciesDict[dependency] + " | " + bomDepdanciesDict[dependency] + " |")
    print("")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Compare two Java pom files to see what they have in common with regards to dependancies. This is designed to assist with large scale analysis of Java maven projects for BOM inclusion. Outputs a markdown format table.", formatter_class=argparse.ArgumentDefaultsHelpFormatter)

    parser.add_argument("-t", "--template", help="Template pom created via \"mvn help:effective-pom -Doutput=effectivepom.xml.\"")
    parser.add_argument("-p", "--pom", help="pom.xml of the Java project in question")
    args = parser.parse_args()
    config = vars(args)

    bomPom = open(args.template,'r')
    appPom = open(args.pom,'r')
    compare_poms(appPom, bomPom)
