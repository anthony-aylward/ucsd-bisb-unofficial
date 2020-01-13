#===============================================================================
# bisb_cohort_rotation_database.py
#===============================================================================

"""Class to facilitate handling the BISB Cohort Rotation google sheet"""




# Imports ======================================================================

import csv
import json

from pytablewriter import MarkdownTableWriter




# Classes ======================================================================

class RotationDatabase:
    """Compile rotation information into a table
    
    Parameters
    ----------
    csv_file_path : str
        path to a CSF file containing rotation information

    Attributes
    ----------
    header : str
        header names for the table
    dict : dict
        dictionary containing table data
    """

    def __init__(self, csv_file_path: str):
        with open(csv_file_path, 'r') as f:
            self.header = f.readline().rstrip().split(',')[1:]
            self.dict = {name: data for name, *data, in csv.reader(f)}
    
    def add_column(self, column_name: str, d: dict):
        """Add a column to the table from name and dict
        
        Parameters
        ----------
        column_name : str
            name of the column to be added
        d : dict
            dictionary containing column data
        """

        self.header.append(column_name)
        for name in self.dict.keys():
            self.dict[name].append(d.get(name, ''))
    
    def add_json(self, column_name, json_file_path: str):
        """Add a column to the table from a json file
        
        Parameters
        ----------
        json_file_path : str
            path to a JSON file containing column information
        """

        with open(json_file_path, 'r') as f:
            self.add_column(column_name, json.load(f))
    
    def markdown_table(self, *columns):
        """Export a markdown-formatted version of the table
        
        Parameters
        ----------
        *columns
            Names of columns to include in the exported table
        """

        writer = MarkdownTableWriter()
        writer.header_list = ['Name'] + (
            [self.header[col] for col in columns] if columns else self.header
        )
        writer.value_matrix = [
            [name] + (
                [self.dict[name][col] for col in columns]
                if columns else self.dict[name]
            )
            for name in sorted(self.dict.keys())
        ]
        return writer.dumps()
