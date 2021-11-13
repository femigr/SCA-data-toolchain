from sca_data_processing.dataset import Dataset

def create_dataset(path):
    """
    Creates a dataset from a given path.
    """

    return Dataset(path)

def get_src_file_paths(result_path):
    """
    Returns the paths to the source files affected in the issues in the given result file.
    """

    paths = set()

    for issue in Dataset(result_path).get_issues():
        for location in issue.locations:
            paths.add(location['file'])
    return paths