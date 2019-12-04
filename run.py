import json
import os

data_in_files = []
elements = {}
elements['elements with source'] = []


def parse_data(data_in_file):
    source = data_in_file.get('designMeta').get('hiddenSchema')
    target = data_in_file.get('designMeta').get('viewedSchema')
    source_info = '{}_{}_{}'.format(source.get('format'), source.get('version'), source.get('document'))
    target_info = '{}_{}_{}'.format(target.get('format'), target.get('version'), target.get('document'))
    find_children('', data_in_file, source_info, target_info)


def find_children(parent_name, parent, source_info, target_info):
    for child in parent.get('children'):
        name = '{}/{}'.format(parent_name, child.get('name'))
        if child.get('sourcing') is not None:
            element = {'Source': source_info, 'Destination': target_info, 'ElementPath': name[1:], 'SourcePath': child.get('sourcing').get('location'), 'Occurrence': 1}
            add_element(element)
        if child.get('children') is not None:
            find_children(name, child, source_info, target_info)


def add_element(element):
    is_present = False
    for target in elements['elements with source']:
        if element.get('Source') == target.get('Source') and element.get('Destination') == target.get('Destination') and element.get('ElementPath') == target.get('ElementPath') and element.get('SourcePath') == target.get('SourcePath'):
            target['Occurrence'] = target.get('Occurrence') + 1
            is_present = True
    if not is_present:
        elements['elements with source'].append(element)


directory = 'files'
for filename in os.listdir(directory):
    if filename.endswith(".json"):
        with open(os.path.join(directory, filename)) as json_file:
            data_in_files.append(json.load(json_file))


for data_in_file in data_in_files:
    parse_data(data_in_file)

with open('result.json', 'w') as result_file:
    result_file.write(json.dumps(elements, indent=4 ))

