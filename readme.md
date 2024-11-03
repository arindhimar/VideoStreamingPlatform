    # ANIMEX - Anime Streaming Platform

    ANIMEX is an anime streaming platform designed to manage and stream anime content effectively. This web application allows users to upload, manage, and stream anime episodes seamlessly, making it easy for both administrators and viewers to enjoy their favorite shows.

    ## Features

    - **Anime Management**: Create, read, update, and delete anime records, including titles, synopses, release dates, and more.
    - **Episode Management**: Upload episodes in various video formats, process them for streaming, and manage episode details.
    - **Genre Management**: Add, update, and delete genres for organizing anime content.
    - **Image Uploads**: Automatically upload anime thumbnails and banners to ImgBB.
    - **Background Processing**: Utilize background tasks for video processing with FFmpeg.
    - **Streaming**: Serve video segments and HLS playlists for smooth streaming experiences.

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

    ## Getting Started

    1. Clone the repository:
    ```bash
    git clone "https://github.com/arindhimar/VideoStreamingPlatform/"
    cd animex
