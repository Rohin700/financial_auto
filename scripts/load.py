# /Library/Frameworks/Python.framework/Versions/3.13/bin/python3 i entered this path to sort the connector python issue

import mysql.connector
import pandas as pd

from dotenv import load_dotenv
import os

def load_to_mysql(df):
    try:
        # Connect to MySQL
        connection = mysql.connector.connect(
            host=os.getenv("DB_HOST"),
            user=os.getenv("DB_USER"),
            password=os.getenv("DB_PASSWORD"),
            database=os.getenv("DB_NAME")
        )
        cursor = connection.cursor()

        # Create table if it doesn't exist
        create_table = """
        CREATE TABLE IF NOT EXISTS sales_data (
            id INT AUTO_INCREMENT PRIMARY KEY,
            date DATE,
            product VARCHAR(255),
            category VARCHAR(255),
            quantity INT,
            price DECIMAL(10,2),
            revenue DECIMAL(10,2)
        );
        """
        cursor.execute(create_table)

        # Insert data row-by-row
        insert_query = """
        INSERT INTO sales_data
        (date, product, category, quantity, price, revenue)
        VALUES (%s, %s, %s, %s, %s, %s)
        """

        data_tuples = [tuple(x) for x in df[['date', 'product', 'category', 'quantity', 'price', 'revenue']].values]

        cursor.executemany(insert_query, data_tuples)
        connection.commit()

        print("Data successfully loaded into MySQL!")

    except mysql.connector.Error as e:
        print(f"MySQL Error: {e}")

    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()
            print("MySQL connection closed")


if __name__ == "__main__":
    df = pd.read_csv("../data/cleaned_sales.csv")
    load_to_mysql(df)