import sca_data_processing.api as sca
import argparse

parser = argparse.ArgumentParser(description='Create an SCA dataset.')
parser.add_argument('path', metavar='path', type=str,
                    help='the path of the base folder for the data')

args = parser.parse_args()


print(args.path)



sca_data = sca.create_dataset(args.path)
print(sca_data)