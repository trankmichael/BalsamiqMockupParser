import json

__author__ = 'mtran'


def clean_extract(json_input):
    pref_list = read_input(json_input)
    pref_list = main_control_group(pref_list)
    pref_list = inner_group_pref_data(pref_list)
    pref_list = sort_and_index(pref_list)
    return pref_list


def read_input(json_input):
    with open(json_input) as data_file:
        pref_list = json.load(data_file)
    return pref_list


def main_control_group(pref_list):
    return pref_list['mockup']['controls']['control']


def inner_group_pref_data(control, coords=(0, 0)):
    pref_list = []
    pref = {'name': '', 'type': '', 'summary': '', 'default_val': '',
            'location': (0, 0)}

    for obj in control:
        if is_group(obj):
            coords = extend_list(pref_list, obj, coords)
        else:
            pref = update_pref_data(obj, pref, coords)
    if pref['name'] != '':
        pref_list.append(pref)
    return pref_list


def extend_list(pref_list, obj, coordinates):
    coordinates = add_coords(coordinates, obj)
    pref_list.extend(inner_group_pref_data(obj['children']['controls'][
                                               'control'], coordinates))
    coordinates = subtract_coords(coordinates, obj)
    return coordinates


def update_pref_data(i, pref, coordinates):
    if i['typeID'] == 'CallOut':
        pref['name'] = get_text(i)
        pref['location'] = add_coords(coordinates, i)
    elif 'typeID' in i:
        if i['typeID'] == "CheckBox":
            return handle_checkbox(i, pref)
        elif i['typeID'] == "Label":
            return handle_label(i, pref)
        elif i['typeID'] == 'TextInput':
            return handle_textbox(i, pref)
        elif i['typeID'] == 'List':
            return handle_listbox(i, pref)
    return pref


def handle_listbox(i, pref):
    pref['type'] = 99
    if 'properties' in i and 'text' in i['properties']:
        pref['default_val'] = get_text(i)
    return pref


def handle_textbox(i, pref):
    pref['type'] = 1
    if 'properties' in i and 'text' in i['properties']:
        pref['default_val'] = get_text(i)
    return pref


def handle_label(i, pref):
    pref['summary'] = get_text(i)
    return pref


def handle_checkbox(i, pref):
    pref['summary'] = get_text(i)
    pref['type'] = 3
    if 'state' in i['properties']:
        if i['properties']['state'] == 'selected':
            pref['default_val'] = 'Y'
        else:
            pref['default_val'] = 'N'
    else:
        pref['default_val'] = 'N'
    return pref


def get_text(i):
    return i['properties']['text']


def sort_and_index(pref_list):
    pref_list = sort_from_top_left(pref_list)
    pref_list = index_with_buffer(pref_list)
    return pref_list


def index_with_buffer(pref_list):
    i = 1
    j = 0
    for pref in pref_list:
        if j == 5:
            i += 5
            j = 0
        pref['index'] = i
        i += 1
        j += 1
    return pref_list


def sort_from_top_left(pref_list):
    pref_list = sorted(pref_list, key=lambda k: k['location'][1])
    for pref in pref_list:
        pref['column'] = pref['location'][0] // 1000
    pref_list = sorted(pref_list, key=lambda k: k['column'])
    return pref_list


def is_group(obj):
    return obj['typeID'] == '__group__'


def add_coords(x_y, i):
    new_x = x_y[0] + int(i['x'])
    new_y = x_y[1] + int(i['y'])
    return (new_x, new_y)


def subtract_coords(x_y, i):
    new_x = x_y[0] - int(i['x'])
    new_y = x_y[1] - int(i['y'])
    return (new_x, new_y)
