from flask import Flask
from flask_wtf import CSRFProtect

from Database import criar_tabela
from routes import registrar_rotas

app = Flask(__name__)
app.secret_key = "chave_super_secreta"

#csrf = CSRFProtect(app)

criar_tabela()
registrar_rotas(app)

if __name__ == "__main__":
    app.run(debug=True)