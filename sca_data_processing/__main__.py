import sca_data_processing.api as sca
import argparse

parser = argparse.ArgumentParser(description='Create an SCA dataset.')
parser.add_argument('command', metavar='command', type=str,
                    help='the command: "none", "get_src_paths"')
parser.add_argument('path', metavar='path', type=str,
                    help='the path of the base folder for the data')

args = parser.parse_args()

if args.command == "get_src_paths":
    paths = sca.get_src_file_paths("../sca-data/rolldice")
    for path in paths:
        print(path)

elif args.command == "none":
    sca_data = sca.create_dataset(args.path)
    print(sca_data)


    print(len(sca_data.new_issues))
    print(len(sca_data.old_issues))
    # severities are {'information', 'error', 'recommendation', 'warning'}

    severities = {'information': [], 'error': [], 'recommendation': [], 'warning': []}

    for issue in sca_data.old_issues:
        severities[issue.severity].append(issue)

    for severity in severities:
        print(severity + " " + str(len(severities[severity])))

else:
    print("Unknown command: " + args.command)