from flask import Flask, render_template ,request,url_for,escape,session,redirect,abort
import sqlite3 as sql
# import admin
from flask_bcrypt import Bcrypt
app = Flask(__name__)
app.secret_key = 'any random string'
bcrypt = Bcrypt(app)


def Convert(tup, di):
	di = dict(tup)
	return di



#INITIAL route
@app.route('/')
def index():
	return render_template('sfiplogin.html')


#REGISTER page
@app.route('/signup', methods = ['GET','POST'])
def signup():
	return render_template('sfipreg.html')


# REGISTRATION module
@app.route('/register', methods = ['GET','POST'])
def register():
	if request.method == 'POST':
		name=request.form['name']
		roll_no = request.form['roll']
		branch=request.form['branch']
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
			cur.execute("INSERT INTO users (name,roll_no,branch,semester,email,mobile,password) VALUES (?,?,?,?,?,?,?)",(name,roll_no,branch,semester,email,mobile,password,))
			msg = "registered successfully now login"
			con.commit()
		con.close()
		return render_template('sfiplogin.html',msg=msg)


#LOGIN module
@app.route('/login', methods =['GET','POST'] )
def login():
	if request.method == 'POST':
		con = sql.connect("database.db")
		cur = con.cursor()
		cur.execute("select roll_no from users where roll_no =?",[request.form['roll']])
		name=cur.fetchall()
		cur.execute('SELECT password FROM users WHERE roll_no=?',[request.form['roll']])
		pas=cur.fetchone()
		if name:
			if bcrypt.check_password_hash(pas[0],request.form['password']):
				admin=name[0][0]
				if(admin == "admin"):
					return render_template("admin.html")
				session['roll_no'] = request.form['roll']
				cur.execute("select branch from users where roll_no=?",[request.form['roll']])
				branch = cur.fetchone()
				session['branch']=branch[0]
				print(session['branch'])
				cur.execute("select semester from users where roll_no=?",[request.form['roll']])
				semester = cur.fetchone()
				session['semester']=semester[0]
				print(session['semester'])
				cur.execute("select name,subject from profs where branch=? and semester=? ",(branch[0],semester[0]))
				global lis1
				lis1=cur.fetchall()
				cur.execute("select distinct lecturer,subject from feedback where st_rollno=?", [session['roll_no']])
				global lis2
				lis2 = cur.fetchall()
				global lis3
				lis3 = [x for x in lis1 if x not in lis2]
				dictionary = {}
				session['lisp'] = Convert(lis3, dictionary)
				session['exist'] = Convert(lis2, dictionary)

				con.close()

				return render_template('show_profs.html',lisp=session['lisp'],exist=session['exist'])
			else:
				alr="wrong password"
				return render_template('sfiplogin.html',alr=alr)
		else:
			alr="not registered yet"
			return render_template('sfiplogin.html',alr=alr)
	else:
		session['roll_no']=request.args.get('roll_no')
		return render_template('show_profs.html')
	con.close()


# Show PROFESSOR list
@app.route('/show_profs')
def show_profs():
	return render_template('show_profs.html', lisp=session['lisp'],exist=session['exist'])


# Display feedback FORM
@app.route('/stform')
def stform():
	print(session['branch'],session['semester'])
	return render_template('stform.html', branch=session['branch'],semester=session['semester'])



# FEEDBACK MODULE......
@app.route('/feedback', methods=['POST', 'GET'])
def feedback():
	if request.method == 'POST':
		lecturer = request.form['lecturer']
		st_rollno = session['roll_no']
		semester = session['semester']
		branch = session['branch']
		subject = request.form['subject']
		preparation = request.form['preparedness']
		information = request.form['informative']
		explanation = request.form['explaining']
		pace = request.form['pace']
		leadership = request.form['leading']
		receptive = request.form['receptive']
		interest = request.form['interest']
		discussion = request.form['discussion']
		learning = request.form['learn']
		rapport = request.form['rapport']
		available = request.form['available']
		current = [lecturer,st_rollno,semester,branch,subject]

		con = sql.connect("database.db")
		cur = con.cursor()

		cur.execute("select lecturer,st_rollno,semester,branch,subject from feedback where st_rollno=?",[session['roll_no']])
		alrdyexist=cur.fetchall()

		for i in range(0,len(alrdyexist)):
			if list(alrdyexist[i]) == current:
				msgx="This feedback is already registered"
				con.close()

				return render_template('show_profs.html', lisp=session['lisp'], msgx=msgx, exist=session['exist'])

		else:
			cur.execute("INSERT INTO feedback (lecturer,st_rollno,semester,branch,subject,preparation,information,explanation,pace,leadership,receptive,interest,discussion,learning,rapport,available)VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)",(lecturer,st_rollno,semester,branch,subject,preparation,information,explanation,pace,leadership,receptive,interest,discussion,learning,rapport,available,))
			con.commit()
			cur.execute("select distinct lecturer,subject from feedback where st_rollno=?", [session['roll_no']])
			global lis1,lis2,lis3
			lis2 = cur.fetchall()
			lis3 = [x for x in lis1 if x not in lis2]
			dictionary = {}
			session['lisp'] = Convert(lis3, dictionary)
			session['exist'] = Convert(lis2, dictionary)

			con.close()
			return redirect(url_for('show_profs'))



#view RESPONSE
@app.route('/response', methods=['POST', 'GET'])
def response():
	if request.method == 'POST':
		restech = request.form['restech']
		ressub = request.form['ressub']
		print(restech)
		print(ressub)
		con = sql.connect("database.db")
		cur = con.cursor()
		cur.execute("select preparation,information,explanation,pace,leadership,receptive,interest,discussion,learning,rapport,available from feedback where st_rollno=? and lecturer=? and subject=?",(session['roll_no'],restech,ressub))
		out=cur.fetchall()
		res = [item for t in out for item in t]
		print(res)
		return render_template('response.html', res=res,branch=session['branch'],semester=session['semester'],restech=restech,ressub=ressub)

	else:
		print('this worked')

#
#
# #Add_Teachers
# @app.route('/addtech',methods=['POST','GET'])
# def addtech():
# 	if request.method=='POST':
# 		return render_template("addtech.html")


#
# #detail_Of_teachers
# @app.route('/techdetail',methods=['POST','GET'])
# def techdetail():
# 	if request.method =='POST':
# 		branch=request.form['branch']
# 		semester=request.form['semester']
# 		con = sql.connect("database.db")
# 		cur = con.cursor()
# 		cur.execute('select * from profs where branch=? and semester = ?',(branch,semester))
# 		lis2=cur.fetchall()
# 		return render_template('addtech.html',lis2=lis2)


@app.route('/admin')
def admin():
	return render_template('admin.html')


#final_adding
@app.route('/addinto',methods=['POST','GET'])
def addinto():
	if request.method=='POST':
		name=request.form['nameprof']
		branch=request.form['brnprof']
		subject=request.form['subprof']
		semester=request.form['semprof']
		con = sql.connect("database.db")
		cur = con.cursor()
		cur.execute('INSERT INTO profs (name,branch,subject,semester) VALUES(?,?,?,?)',(name,branch,subject,semester,))
		con.commit()
		cur.execute('select name,subject from profs where branch=? and semester=?', (branch, semester,))
		listde = cur.fetchall()
		return render_template('add_delete.html', listde=listde, branch=branch, semester=semester)

#delete teacher
@app.route('/delete', methods=['POST', 'GET'])
def delete():
	if request.method == 'POST':
		name = request.form['name']
		branch = request.form['branch']
		subject = request.form['sub']
		semester = request.form['sem']
		con = sql.connect("database.db")
		cur = con.cursor()
		cur.execute('Delete from profs where name=? and branch=? and subject=? and semester=?',(name, branch, subject, semester,))
		con.commit()
		cur.execute('select name,subject from profs where branch=? and semester=?', (branch, semester,))
		listde = cur.fetchall()
		return render_template('add_delete.html', listde=listde, branch=branch, semester=semester)


#Evaluation
@app.route('/evaluation',methods=['POST','GET'])
def evaluation():
	if request.method=='POST':
		return render_template("evaluate.html")



		
# #overall_performance
# @app.route('/overall',methods=['POST','GET'])
# def overall():
# 	if request.method=='POST':
# 		con = sql.connect("database.db")
# 		cur = con.cursor()
# 		cur.execute('select lecturer,avg(preparation),avg(information),avg(explanation),avg(pace),avg(leadership),avg(receptive),avg(interest),avg(discussion),avg(learning),avg(rapport),avg(available) from feedback group by lecturer')
# 		values=cur.fetchall()
# 		labels={'preparation','information','explanation','pace','leadership','receptive','interest','discussion','learning','rapport','available'}
# 		return render_template('evaluate.html',values=values,labels=labels)



#list for Performance Evaluation
@app.route('/Purpose',methods=['POST','GET'])
def Purpose():
	if request.method=='POST':
		branch = request.form['branch']
		semester = request.form['semester']
		purpose = request.form['purpose']
		con = sql.connect("database.db")
		cur = con.cursor()
		if(purpose=='add_delete'):
			cur.execute('select name,subject from profs where branch=? and semester=?',(branch,semester,))
			listde = cur.fetchall()
			return render_template('add_delete.html', listde=listde,branch=branch,semester=semester)

		if(purpose=='evaluate'):
			cur.execute('select name from profs where branch=? and semester=?',(branch,semester,))
			listpe=cur.fetchall()
			y = cur.execute('select count(distinct lecturer) from feedback where branch=? and semester=?',(branch,semester,))
			k = y.fetchone()
			n = int(k[0])
			print(n)
			x = cur.execute('select lecturer,avg(preparation),avg(information),avg(explanation),avg(pace),avg(leadership),avg(receptive),avg(interest),avg(discussion),avg(learning),avg(rapport),avg(available) from feedback group by lecturer,branch,semester having branch=? and semester=?',(branch,semester,))
			z = x.fetchall()
			print(z)
			list = []
			for i in range(0, n):
				sum = 0
				for j in range(1, 11):
					sum = sum + z[i][j]
				sum = sum / 110
				sum = round(sum,2)
				list.append(sum)
			print(list)
			return render_template('perflist.html', listpe=listpe,branch=branch,semester=semester,list=list)




#teacher_performance
@app.route('/evgraph',methods=['POST','GET'])
def evgraph():
	if request.method=='POST':
		semester =request.form['semprof']
		print(semester)
		branch = request.form['brnprof']
		print(branch)
		prof = request.form['prof_name']
		print(prof)
		con = sql.connect("database.db")
		cur = con.cursor()
		cur.execute('select avg(preparation),avg(information),avg(explanation),avg(pace),avg(leadership),avg(receptive),avg(interest),avg(discussion),avg(learning),avg(rapport),avg(available) from feedback where lecturer=? and branch=? and semester=?',(prof,branch,semester,))
		values=cur.fetchall()
		print(values)
		labels=('preparation','information','explanation','pace','leadership','receptive','interest','discussion','learning','rapport','available')
		return render_template('evgraph.html',prof=prof,values=values,labels=labels)



#Overall_performance
@app.route('/overall',methods=['POST','GET'])
def overall():
	if request.method=='POST':
		con = sql.connect("database.db")
		cur = con.cursor()
		y=cur.execute('select count(distinct lecturer) from feedback')
		k=y.fetchone()
		n=int(k[0])
		print(n)
		x = cur.execute('select lecturer,avg(preparation),avg(information),avg(explanation),avg(pace),avg(leadership),avg(receptive),avg(interest),avg(discussion),avg(learning),avg(rapport),avg(available) from feedback group by lecturer')
		tech = []
		z = x.fetchall()
		print(z)
		for i in range(0, n):
			tech.append(z[i][0])
		list = []
		for i in range(0, n):
			sum = 0
			for j in range(1, 11):
				sum = sum + z[i][j]
			sum = sum / 11
			list.append(sum)
		print(list)
		print(tech)

		return render_template('overall.html',tech=tech,list=list,n=n)



# #Branch_performance
# @app.route('/brncmp',methods=['POST','GET'])
# def brncmp():
# 	if request.method=='POST':
# 		branch=request.form['brnprof']
# 		print(branch)
# 		semester=request.form['semprof']
# 		print(semester)
# 		con = sql.connect("database.db")
# 		cur = con.cursor()
# 		# y = cur.execute('select count(distinct lecturer) from feedback where branch=? and semester=?',(branch,semester,))
# 		y = cur.execute('select count(distinct lecturer) from feedback where branch="it" and semester="5"')
# 		k = y.fetchone()
# 		print(k)
# 		n = int(k[0])
# 		print(n)
# 		x = cur.execute('select distinct lecturer,avg(preparation),avg(information),avg(explanation),avg(pace),avg(leadership),avg(receptive),avg(interest),avg(discussion),avg(learning),avg(rapport),avg(available) from feedback where branch=? and semester=? group by lecturer',(branch,semester,))
# 		tech = []
# 		z = x.fetchall()
# 		for i in range(0, n):
# 			tech.append(z[i][0])
# 			print(tech)
# 		list = []
# 		for i in range(0, n):
# 			sum = 0
# 			for j in range(1, 11):
# 				sum = sum + z[i][j]
# 			sum = sum / 11
# 			list.append(sum)
#
# 		return render_template('brncmp.html',tech=tech,list=list,n=n)



#LOGOUT module
@app.route('/logout')
def logout():
	session.pop('roll_no',None)
	session.pop('branch', None)
	session.pop('semester', None)
	session.pop('lisp', None)
	session.pop('exist', None)
	return redirect(url_for('index'))


if(__name__ == "__main__"):
	app.run(debug=True)
