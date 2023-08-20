from sql_connection import get_sql_connection

def get_all_employees(connection):
    
    cursor = connection.cursor()

    query = ("SELECT employee.employee_id,employee.first_name,employee.last_name,employee.designation,employee.date_of_joining " 
            "FROM grocery_store.employee ")

    cursor.execute(query)

    response = []

    for (employee_id, first_name,last_name,designation, date_of_joining) in cursor:
        
        response.append(
            {
                'employee_id': employee_id,
                'first_name': first_name,
                'last_name': last_name,
                'designation': designation,
                'date_of_joining': date_of_joining
            }
        )
    return response

def insert_new_employee(connection, employee):
    cursor = connection.cursor()
    query = ("INSERT INTO employee "
             "(first_name,last_name,designation,date_of_joining)"
             "VALUES (%s, %s, %s,%s)")
    data = (employee['first_name'], employee['last_name'],employee['designation'],employee['date_of_joining'])
    cursor.execute(query,data)
    connection.commit()

    return cursor.lastrowid

def delete_employee(connection, employee_id):
    cursor = connection.cursor()
    query = ("DELETE FROM employee where employee_id=" + str(employee_id))
    cursor.execute(query)
    connection.commit()

    return cursor.lastrowid


if __name__=='__main__':
    connection = get_sql_connection()
    print(get_all_employees(connection))