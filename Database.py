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
                email TEXT UNIQUE NOT NULL,
                senha TEXT NOT NULL
            )
        """)

def buscar_cliente_por_id(cliente_id):
    with conectar_db() as conexao:
        return conexao.execute(
            "SELECT * FROM clientes WHERE ID = ?", (cliente_id,)
        ).fetchone()

def buscar_cliente_por_email(email):
    with conectar_db() as conexao:
        return conexao.execute(
            "SELECT * FROM clientes WHERE email = ?", (email,)
        ).fetchone()

def atualizar_cliente(id_cliente, nome, email):
    with conectar_db()as conexao:
        conexao.execute(
            "UPDATE clientes SET nome = ?, email = ? WHERE id = ?",
            (nome, email, id_cliente)
        )

def deletar_cliente(id_cliente):
    with conectar_db() as conexao:
        conexao.execute(
            "DELETE FROM clientes WHERE id = ?",
            (id_cliente,)
        )