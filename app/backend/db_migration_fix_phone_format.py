#!/usr/bin/env python3
"""
Script de migración para ajustar teléfonos a formato 2920 + 6 dígitos
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
        cursor = cnx.cursor(dictionary=True)
        
        print(f"Conectado a la base de datos '{config['database']}'")
        
        # Actualizar SOCIOS
        print("\n1. Ajustando teléfonos en tabla SOCIOS...")
        cursor.execute("SELECT id, telefono FROM SOCIOS")
        socios = cursor.fetchall()
        socios_updated = 0
        for socio in socios:
            telefono = socio['telefono']
            # Extraer solo dígitos después de 2920
            if telefono.startswith('2920'):
                resto = telefono[4:]  # Quitar '2920'
                # Tomar solo los primeros 6 dígitos numéricos
                digitos = ''.join(filter(str.isdigit, resto))[:6]
                if len(digitos) >= 6:
                    nuevo_telefono = '2920' + digitos[:6]
                    if nuevo_telefono != telefono:
                        cursor.execute("UPDATE SOCIOS SET telefono = %s WHERE id = %s", 
                                     (nuevo_telefono, socio['id']))
                        socios_updated += 1
        print(f"   ✓ {socios_updated} teléfonos ajustados en SOCIOS")
        
        # Actualizar ALUMNOS
        print("\n2. Ajustando teléfonos en tabla ALUMNOS...")
        cursor.execute("SELECT id, telefono FROM ALUMNOS")
        alumnos = cursor.fetchall()
        alumnos_updated = 0
        for alumno in alumnos:
            telefono = alumno['telefono']
            if telefono.startswith('2920'):
                resto = telefono[4:]
                digitos = ''.join(filter(str.isdigit, resto))[:6]
                if len(digitos) >= 6:
                    nuevo_telefono = '2920' + digitos[:6]
                    if nuevo_telefono != telefono:
                        cursor.execute("UPDATE ALUMNOS SET telefono = %s WHERE id = %s", 
                                     (nuevo_telefono, alumno['id']))
                        alumnos_updated += 1
        print(f"   ✓ {alumnos_updated} teléfonos ajustados en ALUMNOS")
        
        # Actualizar PROFESORES
        print("\n3. Ajustando teléfonos en tabla PROFESORES...")
        cursor.execute("SELECT id, telefono FROM PROFESORES")
        profesores = cursor.fetchall()
        profesores_updated = 0
        for profesor in profesores:
            telefono = profesor['telefono']
            if telefono.startswith('2920'):
                resto = telefono[4:]
                digitos = ''.join(filter(str.isdigit, resto))[:6]
                if len(digitos) >= 6:
                    nuevo_telefono = '2920' + digitos[:6]
                    if nuevo_telefono != telefono:
                        cursor.execute("UPDATE PROFESORES SET telefono = %s WHERE id = %s", 
                                     (nuevo_telefono, profesor['id']))
                        profesores_updated += 1
        print(f"   ✓ {profesores_updated} teléfonos ajustados en PROFESORES")
        
        cnx.commit()
        
        # Mostrar ejemplos de datos actualizados
        print("\n" + "="*80)
        print("Ejemplos de teléfonos ajustados:")
        print("-" * 80)
        
        cursor.execute("SELECT id, nombre, apellido, telefono FROM SOCIOS LIMIT 5")
        print("\nSOCIOS:")
        for row in cursor:
            print(f"  {row['id']:3} | {row['nombre']:15} {row['apellido']:15} | {row['telefono']}")
        
        cursor.execute("SELECT id, nombre, apellido, telefono FROM ALUMNOS LIMIT 5")
        print("\nALUMNOS:")
        for row in cursor:
            print(f"  {row['id']:3} | {row['nombre']:15} {row['apellido']:15} | {row['telefono']}")
        
        cursor.execute("SELECT id, nombre, apellido, telefono FROM PROFESORES LIMIT 5")
        print("\nPROFESORES:")
        for row in cursor:
            print(f"  {row['id']:3} | {row['nombre']:15} {row['apellido']:15} | {row['telefono']}")
        
        print("-" * 80)
        
        cursor.close()
        cnx.close()
        
        total = socios_updated + alumnos_updated + profesores_updated
        print(f"\n✓ Migración completada exitosamente")
        print(f"Total ajustado: {total} teléfonos")
        print(f"Formato: 2920 + 6 dígitos (total 10 dígitos)")
        
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
    print("MIGRACIÓN: Ajustar teléfonos a formato 2920 + 6 dígitos")
    print("=" * 80)
    migrate()
