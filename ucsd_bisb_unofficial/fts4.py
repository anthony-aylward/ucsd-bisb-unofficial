#===============================================================================
# fts4.py
#===============================================================================

"""Integration with sqlite3 FTS4 tables"""




# Imports ======================================================================

from flask import current_app
from ftscursor import FTSCursor




# Functions ====================================================================

# Functions for the flask-fts4 package -----------------------------------------

def fts4_index(table, id, searchable):
    c = current_app.fts4.cursor(factory=FTSCursor)
    c.attach_source_db(
        current_app.config['SQLALCHEMY_DATABASE_URI'].split(':///')[1]
    )
    c.index(table, id, searchable)
    current_app.fts4.commit()
    c.detach_source_db()


def fts4_delete(table, id):
    c = current_app.fts4.cursor(factory=FTSCursor)
    c.delete(c, table, id)


def fts4_search(table, query, page, per_page):
    c = current_app.fts4.cursor(factory=FTSCursor)
    hits = c.search(table, query)
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
