from flask import Flask, jsonify
import psycopg2

app = Flask(__name__)

DB_HOST = 'localhost'
DB_NAME = 'pagila'
DB_USER = 'your_username'
DB_PASSWORD = ''


def create_connection():
    try:
        connection = psycopg2.connect(
            host=DB_HOST,
            database=DB_NAME,
            user=DB_USER,
            password=DB_PASSWORD
        )
        return connection
    except psycopg2.Error as e:
        print(f"error connecting to database: {e}")
        return None


@app.route('/')
def hello_world():  # put application's code here
    return 'Hello World!'


@app.route('/customers', methods=['GET'])
def get_customers():
    connection = create_connection()
    if connection is None:
        return jsonify({"error": "unable to connect to the database"}), 500

    try:
        with connection.cursor() as cursor:
            cursor.execute("SELECT * FROM customer;")
            customers = cursor.fetchall()

            customer_list = []
            for customer in customers:
                customer_data = {
                    "customer_id": customer[0],
                    "first_name": customer[1],
                    "last_name": customer[2]
                }
                customer_list.append(customer_data)

            return jsonify({"customers": customer_list})
    except psycopg2.Error as e:
        print(f"Error retrieving data from the database: {e}")
        return jsonify({"error": "error retrieving data from the database"}), 500
    finally:
        connection.close()


if __name__ == '__main__':
    app.run(debug=True)
