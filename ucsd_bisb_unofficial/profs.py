#===============================================================================
# profs.py
#===============================================================================

"""BISB faculty database"""




# Imports ======================================================================

import csv

from pytablewriter import MarkdownTableWriter




# Functions ====================================================================

def markdown_table(csv_file_path: str):
    writer = MarkdownTableWriter()
    with open(csv_file_path, 'r') as f:
        writer.header_list = f.readline().rstrip().split(',')
        writer.value_matrix = list(csv.reader(f))
    return writer.dumps()
