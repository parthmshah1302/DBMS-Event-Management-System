from flask import Flask, render_template, request, redirect
from flask_mysqldb import MySQL
import yaml
import time
from datetime import date, datetime

app = Flask(__name__)

# Configure DB
db = yaml.load(open('db.yaml'))
app.config['MYSQL_HOST'] = db['mysql_host']
app.config['MYSQL_USER'] = db['mysql_user']
app.config['MYSQL_PASSWORD'] = db['mysql_password']
app.config['MYSQL_DB'] = db['mysql_db']


mysql = MySQL(app)

# The very basic home page


@app.route('/', methods=['GET', 'POST'])
def index():
    return render_template('index.html')


# Inserts data to login table
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        userDetails = request.form
        email = userDetails['email']
        password = userDetails['password']

        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO login(email, pass) VALUES(%s, %s)",
                    (email, password))
        mysql.connection.commit()
        cur.close()
        return redirect('/loginData')
    return render_template('login.html')

# This function displays the loginData


@app.route('/loginData')
def loginData():
    cur = mysql.connection.cursor()
    resultValue = cur.execute("SELECT * FROM login")
    if resultValue > 0:
        userDetails = cur.fetchall()
        return render_template('loginData.html', userDetails=userDetails)

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

        cur=mysql.connection.cursor()
        cur.execute("INSERT INTO event_table(event_name,event_date,venue,event_time,event_type) VALUES(%s,%s,%s,STR_TO_DATE(%s,'%%H:%%i'),%s)",(event_name,event_date,venue,event_time,event_type))
        mysql.connection.commit()
        cur.close()
        return('Entry is added!')
    return render_template('events.html')

@app.route('/eventsData')
def eventsData():
    cur = mysql.connection.cursor()
    resultValue = cur.execute(
        "SELECT event_no,event_name,DATE_FORMAT(event_date, '%M %d %Y'),venue,TIME_FORMAT(event_time,'%h:%i %p'),event_type from event_table")
    if resultValue > 0:
        eventDetails = cur.fetchall()
        return render_template('eventsData.html', eventDetails=eventDetails)
    else:
        return('<h1 style="text-align:center">No entry exists</h1>')


# Inserts data to bill_table


@app.route('/bill', methods=['GET', 'POST'])
def bill():
    cur = mysql.connection.cursor()
    cur.execute("SELECT email FROM login")
    emailTuple = cur.fetchall()
    mysql.connection.commit()
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
        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO bill( order_no, amount, tax, del_charge,final_amt,bill_date,email) VALUES(%s,%s,%s,%s,%s,%s,%s)",
                    (order_no, amount, tax, del_charge, final_amt, bill_date, email))
        mysql.connection.commit()
        cur.close()

        return redirect('/billData')
    return render_template('bill.html', emailTuple=emailTuple)

# This function displays the billData


@app.route('/billData')
def billData():
    cur = mysql.connection.cursor()
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
        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO vendors(products_taken,amount,invoice_no,vendor_name) VALUES(%s,%s,%s,%s)",
                    (products_taken, amount, invoice_no, vendor_name))
        mysql.connection.commit()
        cur.close()

        return redirect('/vendorsData')
    return render_template('vendors.html')

# This displays the vendors tables


@app.route('/vendorsData')
def vendorsData():
    cur = mysql.connection.cursor()
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
        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO inventory(item_code,item_name,quantity) VALUES(%s,%s,%s)",
                    (item_code, item_name, quantity))
        mysql.connection.commit()
        cur.close()

        return redirect('/inventoryData')
    return render_template('inventory.html')

# This displays the inventory tables


@app.route('/inventoryData')
def inventoryData():
    cur = mysql.connection.cursor()
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
        cur=mysql.connection.cursor()
        cur.execute("INSERT INTO sponsorship_package(sponsor_type,deliverables) VALUES(%s,%s)",(sponsor_type,deliverables))
        mysql.connection.commit()
        cur.close()
        return redirect('/sponsorshipData')
    return render_template('sponsorship.html')

# This displays the sponsorship table 
@app.route('/sponsorshipData')
def sponsorshipData():
    cur = mysql.connection.cursor()
    resultValue = cur.execute("SELECT sponsor_type,deliverables FROM sponsorship_package")
    if resultValue > 0:
        sponsorshipDetails = cur.fetchall()
        return render_template('sponsorshipData.html', sponsorshipDetails=sponsorshipDetails)
    else:
        return('<h1 style="text-align:center">No entry exists</h1>')


# This creates feedback table
today_date = date.today().strftime('%Y-%m-%d')


@app.route('/feedback', methods=['GET', 'POST'])
def feedback():
    cur = mysql.connection.cursor()
    cur.execute("SELECT email FROM login")
    emailTuple = cur.fetchall()

    mysql.connection.commit()
    if request.method == 'POST':
        feedbackDetails = request.form
        email = feedbackDetails['email']
        title = feedbackDetails['title']
        message = feedbackDetails['message']
        print(today_date)
        now = datetime.now()
        now = now.strftime('%H:%M:%S')
        print(now)

        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO feedback(email,title,message,Date,time) VALUES(%s,%s,%s,%s,%s)",
                    (email, title, message, today_date, now))
        mysql.connection.commit()
        cur.close()

        return redirect('/feedbackData')
    return render_template('feedback.html', emailTuple=emailTuple)

# This displays the feedback tables


@app.route('/feedbackData')
def feedbackData():
    cur = mysql.connection.cursor()
    resultValue = cur.execute(
        "SELECT email,title,message,Date,time from feedback")
    if resultValue > 0:
        feedbackDetails = cur.fetchall()
        return render_template('feedbackData.html', feedbackDetails=feedbackDetails)
    else:
        return('<h1 style="text-align:center">No entry exists</h1>')


if __name__ == '__main__':
    app.run(debug=True)
