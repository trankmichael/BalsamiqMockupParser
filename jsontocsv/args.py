import argparse

__author__ = 'mtran'


def get_args():
    parser = argparse.ArgumentParser(prog='Preference Mockup Utils')
    parser.add_argument(
        '--action', '-a', choices=['generate', 'compare'],
        help='compare a mockup and a valid csv or just generate the mockup '
             'csv given a balsamiq mockup', required=True)
    parser.add_argument(
        '--input', '-i', type=str, help='JSON input Mockup file', required=True)
    parser.add_argument(
        '--output', '-o', type=str, help='CSV output file', required=True)
    parser.add_argument(
        '--spreadsheet', '-s', type=str, help='Correct CSV file',
        required=False)
    args = parser.parse_args()
    if args.action == 'compare' and not args.spreadsheet:
        parser.error('--generate can only be down when a spreadsheet is '
                     'specified')
    return args.input, args.output, args.spreadsheet, args.action