from churchAPP.models import db


class Note(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    data = db.Column(db.String(10000))
    date = db.Column(db.DateTime(timezone=True))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

# class Reminder 

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(50), unique=True)
    password = db.Column(db.String(150))
    first_name = db.Column(db.String(150))
    notes = db.relationship('Note') 

class Payments(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    member_name = db.Column(db.String(50), db.ForeignKey('members.id'))
    due  = db.Column(db.Numeric)
    offering = db.Column(db.Numeric)
    donation = db.Column(db.Numeric)
    tithe = db.Column(db.Numeric)


class Finance(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    payment_id = db.Column(db.Integer, db.ForeignKey('payments.id'))
    revenue = db.Column(db.Numeric)
    expenses = db.Column(db.Numeric)
    total_offering = db.Column(db.Numeric)
    
class Departments(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    member_id = db.Column(db.Integer,  db.ForeignKey('members.id'))

class Irregular_member(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    attendance_id = db.Column(db.Integer,  db.ForeignKey('attendance.id'))
    total_absences = db.Column(db.Integer)
    
class Members(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(150))
    location = db.Column(db.String(150))
    department = db.Column(db.String(150))
    contact = db.Column(db.String(150))
    role_play = db.Column(db.String(150))
    occupation = db.Column(db.String(150))
    relationship = db.Column(db.String(150))
    date_of_birth = db.Column(db.String(150))
    joined_date = db.column(db.DateTime(timezone=True))
    gender = db.Column(db.String(150))

class Attendance(db.Model):
    id = db.Column(db.Integer, primary_key=True) 
    date = db.column(db.DateTime(timezone=True))
    member_id = db.Column(db.Integer,  db.ForeignKey('members.id'))

class New_convert(db.Model):
    id = db.Column(db.Integer, primary_key=True) 
    name = db.Column(db.String(150))
    contact = db.Column(db.String(150))
    location = db.Column(db.String(150))
    date = db.column(db.DateTime(timezone=True))

class Bihdayrt(db.Model):
    id = db.Column(db.Integer, primary_key=True) 
    name = db.Column(db.String(150))
    day  = db.Column(db.Integer)
    month  = db.Column(db.Integer)
    member_id = db.Column(db.Integer,  db.ForeignKey('members.id'))
