from wtforms import Form,IntegerField,StringField,PasswordField, validators,TextAreaField,DateField
from  collections import OrderedDict

class Register(Form):
    name=StringField('Name ')
    email=StringField('Email ')
    username = StringField('Username')
    password=PasswordField('Password ',[validators.DataRequired(),validators.EqualTo('confirm',message='Password do not match')])
    confirm=PasswordField('Confirm Password')

class auth(Form):
    username = StringField('Username')
    password = PasswordField('Password ', [validators.DataRequired()])

class add_expense(Form):
    date=DateField('Date',format='%m/%d/%Y')
    amount = IntegerField('Amount(Rs)')
    category=StringField('Category')
    description=TextAreaField('Description')

class DictSerializable(object):
    def _asdict(self,a):
        result = OrderedDict()
        for key in self.__mapper__.c.keys():
            result[key] = getattr(self, key)
        return result