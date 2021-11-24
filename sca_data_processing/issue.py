import os
from shutil import copyfile
import multiprocessing


class Issue:
    def __init__(self, path, rule, severity, cwe, locations, package) -> None:
        self.path = path # Path to the result file
        self.rule = rule.replace("/","_")
        self.severity = severity
        self.cwe = cwe
        self.locations = locations # e.g. [{'file': 'apps/apps.c', 'start_line': 960, 'start_column': 11, 'end_line': 960, 'end_column': 22}]
        self.package = package
    
    def write_to_file(self, dest_path, metadata_base_path) -> None:
        process_id = multiprocessing.Process()._identity[1]
        location_index = 1
        file_list = []
        for location in self.locations:
            if location['file'] not in file_list:
                file_list.append(location['file'])
                dest_file_name = f"{self.rule}_{process_id}_{location_index}{os.path.splitext(location['file'])[1]}"
                location_index += 1

                file_path = os.path.join(metadata_base_path, self.package, "source/old", location['file']) #TODO soure/old
                try:
                    copyfile(file_path, os.path.join(dest_path, self.rule, dest_file_name))
                except FileNotFoundError:
                    #print(f"File {file_path} not found!")
                    continue