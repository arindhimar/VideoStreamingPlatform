import mysql.connector

class UserModel:
    def __init__(self):
        self.conn = self.get_db_connection()
        self.create_table()

    def get_db_connection(self):
        return mysql.connector.connect(
            host="localhost",
            database="animex",
            user="root",
            password="root"
        )

    def create_table(self):
        query = """
        CREATE TABLE IF NOT EXISTS users (
            user_id INT PRIMARY KEY AUTO_INCREMENT,
            username VARCHAR(50) UNIQUE NOT NULL,
            password VARCHAR(100) NOT NULL,
            email VARCHAR(100) UNIQUE NOT NULL
        )
        """
        cur = self.conn.cursor()
        cur.execute(query)
        self.conn.commit()
        cur.close()

    def create_user(self, username, password, email):
        cur = self.conn.cursor()
        cur.execute("INSERT INTO users (username, password, email) VALUES (%s, %s, %s)", (username, password, email))
        self.conn.commit()
        cur.close()

    def fetch_all_users(self):
        cur = self.conn.cursor(dictionary=True)
        cur.execute("SELECT * FROM users")
        users = cur.fetchall()
        cur.close()
        return users

    def fetch_user_by_id(self, user_id):
        cur = self.conn.cursor(dictionary=True)
        cur.execute("SELECT * FROM users WHERE user_id = %s", (user_id,))
        user = cur.fetchone()
        cur.close()
        return user

    def close_connection(self):
        self.conn.close()
