from db_config import get_db_connection

def test_connection():
    try:
        db = get_db_connection()
        print("Connected to MySQL database successfully!")
        db.close()
    except Exception as e:
        print(f"Failed to connect to MySQL database: {e}")

if __name__ == "__main__":
    test_connection()
