from distutils.log import error
from flask import Flask, Blueprint, render_template, request, jsonify, redirect, flash
import time
from churchAPP import db
# account name """Need authentication"""
churchName= db.execute("SELECT name FROM account")[2]["name"]

MemberData = db.execute("SELECT * FROM members")

# landing page
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

        anniversary = db.execute("SELECT anniversary FROM account")[2]['anniversary']

        # Member's Section
        return render_template("index.html", 
        birth_sum_today=birth_day, birth_sum_this_month=birth_month, newmember=newmember,anniversary=anniversary,
        deparmentSum=deparmentSum, memberSum=memberSum, attendance=attendance,
         absence=absence, absent_percent=absent_percent, present_percent=present_percent,
         church=churchName)
    
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
        member_data["weddingdate"] = request.form.get("weddingdate")
        member_data["date_of_birth"] = request.form.get("date_of_birth")
        member_data["gender"] =request.form.get("gender")

        # print( member_data)
        if len(data) > 0:
            for name in data:
                if name["name"]==member_data["name"]:
                    flash("Name already exist.", category="error")

        db.execute("INSERT INTO members(name, location, department, gender, contact, relationship, occupation, role_play,  date_of_birth, wedding_anniversary, joined_date) VALUES(?, ?, ?, ?, ?, ?, ?, ?,?,?, date('now'))",
                       member_data["name"], member_data["location"], member_data["department"],  member_data["gender"], member_data["contact"], 
                       member_data["relationship"], member_data["occupation"], member_data["role_play"], member_data["date_of_birth"], member_data["weddingdate"])
        
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
        new["date_of_birth"] = request.form.get("date_of_birth")
        new["gender"] =request.form.get("gender")
        new["location"] = request.form.get("location")
        new["contact"] = request.form.get("contact")
        data = db.execute("SELECT * FROM new_convert")
        if len(data) > 0:
            for name in data:
                if name["name"]== new["name"]:
                    flash("Name already exist.", category="error")

            db.execute("INSERT INTO new_convert(name, gender, date_of_birth, contact, location, joined_date) VALUES(?, ?, ?, ?, ?, date('now'))",
                        new["name"], new["gender"], new["date_of_birth"], new["contact"], new["location"])
            return redirect("/convert")

        else:
            db.execute("INSERT INTO new_convert(name, gender, date_of_birth, contact, location, joined_date) VALUES(?, ?, ?, ?, ?, date('now'))",
                        new["name"], new["gender"], new["date_of_birth"], new["contact"], new["location"])
            return redirect("/convert")

    return render_template("add-new-convert.html")

# Display new converts
def convert():
    convert = db.execute("SELECT * FROM new_convert ORDER BY joined_date")
    return render_template("new-convert.html", converts=convert)

# get first timers
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
                    flash("Name already exist.", category="error")
                    
            db.execute("INSERT INTO first_time_visitors(name, contact, location, gender, date_visited) VALUES(?, ?, ?, ?, date('now'))",
             new["name"], new["contact"], new["location"], new["gender"])
            return redirect("/vissitor")

        else:
            db.execute("INSERT INTO first_time_visitors(name, contact, location, gender, date_visited) VALUES(?, ?, ?, ?, date('now'))",
             new["name"], new["contact"], new["location"], new["gender"])
            return redirect("/visitor")

    return render_template("add-first-timers.html")

# display first time visitors
def visitors():
    visitors_name = db.execute("SELECT * FROM first_time_visitors ORDER BY id")
    return render_template("first-time-visitor.html", visitors_name=visitors_name)

# display birthday
def birthday():
    # Months for birthday
    months = ["1", "January","February","March","April", "May","June","July","August","September", "October","November","December"]
    this_month = int(db.execute("SELECT strftime('%m','now');")[0]["strftime('%m','now')"])
    birth_rec = db.execute("SELECT name, strftime('%Y',date_of_birth) as 'Year', strftime('%m',date_of_birth) as 'Month', strftime('%d',date_of_birth) as 'Day'FROM members;")
    return render_template("birthday.html", member=birth_rec, thisMONTH=this_month, months=months)

def weddingAnniversary():
    # Months for wedding
    months = ["1", "January","February","March","April", "May","June","July","August","September", "October","November","December"]
    this_month = int(db.execute("SELECT strftime('%m','now');")[0]["strftime('%m','now')"])
    birth_rec = db.execute("SELECT name, strftime('%Y',wedding_anniversary) as 'Year', strftime('%m',wedding_anniversary) as 'Month', strftime('%d',wedding_anniversary) as 'Day'FROM members;")
    return render_template("wedding.html", member=birth_rec, thisMONTH=this_month, months=months)

# take attendance
def takeAttendance():
    if request.method == "POST":
        num = request.form.getlist("num")
        totatl_attendance = len(num)
                
        # Check for attendance is taken
        if not num:
            message = "n"
            flash("Num field empty.", category="error")

            
        # Loop through the attendance , total_attendance=:total, total=totatl_attendance
        for name in num:
            db.execute("UPDATE attendance SET name=:name, total_attendance=:total, date=date('now') WHERE id >= 0",total=totatl_attendance,  name=name)
        
    member_names = db.execute("SELECT DISTINCT(name), id FROM members")

    return render_template("new-attendance.html", member_names=member_names)

# send apology for invalid input
def apology(message):
    return render_template("apology.html", message=message)

# get Offering
def payOffering():
    data = db.execute("SELECT * FROM offering;")

    if request.method == "POST":
        offering={}
        offering["name"] = request.form.get("name")
        offering["amount"] = request.form.get("amount")
        offering["number"] = request.form.get("account")
        if len(data) > 0:
            for name in data:
                if name["name"]== offering["name"]:
                    db.execute("UPDATE offering SET member_name=:name, amount=:amount, number=number, pay_day=date('now') WHERE id >= 0",name= offering["name"], amount=offering["amount"], number=offering["number"])
                    return redirect("/home")
            db.execute("INSERT INTO offering(member_name, amount, number, pay_day) VALUES(?, ?, ?, date('now'))", offering["name"], offering["amount"], offering["number"])
            return redirect("/home")

        else:
            db.execute("INSERT INTO offering(member_name, amount, number, pay_day) VALUES(?, ?, ?, date('now'))", offering["name"], offering["amount"], offering["number"])
            return redirect("/home")
    
    return render_template("offering.html", church=churchName)

# display notification
def notification():
    render_offering = db.execute("SELECT * FROM offering ORDER BY pay_day DESC;")
    # db.execute("DELETE FROM offering WHERE id > 0")
    return render_template("notification.html", notifying=render_offering)

# def sendAccountName():
#     acc = db.execute("SELECT name FROM account")
#     for name, same in zip(acc, acc_name):
#         print(name, same)

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