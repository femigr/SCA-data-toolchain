class Issue:
    def __init__(self, path, rule, severity, cwe, locations, package) -> None:
        self.path = path
        self.rule = rule
        self.severity = severity
        self.cwe = cwe
        self.locations = locations
        self.package = package