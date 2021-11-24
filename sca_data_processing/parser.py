import json
import xml.etree.ElementTree as ET
from sca_data_processing.issue import Issue
from sca_data_processing.codefile import CodeFile


def parse_sca_xml(xml_file, package):
    """
    Parses the SCA XML file and returns a list with the data.

    :param xml_file: The XML file to parse.
    :return: A list of issues (dictionaries) with the data.
    """
    tree = ET.parse(xml_file)
    root = tree.getroot()

    issues = []
    rules = set()
    for child in root[1]:
        issues.append(Issue(xml_file, child.attrib['id'], child.attrib['severity'], child.attrib['cwe'] if 'cwe' in child.attrib else '', convert_xml_locations(child), package))
        rules.add(child.attrib['id'])
    return issues, rules

def parse_sarif(sarif_file, package):
    """
    Parses the SARIF file and returns a dictionary with the data.

    :param sarif_file: The SARIF file to parse.
    :return: A dictionary with the data.
    """
    with open(sarif_file, 'r') as f:
        data = json.load(f)['runs'][0]
    
    rules = {}
    for rule in data['tool']['driver']['rules']:
        # making sure my assumptions are correct:
        assert rule['id'] == rule['name']

        cwe = None
        for tag in rule['properties']['tags']:
            if tag.startswith('external/cwe/cwe-'):
                cwe = tag[len('external/cwe/cwe-'):]
                break

        rules.update({rule['id']: {
            'severity': rule['properties']['problem.severity'],
            'cwe': cwe
        }})

    issues = []
    occuring_rules = set()
    for result in data['results']:
        locations = convert_sarif_locations(result['locations'])
        if locations == []:
            continue
        issues.append(Issue(sarif_file, result['ruleId'][4:], rules[result['ruleId']]['severity'], rules[result['ruleId']]['cwe'], locations, package))
        occuring_rules.add(result['ruleId'][4:])
    return issues, occuring_rules

def convert_sarif_locations(sarif_locations):
    locations = []

    for location in sarif_locations:
        if location['physicalLocation']['artifactLocation']['uri'].startswith('debian/'):
            #issue was scanned in the build result folder
            continue

        if 'region' in location['physicalLocation']:
            locations.append({
                'file': location['physicalLocation']['artifactLocation']['uri'],
                'start_line': location['physicalLocation']['region']['startLine'],
                'start_column': location['physicalLocation']['region']['startColumn'] if 'startColumn' in location['physicalLocation']['region'] else 0,
                'end_line': location['physicalLocation']['region']['endLine'] if 'endLine' in location['physicalLocation']['region'] else location['physicalLocation']['region']['startLine'],
                'end_column': location['physicalLocation']['region']['endColumn']
            })
        else:
            #sometimes an issue affects a file as a whole so there is no region. This will set it to the beginning of the file
            #Example: {'ruleId': 'cpp/missing-header-guard', 'ruleIndex': 95, 'rule': {'id': 'cpp/missing-header-guard', 'index': 95}, 'message': {'text': 'This header file should contain a header guard to prevent multiple inclusion.'}, 'locations': [{'physicalLocation': {'artifactLocation': {'uri': 'panels/datetime/date-endian.h', 'uriBaseId': '%SRCROOT%', 'index': 52}}}], 'partialFingerprints': {'primaryLocationLineHash': '6035c534733a2797:1'}} 
            locations.append({
                'file': location['physicalLocation']['artifactLocation']['uri'],
                'start_line': 0,
                'start_column': 0,
                'end_line': 0,
                'end_column': 0
            })

    return locations

def convert_xml_locations(xml_locations):
    return [{
                'file': location.attrib['file'][location.attrib['file'].find('/') + 1:], # omits package name at start of string including the slash
                'start_line': location.attrib['line'],
                'start_column': location.attrib['column'],
                # because cpp check only tags a single spot, end_line and end_column are set to the same values: 
                'end_line': location.attrib['line'],
                'end_column': location.attrib['column']
            } for location in xml_locations if location.tag == 'location']