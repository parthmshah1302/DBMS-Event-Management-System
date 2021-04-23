from flask import Flask, render_template, request, redirect, flash
from flask_mysqldb import MySQL
import mysql.connector
from mysql.connector import MySQLConnection, Error
import yaml
import time
from datetime import date, datetime
from senti import *

app = Flask(__name__,static_url_path='',static_folder='static')
app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'

# Configure DB
db = yaml.load(open('db.yaml'))
app.config['MYSQL_USER'] = db['mysql_user']
app.config['MYSQL_HOST'] = db['mysql_host']
app.config['MYSQL_PASSWORD'] = db['mysql_password']
app.config['MYSQL_DB'] = db['mysql_db']


mysqlcon = MySQL(app)

# The very basic home page


@app.route('/', methods=['GET', 'POST'])
def index():
    return render_template('index.html')


# Inserts data to login table
@app.route('/login', methods=['GET', 'POST'])
def login():
    try:    
        if request.method == 'POST':
            userDetails = request.form
            email = userDetails['email']
            password = userDetails['password']

            cur = mysqlcon.connection.cursor()
            cur.execute("INSERT INTO login(email, pass) VALUES(%s, %s)",
                        (email, password))
            mysqlcon.connection.commit()
            cur.close()
            return redirect('/loginData')
        return render_template('login.html')
    except:
        return('<h1 style="text-align:center">Email is invalid/duplicate. Please try again!</h1?')
        
@app.route('/loginData')
def loginData():
    cur = mysqlcon.connection.cursor()
    resultValue = cur.execute("SELECT * FROM login")
    if resultValue > 0:
        userDetails = cur.fetchall()
        return render_template('loginData.html', userDetails=userDetails)
    else:
        return "Data does not exist, go to home page"

# Inserts data to event_table


curr_time = time.localtime()
event_time = time.strftime("%H:%M:%S", curr_time)

@app.route('/events',methods=['GET','POST'])
def events():
    if request.method=='POST':
        eventDetails=request.form
        event_name=eventDetails['event_name']
        event_date=eventDetails['event_date']
        venue=eventDetails['venue']
        event_time=eventDetails['event_time']
        event_type=eventDetails['event_type']

        cur=mysqlcon.connection.cursor()
        cur.execute("INSERT INTO event_table(event_name,event_date,venue,event_time,event_type) VALUES(%s,%s,%s,STR_TO_DATE(%s,'%%H:%%i'),%s)",(event_name,event_date,venue,event_time,event_type))
        mysqlcon.connection.commit()
        cur.close()
        return redirect('/eventsData')
    return render_template('events.html')

@app.route('/eventsData')
def eventsData():
    cur = mysqlcon.connection.cursor()
    resultValue = cur.execute(
        "SELECT event_no,event_name,DATE_FORMAT(event_date, '%M %d %Y'),venue,TIME_FORMAT(event_time,'%h:%i %p'),event_type from event_table")
    if resultValue > 0:
        eventDetails = cur.fetchall()
        return render_template('eventsData.html', eventDetails=eventDetails)
    else:
        return('<h1 style="text-align:center">No entry exists</h1>')

@app.route('/delete/sponsorsData/<string:table>/<string:deletecolumn1>/<string:deletecolumn2>', methods=['GET'])
def superDeleteTwo(table,deletecolumn1,deletecolumn2):
    #if request.method=='GET':
    #table_details=request.form
    cur = mysqlcon.connection.cursor()
    cur.execute("DELETE from %s where sponsors_name = '%s' and event_no = %s" %(table,deletecolumn1,deletecolumn2))
    mysqlcon.connection.commit()
    cur.close()
    #flash('Deleted Successfully','success')
    return redirect('/sponsorsData')

@app.route('/delete/<string:categ>/<string:table>/<string:deletecolumn>/<string:main_id>', methods=['GET'])
def superDelete(categ,table,deletecolumn,main_id):
    #if request.method=='GET':
    #table_details=request.form
    cur = mysqlcon.connection.cursor()
    cur.execute("DELETE from %s where %s = '%s'" %(table,deletecolumn,main_id))
    mysqlcon.connection.commit()
    cur.close()
    #flash('Deleted Successfully','success')
    return redirect('/'+categ)


@app.route('/bill', methods=['GET', 'POST'])
def bill():
    cur = mysqlcon.connection.cursor()
    cur.execute("SELECT email FROM login")
    emailTuple = cur.fetchall()
    mysqlcon.connection.commit()
    cur.close()
    if request.method == 'POST':
        billDetails = request.form
        order_no = billDetails['order_no']
        amount = billDetails['amount']
        tax = billDetails['tax']
        del_charge = billDetails['del_charge']
        bill_date = billDetails['bill_date']
        email = billDetails['email']
        final_amt = int(amount)+int(amount)*int(tax)/100+int(del_charge)
        cur = mysqlcon.connection.cursor()
        cur.execute("INSERT INTO bill( order_no, amount, tax, del_charge,final_amt,bill_date,email) VALUES(%s,%s,%s,%s,%s,%s,%s)",
                    (order_no, amount, tax, del_charge, final_amt, bill_date, email))
        mysqlcon.connection.commit()
        cur.close()

        return redirect('/billData')
    return render_template('bill.html', emailTuple=emailTuple)
# This function displays the billData


@app.route('/billData')
def billData():
    cur = mysqlcon.connection.cursor()
    resultValue = cur.execute(
        "SELECT bill_no,order_no,amount,tax,del_charge,final_amt,DATE_FORMAT(bill_date, '%M %d %Y'),email from bill")
    if resultValue > 0:
        billDetails = cur.fetchall()
        return render_template('billData.html', billDetails=billDetails)
    else:
        return('<h1 style="text-align:center">No entry exists</h1>')

# This creates the vendors tables


@app.route('/vendors', methods=['GET', 'POST'])
def vendors():
    if request.method == 'POST':
        vendorDetails = request.form
        products_taken = vendorDetails['products_taken']
        amount = vendorDetails['amount']
        invoice_no = vendorDetails['invoice_no']
        vendor_name = vendorDetails['vendor_name']
        cur = mysqlcon.connection.cursor()
        cur.execute("INSERT INTO vendors(products_taken,amount,invoice_no,vendor_name) VALUES(%s,%s,%s,%s)",
                    (products_taken, amount, invoice_no, vendor_name))
        mysqlcon.connection.commit()
        cur.close()

        return redirect('/vendorsData')
    return render_template('vendors.html')

# This displays the vendors tables


@app.route('/vendorsData')
def vendorsData():
    cur = mysqlcon.connection.cursor()
    resultValue = cur.execute(
        "SELECT products_taken,amount,invoice_no,vendor_name from vendors")
    if resultValue > 0:
        vendorDetails = cur.fetchall()
        return render_template('vendorsData.html', vendorDetails=vendorDetails)
    else:
        return('<h1 style="text-align:center">No entry exists</h1>')


@app.route('/inventory', methods=['GET', 'POST'])
def inventory():
    if request.method == 'POST':
        inventoryDetails = request.form
        item_code = inventoryDetails['item_code']
        item_name = inventoryDetails['item_name']
        quantity = inventoryDetails['quantity']
        cur = mysqlcon.connection.cursor()
        cur.execute("INSERT INTO inventory(item_code,item_name,quantity) VALUES(%s,%s,%s)",
                    (item_code, item_name, quantity))
        mysqlcon.connection.commit()
        cur.close()

        return redirect('/inventoryData')
    return render_template('inventory.html')

# This displays the inventory tables


@app.route('/inventoryData')
def inventoryData():
    cur = mysqlcon.connection.cursor()
    resultValue = cur.execute(
        "SELECT item_code,item_name,quantity from inventory")
    if resultValue > 0:
        inventoryDetails = cur.fetchall()
        return render_template('inventoryData.html', inventoryDetails=inventoryDetails)
    else:
        return('<h1 style="text-align:center">No entry exists</h1>')

# This creates sponsorship table
@app.route('/sponsorship',methods=['GET','POST'])
def sponsorship():
    if request.method=='POST':
        sponsorshipDetails=request.form
        sponsor_type=sponsorshipDetails['sponsor_type']
        deliverables=sponsorshipDetails['deliverables']
        cur=mysqlcon.connection.cursor()
        cur.execute("INSERT INTO sponsorship_package(sponsor_type,deliverables) VALUES(%s,%s)",(sponsor_type,deliverables))
        mysqlcon.connection.commit()
        cur.close()
        return redirect('/sponsorshipData')
    return render_template('sponsorship.html')

# This displays the sponsorship table 
@app.route('/sponsorshipData')
def sponsorshipData():
    cur = mysqlcon.connection.cursor()
    resultValue = cur.execute("SELECT sponsor_type,deliverables FROM sponsorship_package")
    if resultValue > 0:
        sponsorshipDetails = cur.fetchall()
        return render_template('sponsorshipData.html', sponsorshipDetails=sponsorshipDetails)
    else:
        return('<h1 style="text-align:center">No entry exists</h1>')

# This creates sponsors table 
@app.route('/sponsors',methods=['GET','POST'])
def sponsors():
    cur = mysqlcon.connection.cursor()
    cur.execute("SELECT event_name FROM event_table")
    eventnameTuple=cur.fetchall()
    cur.close()
    cur = mysqlcon.connection.cursor()
    cur.execute("SELECT event_no FROM event_table")
    eventnoTuple=cur.fetchall()
    cur.close()
    cur = mysqlcon.connection.cursor()
    cur.execute("SELECT sponsor_type FROM sponsorship_package")
    sponsorshipTuple=cur.fetchall()
    cur.close()
    
    if request.method=='POST':
        sponsorDetails=request.form
        sponsors_name=sponsorDetails['sponsors_name']
        address=sponsorDetails['address']
        amount=sponsorDetails['amount']
        mob_num=sponsorDetails['mob_num']
        sponsor_type=sponsorDetails['sponsor_type']
        event_no=sponsorDetails['event_no']
        event_name=sponsorDetails['event_name']
        cur=mysqlcon.connection.cursor()
        cur.execute("INSERT INTO sponsors(sponsors_name,address,amount,mob_num,sponsor_type,event_no,event_name) VALUES(%s,%s,%s,%s,%s,%s,%s)",(sponsors_name,address,int(amount),int(mob_num),sponsor_type,int(event_no),event_name))
        mysqlcon.connection.commit()
        cur.close()
        return redirect('/sponsorsData')
    return render_template('sponsors.html',eventnameTuple=eventnameTuple,eventnoTuple=eventnoTuple,sponsorshipTuple=sponsorshipTuple)

@app.route('/sponsorsData')
def sponsorsData():
    cur = mysqlcon.connection.cursor()
    resultValue = cur.execute(
        "SELECT sponsors_name,address,amount,mob_num,sponsor_type,event_no,event_name from sponsors")
    if resultValue > 0:
        sponsorsDetails = cur.fetchall()
        return render_template('sponsorsData.html', sponsorsDetails=sponsorsDetails)
    else:
        return('<h1 style="text-align:center">No entry exists</h1>')

# This creates feedback table
today_date = date.today().strftime('%Y-%m-%d')


@app.route('/feedback', methods=['GET', 'POST'])
def feedback():
    cur = mysqlcon.connection.cursor()
    cur.execute("SELECT email FROM login")
    emailTuple = cur.fetchall()

    mysqlcon.connection.commit()
    if request.method == 'POST':
        feedbackDetails = request.form
        email = feedbackDetails['email']
        title = feedbackDetails['title']
        message = feedbackDetails['message']
        # print(today_date)
        now = datetime.now()
        now = now.strftime('%H:%M:%S')
        # print(now)
        sentiment=Sentiment(message)
        cur = mysqlcon.connection.cursor()
        cur.execute("INSERT INTO feedback(email,title,message,Date,time,Sentiment) VALUES(%s,%s,%s,%s,%s,%s)",
                    (email, title, message, today_date, now,sentiment))
        mysqlcon.connection.commit()
        cur.close()

        return redirect('/feedbackData')
    return render_template('feedback.html', emailTuple=emailTuple)

# This displays the feedback tables


@app.route('/feedbackData')
def feedbackData():
    cur = mysqlcon.connection.cursor()
    resultValue = cur.execute(
        "SELECT email,title,message,Date,time,Sentiment from feedback")
    if resultValue > 0:
        feedbackDetails = cur.fetchall()
        return render_template('feedbackData.html', feedbackDetails=feedbackDetails)
    else:
        return('<h1 style="text-align:center">No entry exists</h1>')
#Inserts into account table

@app.route('/account',methods=['GET','POST'])
def account_table():

    cur=mysqlcon.connection.cursor()
    cur.execute("SELECT bill_no FROM bill")
    billno_Tuple=cur.fetchall()
    
    mysqlcon.connection.commit()
    print(billno_Tuple)
    if request.method=='POST':
        accountDetails=request.form
        balance=accountDetails['balance']
        misc_charges=accountDetails['misc_charges']
        receipt_name=accountDetails['receipt_name']
        account_date=accountDetails['account_date']
        bill_no=accountDetails['bill_no']
        tot_amt=accountDetails['tot_amt']
        paid_amt=accountDetails['paid_amt']
        cur=mysqlcon.connection.cursor()
        cur.execute("INSERT INTO account_table(balance,misc_charges,receipt_name,account_date,bill_no,tot_amt, paid_amt) VALUES(%s,%s,%s,%s,%s,%s,%s)",(balance,misc_charges,receipt_name,account_date,bill_no,tot_amt, paid_amt))
        mysqlcon.connection.commit()
        cur.close()
        
        return redirect('/accountData')
    return render_template('account.html', billno_Tuple=billno_Tuple)

# This function displays the accountData

@app.route('/accountData')
def accountData():
    cur=mysqlcon.connection.cursor()
    resultValue=cur.execute("SELECT balance,misc_charges,receipt_name,account_date,bill_no, tot_amt, paid_amt  from account_table")
    if resultValue>0:
        accountDetails=cur.fetchall()
        return render_template('accountData.html',accountDetails=accountDetails)
    else:
        return('<h1 style="text-align:center"> No entry exists</h1>')

#Insert in Registration

@app.route('/registration',methods=['GET','POST'])
def registration():

    cur=mysqlcon.connection.cursor()
    cur.execute("SELECT email FROM login")
    emailTuple=cur.fetchall()

    cur=mysqlcon.connection.cursor()
    cur.execute("SELECT event_no FROM event_table")
    event_no_Tuple=cur.fetchall()

    if request.method=='POST':
        registrationdets=request.form
        fees=registrationdets['fees']
        customer_name=registrationdets['customer_name']
        mob_name=registrationdets['mob_name']
        email=registrationdets['email']
        payment_mode=registrationdets['payment_mode']
        sr_no=registrationdets['sr_no']
        college_name=registrationdets['college_name']
        register_receipt=registrationdets['register_receipt']
        event_name=registrationdets['event_name']
        event_no=registrationdets['event_no']
        cur=mysqlcon.connection.cursor()
        cur.execute("INSERT INTO registration(fees,customer_name, mob_name, email, payment_mode, sr_no, college_name, register_receipt, event_name,event_no) VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)",(fees,customer_name, mob_name, email, payment_mode, sr_no, college_name, register_receipt, event_name,event_no))
        mysqlcon.connection.commit()
        cur.close()

        return redirect('/registrationData')
    return render_template('registration.html',emailTuple=emailTuple,event_no_Tuple=event_no_Tuple)

#This function displays registration table

@app.route('/registrationData')
def registrationData():
    cur=mysqlcon.connection.cursor()
    resultValue=cur.execute("SELECT fees,customer_name, mob_name, email, payment_mode, sr_no, college_name, register_receipt, event_name,event_no from registration")
    if resultValue>0:
        registrationDetails=cur.fetchall()
        return render_template('registrationData.html',registrationDetails=registrationDetails)
    else:
        return('<h1 style="text-align:center"> No entry exists</h1>')

@app.route('/team',methods=['GET','POST'])
def team():
    cur = mysqlcon.connection.cursor()
    cur.execute("SELECT department_name from department")
    departmentTuple = cur.fetchall()
    mysqlcon.connection.commit()
    
    if request.method == 'POST':
        teamDetails = request.form
        member_name = teamDetails['member_name']
        mob_num = teamDetails['mob_num']
        department_name=teamDetails['department_name']
        email = teamDetails['email']
        team_member_id=teamDetails['team_member_id']
        position=teamDetails['position']

        cur = mysqlcon.connection.cursor()
        cur.execute("INSERT INTO team(member_name,mob_num,department_name,email,team_member_id,position) VALUES(%s,%s,%s,%s,%s,%s)", (member_name,mob_num,department_name,email,team_member_id,position))
        mysqlcon.connection.commit()
        cur.close()
        return redirect('/teamData')
    return render_template('team.html', departmentTuple=departmentTuple)

@app.route('/teamData')
def teamData():
    cur=mysqlcon.connection.cursor()
    resultValue=cur.execute("SELECT member_name,mob_num,department_name,email,team_member_id,position FROM team")
    if resultValue>0:
        teamDetails=cur.fetchall()
        return render_template('teamData.html',teamDetails=teamDetails)
    else:
        return('<h1 style="text-align:center"> No entry exists</h1>')

@app.route('/department',methods=['GET','POST'])
def department():
    cur = mysqlcon.connection.cursor()
    cur.execute("SELECT vendor_name from vendors")
    vendorTuple = cur.fetchall()
    mysqlcon.connection.commit()
    
    if request.method == 'POST':
        departmentDetails = request.form
        department_name = departmentDetails['department_name']
        vendor_relation = departmentDetails['vendor_relation']
        work_scope = departmentDetails['work_scope']

        cur = mysqlcon.connection.cursor()
        cur.execute("INSERT INTO department(department_name,vendor_relation,work_scope) VALUES(%s,%s,%s)", (department_name,vendor_relation,work_scope))
        mysqlcon.connection.commit()
        cur.close()
        return redirect('/departmentData')
    return render_template('department.html', vendorTuple=vendorTuple)

@app.route('/departmentData')
def departmentData():
    cur=mysqlcon.connection.cursor()
    resultValue=cur.execute("SELECT department_name,vendor_relation,work_scope from department")
    if resultValue>0:
        departmentDetails=cur.fetchall()
        return render_template('departmentData.html',departmentDetails=departmentDetails)
    else:
        return('<h1 style="text-align:center"> No entry exists</h1>')

#@app.route('/team',methods=['GET','POST'])
#def team():

      
@app.route('/realfiltervenue')
def filtven():
    try:
        connection = mysql.connector.connect(host='localhost',database='dbmsEventManagement',user='admin',password='password')
        cursor = connection.cursor()
        cursor.callproc('filtervenue')
        for result in cursor.stored_results():
            print(result.fetchall())
    except mysql.connector.Error as error:
        print("Failed to execute stored procedure: {}".format(error))
    finally:
        if (connection.is_connected()):
            cursor.close()
            connection.close()
            print("MySQL connection is closed")
    return("hi")
    # cur=mysql.connection.cursor()
    # cur.callproc('filtervenue')

    # r_filtervenue = list(cur.fetchall())
    # venuelist=[]
    # for i in r_filtervenue:
    #     venuelist.append(i)
    #     print("=====",venuelist)
    # return('venuelist')

### Code for HTML Procedures
@app.route('/procedures', methods=['GET','POST'])
def procedures():
    return render_template("procedures/procedures.html")

@app.route('/calctotalfromevent', methods=['GET','POST'])
def calctotalfromevent():
    return render_template("procedures/calctotalfromevent.html")

@app.route('/contactus', methods=['GET','POST'])
def contactUs():
    return render_template("procedures/contactus.html")

@app.route('/eventfeedback', methods=['GET','POST'])
def procedureEventFeedback():
    return render_template("procedures/eventfeedback.html")

@app.route('/eventsponsors', methods=['GET','POST'])
def proceduresEventSponsors():
    return render_template("procedures/eventsponsors.html")

@app.route('/extractedusers', methods=['GET','POST'])
def proceudureExtractedUsers():
    return render_template("procedures/extractedusers.html")

@app.route('/filtervenue', methods=['GET','POST'])
def filtervenue():
    return render_template("procedures/filtervenue.html")

@app.route('/userbill', methods=['GET','POST'])
def userbill():
    return render_template("procedures/userbill.html")

## For Functions
@app.route('/event_spcount', methods=['GET','POST'])
def Fevent_sponsorcount():
    return render_template("procedures/event_spcount.html")

@app.route('/event_count', methods=['GET','POST'])
def Fevent_count():
    return render_template("procedures/event_count.html")

if __name__=='__main__':
    app.run(debug=True)   
