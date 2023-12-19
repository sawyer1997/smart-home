from django.db import connection


def get_query(sql_query):
    with connection.cursor() as cursor:
        cursor.execute(sql_query)
        result = cursor.fetchall()
    return result


def update_insert_query(sql_query):
    with connection.cursor() as cursor:
        cursor.execute(sql_query)
        connection.commit()
