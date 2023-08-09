# /srv/salt/_modules/get_actors.py
import psycopg2


def is_new_actor(cursor, actor):
    select_query = "SELECT 1 FROM actor WHERE actor_id = %(customer_id)s"
    cursor.execute(select_query, {"actor_id": actor["actor_id"]})
    return cursor.fetchone() is None


def get_actors():
    try:
        url = "http://localhost:5000/get_actors"
        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()
            return data
        else:
            print(f"Error: Unable to fetch data from agnes's API. Status Code: {response.status_code}")
            return None
    except requests.RequestException as e:
        print(f"Error connecting to agnes's API: {e}")
        return None


def sync_actors():
    try:
        customer_data = get_actors()

        conn = psycopg2.connect(
            dbname='pagilascada',
            user='timthom',
            password='',
            host='192.168.56.201',
            port='5432',
        )

        cursor = conn.cursor()
        new_actors = [actor for actor in actor_data if is_new_actor(cursor, actor)]
        insert_query = """
            INSERT INTO actor (actor_id, first_name, last_name)
            SELECT %(actor_id)s, %(first_name)s, %(last_name)s
            WHERE NOT EXISTS (SELECT 1 FROM actor WHERE actor_id = %(actor_id)s)
        """
        cursor.executemany(insert_query, new_actors)
        conn.commit()
        conn.close()
        return "actor data synchronized successfully"
    except psycopg2.Error as e:
        return f"Error synchronizing actor data: {e}"

