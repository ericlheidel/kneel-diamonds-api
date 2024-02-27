import sqlite3
import json


def list_orders():

    # Open a connection to the database
    with sqlite3.connect("./kneeldiamonds.sqlite3") as connection:
        connection.row_factory = sqlite3.Row
        database_cursor = connection.cursor()

        # Write the SQL query to get the information you want
        database_cursor.execute(
            """
                SELECT
                    o.id,
                    o.metal_id,
                    o.size_id,
                    o.style_id,
                    o.type_id
                FROM Orders o
            """
        )
        query_results = database_cursor.fetchall()

        orders = []
        for row in query_results:
            orders.append(dict(row))

        serialized_orders = json.dumps(orders)

    return serialized_orders


def get_single_order(pk):
    with sqlite3.connect("./kneeldiamonds.sqlite3") as connection:
        connection.row_factory = sqlite3.Row
        database_cursor = connection.cursor()

        database_cursor.execute(
            """
                SELECT
                    o.id,
                    o.metal_id,
                    o.size_id,
                    o.style_id,
                    o.type_id
                FROM Orders o
                WHERE o.id = ?
            """,
            (pk,),
        )
        query_results = database_cursor.fetchone()

        dictionary_version_of_object = dict(query_results)
        serialized_order = json.dumps(dictionary_version_of_object)

        return serialized_order
