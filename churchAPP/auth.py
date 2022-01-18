from flask import render_template, g, url_for, request, redirect, flash, session
from werkzeug.security import generate_password_hash, check_password_hash
import functools
from . import db

from flask import Blueprint

auth = Blueprint("auth", __name__)

# auth.secret_key = "hello"
# auth.permanent_session_lifetime = timedelta(minutes=5)

# sign-up
@auth.route('/', methods=["GET", "POST"])
def registerAccount():
    # Create church account
    data = db.execute("SELECT * FROM account")
    if request.method == "POST":
        
        fullname = request.form.get("full_name")
        email = request.form.get("email")
        code = request.form.get("code")
        password =generate_password_hash(request.form.get("password"), "sha256")
        phone = request.form.get("phone")
        anniversary = request.form.get("anniversary")
        account = request.form.get("account")

        error = None
        if not fullname:
            error = "Invalid name"
        print(request.form.get("email"))

        if len(fullname) < 2:
            error = "Full name must be more than 2 characters."
        elif len(code) < 3:
            error = "Password must be 7 characters or more."
        
        if len(data) > 0:
            for name in data:
                if name["name"]==fullname:
                    error = "Church already exist."

            db.execute("INSERT INTO account(name, code, email, password, phone, bank_account, anniversary) VALUES(?, ?, ?, ?, ?, ?, ?)", fullname, code, email, password, phone,  account, anniversary)
            return redirect("/login") 
        # Add account if not exist
        db.execute("INSERT INTO account(name, code, email, password, phone, bank_account, anniversary) VALUES(?, ?, ?, ?, ?, ?, ?)", fullname, code, email, password, anniversary, phone,  account)
        
        flash(error, category="error") 

        return redirect("/login")       
    return render_template("index17.html")     
  
# Sign in
@auth.route("/login", methods=["GET", "POST"])
def loginAccount():
    if request.method == "POST":
        session.permanent=True

        email = request.form.get("email")
        code = int(request.form.get("code"))
        password =request.form.get("password")
                
        if not email:
            error = "Invalid email!"
        if code:
            error = "Invalid code!"
        if not password:
            error = "Invalid password!"

        user = db.execute("SELECT * FROM account WHERE email=:mail", mail=str(email))[0]
        print(user)
        if user is None:
            error = "User not provided"
        elif len(user) != 1 or not check_password_hash(user["password"], password):
            error = "Invalid email and Passoword!"

        session["user_id"] = user["id"]

        flash(error, category="error")
        print("last======")
        return redirect("/home")

        
    return render_template('login.html')

@auth.before_app_request
def load_logged_in_user():
    user_id = session.get('user_id')

    if user_id is None:
        g.user = None
    else:
        g.user = db.execute(
            'SELECT * FROM account WHERE id = ?', (user_id,)
        )[0]

# Log in required
def login_required(view):
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if g.user is None:
            return redirect("/login")
        return view(**kwargs)

    return wrapped_view

# Log out
@auth.route("/logout")
@login_required
def logout(): 
    session.pop("user_id",None)
    return redirect("/login")
