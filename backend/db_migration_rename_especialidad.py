#!/usr/bin/env python3
"""
Script de migración para renombrar columna especialidad a horarios_clases
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
        
        # Verificar si la columna especialidad existe
        cursor.execute("""
            SELECT COUNT(*) 
            FROM INFORMATION_SCHEMA.COLUMNS 
            WHERE TABLE_SCHEMA = %s 
            AND TABLE_NAME = 'PROFESORES' 
            AND COLUMN_NAME = 'especialidad'
        """, (config['database'],))
        
        exists_especialidad = cursor.fetchone()[0]
        
        # Verificar si ya existe horarios_clases
        cursor.execute("""
            SELECT COUNT(*) 
            FROM INFORMATION_SCHEMA.COLUMNS 
            WHERE TABLE_SCHEMA = %s 
            AND TABLE_NAME = 'PROFESORES' 
            AND COLUMN_NAME = 'horarios_clases'
        """, (config['database'],))
        
        exists_horarios = cursor.fetchone()[0]
        
        if exists_horarios:
            print("✓ La columna 'horarios_clases' ya existe en la tabla PROFESORES")
        elif exists_especialidad:
            print("Renombrando columna 'especialidad' a 'horarios_clases'...")
            cursor.execute("""
                ALTER TABLE PROFESORES 
                CHANGE COLUMN especialidad horarios_clases VARCHAR(100) NOT NULL
            """)
            cnx.commit()
            print("✓ Columna renombrada exitosamente")
        else:
            print("Agregando columna 'horarios_clases'...")
            cursor.execute("""
                ALTER TABLE PROFESORES 
                ADD COLUMN horarios_clases VARCHAR(100) NOT NULL DEFAULT ''
            """)
            cnx.commit()
            print("✓ Columna agregada exitosamente")
        
        # Mostrar estructura actualizada
        cursor.execute("DESCRIBE PROFESORES")
        print("\n" + "="*80)
        print("Estructura actualizada de la tabla PROFESORES:")
        print("-" * 80)
        for (field, type, null, key, default, extra) in cursor:
            print(f"{field:20} {type:20} {null:10} {key:10} {str(default):15} {extra}")
        print("-" * 80)
        
        # Mostrar ejemplos
        cursor.execute("SELECT id, nombre, apellido, horarios_clases FROM PROFESORES LIMIT 5")
        print("\nEjemplos de profesores:")
        print("-" * 80)
        for (id, nombre, apellido, horarios) in cursor:
            print(f"  {id:3} | {nombre:15} {apellido:15} | {horarios}")
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
    print("MIGRACIÓN: Renombrar 'especialidad' a 'horarios_clases' en PROFESORES")
    print("=" * 80)
    migrate()
