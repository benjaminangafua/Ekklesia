from flask import Flask, Blueprint, render_template, request, jsonify, redirect
# from sqlalchemy.sql.expression import join
from churchAPP import db
from .email import sendMail


# Create church account
def createChurchAccount():
    data = db.execute("SELECT * FROM account")

    if request.method == "POST":
        churchData = {}
        churchData["name"] = request.form.get("name")
        churchData["mail"] = request.form.get("mail")
        churchData["phone"] = request.form.get("phone")
        churchData["bankNo"] = request.form.get("bankNo")
        churchData["code"] = int(request.form.get("code"))
        if len(data) > 0:
            for name in data:
                if name["name"]==churchData["name"]:
                    message =  "Church already exist"
                    apology(message)
        db.execute("INSERT INTO account(name, code, email, phone, bank_account) VALUES(?, ?, ?, ?, ?)",
                    churchData["name"], churchData["code"], churchData["mail"], churchData["phone"],  churchData["bankNo"])
        return redirect("/home")   
    return render_template("create.church.html")     
# home
def home():
    
    # account name """Need authentication"""
    church = db.execute("SELECT name FROM account")[0]["name"]
    print(church)

    # Birthday's section
    data = db.execute("SELECT * FROM birthday")
    memberSum = db.execute('SELECT COUNT(*) FROM members')[0]['COUNT(*)']
    
    # Department's Section
    deparmentSum = db.execute('SELECT COUNT(DISTINCT(department)) FROM members')[0]['COUNT(DISTINCT(department))']

    if len(data) > 0:
        # Birthday entry
        this_month = int(db.execute("SELECT strftime('%m','now');")[0]["strftime('%m','now')"])
        this_day = int(db.execute("SELECT strftime('%d','now');")[0]["strftime('%d','now')"])
        birth_record = db.execute(f"SELECT COUNT(*) FROM birthday WHERE month = {this_month}")[0]['COUNT(*)']
        today_birtday = db.execute(f"SELECT COUNT(DISTINCT(name)) FROM birthday WHERE day = {this_day}")[0]['COUNT(DISTINCT(name))']
        
        # print(birth_record)
        # Attendance
        attendance = int(db.execute("SELECT total_attendance FROM attendance")[0]["total_attendance"])
        
        floating_pre = (attendance * 100) / int(memberSum)
        present_percent = float("{:.2f}".format(floating_pre))

        # print("Presence =================>>>>",present_percent)

        # Absence
        absence = int(memberSum) - attendance
        floating = (absence * 100) / int(memberSum)
        absent_percent = float("{:.2f}".format(floating))

        # print("Absence =================>>>>", absent_percent)

        # Member's Section
        return render_template("index.html", 
        numOfBirthday=birth_record, todayNumOfBirthday=today_birtday, 
        deparmentSum=deparmentSum, memberSum=memberSum, attendance=attendance,
         absence=absence, absent_percent=absent_percent, present_percent=present_percent,
         church=church)
    
    return render_template("index.html", deparmentSum=deparmentSum, memberSum=memberSum)

# creat member
def createMember():

    data = db.execute("SELECT * FROM members")
    if request.method == "POST":
        member_data = {}
        member_data["relationship"] = request.form.get("relationship")
        member_data["name"]=request.form.get("name")
        member_data["location"] = request.form.get("location")
        member_data["department"] = request.form.get("department")
        member_data["contact"] = request.form.get("contact")
        member_data["role_play"] = request.form.get("role")
        member_data["occupation"] = request.form.get("occupation")
        
        member_data["date_of_birth"] = request.form.get("date_of_birth")
        member_data["gender"] =request.form.get("gender")

        # print( member_data)
        if len(data) > 0:
            for name in data:
                if name["name"]==member_data["name"]:
                    message =  "Name already exist"
                    apology(message)
        db.execute("INSERT INTO members(name, location, department, gender, contact, relationship, occupation, role_play,  date_of_birth, joined_date) VALUES(?, ?, ?, ?, ?, ?, ?, ?,?, date('now'))",
                       member_data["name"], member_data["location"], member_data["department"],  member_data["gender"], member_data["contact"], member_data["relationship"], member_data["occupation"], member_data["role_play"], member_data["date_of_birth"])
        
        dob = db.execute("SELECT name, strftime('%Y',date_of_birth) as 'Year', strftime('%m',date_of_birth) as 'Month', strftime('%d',date_of_birth) as 'Day'FROM members;")
       
        DATEOFBIRTH = db.execute("SELECT * FROM birthday")
        
        for new in dob:

            # Check for duplicate
            if len(data) > 0:
                if len(DATEOFBIRTH) > 0:
                    for name in DATEOFBIRTH:
                        if name["name"]== new["name"]:

                            message = "Nam already taken."
                            apology(message)
                        # Insert Date of birth
                        db.execute("INSERT INTO birthday(name, day, month) VALUES(?, ?, ?)", new["name"], new["Day"], new["Month"])
            db.execute("INSERT INTO birthday(name, day, month) VALUES(?, ?, ?)", new["name"], new["Day"], new["Month"])
            
        return redirect("/home")
    return render_template('add-new-member.html')

# view members' data
def seeMember():
    members = db.execute("SELECT * FROM members ORDER BY id")
    return render_template("member.html",members=members)
# Get new converts
def new_convert():
    if request.method == "POST":
        new={}
        new["name"]=request.form.get("name")
        new["location"] = request.form.get("location")
        new["contact"] = request.form.get("contact")
        data = db.execute("SELECT * FROM new_convert")
        if len(data) > 0:
            for name in data:
                if name["name"]== new["name"]:
                    message = "Nam already taken."
                    apology(message)

            db.execute("INSERT INTO new_convert(name, contact, location) VALUES(?, ?, ?, date('now'))", new["name"], new["contact"], new["location"])
            return redirect("/convert")

        else:
            db.execute("INSERT INTO new_convert(name, contact, location) VALUES(?, ?, ?, date('now'))", new["name"], new["contact"], new["location"])
            return redirect("/convert")

    return render_template("add-new-convert.html")

# Display new converts
def convert():
    convert = db.execute("SELECT * FROM new_convert ORDER BY joined_date")
    return render_template("new-convert.html", converts=convert)

def first_timer():
    if request.method == "POST":
        new={}
        new["name"]=request.form.get("name")
        new["location"] = request.form.get("location")
        new["contact"] = request.form.get("contact")
        new["gender"] = request.form.get("gender")
        data = db.execute("SELECT * FROM first_time_visitors")
        if len(data) > 0:
            for name in data:
                if name["name"]== new["name"]:
                    message = "Nam already taken."
                    apology(message)

            db.execute("INSERT INTO first_time_visitors(name, contact, location, gender, date_visited) VALUES(?, ?, ?, ?, date('now'))",
             new["name"], new["contact"], new["location"], new["gender"])
            return redirect("/vissitor")

        else:
            db.execute("INSERT INTO first_time_visitors(name, contact, location, gender) VALUES(?, ?, ?, ?, date('now'))",
             new["name"], new["contact"], new["location"], new["gender"])
            return redirect("/visitor")

    return render_template("add-first-timers.html")

def visitors():
    visitors_name = db.execute("SELECT * FROM first_time_visitors ORDER BY id")
    return render_template("first-time-visitor.html", visitors_name=visitors_name)
   
def birthday():
    
    # Months for birthday
    months = ["1", "January","February","March","April", "May","June","July","August","September", "October","November","December"]
    this_month = int(db.execute("SELECT strftime('%m','now');")[0]["strftime('%m','now')"])
    birth_rec = db.execute("SELECT * FROM birthday")
        
    return render_template("birthday.html", member=birth_rec, thisMONTH=this_month, months=months)

def takeAttendance():
    if request.method == "POST":

        num = request.form.getlist("num")
        totatl_attendance = len(num)
                
        # Check for attendance is taken
        if not num:
            message = "num field empty."
            apology(message)
            
        # Loop through the attendance , total_attendance=:total, total=totatl_attendance
        for name in num:
            
            db.execute("UPDATE attendance SET name=:name, total_attendance=:total, date=date('now') WHERE id >= 0",total=totatl_attendance,  name=name)
        
    member_names = db.execute("SELECT DISTINCT(name), id FROM members")

    return render_template("new-attendance.html", member_names=member_names)

def apology(message):
    return render_template("apology.html", message=message)

# Offering
def payOffering():
    if request.method == "POST":
        offering={}
    return render_template("offering.html")
    
# ------------------------------
# communication | Finance
# -------------------------------
# email         | online donation   
# sms           | offering giving
# --------------|----------------

# ------------------------------
# contact       | setting
# -------------------------------
# email/phone   | profle   
# sms           | offering giving
# --------------|----------------

# ------------------------------
# report        | authentication
# -------------------------------
# members'      |sign-up
#  statistic    |  login   
# finance       |  
# celebration   |logout
# --------------|----------------

# notification