def test_connection():
    try:
        print("Connected to MySQL database successfully!")
        db.close()
    except Exception as e:
        print(f"Failed to connect to MySQL database: {e}")

if __name__ == "__main__":
    test_connection()
