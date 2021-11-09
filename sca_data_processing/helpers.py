import os

old_postfix = '_12_04'
new_postfix = '_21_04'
file_extensions = ['.xml', '.sarif']
amount_of_scans = 2

def get_packages(path):
    """
    Get all packages (folders) in the given path.
    """
    return [name for name in os.listdir(path) if os.path.isdir('%s/%s' % (path, name))]
    
def get_files(path, package):
    """
    Get all files in the given package folder.
    """
    return os.listdir('%s/%s' % (path, package))

def get_package_files(path):
    """
    Get all paths of all files of scanned packages in the given path.
    """
    files = {}
    for package in get_packages(path):
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
            'path': '%s/%s/' % (path, name)
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