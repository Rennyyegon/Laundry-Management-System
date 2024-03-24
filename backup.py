from flask import Flask, render_template, request, redirect, flash
from database import adduser, fetch_data

app = Flask(__name__)

app.secret_key = "12345678"

@app.route("/")  # this sets the route to this page
def home():
    return render_template("index.html")

@app.route("/signup", methods=["POST", "GET"])
def register():
    if request.method == "POST":
        full_name = request.form["full_name"]
        email = request.form["email"]
        contact = request.form["contact"] 
        address = request.form["address"]
        password = request.form["password"]
        user = (full_name, email, contact, address, password, 'now()')
        adduser(user)
        flash("Account successfully created. Please proceed to login.", "success")
        return redirect("/signup")
    
    return render_template("register.html")


@app.route("/login", methods=["POST", "GET"])
def login():
    if request.method == "POST":
        email = request.form["email"]
        password = request.form["password"]
        users = fetch_data("users")
        for user in users:
            db_email = user[2]   
            db_pass = user[5]
            if db_email == email and db_pass == password:
                return redirect("/")
        else:
            flash("Incorrect email or password. Please try again.", "error")
    return render_template("login.html")

@app.route("/dashboard")
def dashboard():
    user = fetch_data("users")
    return render_template("dashboard.html", user = user)

@app.route("/service")
def services():
    service = fetch_data("services")
    return render_template("dashboard.html", service = service)

if __name__ == "__main__":
    app.run(port=5001, debug=True)
