# -----------------------------------------
@app.route('/filtervenue', methods=['GET','POST'])
def filtven():
    connection = mysql.connector.connect(host='localhost',database='dbmsEventManagement',user='admin',password='password')
    cursor = connection.cursor()
    cursor.callproc('filtervenue')
    for result in cursor.stored_results():
        print(result.fetchall())
    return("procedures/filtervenue.html",result)
# -------------------------------------------------

@app.route('/calctotalfromevent', methods=['GET','POST'])
def calctotalfromevent():
    if request.method == 'POST':
            totalReq = request.form
            fees = totalReq['fees']
            event_name = totalReq['event_name']
            connection = mysql.connector.connect(host='localhost',database='dbmsEventManagement',user='admin',password='password')
            cursor = connection.cursor()
            cursor.callproc('totalcollection',(fees,event_name))
            for result in cursor.stored_results():
                print(result.fetchall())
    return render_template("procedures/calctotalfromevent.html",result)

# -------------------------------------------------

@app.route('/contactus', methods=['GET','POST'])
def contactUs():
    if request.method == 'POST':
        contactForm = request.form
        dept_name = contactForm['dept_name']
        connection = mysql.connector.connect(host='localhost',database='dbmsEventManagement',user='admin',password='password')
        cursor = connection.cursor()
        cursor.callproc('contact_us')
        for result in cursor.stored_results():
            print(result.fetchall())
    return render_template("procedures/contactus.html",result)
# -------------------------------------------------

# @app.route('/eventfeedback', methods=['GET','POST'])
# def procedureEventFeedback():
#     connection = mysql.connector.connect(host='localhost',database='dbmsEventManagement',user='admin',password='password')
#     cursor = connection.cursor()
#     cursor.callproc('filtervenue')
#     for result in cursor.stored_results():
#         print(result.fetchall())
#     return render_template("procedures/eventfeedback.html")
# -------------------------------------------------

@app.route('/eventsponsors', methods=['GET','POST'])
def proceduresEventSponsors():
    connection = mysql.connector.connect(host='localhost',database='dbmsEventManagement',user='admin',password='password')
    cursor = connection.cursor()
    cursor.callproc('sponsor_event')
    for result in cursor.stored_results():
        print(result.fetchall())
    return render_template("procedures/eventsponsors.html",result)
# -------------------------------------------------

@app.route('/extractedusers', methods=['GET','POST'])
def proceudureExtractedUsers():
    connection = mysql.connector.connect(host='localhost',database='dbmsEventManagement',user='admin',password='password')
    cursor = connection.cursor()
    cursor.callproc('registeredUsers')
    for result in cursor.stored_results():
        print(result.fetchall())
    return render_template("procedures/extractedusers.html",result)
# -------------------------------------------------

@app.route('/userbill', methods=['GET','POST'])
def userbill():
    if request.method == 'POST':
            logindet = request.form
            email = logindet['email']
            password = logindet['password']
            connection = mysql.connector.connect(host='localhost',database='dbmsEventManagement',user='admin',password='password')
            cursor = connection.cursor()
            cursor.callproc('customer_bill',(email,password))
            for result in cursor.stored_results():
                print(result.fetchall())
    return render_template("procedures/userbill.html",result)
# -------------------------------------------------

## For Functions
@app.route('/event_spcount', methods=['GET','POST'])
def Fevent_sponsorcount():
    if request.method == 'POST':
            sponsorform = request.form
            event_name = sponsorform['event_name']
            cur = mysqlcon.connection.cursor()
            resultValue = cur.execute("SELECT event_spcount",(event_name))
            mysqlcon.connection.commit()
            cur.close()
    return render_template("procedures/event_spcount.html",resultValue)
# -------------------------------------------------

@app.route('/event_count', methods=['GET','POST'])
def Fevent_count():
    if request.method == 'POST':
            venueform = request.form
            city_name = venueform['event_name']
            cur = mysqlcon.connection.cursor()
            resultValue = cur.execute("SELECT event_count",(city_name))
            mysqlcon.connection.commit()
            cur.close()
    return render_template("procedures/event_count.html",resultValue)

# -------------------------------------------------
