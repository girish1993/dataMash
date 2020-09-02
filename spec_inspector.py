#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Sep  1 16:08:58 2020

@author: girishbhatta
"""
import json
import sys
import re


def read_spec_file(path):
    """
    function to read the specification file in json format. 

    Parameters
    ----------
    path : Location to the file.

    Raises
    ------
    Exception
        When the specified location is incorrect.
    AttributeError
        When the spec file does not have atleast "ColumnName" and "Offset" keys.

    Returns
    -------
    spec_data : a json object.

    """
    
    try:
        with open(path) as file:
            spec_data = json.load(file)
    except FileNotFoundError:
        raise Exception("The file cannot be found in the specified location")

    if check_spec_file_fields(spec_data) and check_spec_field_values(spec_data):
        spec_data["Offsets"] = get_int_offset_values(spec_data["Offsets"])
        return spec_data
    else:
        sys.exit()
        
        
def check_spec_file_fields(spec_data):
    """
    Function to check the validity and minimum requirements of the details mentioned in the specifications file.

    Parameters
    ----------
    spec_data : a dictionary of the specification.

    Returns
    -------
    flag : True if the specification object has all the minimum necessary field names or False otherwise.

    """
    
    flag = True
    expected_list_of_fields = ['ColumnNames', 'Offsets', 'FixedWidthEncoding',
                               'IncludeHeader', 'DelimitedEncoding']
    if (set(spec_data.keys()) == set(expected_list_of_fields)) or (set(spec_data.keys()).intersection(set(expected_list_of_fields)) == set(['ColumnNames', 'Offsets'])):
        print("The spec file has all the expected attributes. Proceeding with further processing..")
    else:
        raise AttributeError("The provided spec file does not have the necessary attributes for further processing.")
        flag = False
    return flag

    
def check_spec_field_values(spec_data):
    """
    Function to check the validity of the field values.

    Parameters
    ----------
    spec_data : a dictionary of the specification which has passed through the validity of key values.

    Returns
    -------
    isValid: True if the field values are complying and False otherwise.

    """
    isValid = True
    
    column_names = spec_data["ColumnNames"]
    offset_values = spec_data["Offsets"]
    
    column_values_regex = re.compile('[+@!#$%^&*()<>?/\|}{~:]')
    offset_values_regex = re.compile('^([\d]+)$')
    
    #checking for column values
    for each_column_value in column_names:
        if column_values_regex.match(each_column_value):
            isValid = False
            raise ValueError("A Column name can only have alphanumeric characters with '_' included.")
                  
    #checking for offset values
    for each_offset_value in offset_values:
        if not offset_values_regex.match(each_offset_value):
            isValid = False
            raise ValueError("An Offset value should only contain positive integers.") 
    
    return isValid
    

def get_int_offset_values(offset_values):
    """
    Function to convert the list of string represenation of offset values to integers

    Parameters
    ----------
    offset_values : list of offset values

    Returns
    -------
    list : integer list of offset values.

    """
    
    return [int(each_value) for each_value in offset_values]

spec_data = read_spec_file("spec.json")