from re import S

from jinja2 import Template
from flask import Flask, Blueprint, render_template, request, jsonify, redirect
# from sqlalchemy.sql.expression import join
from flask_login import login_user, logout_user, login_required, current_user

from churchAPP import db
from .controller import notification, convert, payOffering, home,createMember, seeMember, new_convert, first_timer, visitors, birthday, weddingAnniversary, takeAttendance
views = Blueprint('views', __name__)

# Landing page


# dashboard
@views.route("/home")
@login_required
def index():
    return home()

# create New member
@views.route('/add-new-member', methods=["GET", "POST"])
@login_required
def addNewMember():
    return createMember()

# Display members
@views.route("/member")
@login_required
def member():
    return seeMember()

# New convert
@views.route("/add-new-convert", methods=["GET", "POST"])
@login_required
def get_new_convert():
    return new_convert()

# Convert
@views.route("/convert")
def displayNewConverts():
    return convert()

# First time visitor
@views.route("/add-first-timer", methods=["GET", "POST"])
@login_required
def get_FirtTimmer():
    return first_timer()

# get new visitor
@views.route("/visitor")
@login_required
def getVisitor():
     return visitors()

# Birthday list
@views.route("/birthday")
@login_required
def getBirthday():
    return birthday()

# wedding list
@views.route("/wedding")
@login_required
def sendWedding():
    return weddingAnniversary()
# create attendance
@views.route("/new-attendance", methods=["GET", "POST"])
@login_required
def attendance():
    return takeAttendance()

# calendar
@views.route('/calendar')
@login_required
def calendar():
    return render_template('calendar.html')

# graph
@views.route('/charts')
def charts():
    return render_template('charts.html')

# Contact
@views.route('/contact')
@login_required
def contact():
    return render_template('contact.html')

# Home 
@views.route('/dashboard')
def dashboard():
    return render_template('index.html')

# Emailing
@views.route('/email')
@login_required
def email():
    return render_template('email.html')


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
def getOffering():
    return payOffering()

# send notification
@views.app_context_processor
@login_required
def notifyUpdate():
    notify = len(db.execute("SELECT * FROM offering;"))
    return  dict(notify=notify)
    
# render notification template
@views.route("/notification")
@login_required
def renderNotification():
    return notification(), clearBNotification(notifyUpdate())

def clearBNotification(notes):
    notes = 0
    return notes