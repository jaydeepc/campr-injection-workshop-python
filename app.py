import os
import webbrowser

import werkzeug
from flask import Flask, render_template, request, json, session, send_file, g, url_for
from flaskext.mysql import MySQL

app = Flask(__name__)

mysql = MySQL()

# MySQL configurations
app.config['MYSQL_DATABASE_USER'] = 'root'
app.config['MYSQL_DATABASE_PASSWORD'] = ''
app.config['MYSQL_DATABASE_DB'] = 'Injection'
app.config['MYSQL_DATABASE_HOST'] = 'localhost'
app.config['MYSQL_PORT'] = '3306'
mysql.init_app(app)


@app.route("/")
def main():
    conn = mysql.connect()
    cursor = conn.cursor()

    all_users = fetch_users(conn, cursor)

    return render_template('login.html', users=all_users)


def fetch_users(conn, cursor):
    query = "select vendor_name from users"
    try:
        cursor.execute(query)
        all_data = cursor.fetchall()
    except:
        conn.rollback()
    return all_data


@app.route('/', methods=['POST'])
def login():

    _username = request.form["vendor"]
    _password = request.form['password']

    if _username and _password:
        conn = mysql.connect()
        cursor = conn.cursor()
        query = "select vendor_name from users where vendor_name='{0}' and password='{1}'".format(_username,
                                                                                                          _password)
        try:
            cursor.execute(query)
            data = cursor.fetchone()
        except Exception as ex:
            raise Exception(query, ex)

        all_users = fetch_users(conn, cursor)
        conn.close()


        if data is not None:
            return render_template('login.html', data=data, users=all_users, auth="right")
        else:
            data = "please check your vendor and password combination"
            return render_template('login.html', data=[data], users=all_users, auth="wrong")

    else:
        return json.dumps({'html': '<span>Enter the required fields</span>'})



if __name__ == "__main__":
    app.run(host='0.0.0.0', debug=True)
