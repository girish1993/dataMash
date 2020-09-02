# -*- coding: utf-8 -*-

import random
import string
import spec_inspector
import sys


class Generate_Fixed_Width_File:
    
    #constants representing the keys
    KEY_COLUMN_NAMES = "ColumnNames"
    KEY_OFFSET_VALUES = "Offsets"
    KEY_ENCODING_TYPE = "FixedWidthEncoding"
    KEY_INCLUDE_HEADER = "IncludeHeader"
    
    #instance variables to hold the values.
    spec_data = None
    column_names = None
    offsets = None
    
    #default values if not supplied in the specifications
    fixed_width_encoding = "windows-1252"
    include_header = "True"

    
    
    def __init__(self, spec_data):
        """
        Constructor to initialise the specification data for creation of the fixed width file

        Parameters
        ----------
        spec_data : The checked specification data that meets the compalinace measures

        Returns
        -------
        None.

        """
        
        self.spec_data = spec_data
        self.column_names = self.get_column_names()
        self.offsets = self.get_offsets()

    
    def get_column_names(self):
        """
        Getter method to get the column names

        Returns
        -------
        A list of column names

        """
        return self.spec_data[self.KEY_COLUMN_NAMES]
        

    def get_offsets(self):
        """
        Getter method for offsets

        Returns
        -------
        A list of offset values.

        """
        
        return self.spec_data[self.KEY_OFFSET_VALUES]
    
    
    def get_encoding_type(self):
        """
        Getter method for encoding

        Returns
        -------
        String
            specified encoding type if present, if not, the default.

        """
        
        if self.KEY_ENCODING_TYPE in self.spec_data:
            return self.spec_data[self.KEY_ENCODING_TYPE]
        return self.fixed_width_encoding
        
    
    def get_include_header(self):
        """
        Method to get the header information.

        Returns
        -------
        String
            True if the header is to be included, False otherwise.

        """
        
        if self.KEY_INCLUDE_HEADER in self.spec_data:
            return self.spec_data[self.KEY_INCLUDE_HEADER]
        return self.include_header


    def get_column_len(self):
        """
        Method to get the length of column values

        Returns
        -------
        number of column values.

        """
        return len(self.get_column_names())


    def get_offsets_len(self):
        """
        Method to get the length of offset values

        Returns
        -------
        number of offset values in the list.

        """
        
        return len(self.get_offsets())
    

    def compare_before_writing_file(self):
        """
        A utility method that checks if there are offsets for each of the 
        columns.

        Returns
        -------
        bool 
            True if the sizes of offsets and column names are equal and
        False otherwise.

        """
        
        if self.get_column_len() == self.get_offsets_len():
            print("There is a corresponding offset for each column. Proceeding..")
            return True
        else:
            return False
            
    
    
    def create_fixed_width_file(self):
        """
        Method to create a fixed width file.

        Raises
        ------
        Exception
            if there is a mismatch between the number of columns and their
            corresponding offsets.

        Returns
        -------
        None.

        """
        
        if self.compare_before_writing_file():
            column_values = tuple(self.get_column_names())
            offset_values = tuple(self.get_offsets())
            self.create_random_data_write_to_file(offset_values, column_values, 
                                    self.get_offsets_len(), 
                                    self.get_column_len())
        else:
            raise Exception("There is a mismatch between the number of columns and their corresponding offsets. Aborting.")
            sys.exit()
            
        
    def create_random_data_write_to_file(self,offset_values, column_values, offset_values_len, column_values_len):
        """
        Method to create random generated data to populate the files.

        Parameters
        ----------
        offset_values : list
            list of offset for each column.
        column_values : list
            list of column names.
        offset_values_len : int
            length of the list of offset list.
        column_values_len : int
            length of the list of column values.

        Returns
        -------
        None.

        """
        
        random_content = []
        content_to_be_written_to_file = []
        
        if self.get_include_header().lower() == "True":                        
            header_str = "".join("%*s" % i for i in zip(tuple(offset_values),tuple(column_values)))
            content_to_be_written_to_file.append(header_str)
        
        #lets write 100 records to the file
        for i in range(100):
            for each in offset_values:
                
                # leaving some whitespace on purpose and reducing the size of the string.
                content = "".join(random.choices(string.ascii_lowercase,k = each-3 if each > 5 else each))
                random_content.append(content)
            
            content_str = "".join("%*s" % i for i in zip(tuple(offset_values),tuple(random_content)))
            content_to_be_written_to_file.append(content_str)
        self.write_to_file(content_to_be_written_to_file)


        
    def write_to_file(self,content):
        """
        Method to write contents to a file.

        Parameters
        ----------
        content : list
            list of randomly generated strings.

        Returns
        -------
        None.

        """
        
        with open("my_data.fwf",'w',encoding=self.get_encoding_type()) as f:
            for item in content:
                f.write("%s\n" % item)
