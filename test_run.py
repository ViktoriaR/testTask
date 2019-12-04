import pytest
import json
import os
from run import *
import run

file = os.path.join('test_files', 'El_Palacio_de_Hierro_RSX_7.7_Invoices_to_X12_5010_Transaction-810.json')


def test_add_element_not_present():
    elements['elements with source'] = []
    element = {'Source': 'RSX_7.7_Invoices', 'Destination': 'X12_4010_Transaction-810', 'ElementPath': 'Segment-BIG/BIG01', 'SourcePath': 'Invoice/Header/InvoiceHeader/InvoiceDate', 'Occurrence': 1}
    add_element(element)
    assert len(elements['elements with source']) == 1 and elements['elements with source'][0].get('Occurrence') == 1


def test_add_element_present():
    elements['elements with source'] = []
    element = {'Source': 'RSX_7.7_Invoices', 'Destination': 'X12_4010_Transaction-810', 'ElementPath': 'Segment-BIG/BIG01', 'SourcePath': 'Invoice/Header/InvoiceHeader/InvoiceDate', 'Occurrence': 1}
    elements['elements with source'].append(element)
    add_element(element)
    assert len(elements['elements with source']) == 1 and elements['elements with source'][0].get('Occurrence') == 2


def test_add_element_other_element_present():
    elements['elements with source'] = []
    element1 = {'Source': 'RSX_7.7_Invoices', 'Destination': 'X12_4010_Transaction-810', 'ElementPath': 'Segment-BIG/BIG01', 'SourcePath': 'Invoice/Header/InvoiceHeader/InvoiceDate', 'Occurrence': 1}
    element2 = {'Source': 'RSX_7.7_Invoices', 'Destination': 'X12_5010_Transaction-810', 'ElementPath': 'Segment-BIG/BIG01', 'SourcePath': 'Invoice/Header/InvoiceHeader/InvoiceDate', 'Occurrence': 1}
    elements['elements with source'].append(element1)
    add_element(element2)
    assert len(elements['elements with source']) == 2 and elements['elements with source'][0].get('Occurrence') == 1 and elements['elements with source'][1].get('Occurrence') == 1


def test_parse_data(mocker):
    mocker.patch('run.find_children')

    with open(file) as json_file:
        data_in_file = json.load(json_file)
        parse_data(data_in_file)

    run.find_children.assert_called_once_with('', data_in_file, 'RSX_7.7_Invoices', 'X12_5010_Transaction-810')


def test_find_children_with_sourcing(mocker):
    mocker.patch('run.add_element')
    with open(file) as json_file:
        data_in_file = json.load(json_file)

    find_children('/Segment-BIG',data_in_file.get('children')[0], 'RSX_7.7_Invoices', 'X12_5010_Transaction-810')
    element = {'Source': 'RSX_7.7_Invoices', 'Destination': 'X12_5010_Transaction-810', 'ElementPath': 'Segment-BIG/BIG01', 'SourcePath': 'Invoice/Header/InvoiceHeader/InvoiceDate', 'Occurrence': 1}
    run.add_element.assert_called_once_with(element)


def test_find_children_no_with_children(mocker):
    mocker.patch('run.find_children')
    with open(file) as json_file:
        data_in_file = json.load(json_file)

    find_children('',data_in_file, 'RSX_7.7_Invoices', 'X12_5010_Transaction-810')
    run.find_children.assert_called_with('/Segment-BIG',data_in_file.get('children')[0], 'RSX_7.7_Invoices', 'X12_5010_Transaction-810')


def test_main():
    file_name = 'test_result.json'
    main('test_files', file_name)
    expected_result = open('test_result_expected.json', 'r')
    file = open(file_name, 'r')
    assert json.load(file) == json.load(expected_result)

