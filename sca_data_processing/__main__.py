import sca_data_processing.api as sca
import argparse

parser = argparse.ArgumentParser(description='Create an SCA dataset.')
parser.add_argument('path', metavar='path', type=str,
                    help='the path of the base folder for the data')

args = parser.parse_args()


print(args.path)

print(sca.get_src_file_paths("../sca-data/rolldice"))


sca_data = sca.create_dataset(args.path)
print(sca_data)


print(len(sca_data.new_issues))
print(len(sca_data.old_issues))
# severities = {'information', 'error', 'recommendation', 'warning'}

severities = {'information': [], 'error': [], 'recommendation': [], 'warning': []}

for issue in sca_data.old_issues:
    severities[issue.severity].append(issue)

for severity in severities:
    print(severity + " " + str(len(severities[severity])))

