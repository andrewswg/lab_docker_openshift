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
def profile_get():
    content = request.json
    if 'email' in content:
        print('email: ' + content['email'])
        email = content['email']
        # insert_db(email, password)
        result_find_user_id = find_user_id(email)

        if result_find_user_id is not None:
            print(result_find_user_id)
            return jsonify({"results":get_profile(result_find_user_id)})
        else:
            return jsonify({"results":"failed, user not found!"})
    else:
        return jsonify({"results":"failed, missing some input data"})

def current_milli_time():
    return round(time.time() * 1000)

def get_profile(id):
    connection = mysql_get_mydb()
    print(connection)
    
    db_cursor = connection.cursor()

    sql = "SELECT * FROM profiles WHERE user_id = %s"
    input_id = (id, )

    db_cursor.execute(sql, input_id)

    results = db_cursor.fetchall()

    db_cursor.close()
    connection.close()

    if len(results)==1:
        return results[0]
    else:
        return None

def find_user_id(email):
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
        return results[0][0]
    else:
        return None

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')