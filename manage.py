from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand
from marshmallow import Schema, fields, ValidationError,pre_load

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:1234@localhost/harshit?sslmode=require'

db = SQLAlchemy(app)
migrate = Migrate(app, db)

manager = Manager(app)
manager.add_command('db', MigrateCommand)

class Expense(db.Model):
    expenseid = db.Column(db.Integer, autoincrement=True, primary_key=True)
    email=db.Column(db.String, db.ForeignKey('user_detail.email'))
    date = db.Column(db.String)
    amount = db.Column(db.Float)
    category = db.Column(db.String(80))
    description = db.Column(db.String(80))

    def __init__(self):
        expenseid=self.expenseid,
        date=self.date,
        amount=self.amount,
        category=self.category


class user_detail(db.Model):
    uid = db.Column(db.Integer, autoincrement=True)
    uname = db.Column(db.String(30))
    email = db.Column(db.String(30),primary_key=True)
    username = db.Column(db.String(80))
    password = db.Column(db.String(80))

class category(db.Model):
    cid=db.Column(db.Integer, autoincrement=True, primary_key=True)
    cname=db.Column(db.String(30))

class ExpenseSchema(Schema):
    expenseid = fields.Int(dump_only=True)
    date = fields.Date()
    amount = fields.Int()
    category=fields.Str()

    def format_name(self, Expense):
        return "{}, {}".format(Expense.date, Expense.amount)


# Custom validator
def must_not_be_blank(data):
    if not data:
        raise ValidationError('Data not provided.')

expense_schema = ExpenseSchema()

if __name__ == '__main__':
    manager.run()
