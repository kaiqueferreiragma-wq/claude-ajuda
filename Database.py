import sqlite3

def conectar_db():
    conexao = sqlite3.connect('clientes.db')
    conexao.row_factory = sqlite3.Row
    return conexao

def criar_tabela():
    with conectar_db() as conexao:
        conexao.execute("""
            CREATE TABLE IF NOT EXISTS clientes (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nome TEXT NOT NULL,
                email TEXT UNIQUE NOT NULL
            )
        """)