import psycopg2
def conneccion():
    PG_HOST = 'yyyyyyyyyy'
    PG_USER = 'db_api_flask_user'
    PG_PASSWORD = 'XBfDf1jS5To8OYMNT3zE1ImVglTdZOKk'
    PG_DB = 'db_api_flask'
    con = psycopg2.connect(database=PG_DB, host=PG_HOST, user=PG_USER, password=PG_PASSWORD, port=5432)
    return con
