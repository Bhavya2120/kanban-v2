from flask import Flask,jsonify, render_template,session,request,make_response,render_template,jsonify,send_file,redirect
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import create_access_token
from flask_jwt_extended import get_jwt_identity
from flask_jwt_extended import jwt_required
from flask_jwt_extended import JWTManager,get_jwt
from datetime import timedelta,datetime,date
import bcrypt
from cache import cache
from flask_cors import CORS
import pandas as pd
import matplotlib.pylab as plt
'''Done for testing GoogleSpace'''
import os
import requests
'''Ends Here'''

'''Celery'''
from celery import Celery
from celery.schedules import crontab
'''Ends Here'''

'''Sending Email'''
from jinja2 import Environment, PackageLoader,Template
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication
from os.path import basename
import smtplib
'''Ends Here'''

'''Convert HTML to PDF'''
from weasyprint import HTML
'''Ends Here'''
app = Flask(__name__)
cache.init_app(app)

ACCESS_EXPIRES = timedelta(hours=2)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///project.sqlite3'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
CORS(app, origins='*')
app.config["JWT_SECRET_KEY"] = "kanbanv2bhavyadua9521/f10036/4" 
app.config["JWT_ACCESS_TOKEN_EXPIRES"] = ACCESS_EXPIRES

app.config['CACHE_REDIS_URL'] = 'redis://localhost:6379/3'
app.config['CACHE_TYPE'] = 'RedisCache'
app.config['CACHE_DEFAULT_TIMEOUT'] = 15
jwt = JWTManager(app)

def make_celery(app):
    #Celery configuration
    app.config['CELERY_BROKER_URL'] = 'redis://localhost:6379/0'
    app.config['CELERY_RESULT_BACKEND'] = 'redis://localhost:6379/0'
    app.config['CELERYBEAT_SCHEDULE'] = {
        # Executes every day at 10 PM
        'daily_reminder-every-minute': {
            'task': 'daily_reminder',
            'schedule': crontab(minute=0,hour=22)
        },
            'monthly_report-every-month': {
                'task': 'monthly_report',
                'schedule': crontab(0, 0, day_of_month='1')
            }
    }

    celery = Celery(app.import_name, broker=app.config['CELERY_BROKER_URL'])
    celery.conf.update(app.config)
    TaskBase = celery.Task
    class ContextTask(TaskBase):
        abstract = True
        def __call__(self, *args, **kwargs):
            with app.app_context():
                return TaskBase.__call__(self, *args, **kwargs)
    celery.Task = ContextTask
    return celery
celery = make_celery(app)

#---------------------------------------------MODELS-------------------------------------------------------------------
class users(db.Model):
    __name__ = "users"
    user_id = db.Column(db.Integer, primary_key=True, autoincrement=True,nullable=False)
    user_name = db.Column(db.String(255),nullable=False)
    user_mail = db.Column(db.String(255),unique=True,nullable=False)
    user_password = db.Column(db.String(150),nullable=False)

class lists(db.Model):
    __name__ = "lists"
    list_id = db.Column(db.Integer, primary_key=True,autoincrement=True,nullable=False)
    list_name=db.Column(db.String(255),nullable=False)
    list_user= db.Column(db.Integer,db.ForeignKey('users.user_id'),nullable=False)

class cards(db.Model):
    __name__ = "cards"
    card_id = db.Column(db.Integer, primary_key=True,autoincrement=True,nullable=False)
    card_title=db.Column(db.String(255),nullable=False)
    card_content=db.Column(db.String(255))
    card_complete=db.Column(db.Boolean,default=False)
    card_complete_date=db.Column(db.Text)
    card_create_date=db.Column(db.DateTime,nullable=False,default = datetime.utcnow())
    card_deadline=db.Column(db.DateTime,nullable=False)
    card_user=db.Column(db.Integer,db.ForeignKey('users.user_id'),nullable=False)
    card_list=db.Column(db.Integer,db.ForeignKey('lists.list_id'),nullable=False)

#db.create_all()


#---------------------------------------------ROUTES-------------------------------------------------------------------

#---------------User Stuff------------
@app.route('/')
@jwt_required()
def home():
    if not get_jwt_identity():
        raise("Identity not verified")
    current_user = get_jwt_identity()
    return jsonify(logged_in_as=current_user), 200

@app.route('/register', methods=['GET','POST'])
def register():
    if request.method=='POST':
        data = request.json
        name = data['name']
        mail = data['mail']
        password = data['password']
        encrypt = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
        new_user = users(user_name=name,user_mail=mail,user_password=encrypt)
        db.session.add(new_user)
        db.session.commit()
        return "Success",200

@app.route("/login",methods=['GET','POST'])
def login():    
  data = request.json
  enc = data['password'].encode('utf-8')
  cur_user = users.query.filter_by(user_mail=data['mail']).first()
  token = create_access_token(identity={"mail":cur_user.user_mail})
  if(bcrypt.checkpw(enc,cur_user.user_password)):
    return jsonify({'access_token': token, 'name':cur_user.user_name,'id':cur_user.user_id})
  else:
    return "Failure",402

#---------------List Stuff-----------------

@app.route('/createlist/<int:id>', methods=['GET', 'POST'])
def createlist(id):
    if request.method=='POST':
        data = request.json
        listname = data['listname']
        newlist = lists(list_user=id,list_name=listname)
        db.session.add(newlist)
        db.session.commit()
        return "Success",200

@app.route('/lists/<int:list_user>', methods=['GET', 'POST'])
#@cache.memoize(timeout=10)
def users_list(list_user):
    all_lou = lists.query.filter_by(list_user=list_user).all()
    l = []
    for i in all_lou:
        d = {
            'userid' : i.list_user,
            'listid' : i.list_id,
            'listname' : i.list_name,
        }
        l.append(d)
    return jsonify(
        {
            'list' : l,
            'message' : 'Success'
        }
    )

@app.route('/lists/update/<int:list_id>', methods=['GET','POST'])
def update_list(list_id):
    currentlist= lists.query.filter_by(list_id=list_id).first()
    if request.method == 'POST':
        data=request.json
        currentlist.list_name=data['list_name']
        db.session.add(currentlist)
        db.session.commit()
    return jsonify({'message': 'success'})

@app.route('/lists/delete/<int:id>', methods=['GET'])
def del_list(id):
    listdel = lists.query.filter_by(list_id=id).first()
    flag=0
    if(listdel):
        flag=1
        cardsdel = cards.query.filter_by(card_list=id).all()
        for i in cardsdel:
            db.session.delete(i)
    db.session.delete(listdel)
    db.session.commit()
    if flag==1:
        return jsonify({'message': 'success'})
    else:
        return jsonify({'message': 'No List Found!'})

@app.route('/export/<int:id>',methods=['GET', 'POST'])
@celery.task(name='exportlist')
def export_lists(id):
    lou = lists.query.filter_by(list_user=id)
    exportable = []
    for i in lou:
        l=[]
        count=0
        l.append(i.list_name)
        exportable.append(l)
    df=pd.DataFrame(exportable, columns=['List Name'])
    fp=open('yourlists.csv','w')
    fp.close()
    #root='c:\\Users\\sam68\\OneDrive\\Desktop\\MAD2Project\\backend' - works on Windows
    #df.to_csv(root+'\\'+'yourlists.csv',index=False)
    df.to_csv('yourlists.csv',index=False) # - works on WSL
    return send_file('yourlists.csv')

@app.route('/summary/<int:list_id>',methods=['GET', 'POST'])
def summary_list(list_id):
    currentlist=lists.query.filter_by(list_id=list_id).first()
    col=cards.query.filter_by(card_list=list_id).all()
    s=[]
    graph={}
    complete_cards=0
    total_cards=0
    incomplete_cards=0
    tasks_past_deadline=0
    tasks_completed_past_deadline=0
    for i in col:
        if i.card_complete_date=='Not yet Complete':
            today=date.today()
            i.card_deadline=str(i.card_deadline)
            i.card_deadline=i.card_deadline[0:10]
            i.card_deadline=datetime.strptime(i.card_deadline,'%Y-%m-%d').date()
            if today>i.card_deadline:
                tasks_past_deadline+=1
        total_cards+=1
        if i.card_complete==1:
            i.card_deadline = i.card_deadline.date()
            i.card_complete_date = datetime.strptime(i.card_complete_date,"%Y-%m-%d").date()
            curdate=i.card_complete_date
            count=0
            allcards=cards.query.filter_by(card_complete_date=curdate,card_list=list_id)
            for x in allcards:
                count+=1
            graph.update({i.card_complete_date:count})
            complete_cards+=1
            #i.card_complete_date=datetime.strptime(i.card_complete_date, '%Y-%m-%d').date()
            #i.card_deadline=str(i.card_deadline)
            #i.card_deadline=i.card_deadline[0:10]
            #i.card_deadline=datetime.strptime(i.card_deadline,'%Y-%m-%d').date()
            if i.card_complete_date>i.card_deadline:
                tasks_completed_past_deadline+=1
        s=[{
            'list_name':currentlist.list_name,
            'total_cards': total_cards,
            'complete_cards': complete_cards,
            'tasks_past_deadline': tasks_past_deadline,
            'tasks_completed_past_deadline': tasks_completed_past_deadline
        }]
    plt.bar(*zip(*graph.items()))
    plt.title('Date vs Number of Cards completed on that date')
    plt.xlabel('Date')
    plt.ylabel('Number of Cards')
    plt.xticks(rotation=30)
    plt.savefig('../frontend/src/assets/logo.png')
    return jsonify({
        'status': 'success',
        'summaryoflist': s,
        })



#---------------Card Stuff-----------------

@app.route('/addcard/<int:list_id>', methods=['GET', 'POST'])
def addcard(list_id):
    newcard = lists.query.filter_by(list_id=list_id).first()
    d = {
            'card_user' : newcard.list_user,
            'card_list' : newcard.list_id
        }

    if request.method=='POST':
        data = request.json
        title = data['card_title']
        content = data['card_content']
        complete = data['card_complete']
        complete_date = data['card_complete_date']
        deadline = data['card_deadline']
        complete=bool(complete)
        deadline = datetime.strptime(deadline, '%Y-%m-%d').date()
        if complete_date=='':
            complete_date='Not yet Complete'
        else:
            complete_date=data['card_complete_date']
            complete_date=datetime.strptime(complete_date, '%Y-%m-%d').date()
        newcard = cards(card_user=newcard.list_user,card_list=newcard.list_id,card_title=title,card_content=content,card_complete=complete,card_deadline=deadline,card_complete_date=complete_date)
        db.session.add(newcard)
        db.session.commit()

        return jsonify({'message':'success'})
    else:
        return jsonify({'message':'failure' })

@app.route('/cards/<int:cardlist>', methods=['GET', 'POST'])
def lists_card(cardlist):
    acol = cards.query.filter_by(card_list=cardlist).all()
    l=[]
    for i in acol:
        d1 = {
            'cardid' : i.card_id,
            'card_list' : i.card_list,
            'card_title' : i.card_title,
            'card_content' : i.card_content,
            'card_complete' : i.card_complete,
            'card_complete_date' : i.card_complete_date,
            'card_deadline' : i.card_deadline
        }
        l.append(d1)
    return jsonify({'cardsoflist' : l})


@app.route('/cards/update/<int:id>',methods=['GET', 'POST'])
def update_card(id):
    currentcard=cards.query.filter_by(card_id=id).first()
    currentlist=lists.query.filter_by(list_id=currentcard.card_list).first()
    currentuser=users.query.filter_by(user_id=currentcard.card_user).first()
    d = {
            'card_id' : currentcard.card_id,
            'card_user' : currentcard.card_list,
            'list_name' : currentlist.list_name,
            'user_id' : currentuser.user_id

        }
    if request.method == 'POST':
        data=request.json
        currentcard.card_title=data['card_title']
        currentcard.card_content=data['card_content']
        currentcard.card_complete=bool(data['card_complete'])
        currentcard.card_list=data['card_list']
        currentcard.card_complete_date=data['card_complete_date']
        if currentcard.card_complete_date!='':
            currentcard.card_complete_date=datetime.strptime(currentcard.card_complete_date, '%Y-%m-%d').date()
    db.session.add(currentcard)
    db.session.commit()
    return jsonify({'message': 'success'})

@app.route('/cards/delete/<int:card_id>', methods=['GET'])
def del_card(card_id):
    carddel = cards.query.filter_by(card_id=card_id).first()
    db.session.delete(carddel)
    db.session.commit()
    return jsonify({'message': 'success'})

@app.route('/exportcard/<int:list_id>',methods=['GET', 'POST'])
@celery.task(name='exportcard')
def export_cards(list_id):
    col = cards.query.filter_by(card_list=list_id) #.all() not required
    curlist=lists.query.filter_by(list_id=list_id).first()
    NAME=curlist.list_name
    exportable = []
    for i in col:
        l=[]
        l.append(i.card_title)
        l.append(i.card_content)
        l.append(i.card_complete)
        l.append(i.card_complete_date)
        l.append(i.card_deadline)
        exportable.append(l)
    df=pd.DataFrame(exportable, columns=['Card Title','Card Content','Completion Status','Completion Date','Deadline'])
    file=NAME+'_cards.csv'
    fp=open(file,'w')
    fp.close()
    #root='c:\\Users\\sam68\\OneDrive\\Desktop\\MAD2Project\\backend'
    #df.to_csv(root+'\\'+ file,index=False)
    df.to_csv(file,index=False)
    return send_file(file)
    
#-------------------------------------------------PERIODIC TASKS-------------------------------
@app.route('/daily_reminder')
@celery.task(name="daily_reminder")
def daily_reminder():
    WEBHOOK_URL='https://chat.googleapis.com/v1/spaces/AAAAunf78_Y/messages?key=AIzaSyDdI0hCZtE6vySjMm-WEfRq3CPzqKqqsHI&token=oaeqO7iUPOYk3R41fwaz7kThSnWlT23UoaCFNgdbKWU%3D' #this is for single user wtf
    allusers=users.query.all()
    for i in allusers:
        cou=cards.query.filter_by(card_user=i.user_id).all()
        for j in cou:
            if j.card_complete==0:
                x='Hi, you have your card '
                y=j.card_title
                z=' pending, please complete it! '
                a='It is due for completion by '
                b=str(j.card_deadline)
                b=b[0:10]
                res = requests.post(WEBHOOK_URL, json={'text': x+y+z+a+b})
    return "Alert Sent!"

@app.route('/monthly_report')
@celery.task(name="monthly_report")
def monthly_report():
    with app.app_context():
        file_loader = PackageLoader("app", "templates")
        env = Environment(loader=file_loader)
        allusers = users.query.all()
        for user in allusers:
            userid = user.user_id
            userdata = users.query.filter_by(user_id=userid).first()
            list1 = lists.query.filter_by(list_user=userid).all()
            l=[]
            for i in list1:
                data={}
                count=0
                allcards = cards.query.filter_by(card_list=i.list_id).all()
                numberofcards=0
                late_complete=0
                within_time=0
                for j in allcards:
                    numberofcards+=1
                    data['list_name'] = i.list_name
                    if j.card_complete==1:
                        count+=1
                        j.card_complete_date=datetime.strptime(j.card_complete_date, '%Y-%m-%d').date()
                        j.card_deadline=str(j.card_deadline)
                        j.card_deadline=j.card_deadline[0:10]
                        j.card_deadline=datetime.strptime(j.card_deadline,'%Y-%m-%d').date()
                        if j.card_complete_date>j.card_deadline:
                            late_complete+=1
                        elif j.card_complete_date<=j.card_deadline:
                            within_time+=1
                    data['completed_cards'] = count
                    data['late_complete']=late_complete
                    data['within_time']=within_time
                data['number_of_cards']=numberofcards
                l.append(data)
                msg = format_report("./templates/report.html",data=l,User=user.user_name)
                html = HTML(string=msg)
                file_name = str(user.user_name)+"report"+".pdf"
                html.write_pdf(target=file_name)
            msg = MIMEMultipart()
            msg["From"] = 'sam689756@gmail.com'
            msg["To"] = user.user_mail
            msg["Subject"] = "Monthly Report"
            body = MIMEText("Here is your Monthly Report", "plain")
            msg.attach(body)
            
            #rendered = env.get_template("report.html").render(userdata=userdata,data=l)
            #filename = "report.html"
            #with open(f"{filename}", "w") as f:
            #        f.write(rendered)
            with open(f"{file_name}", "rb") as f:
                    attachment = MIMEApplication(f.read(), Name=basename(file_name))
                    attachment["Content-Disposition"] = 'attachment; filename="{}"'.format(basename(file_name))

            msg.attach(attachment)

            with smtplib.SMTP("smtp.gmail.com") as connection:
                    connection.starttls()
                    connection.login(user='sam689756@gmail.com', password='dmynbrfjcvqvykjp')
                    connection.send_message(
                        msg=msg,
                        from_addr='sam689756@gmail.com',
                        to_addrs=[user.user_mail],
                    ) 
            #Check ends here
        return "Monthly Report Sent"

def format_report(template1,data,User="User"):
    with open(template1) as file:
        temp = Template(file.read())
        return temp.render(data=data,User=User)
       
def pdf_report(d,User):
    msg = format_report("./templates/report.html",data=d,User=User)
    html = HTML(string=msg)
    file_name = str(User)+"report"+".pdf"
    html.write_pdf(target=file_name)

if __name__ == '__main__':
    app.run(debug=True)