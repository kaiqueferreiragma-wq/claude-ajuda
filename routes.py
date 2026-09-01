from flask import render_template, request, redirect, url_for, flash, session
from werkzeug.security import generate_password_hash, check_password_hash
from database import ( 
    conectar_db, buscar_cliente_por_id, buscar_cliente_por_email,
    atualizar_cliente, deletar_cliente
)
from functools import wraps
import re
import sqlite3


def login_obrigatorio(funcao):
    @wraps(funcao)
    def decorada(*args, **kwargs):
        if "cliente_id" not in session:
            flash("voce precisa estar logado para acessar essa pagina!")
            return redirect(url_for("login"))
        return funcao(*args, **kwargs)
    return decorada

def admin_obrigatorio(funcao):
    @wraps(funcao)
    def decorada(*args, **Kwargs):
        if not session.get("admin"):
            flash("Acesso restrito ao administrador.")
            return redirect(url_for("admin_login"))
        return funcao(*args, **Kwargs)
    return decorada

def registrar_rotas(app):

    @app.route("/")
    def home():
        return ("olá, seja bem vindo ao sistema pupumpa")

    @app.route("/clientes")
    @login_obrigatorio
    def listar_clientes():
        conexao = conectar_db()
        clientes = conexao.execute(
            "SELECT * FROM clientes"
        ).fetchall()
        conexao.close()

        return render_template(
            "clientes.html",
            clientes=clientes
        )

    @app.route("/cadastro", methods=["GET", "POST"])
    def cadastro():

        if request.method == "POST":
            nome = request.form.get("nome", "").strip()
            email = request.form.get("email", "").strip()
            senha = request.form.get("senha", "").strip()

            if not nome or not email:
                flash("nome, email e senha são obrigatorios!")
                return redirect(url_for("cadastro"))

            if not re.match(r"[^@]+@[^@]+\.[^@]+", email):
                flash("email invalido")
                return redirect(url_for("cadastro"))

            if len(senha) < 6:
                flash("senha deve ter 6 caracteres!")
                return redirect(url_for("cadastro"))

            senha_hash = generate_password_hash(senha)

            try:
                with conectar_db() as conexao:
                    conexao.execute(
                    "INSERT INTO clientes (nome, email, senha) VALUES (?, ?, ?)",
                    (nome, email, senha_hash)
                )
                flash("cliente cadastrado com suceso, faça login para acessar o sistema!")
                return redirect(url_for("login"))
            except sqlite3.IntegrityError:
                flash("esse email ja esta cadastrado!")
                return redirect(url_for("cadastro"))


        return render_template("cadastro.html")

    @app.route("/editar/<int:cliente_id>", methods=["GET", "POST"])
    @admin_obrigatorio
    def editar_cliente(cliente_id): 
        cliente = buscar_cliente_por_id(cliente_id)

        if cliente is None:
            flash("cliente nao encontrado!")
            return redirect(url_for("listar_clientes"))

        if request.method == "POST":
            nome = request.form.get("nome", "").strip()
            email = request.form.get("email", "").strip()

            if not nome or not email:
                flash("Nome e email são obrigatorios!")
                return redirect(url_for("editar_cliente", cliente_id=cliente_id))

            if not re.match(r"[^@]+@[^@]+\.[^@]+", email):
                flash("email invalido")
                return redirect(url_for("editar_cliente", cliente_id=cliente_id))

            try:
                atualizar_cliente(cliente_id, nome, email)
                flash("cliente atualizado com sucesso!")
            except sqlite3.IntegrityError:
                flash("esse email ja esta cadastrado!")
                return redirect(url_for("editar_cliente", cliente_id=cliente_id))

            return redirect(url_for("listar_clientes"))

        return render_template("editar_cliente.html", cliente=cliente)

    @app.route("/login", methods=["GET","POST"])
    def login():
        if request.method == "POST":
            email = request.form.get("email", "").strip()
            senha = request.form.get("senha", "").strip()

            cliente = buscar_cliente_por_email(email)

            if cliente is None or not check_password_hash(cliente["senha"], senha):
                flash("email ou senha incorretos!")
                return redirect(url_for("login"))

            session["cliente_id"] = cliente["id"]
            session["cliente_nome"] = cliente["nome"]
            flash(f"bem-vindo, {cliente['nome']}!")
            return redirect(url_for("listar_clientes"))

        return render_template("login.html")

    @app.route("/logout")
    def logout():
        session.clear()
        flash("voce saiu com sucesso!")
        return redirect(url_for("login"))

    @app.route("/excluir/<int:cliente_id>", methods=["GET", "POST"])
    @admin_obrigatorio
    def excluir_cliente(cliente_id):
        cliente = buscar_cliente_por_id(cliente_id)

        if cliente is None:
            flash("cliente nao encontrado!")
            return redirect(url_for("listar_clientes"))

        if request.method == "POST":
            deletar_cliente(cliente_id)
            flash("cliente excluido com sucesso!")
            return redirect(url_for("listar_clientes"))

        return render_template("excluir_cliente.html", cliente=cliente)

    @app.route("/admin/login", methods=["GET", "POST"])
    def admin_login():
        if request.method == "POST":
            email = request.form.get("email", "").strip()
            senha = request.form.get("email", "").strip()

            if email == app.config["ADMIN_EMAIL"] and senha == app.config["ADMIN_SENHA"]:
                session["admin"] = True
                flash("bem vindo, administrador!")
                return redirect(url_for("listar_clientes"))

            flash("credenciais de administrador incorretas.")
            return redirect(url_for("admin_login"))

        return render_template("admin_login.html")

    @app.route("/admin/logout")
    def admin_logout():
        session.pop("admin", None)
        flash("você saiu do modo administrador")
        return redirect(url_for("admin_login"))