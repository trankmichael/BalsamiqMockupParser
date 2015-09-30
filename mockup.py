from jsontocsv.args import get_args
from jsontocsv.compare import match_and_compare
from jsontocsv.parse import clean_extract
from jsontocsv.spreadsheet import generate_csv

__author__ = 'mtran'

import sys

def main(argv):
    input, output, compare, action = get_args()
    mock = clean_extract(input)
    if action == 'compare':
        mock = match_and_compare(mock, compare)
    generate_csv(mock, output)


if __name__ == "__main__":
    main(sys.argv)
