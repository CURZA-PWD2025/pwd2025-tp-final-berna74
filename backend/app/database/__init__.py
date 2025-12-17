import mysql.connector
import os
from dotenv import load_dotenv

load_dotenv()

class ConectDB:
    
    @staticmethod
    def get_connect():
        try:
            conn = mysql.connector.connect(
                user=os.getenv("DB_USER", "root"),  # Clave correcta para el usuario
                password=os.getenv("DB_PASSWORD", ""),  # Clave correcta para la contraseña
                database=os.getenv("DB_NAME"),  # Nombre de la base de datos
                host=os.getenv("DB_HOST", "localhost"),  # Host de la base de datos
                port=int(os.getenv("DB_PORT", 3306))  # Puerto de la base de datos
            )
            print("Conexión exitosa a la base de datos")
            return conn
        except mysql.connector.Error as ex:
            print(f"Error al conectar a la base de datos: {ex}")
            return None