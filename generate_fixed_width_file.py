# -*- coding: utf-8 -*-

import random
import string
import spec_inspector
import sys


class Generate_Fixed_Width_File:
    spec_data = None
    column_names = None
    offsets = None
    fixed_width_encoding = "windows-1252"
    include_header = True
    delimited_encoding = "utf-8"
    
    
    def __init__(self, spec_data):
        self.spec_data = spec_data
        self.column_names = self.get_column_names()
        self.offsets = self.get_offsets()

    
    def get_column_names(self):
        return self.spec_data["ColumnNames"]
        

    def get_offsets(self):
        return self.spec_data["Offsets"]


    def get_column_len(self):
        return len(self.get_column_names())


    def get_offsets_len(self):
        return len(self.get_offsets())
    

    def compare_before_writing_file(self):
        if self.get_column_len() == self.get_offsets_len():
            print("There is a corresponding offset for each column. Proceeding..")
            return True
        else:
            return False
            
    
    
    def create_fixed_width_file(self):
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
        random_content = []
        content_to_be_written_to_file = []
        #lets write the headers first
        if self.include_header:
            header_str = "".join("%*s" % i for i in zip(tuple(offset_values),tuple(column_values)))
            content_to_be_written_to_file.append(header_str)
        
        #lets write 100 records to the file
        for i in range(100):
            for each in offset_values:
                content = "".join(random.choices(string.ascii_lowercase,k = each-3 if each > 5 else each))
                random_content.append(content)
            content_str = "".join("%*s" % i for i in zip(tuple(offset_values),tuple(random_content)))
            content_to_be_written_to_file.append(content_str)
        self.write_to_file(content_to_be_written_to_file)

        
    def write_to_file(self,content):
        with open("my_data.fwf",'w') as f:
            for item in content:
                f.write("%s\n" % item)
 
            
spec_data = spec_inspector.read_spec_file("spec.json")
p = Generate_Fixed_Width_File(spec_data)
p.create_fixed_width_file()