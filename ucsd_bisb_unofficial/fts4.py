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
    cursor.execute(f'SELECT * FROM {source_db_name}.{table_name}')
    if not set(column_names) <= {tup[0] for tup in cursor.description}:
        raise ValueError('Invalid column names')


def table_is_indexed(cursor, table_name):
    return table_name in {
        tup[0] for tup in cursor.execute(
            "SELECT name FROM main.sqlite_master WHERE type='table'"
        )
    }


def searchable_columns(cursor, table_name):
    cursor.execute(f'SELECT * FROM main.{table_name}')
    return tuple(tup[0] for tup in cursor.description)


def fts4_index(table, id, searchable):
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
    validate_column_names(c, source_db_name, table, *searchable)
    if not table_is_indexed(c, table):
        c.execute(
            f"CREATE VIRTUAL TABLE {table} USING fts4({', '.join(searchable)})"
        )
    c.execute(f'DELETE FROM {table} WHERE docid = ?', (id,))
    c.execute(f"""
        INSERT INTO {table}(docid, {', '.join(searchable)})
        SELECT id, {', '.join(searchable)}
        FROM {source_db_name}.{table}
        WHERE id = ?
        """,
        (id,)
    )
    current_app.fts4.commit()
    c.execute('DETACH ?', (source_db_name,))


def fts4_delete(table, id):
    c = current_app.fts4.cursor()
    validate_table_name(c, 'main', table)
    c.execute(f'DELETE FROM {table} WHERE id = ?', (id,))


def fts4_search(table, query, page, per_page):
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
    c.execute('DETACH ?', (source_db_name,))
    searchable = searchable_columns(c, table)
    hits = tuple(
        tup[0] for tup in c.execute(
            f'SELECT docid FROM {table} WHERE {table} MATCH ?',
            (' OR '.join(f'{col}:{query}' for col in searchable),)
        )
    )
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
    fts4_index(table=index, id=model.id, searchable=model.__searchable__)
    

def remove_from_index(index, model):
    if not current_app.fts4:
        return
    fts4_delete(table=index, id=model.id)


def query_index(index, query, page, per_page):
    if not current_app.fts4:
        return [], 0
    search = fts4_search(table=index, query=query, page=page, per_page=per_page)
    return search_results(search)
