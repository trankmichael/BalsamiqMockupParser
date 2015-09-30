from csv import DictWriter
import sys

__author__ = 'mtran'


def generate_csv(data, output):
    keys = ['index', 'name', 'summary', 'type', 'default_val', 'location',
            'column']
    if sys.version_info[0] == 2:
        access = 'wb'
        kwargs = {}
    else:
        access = 'wt'
        kwargs = {'newline':''}

    with open(output, access, **kwargs) as output_file:
        dict_writer = DictWriter(output_file, keys)
        dict_writer.writeheader()
        dict_writer.writerows(data)