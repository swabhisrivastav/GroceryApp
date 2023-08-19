from sql_connection import get_sql_connection

def get_all_products(connection):
    
    cursor = connection.cursor()

    query = ("SELECT product.product_id,product.product_name,product.uom_id,product.product_Price,uom.uom_name " 
            "FROM grocery_store.product inner join uom on product.uom_id = uom.uom_id")

    cursor.execute(query)

    response = []

    for (product_id, product_name,uom_id,product_Price, uom_name) in cursor:
        
        response.append(
            {
                'product_id': product_id,
                'product_name': product_name,
                'uom_id': uom_id,
                'product_Price': product_Price,
                'uom_name': uom_name
            }
        )
    return response

def insert_new_product(connection, product):
    cursor = connection.cursor()
    query = ("INSERT INTO product "
             "(product_name,uom_id,product_Price)"
             "VALUES (%s, %s, %s)")
    data = (product['product_name'], product['uom_id'],product['product_Price'])
    cursor.execute(query,data)
    connection.commit()

    return cursor.lastrowid

def delete_product(connection, product_id):
    cursor = connection.cursor()
    query = ("DELETE FROM product where product_id=" + str(product_id))
    cursor.execute(query)
    connection.commit()

    return cursor.lastrowid


if __name__=='__main__':
    connection = get_sql_connection()
    print(delete_product(connection, 5))