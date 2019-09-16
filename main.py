from flask import Flask, render_template ,request,url_for,escape,session,redirect,abort
import sqlite3 as sql
from flask_bcrypt import Bcrypt
app = Flask(__name__)
app.secret_key = 'any random string'
bcrypt = Bcrypt(app)
#initial route
@app.route('/')
def index():
	return render_template('sfiplogin.html')
#to register as a new user
@app.route('/signup', methods = ['GET','POST'])
def signup():
	return render_template('sfipreg.html')
@app.route('/register', methods = ['GET','POST'])
def register():
	if request.method == 'POST':
		name=request.form['name']
		roll_no = request.form['roll']
		branch=request.form['branch']
		year=request.form['year']
		semester=request.form['semester']
		email=request.form['email']
		mobile=request.form['mobile']
		password =bcrypt.generate_password_hash(request.form['pass']).decode('UTF-8')
		with sql.connect("database.db") as con:
			cur = con.cursor()
			cur.execute("select * from users where roll_no = (?)",[request.form['roll']])
			name2=cur.fetchall()
			if name2:
				ms2="already existing roll no"
				return render_template("sfipreg.html",ms2=ms2)
			cur.execute("INSERT INTO users (name,roll_no,branch,year,semester,email,mobile,password) VALUES (?,?,?,?,?,?,?,?)",(name,roll_no,branch,year,semester,email,mobile,password))
			msg = "registered successfully now login"
			con.commit()
		con.close()
		return render_template('sfiplogin.html',msg=msg)
#login as a user
@app.route('/login', methods =['GET','POST'] )
def login():
	if request.method == 'POST':
		con = sql.connect("database.db")
		cur = con.cursor()
		cur.execute("select * from users where roll_no =?",[request.form['roll']])
		name=cur.fetchall()
		cur.execute('SELECT password FROM users WHERE roll_no=?',[request.form['roll']])
		pas=cur.fetchone();
		if name:
			if bcrypt.check_password_hash(pas[0],request.form['password']):
				session['roll_no'] = request.form['roll']
				cur.execute("select branch from users where roll_no=?",[request.form['roll']])
				branch = cur.fetchone();
				cur.execute("select semester from users where roll_no=?",[request.form['roll']])
				semester = cur.fetchone();
				cur.execute("select * from profs where branch=? and semester=? ",(branch[0],semester[0]))
				lis=cur.fetchall()
				return render_template('stform.html',lis=lis)
			else:
				alr="wrong password"
				return render_template('sfiplogin.html',alr=alr)
		else:
			alr="not registered yet"
			return render_template('sfiplogin.html',alr=alr)
	else:
		session['roll_no']=request.args.get('roll_no')
		return render_template('front.html')
	con.close()
#logout as a user
@app.route('/logout')
def logout():
	session.pop('roll_no',None)
	return redirect(url_for('index'))
if(__name__ == "__main__"):
	app.run(debug = True)
