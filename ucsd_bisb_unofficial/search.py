#===============================================================================
# search.py
#===============================================================================

"""Integration with sqlite3 FTS4 tables"""




# Imports ======================================================================

import sqlite3

from flask import current_app




# Functions ====================================================================

def fts4_search(table, query, per_page):
    
    return search

def query_index(index, query, page, per_page):
    if not current_app.fts4:
        return [], 0
    search = fts4_search(
        table=index,
        body={
            'query': {'multi_match': {'query': query, 'fields': ['*']}},
            'from': (page - 1) * per_page, 'size': per_page
        }
    )
    ids = [int(hit['_id']) for hit in search['hits']['hits']]
    return ids, search['hits']['total']
