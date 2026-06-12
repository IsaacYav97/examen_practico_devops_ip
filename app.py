import os
import time
from flask import Flask, jsonify
import psycopg2

app = Flask(__name__)

APP_NAME = os.getenv("APP_NAME", "Mi Aplicación Flask")
APP_VERSION = os.getenv("APP_VERSION", "1.0.0")
DB_HOST = os.getenv("DB_HOST", "db")
DB_NAME = os.getenv("DB_NAME", "devops_db")
DB_USER = os.getenv("DB_USER", "postgres")
DB_PASSWORD = os.getenv("DB_PASSWORD", "postgres")
DB_PORT = os.getenv("DB_PORT", "5432")

def get_db_connection():
    retries = 5
    while retries > 0:
        try:
            conn = psycopg2.connect(
                host=DB_HOST, database=DB_NAME, user=DB_USER, password=DB_PASSWORD, port=DB_PORT
            )
            return conn
        except psycopg2.OperationalError:
            retries -= 1
            time.sleep(2)
    return None

@app.route('/')
def index():
    conn = get_db_connection()
    status = "Conectado exitosamente" if conn else "Error de conexión"
    if conn: conn.close()

    return jsonify({
        "nombre_aplicacion": APP_NAME,
        "version_actual": APP_VERSION,
        "estado_conexion_postgresql": status
    })

@app.route('/productos')
def list_productos():
    conn = get_db_connection()
    if not conn:
        return jsonify({"error": "No se pudo conectar a la base de datos"}), 500
    
    cur = conn.cursor()
    cur.execute("SELECT id, nombre, precio, stock FROM productos;")
    rows = cur.fetchall()
    cur.close()
    conn.close()

    productos = [{"id": r[0], "nombre": r[1], "precio": float(r[2]), "stock": r[3]} for r in rows]
    return jsonify(productos)

if __name__ == '__main__':
    # Ya no llamamos a init_db(), Docker se encargó de eso
    app.run(host='0.0.0.0', port=5000)