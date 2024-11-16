# ANIMEX - Anime Streaming Platform

![ANIMEX Logo](https://i.ibb.co/k0r9TFC/Logo-No-Backgroud.png)

ANIMEX is an anime streaming platform designed to manage and stream anime content effectively. This web application allows users to upload, manage, and stream anime episodes seamlessly, making it easy for both administrators and viewers to enjoy their favorite shows.

## Features

- **Anime Management**:
  - Full CRUD operations for anime records:
    - Titles
    - Synopses
    - Release dates
    - Thumbnails and banners (via automatic ImgBB uploads)

- **Episode Management**:
  - Upload episodes in multiple video formats
  - Background processing for video conversion and segmentation using FFmpeg
  - Streaming via HLS (HTTP Live Streaming) for smooth playback

- **Genre Management**:
  - Create, update, and delete genres for better content categorization

- **Image Uploads**:
  - Automatically upload and manage anime thumbnails and banners to ImgBB for image hosting

- **Background Processing**:
  - Use of `concurrent.futures` for handling background tasks, such as video processing and segmenting large video files

- **Streaming**:
  - Serve video segments via HLS playlists for seamless anime viewing experiences

## Technologies Used

- **Flask**: A micro web framework in Python that provides the backbone for the application's backend.
- **SQLite/MySQL**: Database systems for storing anime, episode, and genre records.
- **FFmpeg**: A powerful multimedia framework for video encoding and processing, utilized for video file segmenting.
- **ImgBB API**: A third-party API to upload images and store them remotely.
- **dotenv**: Securely manage environment variables for sensitive data like API keys.
- **requests**: For handling HTTP requests, such as uploading images and interacting with external APIs.
- **uuid**: For generating unique identifiers for episodes.
- **concurrent.futures**: To handle background tasks and manage threading for long-running tasks like video processing.

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




