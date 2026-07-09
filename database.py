import os
import mysql.connector


def get_connection():

    if os.getenv("DB_HOST"):

        return mysql.connector.connect(
            host=os.getenv("DB_HOST"),
            port=int(os.getenv("DB_PORT")),
            user=os.getenv("DB_USER"),
            password=os.getenv("DB_PASSWORD"),
            database=os.getenv("DB_NAME")
        )

    else:

        return mysql.connector.connect(
            host="localhost",
            user="root",
            password="",
            database="job_portal"
        )