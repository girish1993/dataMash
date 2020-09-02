# -*- coding: utf-8 -*-


import csv
import sys



class Parse_File:
    KEY_OFFSET_VALUES = "Offsets"
    KEY_COLUMN_NAMES = "ColumnNames"
    FILE_PATH = "my_data.csv"
    KEY_DELIMITED_ENCODING = "DelimitedEncoding"
    
    content = None
    offsetted_content_list = []
    delimited_encoding = "utf-8"
    
    def __init__(self, spec_data):
        """
        Constructor for the Parse_File

        Parameters
        ----------
        spec_data : json object specification
            specification object described.

        Returns
        -------
        None.

        """
        
        self.spec_data = spec_data
        self.offset_values = spec_data[self.KEY_OFFSET_VALUES]
        self.column_names = spec_data[self.KEY_COLUMN_NAMES]
        
        
    def get_delimited_encoding(self):
        """
        Method to get the delimiting type for writing contents to a file

        Returns
        -------
        String
            encoding type for writing to csv file.

        """
        
        if self.KEY_DELIMITED_ENCODING in self.spec_data:
            return self.spec_data[self.KEY_DELIMITED_ENCODING]
        return self.delimited_encoding
        
        
    def read_file_by_line(self,path):
        """
        Method to read the contents of the file by line

        Parameters
        ----------
        path : String
            path to the csv file.

        Raises
        ------
        Exception
            In relation to access of the file.

        Returns
        -------
        None.

        """
        
        try:
            with open(path) as f:
                self.content = f.readlines()
        except FileNotFoundError:
            raise Exception("The file is not present at the specified location.")
            
           
    def slice_by_offsets(self):
        """
        Utility method to slice string content through offsets.
        
        Returns
        -------
        None.

        """
        
        for each_line in self.content:
            each_line_content = self.get_offsetted_content_list(each_line)
            self.offsetted_content_list.append(each_line_content)
        self.write_to_csv_file(self.FILE_PATH)
            
        
    def get_offsetted_content_list(self, each_line):
        """
        method to slice the line content in accordance to respective offsets.

        Parameters
        ----------
        each_line : String
            each line content read from the file.

        Returns
        -------
        each_line_content : list
            list of sliced and stripped susbtrings.

        """
        
        counter = 0
        each_line_content = []
        for each_offset in self.offset_values:
            each_line_content.append(each_line[counter:each_offset+counter].strip())
            counter += each_offset
        return each_line_content
        
    
    def write_to_csv_file(self,path):
        """
        Method to write the contents to a csv file

        Parameters
        ----------
        path : String
            Path to the csv file.

        Raises
        ------
        IOError
            Exception when the write operation terminates unsuccessfully.

        Returns
        -------
        None.

        """
        
        try:
            with open(path,'w+',newline='',encoding=self.get_delimited_encoding()) as f:
                write = csv.writer(f)
                write.writerows(self.offsetted_content_list)
        except:
            raise IOError("The write operation failed.")
            sys.exit()
