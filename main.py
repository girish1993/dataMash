# -*- coding: utf-8 -*-

from spec_inspector import Inspect_file
from generate_fixed_width_file import Generate_Fixed_Width_File
from file_parser import Parse_File

if __name__== "__main__":
    print("Stage 1 : Reading the specifcation file ...")
    read_data = Inspect_file()
    spec_data = read_data.read_spec_file("spec.json")
    
    print("Stage 2 : Generating the fixed width file ..")
    g = Generate_Fixed_Width_File(spec_data)
    g.create_fixed_width_file()
    
    print("Stage 3: Parsing the fixed width file and writing to csv ")
    p = Parse_File(spec_data)
    p.read_file_by_line('my_data.fwf')
    p.slice_by_offsets()