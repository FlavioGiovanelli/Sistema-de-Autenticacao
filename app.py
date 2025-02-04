from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'  # Banco de dados SQLite
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False  # Evita warnings

db = SQLAlchemy(app)
bcrypt = Bcrypt(app)

# Importa os modelos aqui para evitar importações circulares
from models import User

if __name__ == "__main__":
    app.run(debug=True)
