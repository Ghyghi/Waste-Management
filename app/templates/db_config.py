import MySQLdb

def get_db_connection():
    try:
        connection = MySQLdb.connect(
            host="localhost",
            user="root",
            passwd="",
            db="Smart_Waste"
        )
        return connection
    except MySQLdb.Error as e:
        print(f"Error connecting to MySQL: {e}")
        return None
