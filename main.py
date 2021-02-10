import random
import math
from mysql.connector import connect, Error
from getpass import getpass
from datetime import datetime


# create the empty database
def create_database():
    try:
        with connect(
                host="localhost",
                user=input("Enter username: "),
                password=getpass("Enter password: "),
        ) as connection:
            create_db_query = "CREATE DATABASE random_numbers_db"
            with connection.cursor() as cursor:
                cursor.execute(create_db_query)
    except Error as e:
        print(e)


# generate random numbers in the right format
def random_generator():
    rand_list_to_convert = []  # we use this to convert the random number to tuple (int -> list -> tuple)
    rand_list_of_tuples = []  # list of tuples is the accepted format
    for num in range(0, 100):
        rand = math.floor(random.random()*10000)
        rand_list_to_convert.append(rand)
        now = datetime.now()
        formatted_date = now.strftime('%Y-%m-%d %H:%M:%S')
        rand_list_to_convert.append(formatted_date)
        rand_tuple = tuple(rand_list_to_convert)
        rand_list_of_tuples.append(rand_tuple)
        rand_list_to_convert = []
    print(rand_list_of_tuples)
    return rand_list_of_tuples


# insert generated random numbers into a given database
def insert_random_numbers(db="random_numbers_db"):
    try:
        with connect(
            host="localhost",
            user=input("Enter username: "),
            password=getpass("Enter password: "),
            database=db,
        ) as connection:
            insert_query = """
            INSERT INTO random_numbers (rand_num, date) VALUES (%s, %s)
            """
            records = random_generator()
            with connection.cursor() as cursor:
                cursor.executemany(insert_query, records)
                connection.commit()
                for row in cursor.fetchall():
                    print(row)
    except Error as e:
        print(e)


# calculate avg using python
def calculate_mean(last_elements=3):
    summary = 0
    try:
        with connect(
            host="localhost",
            user=input("Enter username: "),
            password=getpass("Enter password: "),
            database="random_numbers_db",
        ) as connection:
            insert_query = """
            SELECT rand_num FROM (SELECT id, rand_num FROM random_numbers ORDER BY id DESC LIMIT """ + str(last_elements) + """) query ORDER BY id ASC"""
            with connection.cursor() as cursor:
                cursor.execute(insert_query)
                for row in cursor.fetchall():
                    row = int(row[0])
                    summary += row
                    print(row)
                print(summary/last_elements) # the mean of the last x elements
    except Error as e:
        print(e)


# calculate avg using sql query
def calculate_avg(last_elements=3):
    try:
        with connect(
            host="localhost",
            user=input("Enter username: "),
            password=getpass("Enter password: "),
            database="random_numbers_db",
        ) as connection:
            insert_query = """
            SELECT AVG(rand_num) AS average FROM (SELECT id, rand_num FROM random_numbers ORDER BY id DESC LIMIT """ + str(last_elements) + """) AS query"""
            with connection.cursor() as cursor:
                cursor.execute(insert_query)
                for row in cursor.fetchall():
                    row = float(row[0])
                    print(row)  # the mean of the last x elements
    except Error as e:
        print(e)


# create_database()
# insert_random_numbers()
calculate_mean()
calculate_avg()


# useful queries:
# DELETE FROM random_numbers WHERE id <= 310;
# SELECT * FROM random_numbers;
# ALTER TABLE random_numbers AUTO_INCREMENT = 0;
# ALTER TABLE random_numbers ADD date DATETIME AFTER rand_num; add new column "date"
