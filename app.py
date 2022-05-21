import os

from flask import Flask, redirect, render_template, request, session, url_for
from helpers import valid_login

__winc_id__ = "8fd255f5fe5e40dcb1995184eaa26116"
__human_name__ = "authentication"

app = Flask(__name__)

app.secret_key = os.urandom(16)


# @app.route("/home")
# def redirect_index():
#     return redirect(url_for("index"))


@app.route("/")
def index():
    return render_template("index.html", title="Betsy Webshop | Unique Handcrafted Gifts")


@app.route("/login", methods=["GET", "POST"])
def login():
    error = None
    # if form is submitted
    if request.method == "POST":
        # record user name and password
        session["username"] = request.form["username"]
        session["password"] = request.form["password"]

        print(session["username"])
        print(session["password"])

        # if login is valid
        if valid_login(session["username"], session["password"]):
            # redirect to user
            return redirect("/dashboard")

        # if login not valid
        else:
            error = "Invalid_Login"
            # modify login page with error message - access query parameter ("error") - how?

            # redirect to login page
            return redirect(f"/login?error={error}")

    # if form is not submitted (GET login page)
    return render_template("login.html", title="Login | Betsy Webshop")


@app.route("/dashboard", methods=["GET", "POST"])
def dashboard():
    # if form is submitted (Logout button pushed)
    if request.method == "POST":
        # if yes redirect to logout
        return redirect("/logout")

    # if form is not submitted (GET dashboard page)
    return render_template("dashboard.html", title="Dashboard | Betsy Webshop")


@app.route("/logout")
def logout():
    session.pop('username', None)
    return redirect(url_for('index'))
