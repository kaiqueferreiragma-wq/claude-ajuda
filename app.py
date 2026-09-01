from flask import Flask
from flask_wtf import CSRFProtect
import os

from database import criar_tabela
from routes import registrar_rotas

app = Flask(__name__)
app.secret_key = os.environ.get("SECRET_KEY", "chave-so-para-dev")

app.config["ADMIN_EMAIL"] = os.environ.get("ADMIN_EMAIL", "admin@pupumpa.com")
app.config["ADMIN_SENHA"] = os.environ.get("ADMIN_SENHA", "admin123")

#csrf = CSRFProtect(app)

criar_tabela()
registrar_rotas(app)

if __name__ == "__main__":
    app.run(debug=True)
