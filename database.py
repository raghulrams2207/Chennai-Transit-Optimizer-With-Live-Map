import os
import mysql.connector
from mysql.connector import Error
from dotenv import load_dotenv

load_dotenv()


def get_connection():
    try:
        connection = mysql.connector.connect(
            host=os.getenv("DB_HOST", "localhost"),
            port=int(os.getenv("DB_PORT", 3306)),
            user=os.getenv("DB_USER", "root"),
            password=os.getenv("DB_PASSWORD"),
            database=os.getenv("DB_NAME", "transit_optimizer")
        )

        if connection.is_connected():
            return connection

    except Error as e:
        print("MySQL connection error:", e)

    return None


if __name__ == "__main__":
    connection = get_connection()

    if connection:
        print("✅ MySQL connection successful!")
        connection.close()
    else:
        print("❌ MySQL connection failed!")