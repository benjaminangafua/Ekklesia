from re import S

from jinja2 import Template
from flask import Flask, Blueprint, render_template, request, jsonify, redirect
# from sqlalchemy.sql.expression import join
from churchAPP import db
from .controller import notification, convert, payOffering, home,createMember, seeMember, new_convert, first_timer, visitors, birthday, weddingAnniversary, takeAttendance, createChurchAccount
views = Blueprint('views', __name__)

# Landing page
@views.route("/", methods=["GET", "POST"])
def registerChurch():
    return createChurchAccount()


# dashboard
@views.route("/home")
def index():
    return home()

# create New member
@views.route('/add-new-member', methods=["GET", "POST"])
def addNewMember():
    return createMember()

# Display members
@views.route("/member")
def member():
    return seeMember()

# New convert
@views.route("/add-new-convert", methods=["GET", "POST"])
def get_new_convert():
    return new_convert()

# Convert
@views.route("/convert")
def displayNewConverts():
    return convert()

# First time visitor
@views.route("/add-first-timer", methods=["GET", "POST"])
def get_FirtTimmer():
    return first_timer()

# get new visitor
@views.route("/visitor")
def getVisitor():
     return visitors()

# Birthday list
@views.route("/birthday")
def getBirthday():
    return birthday()

# wedding list
@views.route("/wedding")
def sendWedding():
    return weddingAnniversary()
# create attendance
@views.route("/new-attendance", methods=["GET", "POST"])
def attendance():
    return takeAttendance()

# calendar
@views.route('/calendar')
def calendar():
    return render_template('calendar.html')

# graph
@views.route('/charts')
def charts():
    return render_template('charts.html')

# Contact
@views.route('/contact')
def contact():
    return render_template('contact.html')

# Home 
@views.route('/dashboard')
def dashboard():
    return render_template('index.html')

# Emailing
@views.route('/email')
def email():
    return render_template('email.html')

# login
@views.route('/login')
def login():
    return render_template('login.html')

# sign-up
@views.route('/sign-up')
def signUp():
    return render_template('signUp.html')

# location
@views.route('/map')
def map():
    return render_template('map.html')
# price
@views.route('/price')
def price():
    return render_template('price.html')

# use's -profie
@views.route('/profile')
def profile():
    return render_template('profile.html')

#setting
@views.route('/settings')
def setting():
    return render_template('settings.html')

# table
@views.route('/table')
def table():
    return render_template('tables.html')
# offering
@views.route('/offering', methods=["GET", "POST"])
def getOffering():
    return payOffering()

# send notification
@views.app_context_processor
def notifyUpdate():
    notify = len(db.execute("SELECT * FROM offering;"))
    return  dict(notify=notify)
    
# render notification template
@views.route("/notification")
def renderNotification():
    return notification(), clearBNotification(notifyUpdate())

def clearBNotification(notes):
    notes = 0
    return notes