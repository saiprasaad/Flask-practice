from flask import Flask, render_template

app = Flask(__name__)

@app.route("/exercise-1")
def Exercise_1():
    return render_template("index.html", content=["tim", "joe", "bill"])


@app.route("/exercise-2")
def Exercise_2():
    return render_template("child.html")


if __name__ == "__main__":
    app.run(debug=True)