from typing import runtime_checkable
import sca_data_processing.parser as parser
import sca_data_processing.helpers as helpers

# Datset class:
class Dataset:
    def __init__(self, path):
        self.old_issues = []
        self.new_issues = []

        packages = helpers.get_full_package_files(path)
        for package in packages:
            self.add_package(package)

    def get_issues(self):
        return self.old_issues + self.new_issues

    def add_package(self, package):
        for scan in package['scans']['old']:
            filepath = (package['path'] + scan)
            if filepath.endswith('.xml'):
                self.old_issues += parser.parse_sca_xml(filepath, package['name'])
            elif filepath.endswith('.sarif'):
                self.old_issues += parser.parse_sarif(filepath, package['name'])
        
        for scan in package['scans']['new']:
            filepath = (package['path'] + scan)
            if filepath.endswith('.xml'):
                self.new_issues += parser.parse_sca_xml(filepath, package['name'])
            elif filepath.endswith('.sarif'):
                self.new_issues += parser.parse_sarif(filepath, package['name'])
    