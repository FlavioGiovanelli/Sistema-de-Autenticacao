from flask import Flask, render_template, request, redirect, url_for, flash, session
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///users.db"
app.config["SECRET_KEY"] = "sua_chave_secreta"

db = SQLAlchemy(app)
bcrypt = Bcrypt(app)

# Modelo de Usuário
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(150), unique=True, nullable=False)
    password = db.Column(db.String(150), nullable=False)

# Rota de Registro
@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        email = request.form["email"]
        password = request.form["password"]
        hashed_password = bcrypt.generate_password_hash(password).decode("utf-8")
        
        user = User(email=email, password=hashed_password)
        db.session.add(user)
        db.session.commit()
        
        flash("Usuário cadastrado com sucesso!", "success")
        return redirect(url_for("login"))

    return render_template("register.html")

# Rota de Login
@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form["email"]
        password = request.form["password"]
        
        user = User.query.filter_by(email=email).first()
        if user and bcrypt.check_password_hash(user.password, password):
            session["user_id"] = user.id
            flash("Login realizado com sucesso!", "success")
            return redirect(url_for("dashboard"))
        else:
            flash("Credenciais inválidas!", "danger")

    return render_template("login.html")

# Rota protegida (Dashboard)
@app.route("/dashboard")
def dashboard():
    if "user_id" not in session:
        flash("Você precisa estar logado para acessar esta página!", "warning")
        return redirect(url_for("login"))
    return render_template("dashboard.html")

# Rota de Logout
@app.route("/logout")
def logout():
    session.pop("user_id", None)
    flash("Logout realizado com sucesso!", "info")
    return redirect(url_for("login"))

if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True)
