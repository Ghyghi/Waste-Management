import MySQLdb

def get_db_connection():
    return MySQLdb.connect(
        host="localhost",
        user="root",
        passwd="", 
        db="Smart_Waste",
        cursorclass=MySQLdb.cursors.DictCursor
    )
