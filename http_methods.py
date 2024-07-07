from flask import Flask, render_template, request, redirect, url_for, session, flash

app = Flask(__name__)
app.secret_key = "hello"

@app.route("/login", methods = ["POST", "GET"])
def login():
    if(request.method == "POST"):
        user = request.form['username']
        session["user"] = user
        flash(f"Login Successful")
        return redirect(url_for("user"))
    else:
        if "user" in session:
            return redirect(url_for("user"))
        else:
            return render_template("login.html")

@app.route("/user")
def user():
    if "user" in session:
        user = session["user"]
        return render_template("user.html", user=user)
    else:
        flash("You are not logged in")
        return redirect(url_for("login"))

@app.route("/logout")
def logout():
    if "user" in session:
        user = session["user"]
        flash(f"You have been logged out {user}", "info")
    session.pop("user", None)
    return redirect(url_for("login"))

if __name__ == '__main__':
    app.run(debug=True)