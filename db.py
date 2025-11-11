import mysql.connector

DB_CONFIG = {
    "host": "localhost",
    "user": "server",
    "password": "pirineus",
    "database": "Control",
    "port": 27090,
    "use_pure": True
}

conn = mysql.connector.connect(**DB_CONFIG)
cursor = conn.cursor()
cursor.execute("SELECT COUNT(*) FROM Tarjetas WHERE coditarjeta = %s", ("6385d51d",))
print(cursor.fetchone())
cursor.close()
conn.close()