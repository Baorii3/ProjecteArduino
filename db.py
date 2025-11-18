import mysql.connector
from mysql.connector import Error 

# DB
DB_CONFIG = {
    "host": "54.85.160.68",
    "user": "server",
    "password": "pirineus",
    "database": "Control",
    "port": 3306,
    "use_pure": True
}

# Crear conexión a DB
def create_connection():
    try:
        connection = mysql.connector.connect(**DB_CONFIG)
        return connection
    except Error as e:
        print(f"Error al conectar a la DB: {e}")
        return None
    
# Ejecutar consulta en la DB
def execute_query(coditarjeta, client):
    connection = create_connection()
    if connection is None:
        print("No se pudo conectar a la DB")
        return
    try:
        cursor = connection.cursor()
        query = "SELECT COUNT(*) FROM TARGETA WHERE TARGETA.CODI = %s"
        cursor.execute(query, (coditarjeta,))
        result = cursor.fetchone()
        if result[0] > 0:
            if not check_assistance(coditarjeta):
                create_assistance(coditarjeta)
                return result[0]
            else:
                print(f"Asistencia ya registrada para la tarjeta con codi {coditarjeta}")
                return 0
        print(f"Cantidad de tarjetas amb codi {coditarjeta}: {result[0]}")
        cursor.close()
        return -1
    
    finally:
        connection.close()

# Comprovem si hi ha assistencia d'aquell usuari aquell dia
def check_assistance(coditarjeta):
    connection = create_connection()
    if connection is None:
        print("No se pudo conectar a la DB")
        return False
    try:
        cursor = connection.cursor()
        query = """
            SELECT COUNT(*) 
            FROM ASISTENCIA a
            JOIN TARGETA t ON a.ID_TARGETA = t.ID_TARGETA
            WHERE t.CODI = %s AND DATE(a.Fecha) = CURDATE()
        """
        cursor.execute(query, (coditarjeta,))
        result = cursor.fetchone()
        cursor.close()
        return result[0] > 0
    finally:
        connection.close()


# Crear una asistencia en la BBDD
def create_assistance(coditarjeta):
    connection = create_connection()
    if connection is None:
        print("No se pudo conectar a la DB")
        return
    try:
        cursor = connection.cursor()
        query = """
            INSERT INTO ASISTENCIA (ID_ASISTENCIA, ID_TARGETA, ID_DISPOSITIU, ID_HORARI, Fecha, Estat)
            Select 1, u.ID_TARGETA, 1, g.ID_HORARI, NOW(), 'Present'
            from USUARI u 
            join TARGETA t on u.ID_TARGETA = t.ID_TARGETA
            join USUARI_GRUP ug on u.ID_USUARI = ug.ID_USUARI
            join GRUP g on ug.ID_GRUP = g.ID_GRUP
            where t.CODI = %s
        """
        cursor.execute(query, (coditarjeta,))
        connection.commit()
        cursor.execute("SELECT Nombre FROM USUARI u WHERE u.ID_TARGETA = (SELECT t.ID_TARGETA FROM TARGETA t WHERE CODI = %s)", (coditarjeta,))
        nombre = cursor.fetchone()[0]
        print(f"Asistencia creada para el usuari: {nombre} con codi targeta: {coditarjeta}")
        cursor.close()
    finally:
        connection.close()
