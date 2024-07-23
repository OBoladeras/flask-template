import secrets
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from flask import Flask, request, session, jsonify, render_template, redirect, url_for, flash

app = Flask(__name__)
app.config['SECRET_KEY'] = secrets.token_urlsafe(16)
limiter = Limiter(get_remote_address, app=app)


# Session Management
@app.before_request
def sessionChecks():
    session.permanent = True
    app.permanent_session_lifetime = 60 * 60

    if 'username' not in session and request.endpoint not in ['login', 'favicon', 'static', 'api']:
        return render_template('login.html')


# Error Handling
# In case of using a custom error page, uncomment the following code

# @app.errorhandler(429) # Too Many Requests
# def ratelimit_handler(e):
#     return render_template("429.html"), 429

# @app.errorhandler(404)  # Page Not Found
# def page_not_found(e):
#     return render_template("404.html"), 404


@app.route("/favicon.ico")
def favicon():
    return redirect(url_for("static", filename="favicon.ico"), code=302)


@app.route('/')
@limiter.exempt
def index():
    return render_template('index.html')


@app.route('/login', methods=['GET', 'POST'])
@limiter.limit("5 per minute")  # Limit to 5 login attempts per minute
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        if username == 'admin' and password == 'admin':
            session['username'] = username
            flash("Login Successful", "success")

            return redirect(url_for('index'))
        else:
            flash("Invalid Credentials", "error")

    return render_template('login.html')


# API Endpoints
@app.route('/api', methods=['GET', 'POST'])
def api():
    if request.method == 'GET':
        return jsonify({'status': 'success', 'message': 'GET request received'})
    elif request.method == 'POST':
        data = request.get_json()
        return jsonify(data)


if __name__ == '__main__':
    app.run(debug=True)
