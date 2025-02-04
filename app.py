from flask import Flask, render_template, redirect, url_for, flash, request
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user

app = Flask(__name__)
app.config['SECRET_KEY'] = 'mysecretkey'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'

# Modelo de usuário
class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), unique=True, nullable=False)
    password = db.Column(db.String(150), nullable=False)

# Carregar usuário para o Flask-Login
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# Rota de cadastro
@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form['username']
        password = request.form['password']
        hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')
        
        user = User(username=username, password=hashed_password)
        db.session.add(user)
        db.session.commit()
        
        flash("Cadastro realizado com sucesso!", "success")
        return redirect(url_for('login'))
    
    return render_template("register.html")

# Rota de login
@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form['username']
        password = request.form['password']
        
        user = User.query.filter_by(username=username).first()
        
        if user and bcrypt.check_password_hash(user.password, password):
            login_user(user)
            flash("Login realizado com sucesso!", "success")
            return redirect(url_for('dashboard'))
        else:
            flash("Login inválido. Verifique suas credenciais.", "danger")
    
    return render_template("login.html")

# Rota de dashboard (após login)
@app.route("/dashboard")
@login_required
def dashboard():
    return f"Olá, {current_user.username}! Bem-vindo ao seu painel."

# Rota de logout
@app.route("/logout")
@login_required
def logout():
    logout_user()
    flash("Você foi deslogado!", "success")
    return redirect(url_for('login'))

# Iniciar o servidor
if __name__ == "__main__":
    app.run(debug=True)