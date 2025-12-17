#!/usr/bin/env python3
"""
Script de migración para agregar prefijo 2920 a teléfonos que no lo tienen
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
        
        # Actualizar SOCIOS
        print("\n1. Actualizando teléfonos en tabla SOCIOS...")
        cursor.execute("""
            UPDATE SOCIOS 
            SET telefono = CONCAT('2920', telefono) 
            WHERE telefono NOT LIKE '2920%'
        """)
        socios_updated = cursor.rowcount
        print(f"   ✓ {socios_updated} teléfonos actualizados en SOCIOS")
        
        # Actualizar ALUMNOS
        print("\n2. Actualizando teléfonos en tabla ALUMNOS...")
        cursor.execute("""
            UPDATE ALUMNOS 
            SET telefono = CONCAT('2920', telefono) 
            WHERE telefono NOT LIKE '2920%'
        """)
        alumnos_updated = cursor.rowcount
        print(f"   ✓ {alumnos_updated} teléfonos actualizados en ALUMNOS")
        
        # Actualizar PROFESORES
        print("\n3. Actualizando teléfonos en tabla PROFESORES...")
        cursor.execute("""
            UPDATE PROFESORES 
            SET telefono = CONCAT('2920', telefono) 
            WHERE telefono NOT LIKE '2920%'
        """)
        profesores_updated = cursor.rowcount
        print(f"   ✓ {profesores_updated} teléfonos actualizados en PROFESORES")
        
        cnx.commit()
        
        # Mostrar ejemplos de datos actualizados
        print("\n" + "="*80)
        print("Ejemplos de teléfonos actualizados:")
        print("-" * 80)
        
        cursor.execute("SELECT id, nombre, apellido, telefono FROM SOCIOS LIMIT 5")
        print("\nSOCIOS:")
        for (id, nombre, apellido, telefono) in cursor:
            print(f"  {id:3} | {nombre:15} {apellido:15} | {telefono}")
        
        cursor.execute("SELECT id, nombre, apellido, telefono FROM ALUMNOS LIMIT 5")
        print("\nALUMNOS:")
        for (id, nombre, apellido, telefono) in cursor:
            print(f"  {id:3} | {nombre:15} {apellido:15} | {telefono}")
        
        cursor.execute("SELECT id, nombre, apellido, telefono FROM PROFESORES LIMIT 5")
        print("\nPROFESORES:")
        for (id, nombre, apellido, telefono) in cursor:
            print(f"  {id:3} | {nombre:15} {apellido:15} | {telefono}")
        
        print("-" * 80)
        
        cursor.close()
        cnx.close()
        
        print("\n✓ Migración completada exitosamente")
        print(f"Total actualizado: {socios_updated + alumnos_updated + profesores_updated} teléfonos")
        
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
    print("MIGRACIÓN: Agregar prefijo 2920 a teléfonos existentes")
    print("=" * 80)
    migrate()
