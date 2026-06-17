from flask import app, render_template, request, redirect, url_for, flash
from Database import conectar_db
import re


def registrar_rotas(app):

    @app.route("/")
    def home():
        return ("olá, seja bem vindo ao sistema pupumpa")

    @app.route("/clientes")
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
            nome = request.form["nome"]
            email = request.form["email"]

            conexao = conectar_db()
            cursor = conexao.cursor()

            cursor.execute(
                "INSERT INTO clientes (nome, email) VALUES (?, ?)",
                (nome, email)
            )

            conexao.commit()
            conexao.close()

            flash("Cliente cadastrado com sucesso!")
            return redirect(url_for("listar_clientes"))

        return render_template("cadastro.html")
