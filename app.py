from flask import Flask, redirect, url_for
from flask import request

app = Flask(__name__)

@app.route("/home")
def home():
    return 'Hello world <h1>Hi</h1>'

@app.route("/user/<name>")
def user(name):
    return f"Hello {name}!"

@app.route("/profile")
def profile():
    name = request.args.get('user')
    return f"Hello {name}!"

@app.route("/admin")
def admin():
    return redirect(url_for("user", name="Saiprasaad"))

if __name__ == '__main__':
    app.run(debug=True)