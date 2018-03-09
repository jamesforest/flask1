from flask import Flask,render_template,url_for,request,redirect,flash,session
from flask.ext.mysql import MySQL







app=Flask(__name__)
app.secret_key = 'frank'


app.config['MYSQL_DATABASE_USER'] = 'root'
app.config['MYSQL_DATABASE_PASSWORD'] = 'root'
app.config['MYSQL_DATABASE_DB'] = 'test'
app.config['MYSQL_DATABASE_HOST'] = 'localhost'

mysql=MySQL()
mysql.init_app(app)

conn=mysql.connect()
cursor=conn.cursor()



@app.route('/')
def homepage():
    return render_template('homepage.html')
    

@app.route('/detail')
def detail():
    if 'name' in session:
        query="select * from users;"
        cursor.execute(query)
        results=cursor.fetchall()
        
        return render_template('detail.html',results=results)
    return redirect(url_for('login'))


@app.route('/login',methods=['GET','POST'])
def login():
    if (request.method=='POST'):
        query="select * from users where name=%s and password=%s;"
        parameter=(request.form['name'],request.form['password'])
        results=cursor.execute(query,parameter)
        if results ==1:
            session['name']=request.form['name']
            message="Welcome "+request.form['name']
            flash(message)
            return redirect(url_for('detail'))
    
    return render_template('login.html')


@app.route('/signup',methods=['GET','POST'])
def signup():
    if (request.method=='POST'):
        query="select * from users where name=%s ;"
        parameter=(request.form['name'])
        results=cursor.execute(query,parameter)
        
        if results !=0:
            message="Name used please try another name"
            flash(message)
            return redirect(url_for('signup'))
        query="insert into users values (%s,%s) ;"
        parameter=(request.form['name'],request.form['password'])
        cursor.execute(query,parameter)
        conn.commit()
        return redirect(url_for('login'))
        
            
    
    return render_template('signup.html')



if __name__=="__main__":
    app.run(debug=True, host='0.0.0.0', port=8080)