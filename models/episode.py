import mysql.connector


class EpisodeModel:
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
        CREATE TABLE IF NOT EXISTS episodes (
            episode_id INT PRIMARY KEY AUTO_INCREMENT,
            anime_id INT,
            title VARCHAR(100),
            episode_number INT,
            video_url VARCHAR(255),
            FOREIGN KEY (anime_id) REFERENCES anime(anime_id)
        )
        """
        cur = self.conn.cursor()
        cur.execute(query)
        self.conn.commit()
        cur.close()

    def create_episode(self, anime_id, title, episode_number, video_url):
        cur = self.conn.cursor()
        cur.execute(
            "INSERT INTO episodes (anime_id, title, episode_number, video_url) VALUES (%s, %s, %s, %s)",
            (anime_id, title, episode_number, video_url)
        )
        self.conn.commit()
        cur.close()
