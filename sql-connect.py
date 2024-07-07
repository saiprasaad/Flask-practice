from flask import Flask, session, request, flash, render_template, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.secret_key = "hello"
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.sqlite3'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

class users(db.Model):
    _id = db.Column("id", db.Integer, primary_key = True)
    name = db.Column(db.String(100))
    email = db.Column(db.String(100))

    def __init__(self, name, email):
        self.name = name
        self.email = email

@app.route("/")
def test():
    return "You are good to go !"

@app.route("/view-users")
def view_users():
    return render_template("view.html", values = users.query.all())


@app.route("/login", methods = ["POST", "GET"])
def login():
    if(request.method == "POST"):
        user = request.form['username']
        session["user"] = user
        found_user = users.query.filter_by(name=user).first()
        if found_user:
            session["email"] = found_user.email
        else:
            usr = users(user, "")
            db.session.add(usr)
            db.session.commit()

        flash(f"Login Successful")
        return redirect(url_for("user"))
    else:
        if "user" in session:
            flash("You are already loggedin !")
            return redirect(url_for("user"))
        else:
            return render_template("login.html")

@app.route("/user", methods = ["POST", "GET"])
def user():
    email = None
    if "user" in session:
        user = session["user"]
        if request.method == "POST":
            email = request.form["email"]
            session["email"] = email
            found_user = users.query.filter_by(name=user).first()
            found_user.email = email
            db.session.commit()
            flash("Email is saved successfully")
        else:
            if "email" in session:
                email = session["email"]
        return render_template("user.html", email=email)
    else:
        flash("You are not logged in")
        return redirect(url_for("login"))
    
    
@app.route("/logout")
def logout():
    if "user" in session:
        user = session["user"]
        flash(f"You have been logged out {user}", "info")
    session.pop("user", None)
    session.pop("email", None)
    return redirect(url_for("login"))

@app.route("/delete/<name>")
def delete_user(name):
    found_user = users.query.filter_by(name = name).delete()
    db.session.commit()
    if found_user:
        return "User deleted successfully"
    else:
        return f"No users found with name {user}"

if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True)
