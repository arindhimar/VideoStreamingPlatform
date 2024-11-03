# ANIMEX - Anime Streaming Platform

![ANIMEX Logo](https://github.com/arindhimar/VideoStreamingPlatform/blob/ANIMEX/static/images/Logo-NoBackgroud.png)

ANIMEX is an anime streaming platform designed to manage and stream anime content effectively. This web application allows users to upload, manage, and stream anime episodes seamlessly, making it easy for both administrators and viewers to enjoy their favorite shows.

## Features

- **Anime Management**:
  - Create, read, update, and delete anime records, including:
    - Titles
    - Synopses
    - Release dates
- **Episode Management**:
  - Upload episodes in various video formats
  - Process them for streaming and manage episode details
- **Genre Management**:
  - Add, update, and delete genres for organizing anime content
- **Image Uploads**:
  - Automatically upload anime thumbnails and banners to ImgBB
- **Background Processing**:
  - Utilize background tasks for video processing with FFmpeg
- **Streaming**:
  - Serve video segments and HLS playlists for smooth streaming experiences

## Technologies Used

- **Flask**: A micro web framework for Python, providing the backend structure for our application.
- **SQLite/MySQL**: Database management system for storing anime and episode records.
- **FFmpeg**: A powerful multimedia framework for processing video and audio files.
- **ImgBB API**: Used for uploading images and retrieving URLs.
- **dotenv**: To manage environment variables and sensitive information securely.

## Libraries

- `Flask`: For creating web applications.
- `requests`: For making HTTP requests, such as uploading images to ImgBB.
- `python-dotenv`: For loading environment variables from a `.env` file.
- `uuid`: To generate unique identifiers for episodes.
- `concurrent.futures`: For managing background tasks and threading.
- `subprocess`: To run FFmpeg commands for video processing.
- `os`: For interacting with the operating system.

## Endpoints

### Anime Endpoints

- `GET /anime/`: Retrieve all anime records.
- `GET /anime/<anime_id>/`: Retrieve a specific anime record by ID.
- `POST /anime/`: Create a new anime record (supports thumbnail and banner uploads).
- `PUT /anime/<anime_id>/`: Update an existing anime record.
- `DELETE /anime/<anime_id>/`: Delete an anime record by ID.

### Episode Endpoints

- `GET /anime/<anime_id>/episodes`: Retrieve all episodes for a specific anime by its ID.
- `POST /episodes/upload`: Upload a new episode video.
- `GET /stream/<anime_id>/<episode_number>/index.m3u8`: Stream the HLS playlist for an episode.
- `GET /stream/<anime_id>/<episode_number>/segment<filename>`: Stream a specific video segment.

### Genre Endpoints

- `GET /genres/`: Retrieve all genres.
- `GET /genres/<genre_id>/`: Retrieve a specific genre by ID.
- `POST /genres/`: Create a new genre.
- `PUT /genres/<genre_id>/`: Update an existing genre.
- `DELETE /genres/<genre_id>/`: Delete a genre by ID.

### Anime Endpoints

- `GET /anime/`: Retrieve all anime records.
  
  **Example Response:**
  ```json
  [
    {
      "id": 1,
      "title": "Attack on Titan",
      "synopsis": "Humans vs Titans",
      "release_date": "2013-04-07"
    },
    {
      "id": 2,
      "title": "My Hero Academia",
      "synopsis": "Heroes in Training",
      "release_date": "2016-04-03"
    }
    ...
  ]

## Getting Started

To get started with ANIMEX, follow these steps:

1. Clone the repository:
   ```bash
   git clone "https://github.com/arindhimar/VideoStreamingPlatform/"
   cd animex

2. Install the required packages:
   ```bash
    pip install -r requirements.txt

3. Set up your environment variables in a .env file. You can use the example .env.example file provided in the repository as a reference.

4. Run the application:
    ```bash
    python app.py
5. Open your web browser and navigate to http://127.0.0.1:5000/ to access the ANIMEX platform




