import psycopg2
def conneccion():
    PG_HOST = 'localhost'
    PG_USER = 'postgres'
    PG_PASSWORD = 'postgres'
    PG_DB = 'db_api_flask'
    con = psycopg2.connect(database=PG_DB, host=PG_HOST, user=PG_USER, password=PG_PASSWORD, port=5432)
    return con