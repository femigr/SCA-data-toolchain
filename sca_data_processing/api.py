from sca_data_processing.dataset import Dataset
from sca_data_processing.helpers import *



def create_dataset(path):
    """
    Creates a dataset from a given path.
    """
    dataset = Dataset()

    packages = get_full_package_files(path)

    for package in packages:
        dataset.add_package(package)

    return dataset