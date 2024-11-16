import mysql.connector
from mysql.connector import pooling

class EpisodeModel:
    def __init__(self):
        self.pool = self.create_pool()  # Create a connection pool
        self.conn = self.pool.get_connection()  # Get an initial connection from the pool
        self.create_table()

    def create_pool(self):
        """
        Create a connection pool to handle multiple MySQL connections efficiently.
        """
        return mysql.connector.pooling.MySQLConnectionPool(
            pool_name="mypool",
            pool_size=32,  # Adjust the pool size according to your needs
            host="localhost",
            database="animex",
            user="root",
            password="root"
        )

    def get_db_connection(self):
        """
        Ensure the connection is valid and re-establish it if needed.
        """
        if not self.conn.is_connected():
            print("Reconnecting to the database...")
            self.conn = self.pool.get_connection()  # Get a fresh connection from the pool
        return self.conn

    def create_table(self):
        """
        Create the 'episodes' table if it doesn't exist already.
        """
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
        """
        Create a new episode record or skip if it already exists.
        """
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
        """
        Update the status of an existing episode and optionally the URLs.
        """
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

    def delete_episode(self, anime_id, episode_number):
        """
        Delete an episode by its anime_id and episode_number.
        """
        cur = self.conn.cursor()
        cur.execute("DELETE FROM episodes WHERE episode_number = %s and anime_id=%s", (episode_number, anime_id))
        self.conn.commit()
        cur.close()

    def get_episode(self, anime_id, episode_number):
        """
        Fetch an episode by anime_id and episode_number.
        """
        # Ensure the connection is available
        self.conn = self.get_db_connection()
        if not self.conn:
            print("MySQL connection not available.")
            return None

        cur = self.conn.cursor(dictionary=True)  # Use dictionary cursor here
        cur.execute('SELECT * FROM episodes WHERE anime_id = %s AND episode_number = %s', (anime_id, episode_number))
        episode = cur.fetchone()
        cur.close()

        return episode
    
    
    def fetch_episodes_by_anime_id(self, anime_id):
        """
        Fetch all episodes for a specific anime_id.
        """
        query = """
        SELECT e.*, a.thumbnail_url
        FROM episodes e
        JOIN anime a ON e.anime_id = a.anime_id
        WHERE e.anime_id = %s
        """
        cur = self.conn.cursor(dictionary=True)  
        cur.execute(query, (anime_id,))
        results = cur.fetchall() 
        cur.close()
        return results
    
    def fetch_latest_episodes(self, limit=5):
        """
        Fetch the latest episodes globally, ordered by the created_at timestamp.

        Args:
        limit (int): The number of latest episodes to fetch.

        Returns:
        List of dictionaries representing the latest episodes.
        """
        query = """
            SELECT e.*, a.thumbnail_url,a.anime_id
            FROM episodes e
            JOIN anime a ON e.anime_id = a.anime_id
            ORDER BY e.created_at DESC
            LIMIT %s;
        """
        cursor = self.conn.cursor(dictionary=True)  # Use self.conn for the database connection
        cursor.execute(query, (limit,))  # Pass the limit parameter for the query
        episodes = cursor.fetchall()
        return episodes
    
    def fetch_episode_details(self, anime_id, episode_number):
        """
        Fetch details for a specific episode of a given anime.
        """
        query = """
        SELECT e.*, a.synopsis, a.title AS anime_title
        FROM episodes e
        JOIN anime a ON e.anime_id = a.anime_id
        WHERE e.anime_id = %s AND e.episode_number = %s
        """
        
        self.conn = self.get_db_connection()
        cur = self.conn.cursor(dictionary=True)
        
        try:
            cur.execute(query, (anime_id, episode_number))
            result = cur.fetchone()  
        finally:
            cur.close()  

        return result
