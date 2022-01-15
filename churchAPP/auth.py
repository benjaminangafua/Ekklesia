
from crypt import methods
from jinja2 import Template
from flask import Flask, Blueprint, render_template, request, jsonify, redirect, flash
import time
from werkzeug.security import generate_password_hash, check_password_hash
from . import db

auth = Blueprint("auth", __name__)

# sign-up
@auth.route('/', methods=["GET", "POST"])
def signUp():
    # Create church account
    data = db.execute("SELECT * FROM account")
    if request.method == "POST":
        register = {}
        register["fullname"] = request.form.get("full_name")
        register["mail"] = request.form.get("email")
        register["code"] = request.form.get("code")
        register["password"] =generate_password_hash(request.form.get("password"), "sha256")
        register["phone"] = request.form.get("phone")
        register["anniversary"] = request.form.get("anniversary")
        register["account"] = request.form.get("account")
        print(request.form.get("email"))

        if len(register["fullname"]) < 2:
            flash("Full name must be more than 2 characters.", category="error")
        elif len(register["code"]) < 7:
            flash("Password must be 7 characters or more.", category="error")

        elif len(data) > 0:
            for name in data:
                if name["name"]==register["fullname"]:
                    flash("Church already exist.", category="error")

            db.execute("INSERT INTO account(name, code, email, password, phone, bank_account, anniversary) VALUES(?, ?, ?, ?, ?, ?, ?)",
                        register["fullname"], register["code"], register["mail"], register["password"], register["phone"],  register["account"], register["anniversary"])
            flash("Account was created!", category="success")
            
            time.sleep(4)
            return redirect("/login") 
        
        # Add account if not exist
        db.execute("INSERT INTO account(name, code, email, password, phone, bank_account, anniversary) VALUES(?, ?, ?, ?, ?, ?, ?)",
                        register["fullname"], register["code"], register["mail"], register["password"], register["anniversary"], register["phone"],  register["account"])
        flash("Account was created!", category="success")
        
        time.sleep(4)
        return redirect("/login")       
    return render_template("index17.html")     

# Sign in
@auth.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        reg = db.execute("SELECT * FROM account;")
        login = {}
        login["mail"] = request.form.get("email")
        login["code"] = int(request.form.get("code"))
        login["password"] =request.form.get("password")
        
        for data in reg:
            if data["email"] == login["mail"]:
                print("==========||| email |||==============")
                
            if data["code"] == login["code"]:
                print("==========||| code  |||==============", data["password"])
            
            if check_password_hash(data["password"], login["password"]):
                print("==========||| password   |||==============")
            return redirect("/home")
    return render_template('login.html')

# Log out
@auth.route("/logout")
def logout(): 
    return render_template("logOut.html")