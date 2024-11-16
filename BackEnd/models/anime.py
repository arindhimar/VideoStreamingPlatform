import mysql.connector

host = "localhost"
database = "animex"
user = "root"
password = "root"

class AnimeModel:
    def __init__(self):
        self.conn = self.get_db_connection()
        self.create_anime_table_if_not_exists()

    def get_db_connection(self):
        return mysql.connector.connect(
            host=host,
            database=database,
            user=user,
            password=password
        )

    def create_anime_table_if_not_exists(self):
        """Create the anime table if it does not already exist."""
        create_table_query = """
        CREATE TABLE IF NOT EXISTS anime (
            anime_id INT AUTO_INCREMENT PRIMARY KEY,
            title VARCHAR(255) NOT NULL,
            synopsis TEXT,
            release_date DATE,
            status ENUM('ongoing', 'completed') DEFAULT 'ongoing',
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
            thumbnail_url VARCHAR(255),
            banner_url VARCHAR(255)
        )
        """
        cur = self.conn.cursor()
        cur.execute(create_table_query)
        self.conn.commit()
        cur.close()

    def fetch_all_anime(self):
        cur = self.conn.cursor(dictionary=True)
        cur.execute("SELECT * FROM anime")
        anime_list = cur.fetchall()
        cur.close()
        return anime_list

    def fetch_anime_by_id(self, anime_id):
        cur = self.conn.cursor(dictionary=True)
        cur.execute("SELECT * FROM anime WHERE anime_id = %s", (anime_id,))
        anime = cur.fetchone()
        cur.close()
        return anime

    def create_anime(self, title, synopsis, release_date, status='ongoing', thumbnail_url=None, banner_url=None):
        cur = self.conn.cursor()
        cur.execute(
            """
            INSERT INTO anime (title, synopsis, release_date, status, thumbnail_url, banner_url)
            VALUES (%s, %s, %s, %s, %s, %s)
            """,
            (title, synopsis, release_date, status, thumbnail_url, banner_url)
        )
        self.conn.commit()
        cur.close()

    def update_anime(self, anime_id, title=None, synopsis=None, release_date=None, status=None, thumbnail_url=None, banner_url=None):
        cur = self.conn.cursor()
        update_fields = []
        values = []
        if title:
            update_fields.append("title = %s")
            values.append(title)
        if synopsis:
            update_fields.append("synopsis = %s")
            values.append(synopsis)
        if release_date:
            update_fields.append("release_date = %s")
            values.append(release_date)
        if status:
            update_fields.append("status = %s")
            values.append(status)
        if thumbnail_url:
            update_fields.append("thumbnail_url = %s")
            values.append(thumbnail_url)
        if banner_url:
            update_fields.append("banner_url = %s")
            values.append(banner_url)

        values.append(anime_id)
        update_query = f"UPDATE anime SET {', '.join(update_fields)}, updated_at = CURRENT_TIMESTAMP WHERE anime_id = %s"
        cur.execute(update_query, tuple(values))
        self.conn.commit()
        cur.close()

    def delete_anime(self, anime_id):
        cur = self.conn.cursor()
        cur.execute("DELETE FROM anime WHERE anime_id = %s", (anime_id,))
        self.conn.commit()
        cur.close()

    def close_connection(self):
        self.conn.close()
