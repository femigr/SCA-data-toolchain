import sca_data_processing.api as sca
import matplotlib.pyplot as plt
import numpy as np
import argparse, os
import time

def dir_path(path):
    if os.path.isdir(path):
        return path
    else:
        raise NotADirectoryError(path)

parser = argparse.ArgumentParser(description='Create an SCA dataset.')
parser.add_argument('command', metavar='command', type=str,
                    help='the command: "get_metrics", "get_src_paths", "get_fully_scanned_packages"')
parser.add_argument('path', metavar='path', type=dir_path,
                    help='the path of the base folder for the data')
parser.add_argument('--dest', metavar='destination', type=dir_path,
                    help='the destination of where you want the output to go')
parser.add_argument('--filtered', '--filt', '-f', action='store_true', default=False,
                    help='if you want the data to be in the filtered state')

args = parser.parse_args()

if args.command == "get_src_paths":
    paths = sca.get_src_file_paths(args.path)
    for path in paths:
        print(path)

elif args.command == "get_metrics":
    sca_data = sca.create_dataset(args.path)
    if args.filtered:
        sca_data = sca.get_fixed_dataset(sca_data)

    print('Total amount of issues in newer versions: ', len(sca_data.new_issues))
    print('Total amount of issues in older versions: ', len(sca_data.old_issues))
    print('_______________________________________________________')
    print('Amount of issues by rule:')

    rules_severity = {'information': [], 'error': [], 'recommendation': [], 'warning': [], 'style': []}
    severities = {'information': [], 'error': [], 'recommendation': [], 'warning': [], 'style': []}
    rules = {}

    for issue in sca_data.get_issues():
        severities[issue.severity].append(issue)
        if issue.rule not in rules_severity[issue.severity]:
            rules_severity[issue.severity].append(issue.rule)
        if issue.rule + ' (%s) cwe:%s' % (issue.severity, issue.cwe) not in rules.keys():
            rules[issue.rule + ' (%s) cwe:%s' % (issue.severity, issue.cwe)] = []
        rules[issue.rule + ' (%s) cwe:%s' % (issue.severity, issue.cwe)].append(issue)

    sorted_rules = sorted(rules, key=lambda rule: len(rules[rule])*(-1))

    i=0
    for rule in sorted_rules:
        i+=1
        print(rule+': ', len(rules[rule]))
    
    print('_______________________________________________________')
    print('Amount of rules: ', i)
    print('Amount of rules by severity:')
    for severity in rules_severity:
        print(severity + ': ', len(rules_severity[severity]))
    print('_______________________________________________________')

    print('Amount of issues by severity:')
    for severity in severities:
        print(severity + ": ", len(severities[severity]))

    print('_______________________________________________________')
    print('Amount of issues by package:')

    packages = {}

    for issue in sca_data.get_issues():
        if issue.package not in packages.keys():
            packages.update({issue.package: {'information': [], 'error': [], 'recommendation': [], 'warning': [], 'style': [], 'total': 0}})
        packages[issue.package][issue.severity].append(issue)
        packages[issue.package]['total'] += 1

    sorted_packages = sorted(packages.keys(), key=lambda package: packages[package]['total']*(-1))

    i=0
    for package in sorted_packages:
        i+=1
        print(package +': ', packages[package]['total'])
    print('Total amount of fully scanned packages included: ', i)
    print('_______________________________________________________')

elif args.command == "plot":
    
    rules = sca.get_issues_by_rules(args.path)
    sorted_rules = sorted(rules, key=lambda rule: len(rules[rule]))

    criterium = lambda rule: len(rules[rule]) > 200
    labels = [rule for rule in sorted_rules if criterium(rule)]
    amount_of_issues = [len(rules[rule]) for rule in sorted_rules if criterium(rule)]

    x = np.arange(len(labels))
    width = 0.35
    fig, ax = plt.subplots()
    rects1 = ax.bar(x, amount_of_issues, width)

    # Add some text for labels, title and custom x-axis tick labels, etc.
    ax.set_ylabel('Amount of issues')
    ax.set_title('Amount of issues (>200) by rule')
    ax.set_xticks(x, labels)

    fig.tight_layout()
    plt.figure(figsize=(200,10))
    if args.dest:
        plt.savefig(args.dest + '/amount_of_issues_by_rule.png')
    else:
        plt.savefig('plots/issues_by_rule.svg', format='svg')
    
elif args.command == "get_fully_scanned_packages":
    packages = sca.get_fully_scanned_packages(args.path)
    for package in packages:
        print(package)

elif args.command == "generate_dataset":
    if args.dest is None:
        raise Exception('Please specify a destination folder: --dest FOLDER')
    print(f'Generating a processable data-set at {args.dest} ...')
    start_time = time.time()
    sca.generate_dataset(args.path, args.dest, args.filtered)
    print(f'Took {time.time() - start_time} seconds')

else:
    print("Unknown command: " + args.command)