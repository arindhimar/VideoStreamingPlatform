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
            m3u8_url VARCHAR(255),  -- Path for the .m3u8 file
            ts_url_prefix VARCHAR(255),  -- Base path for .ts segments
            status ENUM('uploaded', 'processing', 'ready') DEFAULT 'uploaded',
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
            UNIQUE (anime_id, episode_number),  -- Ensure unique anime_id and episode_number
            FOREIGN KEY (anime_id) REFERENCES anime(anime_id)
        )
        """
        cur = self.conn.cursor()
        cur.execute(query)
        self.conn.commit()
        cur.close()

    def create_episode(self, anime_id, title, episode_number, m3u8_url="", ts_url_prefix="", status="processing"):
        cur = self.conn.cursor()
        try:
            # Insert new record or skip if it already exists
            cur.execute(
                "INSERT IGNORE INTO episodes (anime_id, title, episode_number, m3u8_url, ts_url_prefix, status) VALUES (%s, %s, %s, %s, %s, %s)",
                (anime_id, title, episode_number, m3u8_url, ts_url_prefix, status)
            )
            self.conn.commit()
        finally:
            cur.close()

    def update_episode_status(self, anime_id, episode_number, status, m3u8_url=None, ts_url_prefix=None):
        cur = self.conn.cursor()
        query = "UPDATE episodes SET status = %s"
        params = [status]
        
        if m3u8_url:
            query += ", m3u8_url = %s"
            params.append(m3u8_url)
        
        if ts_url_prefix:
            query += ", ts_url_prefix = %s"
            params.append(ts_url_prefix)

        # Ensure anime_id and episode_number are both used in the WHERE clause
        query += " WHERE anime_id = %s AND episode_number = %s"
        params.extend([anime_id, episode_number])

        cur.execute(query, params)
        self.conn.commit()
        cur.close()

    def delete_episode(self, episode_number):
        cur = self.conn.cursor()
        cur.execute("DELETE FROM episodes WHERE episode_number = %s", (episode_number,))
        self.conn.commit()
        cur.close()

    def get_episode(self, anime_id, episode_number):
        cur = self.conn.cursor(dictionary=True)  # Use dictionary cursor here
        cur.execute('SELECT * FROM episodes WHERE anime_id = %s AND episode_number = %s', (anime_id, episode_number))
        episode = cur.fetchone()
        cur.close()
        
        # Return the episode as a dictionary (if found)
        return episode

    def fetch_episodes_by_anime_id(self, anime_id):
        query = "SELECT * FROM episodes WHERE anime_id = %s"
        cur = self.conn.cursor(dictionary=True)  # Use dictionary cursor here
        cur.execute(query, (anime_id,))
        results = cur.fetchall()
        cur.close()
        return results
