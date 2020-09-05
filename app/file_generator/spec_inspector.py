#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import json
import sys
import re

class Inspect_file:
    
    spec_data = None        
    
    def read_spec_file(self,path):
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
                self.spec_data = json.load(file)
        except FileNotFoundError:
            raise Exception("The file cannot be found in the specified location")
    
        if self.check_spec_file_fields() and self.check_spec_field_values():
            self.spec_data["Offsets"] = self.get_int_offset_values(self.spec_data["Offsets"])
            return self.spec_data
        else:
            sys.exit()
            
            
    def check_spec_file_fields(self):
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
        if (set(self.spec_data.keys()).issubset(set(expected_list_of_fields))) or (set(self.spec_data.keys()).intersection(set(expected_list_of_fields)) == set(['ColumnNames', 'Offsets'])):
            print("The spec file has all the expected attributes. Proceeding with further processing..")
        else:
            raise AttributeError("The provided spec file does not have the necessary attributes for further processing.")
            flag = False
        return flag
    
        
    def check_spec_field_values(self):
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
        
        column_names = self.spec_data["ColumnNames"]
        offset_values = self.spec_data["Offsets"]
        
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
        
    
    def get_int_offset_values(self,offset_values):
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
