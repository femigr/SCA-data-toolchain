import os
from shutil import copyfile
import multiprocessing
from sca_data_processing.issue import Issue

class CodeFile:
    def __init__(self, path) -> None:
        self.path = path
        self.issues = []
    
    def write(self, dest_path) -> None:
        content = self.get_content()
        for issue in self.issues:
            pass
    
    def get_content(self) -> str:
        with open(self.path, 'r') as f:
            return f.read()

    def add_issue(self, issue: Issue) -> None:
        self.issues.append(issue)
    
    def __eq__(self, __o: object) -> bool:
        return self.path == __o.path