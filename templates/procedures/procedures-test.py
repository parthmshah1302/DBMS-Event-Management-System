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
    return render_template("procedures/calctotalfromevent.html")

# -------------------------------------------------

@app.route('/contactus', methods=['GET','POST'])
def contactUs():
    return render_template("procedures/contactus.html")
# -------------------------------------------------

@app.route('/eventfeedback', methods=['GET','POST'])
def procedureEventFeedback():
    return render_template("procedures/eventfeedback.html")
# -------------------------------------------------

@app.route('/eventsponsors', methods=['GET','POST'])
def proceduresEventSponsors():
    return render_template("procedures/eventsponsors.html")
# -------------------------------------------------

@app.route('/extractedusers', methods=['GET','POST'])
def proceudureExtractedUsers():
    return render_template("procedures/extractedusers.html")
# -------------------------------------------------

@app.route('/userbill', methods=['GET','POST'])
def userbill():
    return render_template("procedures/userbill.html")
# -------------------------------------------------

## For Functions
@app.route('/event_spcount', methods=['GET','POST'])
def Fevent_sponsorcount():
    return render_template("procedures/event_spcount.html")
# -------------------------------------------------

@app.route('/event_count', methods=['GET','POST'])
def Fevent_count():
    return render_template("procedures/event_count.html")

# -------------------------------------------------
