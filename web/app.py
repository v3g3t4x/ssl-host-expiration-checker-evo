from flask import Flask, request, render_template, redirect, url_for, flash
import redis
import validators
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Necessario per usare flash messages

# Configurazione Redis
r = redis.Redis(host='localhost', port=6379, db=0)

# Configurazione Flask-Login
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

# Database degli utenti simulato
users = {'admin': {'password': 'password123'}}

# Modello utente
class User(UserMixin):
    def __init__(self, id):
        self.id = id

@login_manager.user_loader
def load_user(user_id):
    return User(user_id)

@app.route('/')
@login_required
def index():
    domains = r.lrange('domains', 0, -1)
    return render_template('index.html', domains=[domain.decode('utf-8') for domain in domains])

@app.route('/add', methods=['POST'])
@login_required
def add_domain():
    domain = request.form['domain']
    if validators.domain(domain):
        r.rpush('domains', domain)
        flash(f'Dominio "{domain}" aggiunto con successo!', 'success')
    else:
        flash('Il dominio inserito non è valido. Per favore, inserisci un dominio valido.', 'danger')
    return redirect(url_for('index'))

@app.route('/delete/<domain>')
@login_required
def delete_domain(domain):
    r.lrem('domains', 0, domain)
    flash(f'Dominio "{domain}" rimosso con successo!', 'success')
    return redirect(url_for('index'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if username in users and users[username]['password'] == password:
            user = User(username)
            login_user(user)
            flash('Accesso effettuato con successo!', 'success')
            return redirect(url_for('index'))
        else:
            flash('Nome utente o password errati.', 'danger')
    return render_template('login.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('Disconnesso con successo!', 'success')
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(debug=True)
