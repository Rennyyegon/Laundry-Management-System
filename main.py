from flask import Flask, render_template, request, redirect, flash
from database import *

app = Flask(__name__)

app.secret_key = "12345678"

@app.route("/")  # this sets the route to this page 
def home():
    return render_template("index.html")

@app.route("/signup", methods=["POST", "GET"])
def signup():
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


@app.route("/sign_in", methods=["POST", "GET"])
def login():
    if request.method == "POST":
        email = request.form["email"]
        password = request.form["password"]
        users = fetch_data("users")
        for user in users:
            db_email = user[2]   
            db_pass = user[5]
            if db_email == email and db_pass == password:
                return redirect("/index")
        else:
            flash("Incorrect email or password. Please try again.", "error")
    return render_template("login.html")

@app.route("/customers")
def customer():
    user = fetch_data("users")
    return render_template("customers.html", renny= user)

@app.route("/editservice", methods=['POST', 'GET'])  # Lowercase 'methods'
def editservices():
     if request.method == "POST":
        s_id = request.form['s_id']
        servicetype = request.form["servicetype"]
        itemtype = request.form["itemtype"]
        service_price = request.form["service_price"]
        s= (s_id, servicetype, itemtype, service_price)
        update_service(s)
     return redirect("/inventory")
 
 
@app.route("/addservice", methods=["POST","GET"])
def addservice():
     if request.method=="POST":
         servicetype=request.form["servicetype"]
         itemtype=request.form["itemtype"]
         service_price=request.form["service_price"]
         s = (servicetype,itemtype,service_price)
         add_services(s)
     return redirect('/inventory')
     

@app.route("/services")
def service():
    return render_template("services.html")



@app.route('/deleteservice', methods=["POST"])
def deleteproduct():
    if request.method == "POST":
        s_id = request.form["s_id"]
        delete_services(s_id)
    return redirect("/inventory")

@app.route("/pricing")
def price():
    service = fetch_data("services")
    # Extract unique service types (categories)
    ser = {i[1] for i in service}
    # Create a dictionary to store items grouped by category
    items_by_category = {category: [] for category in ser}
    # Populate the items_by_category dictionary
    for item in service:
        category = item[1]  # Assuming servicetype is at index 1
        items_by_category[category].append(item)
    return render_template("pricing.html", items_by_category=items_by_category, service=service)

@app.route("/index")
def index():
    return render_template("index.html")

@app.route("/inventory")
def services():
    service = fetch_data("services")
    return render_template("inventory.html", service= service)

@app.route("/dashboard")
def dashboard():
    return render_template("layout2.html")

@app.route("/additem", methods=["POST", "GET"])
def additem():
    if request.method == "POST":
        service = request.form["servicetype"]
        item= request.form["itemtype"]
        price= request.form["service_price"] 
        service= (service, item, price)
        insert_item(service)

    return redirect("/inventory")


if __name__ == "__main__":
    app.run(port=5000, debug=True)
    
    

