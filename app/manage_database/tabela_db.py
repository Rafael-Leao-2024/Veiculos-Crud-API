import sqlite3

conn = sqlite3.connect('bancosqlite.db')

cur = conn.cursor()
cur.execute('''
CREATE TABLE IF NOT EXISTS usuarios(
    id INTEGER PRIMARY KEY,
    nome VARCHAR(100) NOT NULL,
    email VARCHAR(100) NOT NULL,
    senha VARCHAR(255),
    disabled BOOLEAN NOT NULL DEFAULT 0
);
''')

cur.execute('''            
CREATE TABLE IF NOT EXISTS veiculos (
    id INTEGER PRIMARY KEY,
    marca TEXT NOT NULL,
    modelo TEXT NOT NULL,
    ano INTEGER NOT NULL,
    cor TEXT,
    preco REAL,
    is_disponivel BOOLEAN NOT NULL DEFAULT 1
);''')

conn.commit()
conn.close() 
 