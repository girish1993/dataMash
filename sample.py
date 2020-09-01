#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Sep  1 16:08:58 2020

@author: girishbhatta
"""
import json
import sys



def read_spec_file(path):
    try:
        with open(path) as file:
            spec_data = json.load(file)
    except FileNotFoundError:
        raise Exception("The file cannot be found in the specified location")

    if check_spec_file_fields(spec_data):
        return spec_data
    else:
        raise AttributeError("The provided spec file does not have the necessary attributes for further processing.")
        sys.exit()


def check_spec_file_fields(spec_data):
    flag = True
    expected_list_of_fields = ['ColumnNames', 'Offsets', 'FixedWidthEncoding',
                               'IncludeHeader', 'DelimitedEncoding']
    if (set(spec_data.keys()) == set(expected_list_of_fields)) or (set(spec_data.keys()).intersection(set(expected_list_of_fields)) == set(['ColumnNames', 'Offsets'])):
        print("The spec file has all the expected attributes. Proceeding with further processing..")
    else:
        flag = False
    return flag

    
