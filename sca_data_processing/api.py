from sca_data_processing.dataset import Dataset
import sca_data_processing.helpers as helpers
from tqdm import tqdm
import multiprocessing as mp
import os

def create_dataset(path, verbose = False):
    """
    Creates a dataset from a given path.
    """

    return Dataset(path, verbose)

def get_fixed_dataset(dataset):
    """
    Returns a dataset with only fixed issues.
    """
    dataset_new = Dataset()
    dataset_new.old_issues, dataset_new.old_issue_classes = dataset.get_filtered_issues() #not nice, sorry
    return dataset_new

def get_src_file_paths(result_path):
    """
    Returns the paths to the source files affected in the issues in the given result file.
    """

    paths = set()

    for issue in Dataset(result_path).get_issues():
        for location in issue.locations:
            paths.add(location['file'])
    return paths

def get_fully_scanned_packages(path):
    """
    Returns a list of fully scanned packages.
    """
    packages = helpers.get_full_package_files(path)

    return [p['name'] for p in packages]

def get_issues_by_rules(path):
    sca_data = create_dataset(path)

    rules = {}

    for issue in sca_data.get_issues():
        if issue.rule not in rules.keys():
            rules.update({issue.rule: []})
        rules[issue.rule].append(issue)

    return rules

def generate_dataset(path, dest_path, filtered):
    print("Parsing meta-data...")
    sca_data = create_dataset(path, verbose = True)
    if filtered:
        print("Using only filtered issues")
        sca_data = get_fixed_dataset(sca_data)
    
    print("Parsed meta-data, generating output...")
    
    for issue_class in sca_data.get_issue_classes():
        if not os.path.exists(os.path.join(dest_path, issue_class)):
            os.mkdir(os.path.join(dest_path, issue_class))

    pbar = tqdm(total=len(sca_data.get_issues()))
    def update(*a): # acts as a callback for the mp pool, updates the progress bar, takes params because no return value will also be returned by the pool
        pbar.update()

    pool = mp.Pool(1) #mp.cpu_count()) #set to 1 to debug #TODO
    jobs = [pool.apply_async(issue.write_to_file,
                args=(dest_path, path),
                callback=update) 
                for issue in sca_data.get_issues()]
    pool.close()
    pool.join()
    for job in jobs:
        if not job._success:
            raise job._value
