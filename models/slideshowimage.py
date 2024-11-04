import mysql.connector

host = "localhost"
database = "animex"
user = "root"
password = "root"

class SlideshowImageModel:
    def __init__(self):
        self.conn = self.get_db_connection()
        self.create_slideshow_images_table_if_not_exists()

    def get_db_connection(self):
        """Establish a database connection."""
        return mysql.connector.connect(
            host=host,
            database=database,
            user=user,
            password=password
        )

    def create_slideshow_images_table_if_not_exists(self):
        """Create the slideshow_images table if it does not already exist."""
        create_table_query = """
        CREATE TABLE IF NOT EXISTS slideshow_images (
            image_id INT AUTO_INCREMENT PRIMARY KEY,
            image_url VARCHAR(255) NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
        )
        """
        cur = self.conn.cursor()
        cur.execute(create_table_query)
        self.conn.commit()
        cur.close()

    def fetch_all_images(self):
        """Retrieve all images in the slideshow."""
        cur = self.conn.cursor(dictionary=True)
        cur.execute("SELECT image_id, image_url FROM slideshow_images")
        images = cur.fetchall()
        cur.close()
        return images

    def fetch_image_by_id(self, image_id):
        """Retrieve a single image by its ID."""
        cur = self.conn.cursor(dictionary=True)
        cur.execute("SELECT image_id, image_url FROM slideshow_images WHERE image_id = %s", (image_id,))
        image = cur.fetchone()
        cur.close()
        return image

    def create_image(self, image_url):
        """Add a new image to the slideshow."""
        cur = self.conn.cursor()
        cur.execute(
            """
            INSERT INTO slideshow_images (image_url)
            VALUES (%s)
            """,
            (image_url,)
        )
        self.conn.commit()
        cur.close()

    def update_image(self, image_id, image_url):
        """Update an existing image's URL."""
        cur = self.conn.cursor()
        cur.execute(
            """
            UPDATE slideshow_images
            SET image_url = %s, updated_at = CURRENT_TIMESTAMP
            WHERE image_id = %s
            """,
            (image_url, image_id)
        )
        self.conn.commit()
        cur.close()

    def delete_image(self, image_id):
        """Delete an image from the slideshow by its ID."""
        cur = self.conn.cursor()
        cur.execute("DELETE FROM slideshow_images WHERE image_id = %s", (image_id,))
        self.conn.commit()
        cur.close()

    def close_connection(self):
        """Close the database connection."""
        self.conn.close()
