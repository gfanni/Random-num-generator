from mysql.connector import connect, Error
from getpass import getpass
from utility import random_generator


class Database:
    def __init__(self, db_name):
        try:
            self.connection = connect(
                host="localhost",
                user=input("Enter username: "),
                password=getpass("Enter password: "),
                database=db_name,
            )
        except Error as e:
            print(e)

    def create_table(self, tbl_name):
        cursor = self.connection.cursor()
        cursor.execute("CREATE TABLE IF NOT EXISTS " + tbl_name + """(id INT AUTO_INCREMENT PRIMARY KEY, rand_num INT,
                                                                      date DATETIME)""")
        self.connection.commit()

    # insert generated random numbers into a given database
    def insert_random_numbers(self, tbl_name):
        insert_query = """
                    INSERT INTO """ + tbl_name + """(rand_num, date) VALUES (%s, %s)
                    """
        random = random_generator()
        cursor = self.connection.cursor()
        cursor.executemany(insert_query, random)
        self.connection.commit()
        for row in cursor.fetchall():
            print(row)

    # calculate avg using python
    def calculate_mean(self, tbl_name, last_elements=3):
        summary = 0
        insert_query = """
                        SELECT rand_num FROM (SELECT id, rand_num FROM """ + tbl_name + """ ORDER BY id DESC LIMIT """ \
                       + str(last_elements) + """) query ORDER BY id ASC"""
        cursor = self.connection.cursor()
        cursor.execute(insert_query)
        for row in cursor.fetchall():
            row = int(row[0])
            summary += row
            print(row)
        print(summary / last_elements)  # the mean of the last x elements

    # calculate avg using sql query
    def calculate_avg(self, tbl_name, last_elements=3):
        insert_query = """
                 SELECT AVG(rand_num) AS average FROM (SELECT id, rand_num FROM """ + tbl_name + """ 
                 ORDER BY id DESC LIMIT """ + str(last_elements) + """) AS query"""
        cursor = self.connection.cursor()
        cursor.execute(insert_query)
        for row in cursor.fetchall():
            row = float(row[0])
            print(row)  # the mean of the last x elements


db = Database("random_numbers_db")
db.create_table("random_table")
db.insert_random_numbers("random_table")
db.calculate_mean("random_table")
db.calculate_avg("random_table")


# useful queries:
# DELETE FROM random_numbers WHERE id <= 310;
# SELECT * FROM random_numbers;
# ALTER TABLE random_numbers AUTO_INCREMENT = 0;
# ALTER TABLE random_numbers ADD date DATETIME AFTER rand_num; add new column "date"

# connect mySQL
# alias mysql=/usr/local/mysql/bin/mysql
# mysql --user=root -p

