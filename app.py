from flask import Flask, request, jsonify
import psycopg2

app = Flask(__name__)

DB_HOST = 'localhost'
DB_NAME = 'pagila'
DB_USER = 'timthom'


def create_connection():
    try:
        connection = psycopg2.connect(
            host=DB_HOST,
            database=DB_NAME,
            user=DB_USER
        )
        return connection
    except psycopg2.Error as e:
        print(f"error connecting to database: {e}")
        return None


@app.route('/')
def hello_world():  # put application's code here
    return 'Hello World!'


@app.route('/get_actors', methods=['GET'])
def get_actors():
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
                    "actor_id": customer[0],
                    "first_name": customer[1],
                    "last_name": customer[2],
                    "last_update": customer[3]
                }
                customer_list.append(customer_data)

            return jsonify({"actors": customer_list})
    except psycopg2.Error as e:
        print(f"Error retrieving data from the database: {e}")
        return jsonify({"error": "error retrieving data from the database"}), 500
    finally:
        connection.close()


@app.route('/create_actor', methods=['POST'])
def create_actor():
    connection = create_connection()
    if connection is None:
        return jsonify({"error": "unable to connect to the database"}), 500

    try:
        data = request.get_json()
        first_name = data.get('first_name')
        last_name = data.get('last_name')

        with connection.cursor() as cursor:
            query = "INSERT INTO actor (first_name, last_name) VALUES (%s, %s) RETURNING actor_id;"
            cursor.execute(query, (first_name, last_name))
            new_actor_id = cursor.fetchone()[0]
            connection.commit()

        return jsonify({"message": f"Actor {new_actor_id} created successfullly"}), 201
    except psycopg2.Error as e:
        print(f"Error creating actor: {e}")
        return jsonify({"error": "failed to create actor"}), 500
    finally:
        connection.close()


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)

