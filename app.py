import secrets
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from flask import Flask, request, jsonify, render_template

app = Flask(__name__)
app.config['SECRET_KEY'] = secrets.token_urlsafe(16)
limiter = Limiter(get_remote_address, app=app)

@app.errorhandler(429)
def ratelimit_handler(e):
    return render_template("429.html"), 429

@app.route("/favicon.ico")
def favicon():
    return redirect(url_for("static", filename="favicon.ico"), code=302)



@app.route('/')
@limiter.exempt
def index():
    return render_template('index.html')


@app.route('/login')
def login():
    return render_template('login.html')


@app.route('/login', methods=['POST'])
@limiter.limit("5 per minute") # Limit to 5 login attempts per minute 
def login_post():
    username = request.form['username']
    password = request.form['password']

    if username == 'admin' and password == 'admin':
        return 'Login success'
    else:
        return 'Login failed'


@app.route('/api', methods=['POST'])
def api():
    data = request.get_json()
    return jsonify(data)


if __name__ == '__main__':
    app.run(debug=True)
