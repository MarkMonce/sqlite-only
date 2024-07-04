

import sqlite3
from clitests import addperson

conn = sqlite3.connect('testdb.db')
cursor = conn.cursor()

create_table_sql = """
CREATE TABLE IF NOT EXISTS person (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    firstname VARCHAR(50) NOT NULL,
    lastname VARCHAR(50) NOT NULL,
    age INTEGER,
    accountbalance REAL
);"""
cursor.execute(create_table_sql)
