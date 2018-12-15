#===============================================================================
# search.py
#===============================================================================

"""Integration with sqlite3 FTS4 tables"""




# Imports ======================================================================

import sqlite3

from flask import current_app
from ucsd_bisb_unofficial.models import Post




# Functions ====================================================================

def validate_table_name(cursor, source_db_name, table_name):
    if table_name not in {
        tup[0] for tup in cursor.execute(
            f"SELECT name FROM {source_db_name}.sqlite_master "
            "WHERE type='table'"
        )
    }:
        raise ValueError('Invalid table name')


def validate_column_names(cursor, source_db_name, table_name, *column_names):
    cursor.execute(f'select * from {source_db_name}.{table_name}')
    if not set(column_names) <= {tup[0] for tup in cursor.description}:
        raise ValueError('Invalid column names')


def fts4_search(table, query, body=None):
    conn = sqlite3.connect(':memory:')
    c = conn.cursor()
    source_db_name = 'source'
    c.execute(
        f'ATTACH ? AS {source_db_name}',
        (current_app.config['SQLALCHEMY_DATABASE_URI'],)
    )
    validate_table_name(c, source_db_name, table)
    validate_column_names(c, source_db_name, table, *Post.__searchable__)
    c.execute(
        f"CREATE VIRTUAL TABLE {table} USING "
        f"fts4({', '.join(Post.__searchable__)})"
    )
    c.execute(
        f"INSERT INTO {table}(docid, {', '.join(Post.__searchable__)}) "
        f"SELECT id, {', '.join(Post.__searchable__)} "
        f"FROM {source_db_name}.{table}"
    )
    hits = c.execute(
        f"SELECT docid, {', '.join(Post.__searchable__)} FROM {table} "
        f"WHERE {table} MATCH ?",
        (f"'{' OR '.join(f'{col}:{query}' for col in Post.__searchable__)}'",)
    ).fetchall()
    return {
        'hits': {'total': len(hits), 'hits': {{'_id': hit[0]} for hit in hits}}
    }


def search_results(search):
    ids = [int(hit['_id']) for hit in search['hits']['hits']]
    return ids, search['hits']['total']


def query_index(index, query, page, per_page):
    search = fts4_search(table=index, query=query)
    return search_results(search)
