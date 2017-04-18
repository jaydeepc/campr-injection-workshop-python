import os
import webbrowser
from flask import jsonify
import werkzeug
from flask import Flask, render_template, request, json, session, send_file, g, url_for
from flaskext.mysql import MySQL

app = Flask(__name__)

mysql = MySQL()

# MySQL configurations
app.config['MYSQL_DATABASE_USER'] = 'root'
app.config['MYSQL_DATABASE_PASSWORD'] = ''
app.config['MYSQL_DATABASE_DB'] = 'Injection'
app.config['MYSQL_DATABASE_HOST'] = 'db_server'
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


@app.route("/invoices")
def invoices():

    conn = mysql.connect()
    cursor = conn.cursor()

    return render_template('invoice.html')


@app.route("/allinvoices", methods=['GET'])
def allinvoices():

    list_text = []
    conn = mysql.connect()
    cursor = conn.cursor()

    all_data = fetch_invoices(conn, cursor)

    conn.close()

    for data in all_data:
        list_text.append(data[0])

    return jsonify(text=list_text)


@app.route("/invoices", methods=['POST'])
def insert_invoices():

    __invoice = request.form["txt_invoice"]

    conn = mysql.connect()
    cursor = conn.cursor()

    query = "insert into invoices (text) values ('{0}');".format(__invoice)
    try:
        cursor.execute(query)
        conn.commit()
    except:
        conn.rollback()

    all_data = fetch_invoices(conn, cursor)
    conn.close()

    return render_template('invoice.html', invoices=all_data)


def fetch_invoices(conn, cursor):
    query = "select text from invoices"
    try:
        cursor.execute(query)
        all_data = cursor.fetchall()
    except:
        conn.rollback()
    return all_data


if __name__ == "__main__":
    app.run(host='0.0.0.0', debug=True)
