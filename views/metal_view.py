import sqlite3
import json


def update_metal(id, metal_data):
    with sqlite3.connect("./kneeldiamonds.sqlite3") as connection:
        database_cursor = connection.cursor()

        database_cursor.execute(
            """
                UPDATE Metals
                    SET
                        metal = ?,
                        price = ?
                    WHERE id = ?
            """,
            (metal_data["metal"], metal_data["price"], id),
        )

        return True if database_cursor.rowcount > 0 else False


def list_metals():

    # Open a connection to the database
    with sqlite3.connect("./kneeldiamonds.sqlite3") as connection:
        connection.row_factory = sqlite3.Row
        database_cursor = connection.cursor()

        # Write the SQL query to get the information you want
        database_cursor.execute(
            """
                SELECT
                    m.id,
                    m.metal,
                    m.price
                FROM Metals m
            """
        )
        query_results = database_cursor.fetchall()

        metals = []
        for row in query_results:
            metals.append(dict(row))

        serialized_metals = json.dumps(metals)

    return serialized_metals


def get_single_metal(pk):
    with sqlite3.connect("./kneeldiamonds.sqlite3") as connection:
        connection.row_factory = sqlite3.Row
        database_cursor = connection.cursor()

        database_cursor.execute(
            """
                SELECT
                    m.id,
                    m.metal,
                    m.price
                FROM Metals m
                WHERE m.id = ?
            """,
            (pk,),
        )
        query_results = database_cursor.fetchone()

        dictionary_version_of_object = dict(query_results)
        serialized_metal = json.dumps(dictionary_version_of_object)

        return serialized_metal
