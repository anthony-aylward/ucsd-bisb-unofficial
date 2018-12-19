#===============================================================================
# search.py
#===============================================================================

"""Integration with sqlite3 FTS4 tables"""




# Imports ======================================================================

import sqlite3

from flask import (
    Blueprint, current_app, g, request, redirect, render_template, url_for
)
from flask_login import current_user, login_required
from ucsd_bisb_unofficial.models import Post
from ucsd_bisb_unofficial.forms import SearchForm




# Blueprint assignment =========================================================

bp = Blueprint('search', __name__, url_prefix='/search')




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
    source_db_name = 'source'
    conn = sqlite3.connect(':memory:')
    c = conn.cursor()
    validate_table_name(c, source_db_name, table)
    validate_column_names(c, source_db_name, table, *Post.__searchable__)
    c.execute(
        f'ATTACH ? AS {source_db_name}',
        (current_app.config['SQLALCHEMY_DATABASE_URI'],)
    )
    c.execute(
        f"""
        CREATE VIRTUAL TABLE {table}
        USING fts4({', '.join(Post.__searchable__)})
        """
    )
    c.execute(
        f"""
        INSERT INTO {table}(docid, {', '.join(Post.__searchable__)})
        SELECT id, {', '.join(Post.__searchable__)}
        FROM {source_db_name}.{table}
        """
    )
    hits = c.execute(
        f"""
        SELECT docid, {', '.join(Post.__searchable__)} FROM {table}
        WHERE {table} MATCH ?
        """,
        (f"'{' OR '.join(f'{col}:{query}' for col in Post.__searchable__)}'",)
    ).fetchall()
    c.execute('DETACH ?', (source_db_name,))
    return {
        'hits': {'total': len(hits), 'hits': {{'_id': hit[0]} for hit in hits}}
    }


def search_results(search):
    ids = [int(hit['_id']) for hit in search['hits']['hits']]
    return ids, search['hits']['total']


def query_index(index, query, page, per_page):
    search = fts4_search(table=index, query=query)
    return search_results(search)


@bp.before_app_request
def before_request():
    if current_user.is_authenticated:
        g.search_form = SearchForm()


@bp.route('/search')
@login_required
def search():
    if not g.search_form.validate():
        return redirect(url_for('jumbotron.index'))
    page = request.args.get('page', 1, type=int)
    posts, total = Post.search(
        g.search_form.q.data,
        page,
        current_app.config['POSTS_PER_PAGE']
    )
    next_url = (
        url_for('search.search', q=g.search_form.q.data, page=page + 1)
        if total > page * current_app.config['POSTS_PER_PAGE']
        else None
    )
    prev_url = (
        url_for('search.search', q=g.search_form.q.data, page=page - 1)
        if page > 1
        else None
    )
    return render_template(
        'search/search.html',
        title='Search',
        posts=posts,
        next_url=next_url,
        prev_url=prev_url
    )
