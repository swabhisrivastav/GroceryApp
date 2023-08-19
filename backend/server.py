from flask import Flask,request,jsonify,render_template
from sql_connection import get_sql_connection
import mysql.connector
import json

import product_dao
import uom_dao
import orders_dao


app = Flask(__name__,template_folder="templates")

connection = get_sql_connection()

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
	

if __name__ == '__main__':
    print("Starting Python Flask Server For Grocery Store Management System")
    app.run(port=5000)