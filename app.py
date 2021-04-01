from flask import Flask, render_template, request, redirect 
from flask_mysqldb import MySQL
import yaml


app=Flask(__name__)

# Configure DB
db=yaml.load(open('db.yaml'))
app.config['MYSQL_HOST']=db['mysql_host']
app.config['MYSQL_USER']=db['mysql_user']
app.config['MYSQL_PASSWORD']=db['mysql_password']
app.config['MYSQL_DB']=db['mysql_db']


mysql=MySQL(app)

# The very basic home page
@app.route('/', methods=['GET','POST'])
def index():
    return ('This is the Home Page!')


# This function inserts data to login table
@app.route('/login', methods=['GET','POST'])
def login():
    if request.method=='POST':
        userDetails=request.form
        email=userDetails['email']
        password=userDetails['password']

        cur=mysql.connection.cursor()
        cur.execute("INSERT INTO login(email, pass) VALUES(%s, %s)",(email,password))
        mysql.connection.commit()
        cur.close()
        return redirect('/users')
    return render_template('login.html')


# This function displays the loginData
@app.route('/loginData')
def loginData():
    cur=mysql.connection.cursor()
    resultValue=cur.execute("SELECT * FROM login")
    if resultValue>0:
        userDetails=cur.fetchall()
        return render_template('loginData.html',userDetails=userDetails)

if __name__=='__main__':
    app.run(debug=True)