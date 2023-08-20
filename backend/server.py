from flask import Flask,request,jsonify,render_template,redirect,url_for, session
from sql_connection import get_sql_connection
import mysql.connector
import json
import re

import product_dao
import uom_dao
import orders_dao
import employee_dao

db_config = {
    'user': 'root',
    'password': 'Swabhi@16',
    'host': '127.0.0.1',
    'database': 'grocery_store'
}
def get_sql_connection():
    try:
        connection = mysql.connector.connect(**db_config)
        return connection
    except mysql.connector.Error as err:
        print(f"Error: {err}")
        return None


app = Flask(__name__,template_folder="templates")

connection = get_sql_connection()

@app.route('/homepage')
def home_page():
    return render_template('homepage.html')


@app.route('/')
def first():
    return render_template('index.html')

@app.route('/getUOM', methods=['GET'])
def get_uom():
    response = uom_dao.get_uoms(connection)
    response = jsonify(response)
    response.headers.add('Access-Control-Allow-Origin', '*')
    return response

@app.route('/getProducts', methods=['GET'])
def get_products():
    products = product_dao.get_all_products(connection)
    return render_template('manage-product.html', products=products)


@app.route('/api/getProducts', methods=['GET'])
def api_get_products():
    response = product_dao.get_all_products(connection)
    response = jsonify(response)
    response.headers.add('Access-Control-Allow-Origin', '*')
    return response


@app.route('/api/insertProduct', methods=['POST'])
def insert_product():
    request_payload = json.loads(request.form['data'])
    product_id = product_dao.insert_new_product(connection, request_payload)
    response = jsonify({
        'product_id': product_id
    })
    response.headers.add('Access-Control-Allow-Origin', '*')
    return response

@app.route('/getAllOrders', methods=['GET'])
def get_all_orders():
    return render_template('order.html')

@app.route('/api/getAllOrders', methods=['GET'])
def api_get_all_orders():
    response = orders_dao.get_all_orders(connection)
    response = jsonify(response)
    response.headers.add('Access-Control-Allow-Origin', '*')
    return response

@app.route('/api/insertOrder', methods=['POST'])
def insert_order():
    request_payload = json.loads(request.form['data'])
    order_id = orders_dao.insert_order(connection, request_payload)
    response = jsonify({
        'order_id': order_id
    })
    response.headers.add('Access-Control-Allow-Origin', '*')
    return response


@app.route('/deleteProduct', methods=['POST'])
def delete_product():
    return_id = product_dao.delete_product(connection, request.form['product_id'])
    response = jsonify({
        'product_id': return_id
    })
    response.headers.add('Access-Control-Allow-Origin', '*')
    return response


@app.route('/login', methods=['GET', 'POST'])
def login():
    msg = ''
    if request.method == 'POST' and 'username' in request.form and 'password' in request.form:
        username = request.form['username']
        password = request.form['password']
        cursor = None
        try:
            connection = get_sql_connection()
            cursor = connection.cursor(dictionary=True)  # Use a dictionary cursor

            # Use parameterized query to prevent SQL injection
            cursor.execute('SELECT * FROM accounts WHERE username = %s AND password = %s', (username, password))
            account = cursor.fetchone()
            if account:
                session['loggedin'] = True
                session['id'] = account['id']
                session['username'] = account['username']
                msg = 'Logged in successfully!'
                return render_template('index.html', msg=msg)
            else:
                msg = 'Incorrect username / password!'
        except mysql.connector.Error as err:
            print(f"Database error: {err}")
            msg = 'Database error'
        finally:
            if cursor:
                cursor.close()
            if connection:
                connection.close()
    return render_template('login.html', msg=msg)


@app.route('/logout')
def logout():
    session.pop('loggedin', None)
    session.pop('id', None)
    session.pop('username', None)
    return redirect(url_for('login'))

@app.route('/register', methods=['GET', 'POST'])
def register():
    msg = ''
    if request.method == 'POST' and 'username' in request.form and 'password' in request.form and 'email' in request.form:
        username = request.form['username']
        password = request.form['password']
        email = request.form['email']
        try:
            connection = get_sql_connection()
            cursor = connection.cursor(dictionary=True)
            
            cursor.execute('SELECT * FROM accounts WHERE username = %s', (username,))
            account = cursor.fetchone()
            if account:
                msg = 'Account already exists!'
            elif not re.match(r'[^@]+@[^@]+\.[^@]+', email):
                msg = 'Invalid email address!'
            elif not re.match(r'[A-Za-z0-9]+', username):
                msg = 'Username must contain only characters and numbers!'
            elif not username or not password or not email:
                msg = 'Please fill out the form!'
            else:
                cursor.execute('INSERT INTO accounts (username, password, email) VALUES (%s, %s, %s)', (username, password, email))
                connection.commit()
                msg = 'You have successfully registered!'
        except mysql.connector.Error as err:
            print(f"Database error: {err}")
            msg = 'Database error'
        finally:
            if cursor:
                cursor.close()
            if connection:
                connection.close()
    elif request.method == 'POST':
        msg = 'Please fill out the form!'
    return render_template('register.html', msg=msg)
	
@app.route('/getEmployees', methods=['GET'])
def get_employees():
    return render_template('employee.html')

@app.route('/api/getEmployees', methods=['GET'])
def api_get_employees():
    response = employee_dao.get_all_employees(connection)
    response = jsonify(response)
    response.headers.add('Access-Control-Allow-Origin', '*')
    return response

@app.route('/api/insertEmployee', methods=['POST'])
def insert_employees():
    request_payload = json.loads(request.form['data'])
    employee_id = employee_dao.insert_new_employee(connection, request_payload)
    response = jsonify({
        'employee': employee_id
    })
    response.headers.add('Access-Control-Allow-Origin', '*')
    return response

@app.route('/deleteEmployee', methods=['POST'])
def delete_employee():
    return_id = employee_dao.delete_employee(connection, request.form['employee_id'])
    response = jsonify({
        'employee_id': return_id
    })
    response.headers.add('Access-Control-Allow-Origin', '*')
    return response

if __name__ == '__main__':
    print("Starting Python Flask Server For Grocery Store Management System")
    app.secret_key = 'your_secret_key'
    app.run(port=5000)


