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

# Show PROFESSOR list
def show_profl():
    @app.route('/show_profs')
    def show_profs():
        return render_template('show_profs.html', lisp=session['lisp'],exist=session['exist'])


# Display feedback FORM
def feedform():
    @app.route('/stform')
    def stform():
        print(session['branch'],session['semester'])
        return render_template('stform.html', branch=session['branch'],semester=session['semester'])



# FEEDBACK MODULE......
def feedmodule():
    @app.route('/feedback', methods=['POST', 'GET'])
    def feedback():
        if request.method == 'POST':
            lecturer = request.form['lecturer']
            st_rollno = session['roll_no']
            year = session['year']
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
            current = [lecturer,st_rollno,year,semester,branch,subject]

            con = sql.connect("database.db")
            cur = con.cursor()

            cur.execute("select lecturer,st_rollno,year,semester,branch,subject from feedback where st_rollno=?",[session['roll_no']])
            alrdyexist=cur.fetchall()

            for i in range(0,len(alrdyexist)):
                if list(alrdyexist[i]) == current:
                    msgx="This feedback is already registered"
                    con.close()

                    return render_template('show_profs.html', lisp=session['lisp'], msgx=msgx, exist=session['exist'])

            else:
                cur.execute("INSERT INTO feedback (lecturer,st_rollno,year,semester,branch,subject,preparation,information,explanation,pace,leadership,receptive,interest,discussion,learning,rapport,available)VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)",(lecturer,st_rollno,year,semester,branch,subject,preparation,information,explanation,pace,leadership,receptive,interest,discussion,learning,rapport,available,))
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
# def viewres():
#     @app.route('/response', methods=['POST', 'GET'])
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
