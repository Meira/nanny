# -*- coding: utf-8 -*-

import sqlite3


DB_NAME = 'nanny.sqlite'
DB_INSERT = 'INSERT INTO "{table}" VALUES ({placeholders});'
DB_CREATE = 'CREATE  TABLE "main"."{table}" ({cols});'
DB_EXISTS = 'SELECT count(*) FROM sqlite_master WHERE type="table" AND name="{table}";'
DB_DROP = 'DROP TABLE "main"."{table}";'
DB_SELECT = 'SELECT * FROM "{table}" WHERE "{col}" LIKE "%{val}%" LIMIT {limit};'


def get_connection(db):
    return sqlite3.connect(db, detect_types=sqlite3.PARSE_DECLTYPES)


def select(conn, table, column, value, limit=100):
    c = conn.cursor()
    table_exists = c.execute(DB_EXISTS.format(table=table)).fetchall()[0][0]
    if table_exists:
        return conn.execute(DB_SELECT.format(table=table, col=column, val=value, limit=limit)).fetchall()
    else:
        return None

def insert_values(conn, table, values):
    try:
        conn.execute(DB_INSERT.format(table=table, placeholders=','.join(['?'] * len(values))), values)
    except Exception, e:
        print values
        raise e
    conn.commit()


def make_table(conn, table, cols):
    c = conn.cursor()
    table_exists = c.execute(DB_EXISTS.format(table=table)).fetchall()[0][0]
    if not table_exists:
        c.execute(DB_CREATE.format(table=table, cols=cols))
    conn.commit()


def drop_table(conn, table):
    conn.execute(DB_DROP.format(table=table))
    conn.commit()
