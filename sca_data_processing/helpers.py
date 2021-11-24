import os

old_postfix = '_12_04'
new_postfix = '_21_04'
file_extensions = ['.xml', '.sarif']
amount_of_scans = 2

def get_packages(path):
    """
    Get all packages (folders) in the given path. Also returns a bool that is true if the folder itself is the package.
    """
    folders = [name for name in os.listdir(path) if os.path.isdir(os.path.join(path, name))]
    if folders == []:
        filenames = ", ".join(os.listdir(path))
        for ext in file_extensions:
            if old_postfix + ext in filenames or new_postfix + ext in filenames:
                return [os.path.basename(path)], True # if the folder itself is the package
        raise Exception("No packages found in %s" % path)
    else:
        return folders, False # if the folder contains packages
    
def get_files(path, package, path_is_package = False):
    """
    Get all files in the given package folder.
    """
    return os.listdir(os.path.join(path, package))

def get_package_files(path):
    """
    Get all paths of all files of scanned packages in the given path.
    """
    files = {}
    packages, is_package_itself = get_packages(path)

    if is_package_itself:
        path = path[:-len(packages[0])-1] # remove the package name from the path including the /

    for package in packages:
        files.update({package: get_files(path, package)})
    
    packages = []
    for name in files.keys():
        package = {
            'name': name,
            'scans':
            {
                'old': [filename for filename in files[name] if match_filename(name, old_postfix, filename)],
                'new': [filename for filename in files[name] if match_filename(name, new_postfix, filename)],
            },
            'path': os.path.join(path, name) + "/"
        }
        packages.append(package)
    return packages

def get_full_package_files(path):
    """
    Get all paths of all files of completely scanned packages in the given path.
    """
    files = get_package_files(path)
    return [package for package in files if len(package['scans']['old'])== amount_of_scans and len(package['scans']['new']) == amount_of_scans]

def match_filename(packagename, postfix, filename):
    for extension in file_extensions:
        if filename == packagename + postfix + extension:
            return True
    return False