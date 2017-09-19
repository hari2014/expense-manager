from flask import Flask,render_template,redirect,flash,url_for,session, logging,request,jsonify,send_file,json
import os
from manage import db
from manage import user_detail,Expense,expense_schema
from forms import add_expense
from sqlalchemy.sql import func,label
from  collections import defaultdict
app = Flask(__name__)

app.config['DEBUG'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True

@app.route("/" )
def index():
    return  render_template('index1.html')


@app.route('/register', methods=['POST'])
def register():
    json_data = request.json
    print json_data['name']
    print json_data['email']

    user = user_detail(
        uname=json_data['name'],
        email=json_data['email'],
        password=json_data['password']
    )
    try:
        db.session.add(user)
        db.session.commit()
        status = 'success'
    except:
        status = 'this user is already registered'
    db.session.close()
    return jsonify({'result': status})


@app.route('/login',methods=['POST'])
def login():
    if request.method=='POST':
        json_data = request.json
        #print json_data
        arg1=json_data['email']
        arg2=json_data['password']

        user = db.session.query(user_detail.password).filter(user_detail.email==arg1).all()
        #print (type(user))
        #print user[0].password
        if user is not None and user[0].password==arg2:
            status = True
            user1 = db.session.query(user_detail.uname).filter(user_detail.email == arg1).all()
            session['logged_in']=True
            session['email'] = json_data['email']
        else:
            status = False
    #print status
    return jsonify({'result': status})


@app.route('/logout')
def logout():
    session.pop('logged_in', None)
    session.pop('email', None)
    return jsonify({'result': 'success'})

@app.route('/filter',methods=['POST'])
def filter():
    if request.method=='POST':
        json_data = request.json
        print json_data
        start=json_data['from']
        end=json_data['to'];
        user = db.session.query(Expense.category, func.sum(Expense.amount)).filter(Expense.date >= start, Expense.date <= end).group_by(Expense.category).all()
        print user
        json_list = json.dumps(user)
        if user==None:
            status = False
            return jsonify({'result': status})
        else:
            status=True
            return json_list




@app.route('/status')
def status():
    if session.get('logged_in'):
        if session['logged_in']:
            print session['logged_in']
            return jsonify({'status': True})
    else:
        return jsonify({'status': False})

@app.route('/add_expense',methods=['POST'])
def expense():
        if request.method == 'POST':
            exp=Expense()
            if request.json:
                json_data = request.json
                print json_data
                exp.date = str(json_data['date'])
                exp.amount = json_data['amount']
                exp.category = json_data['category']
                exp.description = json_data['Description']
                exp.email = session['email']
                db.session.add(exp)
                db.session.commit()
                status="success"
                return jsonify({'result': status})
            else:
                print "No"
                status = "No"
                return jsonify({'result': status})


class DateTimeEncoder(json.JSONEncoder):
    def default(self, obj):
       if hasattr(obj, 'isoformat'):
           return obj.isoformat()
       else:
           return json.JSONEncoder.default(self, obj)


@app.route('/drill',methods=['POST'])
def data_drill():
    if request.method=='POST':
        json_data = request.json
        cat=json_data['message']
        email=session['email']
        print cat
        users=db.session.query(Expense.date, Expense.amount).filter(Expense.category==cat).filter(Expense.email==email).all()
        print users
        json_list = json.dumps(users,cls=DateTimeEncoder)
        print json_list
        return json_list





@app.route('/data')
def detail():
    email = session['email']
    print email
    #check=db.session.query(Expense.category, func.sum(Expense.amount)).filter(Expense.email==email).group_by(Expense.category).first()
    users=db.session.query(Expense.category, func.sum(Expense.amount)).filter(Expense.email==email).group_by(Expense.category).all()
    print users;
    json_list = json.dumps(users)
    return json_list





if __name__ == "__main__":
    app.secret_key = 'super secret key'
    db.init_app(app)
    port = int(os.environ.get('PORT', 5000))  # locally PORT 5000, Heroku will assign its own port
    app.run(host='0.0.0.0', port=port)
