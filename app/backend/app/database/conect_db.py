import mysql.connector
import os
from dotenv import load_dotenv

load_dotenv()

class ConectDB:
    @staticmethod
    def get_connect():
        try:
            conn = mysql.connector.connect(
                user=os.getenv("DB_USER"),
                password=os.getenv("DB_PASSWORD"),
                database=os.getenv("DB_NAME"),
                host=os.getenv("DB_HOST", "localhost"),
                port=int(os.getenv("DB_PORT", 3306)),
                raise_on_warnings=True
            )
            return conn
        except Exception as exc:
            print(f"An exception occurred: {exc}")
            return None

    @staticmethod
    def read(sql: str, params: tuple = ()):
        cxn = ConectDB.get_connect()
        try:
            with cxn.cursor(dictionary=True) as cursor:
                cursor.execute(sql, params)
                result = cursor.fetchall()
                return result if result else False
        except Exception as exc:
            print(f"Error: {str(exc)}")
        finally:
            cxn.close()

    @staticmethod
    def write(sql: str, params=None):
        cxn = ConectDB.get_connect()
        try:
            with cxn.cursor(dictionary=True) as cursor:
                cursor.execute(sql, params or ())
                cxn.commit()
                if cursor.lastrowid:
                    result = cursor.lastrowid
                else:
                    result = cursor.rowcount
                return result
        except Exception as exc:
            print(f"Error: {str(exc)}")
        finally:
            cxn.close()