__author__ = 'mtran'
from csv import DictReader
import re

def match_and_compare(mockup, spreadsheet):
    valid = __csv_to_list_of_dicts(spreadsheet)
    missing, labeled_wrong, extra, updated_mock = __compare(mockup, valid)
    print_report(missing, labeled_wrong, extra)
    return updated_mock

def __csv_to_list_of_dicts(spreadsheet):
    with open(spreadsheet) as valid:
        reader = DictReader(valid, skipinitialspace=True)
        dict_list = [{k: v for k, v in row.items()}
                     for row in reader]
    return dict_list

def __compare(mockup, valid):
    valid_prefs = [x['PREF_CODE'] for x in valid]
    valid_prefs = sorted(valid_prefs)
    mockup = sorted(mockup, key=lambda k: k['name'])
    missing_from_mockup = []
    labeled_wrong = []

    i = 0
    j = 0

    while j < len(valid_prefs) and i < len(mockup):
        pref_name = valid_prefs[j]
        mock_name = mockup[i]['name']
        if mock_name == pref_name:
            i += 1
            j += 1
        else:
            index, diff = __fuzzy_find_difference_in_list(pref_name, [x['name']
                                                                    for x
                                                                    in mockup])
            if diff:
                labeled_wrong.append((mockup[index]['name'], pref_name))
                mockup[index]['name'] = pref_name
            elif index < 0:
                missing_from_mockup.append(pref_name)
            j += 1
    extra = list(set([x['name'] for x in mockup]) - set(valid_prefs))
    return missing_from_mockup, labeled_wrong, extra, mockup


def print_report(missing, labeled, extra):
    print("-------- possibly missing from mockup --------")
    for pref in missing:
        print("    - " + pref)
    print("-------- incorrectly named preferences --------")
    for pref in labeled:
        print("    - " + pref[0] + " should be " + pref[1])
    print("-------------- extras in mockup ---------------")
    for pref in extra:
        print("    - " + pref)

def __fuzzy_find_difference_in_list(name, pref_list):
    i = 0
    tag = re.split("PREF_([A-Z]*)", name)[2]
    for pref in pref_list:
        if re.split("PREF_([A-Z]*)", pref)[2] == tag:
            if (pref != name):
                return i, True
            else:
                return i, False
        i += 1
    return -1, False
