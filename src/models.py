from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Person(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=False, nullable=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    address = db.Column(db.String(120), unique=False, nullable=True)
    phone = db.Column(db.String(120), unique=True, nullable=True)

    def __repr__(self):
        'Person(name='+self.name+', email='+self.email+ ')'
    def serialize(self):
        return {
            "name": self.name,
            "email": self.email,
            "address": self.address,
            "phone": self.phone
        }
class Contact(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=False, nullable=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    address = db.Column(db.String(120), unique=False, nullable=True)
    phone = db.Column(db.String(120), unique=True, nullable=True)

    def __repr__(self):
        'Contact(name='+self.name+', email='+self.email+ ')'
    def serialize(self):
        return {
            "username": self.username,
            "email": self.email,
            "address": self.address,
            "phone": self.phone
        }