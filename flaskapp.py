
import sqlite3
from flask import Flask, render_template, request, redirect ,g, url_for, send_file
import os
app = Flask(__name__)
DATABASE='/home/ubuntu/flaskapp/db/users.db'
UPLOAD_FOLDER='/home/ubuntu/flaskapp/files'

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.route('/login', methods=['POST', 'GET'])
def login():
    if request.method == "POST":
	user_Name = request.form['username']
        password = request.form['password']
        db = getattr(g, '_database', None)
        if db is None:
            db = g._database = sqlite3.connect(DATABASE)
            cur = db.cursor()
            cur.execute('select * from user where user_Name =?', (user_Name,))
            row = cur.fetchone()
            if(row == None):
                return render_template('Registration_page.html', us_exist='false')
            else:
                cur.execute('select * from user where user_Name =? and password =?', (user_Name, password,))
                row = cur.fetchone()
                if (row == None):
                    return render_template('Registration_page.html', us_pwd_exist='false')
                else:
		    if row[5]:
			return render_template('display.html',firstname=row[0],lastname=row[1],email=row[2],username=row[3],password=row[4],filename=row[5],count=row[6])
		    else:
                    	return render_template('display.html',firstname=row[0],lastname=row[1],email=row[2],username=row[3],password=row[4])
            db.close()

    return render_template('Registration_page.html')


@app.route('/register' , methods=['POST', 'GET'])
def register():
    if request.method == "POST":
        first_Name = request.form['firstname']
        last_Name = request.form['lastname']
        email = request.form['email']
        username = request.form['username']
        password = request.form['pwd']
        db = getattr(g, '_database', None)
        if db is None:
            db = g._database = sqlite3.connect(DATABASE)
            cur = db.cursor()
            cur.execute('select * from user where user_Name =?', (username,))
            row = cur.fetchone()
            if(row == None ):
           	cur.execute('select * from user where email =?', (email,))
                row = cur.fetchone()
                if(row == None):
                   cur.execute("insert into user(first_Name, last_Name, user_Name,password,email,file,count) values (?,?,?,?,?,NULL,NULL)",(first_Name,last_Name,username,password,email,))
                   db.commit()
                else:
                   return render_template('Second.html', em_exist='true')
            else:
            	return render_template('Second.html', us_exist = 'true')
                db.close()
        return render_template('Registration_page.html')
    return render_template('Second.html')

@app.route('/', methods=['POST', 'GET'])
def starting():
	return  render_template('Registration_page.html')
@app.route('/upload' , methods=['POST', 'GET'])
def upload():
	if request.method == 'POST':
       	 f = request.files['file']
	 username=request.form['username']
	 password=request.form['password']
       	 filename = f.filename
       	 f.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
	 word_count = count(os.path.join(app.config['UPLOAD_FOLDER'], filename))
	 db = getattr(g, '_database', None)
	 if db is None:
		db = g._database = sqlite3.connect(DATABASE)
		cur = db.cursor()
		cur.execute('update user set file=?, count=? where user_Name =?', (filename,word_count,username))
		db.commit()
            	cur = db.cursor()
            	cur.execute('select * from user where user_Name =?', (username,))
            	row = cur.fetchone()
            	if(row == None):
                	return render_template('Registration_page.html', us_exist='false')
            	else:
                	cur.execute('select * from user where user_Name =? and password =?', (username, password,))
                	row = cur.fetchone()
                	if (row == None):
                    		return render_template('Registration_page.html', us_pwd_exist='false')
                	else:
                    		if row[5]:
            				db.close()
                        		return render_template('display.html',firstname=row[0],lastname=row[1],email=row[2],username=row[3],filename=row[5],count=row[6])
                    		else:
            				db.close()
                        		return render_template('display.html',firstname=row[0],lastname=row[1],email=row[4])

	return render_template('display.html')

def count(file):
	file = open(file)
        word = 0
        for line in file:
                words = line.split()
                word += len(words)
        return word

@app.route('/download/<path:filename>' , methods=['GET', 'POST'])
def download(filename):
	return send_file(os.path.join(app.config['UPLOAD_FOLDER'], filename), attachment_filename=filename, as_attachment=True)
if __name__ == '__main__':
	app.run()
