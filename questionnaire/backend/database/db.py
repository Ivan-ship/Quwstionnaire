import psycopg

conn = psycopg.connect(
    dbname = "questionnaire",
    user = "postgres",
    password = "qwpsql_18",
    host = "localhost",
    port = 5431
)