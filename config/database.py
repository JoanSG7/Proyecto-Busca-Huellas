import os
from contextlib import contextmanager

import mysql.connector
from mysql.connector import Error


DB_CONFIG = {
    "host": os.getenv("DB_HOST", "localhost"),
    "port": int(os.getenv("DB_PORT", "3306")),
    "user": os.getenv("DB_USER", "root"),
    "password": os.getenv("DB_PASSWORD", ""),
    "database": os.getenv("DB_NAME", "busca_huellas"),
    "charset": "utf8mb4",
    "collation": "utf8mb4_general_ci",
}


def get_connection():
    try:
        return mysql.connector.connect(**DB_CONFIG)
    except Error as exc:
        raise RuntimeError("No se pudo conectar con la base de datos.") from exc


@contextmanager
def db_cursor(commit=False):
    connection = get_connection()
    cursor = connection.cursor(dictionary=True)
    try:
        yield cursor
        if commit:
            connection.commit()
    except Exception:
        if commit:
            connection.rollback()
        raise
    finally:
        cursor.close()
        connection.close()
