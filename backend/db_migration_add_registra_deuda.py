#!/usr/bin/env python3
"""
Script de migración para agregar columna registra_deuda a tabla SOCIOS
"""
import mysql.connector
from mysql.connector import errorcode
import os
from dotenv import load_dotenv

load_dotenv()

config = {
    'user': os.getenv("DB_USER"),
    'password': os.getenv("DB_PASSWORD"),
    'host': os.getenv("DB_HOST", "127.0.0.1"),
    'port': int(os.getenv("DB_PORT", 3306)),
    'database': os.getenv("DB_NAME", "sipepa"),
    'raise_on_warnings': True
}

def migrate():
    try:
        cnx = mysql.connector.connect(**config)
        cursor = cnx.cursor()
        
        print(f"Conectado a la base de datos '{config['database']}'")
        
        # Verificar si la columna ya existe
        cursor.execute("""
            SELECT COUNT(*) 
            FROM INFORMATION_SCHEMA.COLUMNS 
            WHERE TABLE_SCHEMA = %s 
            AND TABLE_NAME = 'SOCIOS' 
            AND COLUMN_NAME = 'registra_deuda'
        """, (config['database'],))
        
        exists = cursor.fetchone()[0]
        
        if exists:
            print("✓ La columna 'registra_deuda' ya existe en la tabla SOCIOS")
        else:
            print("Agregando columna 'registra_deuda' a tabla SOCIOS...")
            cursor.execute("""
                ALTER TABLE SOCIOS 
                ADD COLUMN registra_deuda BOOLEAN DEFAULT FALSE AFTER profesor_id
            """)
            cnx.commit()
            print("✓ Columna 'registra_deuda' agregada exitosamente")
        
        # Mostrar estructura actualizada
        cursor.execute("DESCRIBE SOCIOS")
        print("\nEstructura actual de la tabla SOCIOS:")
        print("-" * 80)
        for (field, type, null, key, default, extra) in cursor:
            print(f"{field:20} {type:20} {null:10} {key:10} {str(default):15} {extra}")
        print("-" * 80)
        
        cursor.close()
        cnx.close()
        print("\n✓ Migración completada exitosamente")
        
    except mysql.connector.Error as err:
        if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
            print("✗ Error: Usuario o contraseña incorrectos")
        elif err.errno == errorcode.ER_BAD_DB_ERROR:
            print(f"✗ Error: La base de datos '{os.getenv('DB_NAME', 'sipepa')}' no existe")
        else:
            print(f"✗ Error: {err}")
    except Exception as e:
        print(f"✗ Error inesperado: {e}")

if __name__ == '__main__':
    print("=" * 80)
    print("MIGRACIÓN: Agregar campo 'registra_deuda' a tabla SOCIOS")
    print("=" * 80)
    migrate()
