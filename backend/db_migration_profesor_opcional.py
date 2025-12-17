#!/usr/bin/env python3
"""
Script de migración para hacer profesor_id opcional en tablas SOCIOS y ALUMNOS
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
        
        # Modificar tabla SOCIOS
        print("\n1. Modificando tabla SOCIOS...")
        try:
            # Primero eliminar la foreign key existente
            cursor.execute("""
                SELECT CONSTRAINT_NAME 
                FROM INFORMATION_SCHEMA.KEY_COLUMN_USAGE 
                WHERE TABLE_SCHEMA = %s 
                AND TABLE_NAME = 'SOCIOS' 
                AND COLUMN_NAME = 'profesor_id'
                AND REFERENCED_TABLE_NAME IS NOT NULL
            """, (config['database'],))
            
            fk_result = cursor.fetchone()
            if fk_result:
                fk_name = fk_result[0]
                print(f"   Eliminando constraint existente: {fk_name}")
                cursor.execute(f"ALTER TABLE SOCIOS DROP FOREIGN KEY {fk_name}")
            
            # Modificar la columna para permitir NULL
            cursor.execute("""
                ALTER TABLE SOCIOS 
                MODIFY COLUMN profesor_id int DEFAULT NULL
            """)
            
            # Agregar la foreign key con ON DELETE SET NULL
            cursor.execute("""
                ALTER TABLE SOCIOS 
                ADD CONSTRAINT fk_socios_profesor 
                FOREIGN KEY (profesor_id) REFERENCES PROFESORES(id) ON DELETE SET NULL
            """)
            
            cnx.commit()
            print("   ✓ Tabla SOCIOS actualizada exitosamente")
        except mysql.connector.Error as err:
            if "duplicate" in str(err).lower():
                print("   ✓ La tabla SOCIOS ya tiene la configuración correcta")
            else:
                raise
        
        # Modificar tabla ALUMNOS
        print("\n2. Modificando tabla ALUMNOS...")
        try:
            # Primero eliminar la foreign key existente
            cursor.execute("""
                SELECT CONSTRAINT_NAME 
                FROM INFORMATION_SCHEMA.KEY_COLUMN_USAGE 
                WHERE TABLE_SCHEMA = %s 
                AND TABLE_NAME = 'ALUMNOS' 
                AND COLUMN_NAME = 'profesor_id'
                AND REFERENCED_TABLE_NAME IS NOT NULL
            """, (config['database'],))
            
            fk_result = cursor.fetchone()
            if fk_result:
                fk_name = fk_result[0]
                print(f"   Eliminando constraint existente: {fk_name}")
                cursor.execute(f"ALTER TABLE ALUMNOS DROP FOREIGN KEY {fk_name}")
            
            # Modificar la columna para permitir NULL
            cursor.execute("""
                ALTER TABLE ALUMNOS 
                MODIFY COLUMN profesor_id int DEFAULT NULL
            """)
            
            # Agregar la foreign key con ON DELETE SET NULL
            cursor.execute("""
                ALTER TABLE ALUMNOS 
                ADD CONSTRAINT fk_alumnos_profesor 
                FOREIGN KEY (profesor_id) REFERENCES PROFESORES(id) ON DELETE SET NULL
            """)
            
            cnx.commit()
            print("   ✓ Tabla ALUMNOS actualizada exitosamente")
        except mysql.connector.Error as err:
            if "duplicate" in str(err).lower():
                print("   ✓ La tabla ALUMNOS ya tiene la configuración correcta")
            else:
                raise
        
        # Mostrar estructura actualizada de SOCIOS
        print("\n" + "="*80)
        cursor.execute("DESCRIBE SOCIOS")
        print("Estructura actualizada de la tabla SOCIOS:")
        print("-" * 80)
        for (field, type, null, key, default, extra) in cursor:
            print(f"{field:20} {type:20} {null:10} {key:10} {str(default):15} {extra}")
        print("-" * 80)
        
        # Mostrar estructura actualizada de ALUMNOS
        print("\n" + "="*80)
        cursor.execute("DESCRIBE ALUMNOS")
        print("Estructura actualizada de la tabla ALUMNOS:")
        print("-" * 80)
        for (field, type, null, key, default, extra) in cursor:
            print(f"{field:20} {type:20} {null:10} {key:10} {str(default):15} {extra}")
        print("-" * 80)
        
        cursor.close()
        cnx.close()
        print("\n✓ Migración completada exitosamente")
        print("Ahora profesor_id es opcional en SOCIOS y ALUMNOS")
        
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
    print("MIGRACIÓN: Hacer profesor_id opcional en SOCIOS y ALUMNOS")
    print("=" * 80)
    migrate()
