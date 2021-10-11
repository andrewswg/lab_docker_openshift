import mysql.connector
from flask import Flask, request, jsonify
import hashlib
import time

app = Flask(__name__)

def mysql_get_mydb():
    '''Takes no args, and returns a connection to MYDB via MYSQL.'''
    return mysql.connector.connect(
                host='mysql',
                user='userH4V',
                password='O8pduv1w4xAcotrc',
                database="demo_docker")

@app.route('/', methods=['POST'])
def signup():
    content = request.json
    if 'email' in content and 'password' in content:
        print('email: ' + content['email'])
        print('hashed password: ' + hashlib.md5(content['password'].encode('utf8')).hexdigest())
        email = content['email']
        password = hashlib.md5(content['password'].encode('utf8')).hexdigest()
        # insert_db(email, password)
        if not is_data_exists(email):
            insert_db(email, password)
            return jsonify({"status":"success"})
        else:
            return jsonify({"status":"failed, data exists!"})
    else:
        return jsonify({"status":"failed, missing data"})

def current_milli_time():
    return round(time.time() * 1000)

def is_data_exists(email):
    connection = mysql_get_mydb()
    print(connection)

    db_cursor = connection.cursor()

    sql = "SELECT * FROM users WHERE user_email = %s"
    input_email = (email, )

    db_cursor.execute(sql, input_email)

    results = db_cursor.fetchall()

    db_cursor.close()
    connection.close()

    if len(results)>0:
        print('the data exists!')
        for x in results:
            print('id: ' + x[0])
        return True
    else:
        return False

def insert_db(email, password):
    connection = mysql_get_mydb()
    print(connection)

    db_cursor = connection.cursor()

    sql = "INSERT INTO users (user_id, user_email, user_password) VALUES (%s, %s, %s)"
    val = (str(current_milli_time()), email, password)
    db_cursor.execute(sql, val)

    connection.commit()

    print(db_cursor.rowcount, "record inserted.")

    db_cursor.close()
    connection.close()

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')