# -----------------------------------------
@app.route('/filtervenue', methods=['GET','POST'])
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
    return("filtervenue.html",result)
# -------------------------------------------------

@app.route