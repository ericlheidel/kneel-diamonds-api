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
                    o.size_id,
                    o.style_id,
                    o.metal_id,
                    o.type_id,
                    m.metal,
                    m.price AS metal_price,
                    st.style,
                    st.price AS style_price,
                    si.carets,
                    si.price AS size_price,
                    t.name,
                    t.multiplier
                FROM `Orders` o
                    LEFT JOIN Metals m ON m.id = o.metal_id
                    LEFT JOIN Styles st ON st.id = o.style_id
                    LEFT JOIN Sizes si ON si.id = o.size_id
                    LEFT JOIN Types t ON t.id = o.type_id
            """
        )
        query_results = database_cursor.fetchall()

        orders = []
        for row in query_results:
            # orders.append(dict(row))
            size = {"carets": row["carets"], "price": row["size_price"]}
            style = {"style": row["style"], "price": row["style_price"]}
            metal = {"metal": row["metal"], "price": row["metal_price"]}
            type = {"name": row["name"], "multiplier": row["multiplier"]}
            order = {
                "id": row["id"],
                "size_id": row["size_id"],
                "size": size,
                "style_id": row["style_id"],
                "style": style,
                "metal_id": row["metal_id"],
                "metal": metal,
                "type_id": row["type_id"],
                "type": type,
            }
            orders.append(order)

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
                    o.size_id,
                    o.style_id,
                    o.metal_id,
                    o.type_id,
                    m.metal,
                    m.price AS metal_price,
                    st.style,
                    st.price AS style_price,
                    si.carets,
                    si.price AS size_price,
                    t.name,
                    t.multiplier
                FROM `Orders` o
                    LEFT JOIN Metals m ON m.id = o.metal_id
                    LEFT JOIN Styles st ON st.id = o.style_id
                    LEFT JOIN Sizes si ON si.id = o.size_id
                    LEFT JOIN Types t ON t.id = o.type_id
                WHERE o.id = ?
            """,
            (pk,),
        )
        query_results = database_cursor.fetchone()

        query_results = dict(query_results)

        print(query_results)

        size = {"carets": query_results["carets"], "price": query_results["size_price"]}
        style = {"style": query_results["style"], "price": query_results["style_price"]}
        metal = {"metal": query_results["metal"], "price": query_results["metal_price"]}
        type = {
            "name": query_results["name"],
            "multiplier": query_results["multiplier"],
        }

        order = {
            "id": query_results["id"],
            "size_id": query_results["size_id"],
            "size": size,
            "style_id": query_results["style_id"],
            "style": style,
            "metal_id": query_results["metal_id"],
            "metal": metal,
            "type_id": query_results["type_id"],
            "type": type,
        }

        # dictionary_version_of_object = dict(order)

        # serialized_order = json.dumps(dictionary_version_of_object)
        # serialized_order = json.dumps(order)

        # return serialized_order
        return json.dumps(order)


def post_order(order_info):
    with sqlite3.connect("./kneeldiamonds.sqlite3") as connection:
        database_cursor = connection.cursor()
        database_cursor.execute(
            """
                INSERT INTO Orders (
                    metal_id,
                    size_id,
                    style_id,
                    type_id
                )
                    VALUES (
                        ?,
                        ?,
                        ?,
                        ?
                    )
            """,
            (
                order_info["metal_id"],
                order_info["size_id"],
                order_info["style_id"],
                order_info["type_id"],
            ),
        )
    return True if database_cursor.rowcount > 0 else False


def delete_order(pk):
    with sqlite3.connect("./kneeldiamonds.sqlite3") as connection:
        connection.row_factory = sqlite3.Row
        database_cursor = connection.cursor()

        database_cursor.execute(
            """
                DELETE FROM Orders
                WHERE id = ?
            """,
            (pk,),
        )

    return True if database_cursor.rowcount > 0 else False
