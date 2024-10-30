import mysql.connector


class GenreModel:
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
        CREATE TABLE IF NOT EXISTS genres (
            genre_id INT PRIMARY KEY AUTO_INCREMENT,
            name VARCHAR(50) UNIQUE NOT NULL
        )
        """
        cur = self.conn.cursor()
        cur.execute(query)
        self.conn.commit()
        cur.close()

    def create_genre(self, name):
        cur = self.conn.cursor()
        cur.execute("INSERT INTO genres (name) VALUES (%s)", (name,))
        self.conn.commit()
        cur.close()

    def fetch_all_genres(self):
        """Fetch all genres from the database."""
        cur = self.conn.cursor(dictionary=True)
        cur.execute("SELECT * FROM genres")
        genres = cur.fetchall()
        cur.close()
        return genres

    def fetch_genre_by_id(self, genre_id):
        """Fetch a genre by its ID."""
        cur = self.conn.cursor(dictionary=True)
        cur.execute("SELECT * FROM genres WHERE genre_id = %s", (genre_id,))
        genre = cur.fetchone()
        cur.close()
        return genre