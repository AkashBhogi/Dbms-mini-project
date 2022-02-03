
from flask import Flask,render_template,request,session,redirect,url_for,flash
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from sqlalchemy import false
from werkzeug.security import generate_password_hash,check_password_hash
from flask_login import login_user,logout_user,login_manager,LoginManager,login_required,current_user

local_server = True
app= Flask(__name__)
app.secret_key='akash'



login_manager=LoginManager(app)
login_manager.login_view='login'


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))
#app.config['SQLALCHEMY_DATABASE_URL']='mysql://username:password@localhost/database_table_name'
app.config['SQLALCHEMY_DATABASE_URI']='mysql://root:@localhost/hms'
db=SQLAlchemy(app)

class Test(db.Model):
    id=db.Column(db.Integer,primary_key=True)
    name =db.Column(db.String(100))
    email =db.Column(db.String(100))


class User(db.Model,UserMixin):
    id=db.Column(db.Integer,primary_key=True)
    username=db.Column(db.String(50))
    email=db.Column(db.String(50),unique=True)
    password=db.Column(db.String(1000))

class Booking(db.Model,):
    pid=db.Column(db.Integer,primary_key=True)
    name=db.Column(db.String(50))
    email=db.Column(db.String(50))
    gender=db.Column(db.String(50))
    time=db.Column(db.String(50),nullable=False)
    date=db.Column(db.String(50),nullable=False)
    book=db.Column(db.String(50))
    number=db.Column(db.String(12))


@app.route('/bye')
def hi():
    Test.query.all()
    return 'My database is connected'

@app.route('/')
def index():
    flash("Welcome to home page")
    return render_template('index.html')

@app.route('/doctors')
def doctors():
    return render_template('doctors.html')

@app.route('/booking',methods=['POST','GET'])
@login_required
def booking():
    if request.method=="POST":
        email=request.form.get('email')
        name=request.form.get('name')
        gender=request.form.get('gender')
        time=request.form.get('time')
        date=request.form.get('date')
        book=request.form.get('book')
        number=request.form.get('number')
        query=db.engine.execute(f"INSERT INTO `booking`(`name`,`email`,`gender`,`time`,`book`,`number`,`date`) VALUES('{name}','{email}','{gender}','{time}','{book}','{number}','{date}')")
        flash("Booking Confirmed","info")
    return render_template('booking.html')

@app.route('/booking details')
@login_required
def bookingdetails():
    em=current_user.email
    query=db.engine.execute(f"SELECT * FROM `booking` WHERE email='{em}'")
    return render_template('booking details.html',query=query)

@app.route('/edit/<string:pid>',methods=['POST','GET'])
@login_required
def edit(pid):
    post=Booking.query.filter_by(pid=pid).first()
    if request.method=="POST":
        email=request.form.get('email')
        name=request.form.get('name')
        gender=request.form.get('gender')
        time=request.form.get('time')
        date=request.form.get('date')
        book=request.form.get('book')
        number=request.form.get('number')
        db.engine.execute(f" UPDATE `booking` SET `email`='{email}',`name`='{name}',`gender`='{gender}',`time`='{time}',`date`='{date}',`book`='{book}',`number`='{number}' WHERE `booking`.`pid`={pid}")
        flash("booking is updated","success")
        return redirect(url_for("bookingdetails"))
    return render_template('edit.html',post=post)

@app.route('/delete/<string:pid>',methods=['POST','GET'])
@login_required
def delete(pid):
    db.engin.execute(f"DELETE FROM `booking` WHERE `booking`.`pid`={pid}")
    flash("Slot deleted succesfully","danger")
    return redirect(url_for("bookingdetails"))

@app.route('/login',methods=['POST','GET'])
def login():
    if request.method=="POST":
        email=request.form.get('email')
        password=request.form.get('password')
        user=User.query.filter_by(email=email).first()

        if user and user.password==password:
            login_user(user)
            flash("Login Success","primary")
            return redirect(url_for("index"))
        else:
            flash("Invalid Credentials","danger") 
            return render_template('login.html')
    
    return render_template('login.html')

@app.route('/signup',methods=['POST','GET'])
def signup():
    if request.method=="POST":
        username=request.form.get('username')
        email=request.form.get('email')
        password=request.form.get('password')
        user=User.query.filter_by(email=email).first()
        if user:
            flash("email already exists","Warning" )
            return render_template('signup.html')
        
        new_user=db.engine.execute( f"INSERT INTO `user`(`username`,`email`,`password`) VALUES ('{username}','{email}','{password}');") 
        return render_template('login.html')
    flash("Signup Succes Please Login","success")
    return render_template('signup.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash("Logout SuccessFul","warning")
    return redirect(url_for('login'))

@app.route('/test')
def test():
    return render_template('test.html')

app.run(debug=True)  