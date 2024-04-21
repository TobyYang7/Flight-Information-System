import mysql.connector
import json


def prepare_cursor():
    with open('database/server_config.json') as f:
        config = json.load(f)
    cnx = mysql.connector.connect(**config)
    cursor = cnx.cursor(buffered=True)
    return cursor, cnx


def create_database(database_name):
    try:
        cursor, cnx = prepare_cursor()
        cursor.execute(f"CREATE DATABASE IF NOT EXISTS {database_name}")
        cursor.execute(f"USE {database_name}")
        cnx.commit()
        print(f"Database '{database_name}' created successfully.")

    except mysql.connector.Error as err:
        print(f"Failed creating database: {err}")

    finally:
        if 'cursor' in locals():
            cursor.close()
        if 'cnx' in locals():
            cnx.close()


def create_relation_schema(relation_schema):
    try:
        cursor, cnx = prepare_cursor()
        with open(relation_schema, 'r', encoding='utf-8') as p:
            sql_statements = p.read()

        for sql_statement in sql_statements.split(';'):
            if sql_statement.strip():
                cursor.execute(sql_statement)

        cnx.commit()
        print("Relation schema created successfully.")

    except Exception as e:
        print(f"Failed to create relation schema: {e}")
        cnx.rollback()

    finally:
        if 'cursor' in locals():
            cursor.close()
        if 'cnx' in locals():
            cnx.close()


if __name__ == "__main__":
    create_database('FIS')
    create_relation_schema('database/relation_schema.sql')
