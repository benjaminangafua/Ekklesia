from flask import Blueprint, render_template, request, redirect, flash, session
from .auth import login_required
from churchAPP import db

views = Blueprint('views', __name__)

# Landing page
def churchName():
    row = db.execute("SELECT name FROM account WHERE id =?", session["user_id"])[0]["name"]
    return row
def anniversaryFound():
    sid =  session["user_id"]
    return sid

MemberData = db.execute("SELECT * FROM members")
landingData = {}
# landing page
@views.route("/")
def landingPage():

    return render_template("landing-index.html")
# dashboard
@views.route("/dashboard")
@login_required
def home():
    # Birthday's section
    memberSum = db.execute('SELECT COUNT(*) FROM members')[0]['COUNT(*)']
    
    # Department's Section
    deparmentSum = db.execute('SELECT COUNT(DISTINCT(department)) FROM members')[0]['COUNT(DISTINCT(department))']

    if len(MemberData) > 0:
        # Birthday entry
        this_month = int(db.execute("SELECT strftime('%m','now');")[0]["strftime('%m','now')"])
        today = int(db.execute("SELECT strftime('%d','now');")[0]["strftime('%d','now')"])
        
        birth = db.execute(f"SELECT strftime('%m',date_of_birth) as 'Month', strftime('%d',date_of_birth) as 'Day' FROM members")
        
        # Number of birthdays today
        birth_day = 0
        for day in birth:
            if int(day["Day"]) == today:
               birth_day= int(day["Day"])

        # Number of birthdays this month
        birth_month = 0
        for month in birth:
            if int(month["Month"]) == this_month:
               birth_month = int(month["Month"])

        # Attendance
        attendance = int(db.execute("SELECT total_attendance FROM attendance")[0]["total_attendance"])
        floating_pre = (attendance * 100) / int(memberSum)
        present_percent = float("{:.2f}".format(floating_pre))

        # Absence
        absence = int(memberSum) - attendance
        floating = (absence * 100) / int(memberSum)
        absent_percent = float("{:.2f}".format(floating))

        newmember = db.execute("SELECT COUNT(*) FROM new_convert")[0]['COUNT(*)']

        anniversary = db.execute(f"SELECT anniversary FROM account WHERE id ={anniversaryFound()}")[0]['anniversary']

        landingData["birth_sum_today"]=birth_day
        landingData["birth_sum_this_month"]=birth_month
        landingData["newmember"]=newmember
        landingData["anniversary"]=anniversary
        landingData["deparmentSum"]=deparmentSum
        landingData["memberSum"]=memberSum
        landingData["attendance"]=attendance,
        landingData["absence"]=absence
        landingData["absent_percent"]=absent_percent
        landingData["present_percent"]=present_percent
        landingData["church"]=churchName()

        # Member's Section
        return render_template("dashboard-index.html", 
        birth_sum_today=birth_day, birth_sum_this_month=birth_month, newmember=newmember,anniversary=anniversary,
        deparmentSum=deparmentSum, memberSum=memberSum, attendance=attendance,
         absence=absence, absent_percent=absent_percent, present_percent=present_percent,
         church=churchName())
    
    return render_template("dashboard-index.html", deparmentSum=deparmentSum, memberSum=memberSum)

# create New member
@views.route('/add-new-member', methods=["GET", "POST"])
@login_required
def createMember():
    data = db.execute("SELECT * FROM members")
    if request.method == "POST":
        relationship = request.form.get("relationship")
        name = request.form.get("name")
        location = request.form.get("location")
        department = request.form.get("department")
        contact = request.form.get("contact")
        role_play = request.form.get("role")
        occupation = request.form.get("occupation")
        weddingdate = request.form.get("weddingdate")
        date_of_birth = request.form.get("date_of_birth")
        gender = request.form.get("gender")

        # print( member_data)
        if len(data) > 0:
            for row in data:
                if row["name"]==name:
                    flash("Name already exist.", category="error")

            db.execute("INSERT INTO members(name, location, department, gender, contact, relationship, occupation, role_play,  date_of_birth, wedding_anniversary, joined_date) VALUES(?, ?, ?, ?, ?, ?, ?, ?,?,?, date('now'))",
                       name, location, department,  gender, contact, 
                       relationship, occupation, role_play, date_of_birth, weddingdate)
        db.execute("INSERT INTO members(name, location, department, gender, contact, relationship, occupation, role_play,  date_of_birth, wedding_anniversary, joined_date) VALUES(?, ?, ?, ?, ?, ?, ?, ?,?,?, date('now'))",
                       name, location, department,  gender, contact, 
                       relationship, occupation, role_play, date_of_birth, weddingdate)
        return redirect("/dashboard")
    return render_template('add-new-member.html')

# Display members
@views.route("/member")
@login_required
def seeMember():
    members = db.execute("SELECT * FROM members ORDER BY id")
    print(session["user_id"])
    return render_template("member.html",members=members)

# New convert
@views.route("/add-new-convert", methods=["GET", "POST"])
@login_required
def new_convert():
    if request.method == "POST":
        name=request.form.get("name")
        date_of_birth = request.form.get("date_of_birth")
        gender =request.form.get("gender")
        location = request.form.get("location")
        contact = request.form.get("contact")
        data = db.execute("SELECT * FROM new_convert")
        if len(data) > 0:
            for row in data:
                if row["name"]== name:
                    flash("Name already exist.", category="error")

            db.execute("INSERT INTO new_convert(name, gender, date_of_birth, contact, location, joined_date) VALUES(?, ?, ?, ?, ?, date('now'))",
                        name, gender, date_of_birth, contact, location)
            return redirect("/convert")

        db.execute("INSERT INTO new_convert(name, gender, date_of_birth, contact, location, joined_date) VALUES(?, ?, ?, ?, ?, date('now'))",
                        name, gender, date_of_birth, contact, location)
        return redirect("/convert")

    return render_template("add-new-convert.html")

# Convert
@views.route("/convert")
@login_required
def convert():
    convert = db.execute("SELECT * FROM new_convert ORDER BY joined_date")
    return render_template("new-convert.html", converts=convert)

# First time visitor
@views.route("/add-first-timer", methods=["GET", "POST"])
@login_required
def first_timer():
    if request.method == "POST":
        name=request.form.get("name")
        location = request.form.get("location")
        contact = request.form.get("contact")
        gender = request.form.get("gender")
        data = db.execute("SELECT * FROM first_time_visitors")
        if len(data) > 0:
            for row in data:
                if row["name"]== name:
                    flash("Name already exist.", category="error")
            # Add first timer to existing data
            db.execute("INSERT INTO first_time_visitors(name, contact, location, gender, date_visited) VALUES(?, ?, ?, ?, date('now'))",
             name, contact, location, gender)
            return redirect("/vissitor")
            
        # Add new first timer
        db.execute("INSERT INTO first_time_visitors(name, contact, location, gender, date_visited) VALUES(?, ?, ?, ?, date('now'))",
             name, contact, location, gender)
        return redirect("/visitor")

    return render_template("add-first-timers.html")

# get new visitor
@views.route("/visitor")
@login_required
def visitors():
    visitors_name = db.execute("SELECT * FROM first_time_visitors ORDER BY id")
    return render_template("first-time-visitor.html", visitors_name=visitors_name)

# Birthday list
@views.route("/birthday")
@login_required
def birthday():
    # Months for birthday
    months = ["1", "January","February","March","April", "May","June","July","August","September", "October","November","December"]
    this_month = int(db.execute("SELECT strftime('%m','now');")[0]["strftime('%m','now')"])
    birth_rec = db.execute("SELECT name, strftime('%Y',date_of_birth) as 'Year', strftime('%m',date_of_birth) as 'Month', strftime('%d',date_of_birth) as 'Day'FROM members;")
    return render_template("birthday.html", member=birth_rec, thisMONTH=this_month, months=months)

# wedding list
@views.route("/wedding")
@login_required
def weddingAnniversary():
    # Months for wedding
    months = ["1", "January","February","March","April", "May","June","July","August","September", "October","November","December"]
    this_month = int(db.execute("SELECT strftime('%m','now');")[0]["strftime('%m','now')"])
    birth_rec = db.execute("SELECT name, strftime('%Y',wedding_anniversary) as 'Year', strftime('%m',wedding_anniversary) as 'Month', strftime('%d',wedding_anniversary) as 'Day'FROM members;")
    return render_template("wedding.html", member=birth_rec, thisMONTH=this_month, months=months)
 
# create attendance
@views.route("/new-attendance", methods=["GET", "POST"])
@login_required
def takeAttendance():
    if request.method == "POST":
        num = request.form.getlist("num")
        totatl_attendance = len(num)
                
        # Check for attendance is taken
        if not num:
            flash("Num field empty.", category="error")
        # Loop through the attendance , total_attendance=:total, total=totatl_attendance
        for name in num:
            db.execute("UPDATE attendance SET name=:name, total_attendance=:total, date=date('now') WHERE id >= 0",total=totatl_attendance,  name=name)
            return redirect("/dashboard")
    member_names = db.execute("SELECT DISTINCT(name), id FROM members")

    return render_template("new-attendance.html", member_names=member_names)

# Contact
@views.route('/contact')
@login_required
def contact():
    return render_template('contact.html')

# Home 
@views.route('/dashboard')
@login_required
def dashboard():
    return render_template('dashboard-index.html')

# use's -profie
@views.route('/profile')
@login_required
def profile():
    return render_template('profile.html')

#setting
@views.route('/settings')
@login_required
def setting():
    return render_template('settings.html')

# offering
@views.route('/offering', methods=["GET", "POST"])
@login_required
def payOffering():
    data = db.execute("SELECT * FROM offering;")

    if request.method == "POST":
        name = request.form.get("name")
        amount = request.form.get("amount")
        number = request.form.get("account")
        if len(data) > 0:
            for row in data:
                if row["name"]== name:
                    db.execute("UPDATE offering SET member_name=:name, amount=:amount, number=number, pay_day=date('now') WHERE id >= 0",name= name, amount=amount, number=number)
                    return redirect("/dashboard")
            db.execute("INSERT INTO offering(member_name, amount, number, pay_day) VALUES(?, ?, ?, date('now'))", name, amount, number)
            return redirect("/dashboard")

        db.execute("INSERT INTO offering(member_name, amount, number, pay_day) VALUES(?, ?, ?, date('now'))", name, amount, number)
        return redirect("/dashboard")
    
    return render_template("offering.html", church=churchName())

# send notification
@views.app_context_processor
def notifyUpdate():
    notify = len(db.execute("SELECT * FROM offering;"))
    return  dict(notify=notify)
    
# render notification template
@views.route("/notification")
@login_required
def notification():
    render_offering = db.execute("SELECT * FROM offering ORDER BY pay_day DESC;")
    # db.execute("DELETE FROM offering WHERE id > 0")
    return render_template("notification.html", notifying=render_offering)

def clearBNotification(notes):
    notes = 0
    return notes

def apology(message):
    return render_template("apology.html", message=message)