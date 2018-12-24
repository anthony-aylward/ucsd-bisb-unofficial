#===============================================================================
# fts4.py
#===============================================================================

"""Integration with sqlite3 FTS4 tables"""




# Imports ======================================================================

from flask import current_app




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


def fts4_search(table, query, page, per_page):
    __searchable__ = ('body',)
    c = current_app.fts4.cursor()
    source_db_name = 'source'
    c.execute(
        f'ATTACH ? AS ?',
        (
            current_app.config['SQLALCHEMY_DATABASE_URI'].split(':///')[1],
            source_db_name
        )
    )
    validate_table_name(c, source_db_name, table)
    validate_column_names(c, source_db_name, table, *__searchable__)
    c.executescript(f"""
        CREATE VIRTUAL TABLE {table} USING fts4(
            {', '.join(__searchable__)}
        );

        INSERT INTO {table}(docid, {', '.join(__searchable__)})
        SELECT id, {', '.join(__searchable__)}
        FROM {source_db_name}.{table};
        """
    )
    q = (' OR '.join(f'{col}:{query}' for col in __searchable__),)
    hits = tuple(
        tup[0] for tup in c.execute(
            f'SELECT docid FROM {table} WHERE {table} MATCH ?',
            q
        )
    )
    c.execute(f'DROP TABLE {table}')
    c.execute('DETACH ?', (source_db_name,))
    return {
        'hits': {
            'total': len(hits),
            'hits': tuple(
                {'_id': hit} for hit in hits[
                    (page - 1) * per_page:page * per_page
                ]
            )
        }
    }


def search_results(search):
    ids = [int(hit['_id']) for hit in search['hits']['hits']]
    return ids, search['hits']['total']


def add_to_index(index, model):
    if not current_app.fts4:
        return


def remove_from_index(index, model):
    if not current_app.fts4:
        return


def query_index(index, query, page, per_page):
    if not current_app.fts4:
        return [], 0
    search = fts4_search(table=index, query=query, page=page, per_page=per_page)
    return search_results(search)
