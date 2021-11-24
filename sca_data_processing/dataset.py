from typing import runtime_checkable
import sca_data_processing.parser as parser
import sca_data_processing.helpers as helpers
from tqdm import tqdm
import multiprocessing as mp

# Datset class:
class Dataset:
    def __init__(self, path = None, verbose = False):
        self.old_issues = []
        self.new_issues = []
        self.old_issue_classes = set()
        self.new_issue_classes = set()

        if path is not None:
            packages = helpers.get_full_package_files(path)

            if verbose:
                pbar = tqdm(total=len(packages))
                for package in packages:
                    self.add_package(package)
                    pbar.update()
            else:
                for package in packages:
                    self.add_package(package)



    def get_issues(self):
        return self.old_issues + self.new_issues
    
    def get_issue_classes(self):
        return self.old_issue_classes.union(self.new_issue_classes)

    def add_package(self, package):
        for scan in package['scans']['old']:
            filepath = (package['path'] + scan)
            if filepath.endswith('.xml'):
                issues, rules = parser.parse_sca_xml(filepath, package['name'])
                self.old_issues += issues
                self.old_issue_classes.update(rules)
            elif filepath.endswith('.sarif'):
                issues, rules = parser.parse_sarif(filepath, package['name'])
                self.old_issues += issues
                self.old_issue_classes.update(rules)

        for scan in package['scans']['new']:
            filepath = (package['path'] + scan)
            if filepath.endswith('.xml'):
                issues, rules = parser.parse_sca_xml(filepath, package['name'])
                self.new_issues += issues
                self.new_issue_classes.update(rules)
            elif filepath.endswith('.sarif'):
                issues, rules = parser.parse_sarif(filepath, package['name'])
                self.new_issues += issues
                self.new_issue_classes.update(rules)

    def get_filtered_issues(self):
        path_map = {}
        for issue in self.new_issues:
            if issue.package not in path_map.keys():
                path_map.update({issue.package: {}})
            for location in issue.locations:
                if location['file'] not in path_map[issue.package].keys():
                    path_map[issue.package].update({location['file']: []})
                if issue.rule not in path_map[issue.package][location['file']]:
                    path_map[issue.package][location['file']].append(issue.rule)
        
        issues = []
        rules = set()
        for issue in self.old_issues:
            for location in issue.locations:
                if issue.package not in path_map.keys():
                    # issues.append(issue)
                    continue
                if (location['file'] in path_map[issue.package].keys() and issue.rule not in path_map[issue.package][location['file']]):
                    issues.append(issue)
                    rules.add(issue.rule)
        return issues, rules