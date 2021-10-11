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
def profile_insertupdate():
    content = request.json
    if 'email' in content and 'name' in content:
        print('email: ' + content['email'])
        print('name: ' + content['name'])
        email = content['email']
        # insert_db(email, password)
        result_find_user_id = find_user_id(email)

        if 'address' not in content:
            content['address'] = None
        if 'mobile' not in content:
            content['mobile'] = None

        if result_find_user_id is not None:
            print(result_find_user_id)
            if is_profile_exists(result_find_user_id):
                update_profile(result_find_user_id, content['name'], content['address'], content['mobile'])
            else:
                insert_profile(result_find_user_id, content['name'], content['address'], content['mobile'])
            return jsonify({"status":"success"})
        else:
            return jsonify({"status":"failed, user not found!"})
    else:
        return jsonify({"status":"failed, missing some input data"})

def current_milli_time():
    return round(time.time() * 1000)

def is_profile_exists(id):
    connection = mysql_get_mydb()
    print(connection)

    db_cursor = connection.cursor()

    sql = "SELECT * FROM profiles WHERE user_id = %s"
    input_id = (id, )

    db_cursor.execute(sql, input_id)

    results = db_cursor.fetchall()

    db_cursor.close()
    connection.close()

    if len(results)>0:
        return True
    else:
        return False

def update_profile(user_id, user_name, user_address, user_mobile):
    connection = mysql_get_mydb()
    print(connection)

    db_cursor = connection.cursor()

    sql = "UPDATE profiles SET user_name = %s, user_address = %s, user_mobile = %s WHERE user_id = %s"
    val = (user_name, user_address, user_mobile, user_id)

    db_cursor.execute(sql, val)

    connection.commit()

    print(db_cursor.rowcount, "record(s) affected")

    db_cursor.close()
    connection.close()

def insert_profile(user_id, user_name, user_address, user_mobile):
    connection = mysql_get_mydb()
    print(connection)

    db_cursor = connection.cursor()

    sql = "INSERT INTO profiles (user_id, user_name, user_address, user_mobile) VALUES (%s, %s, %s, %s)"
    val = (user_id, user_name, user_address, user_mobile)
    db_cursor.execute(sql, val)

    connection.commit()

    print(db_cursor.rowcount, "record inserted.")

    db_cursor.close()
    connection.close()

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