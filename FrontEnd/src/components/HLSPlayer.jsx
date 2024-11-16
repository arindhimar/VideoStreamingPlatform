import React, { useRef, useEffect, useState } from 'react';
import ReactHlsPlayer from 'react-hls-player';

const VideoPlayer = React.memo(({ playerRef, src }) => {
    return (
        <ReactHlsPlayer
            playerRef={playerRef}
            src={src}
            autoPlay={false}
            controls={true}
            width="100%"
            height="auto"
            hlsConfig={{
                lowLatencyMode: true,
                enableWorker: false,
            }}
            className="rounded-lg"
        />
    );
});

function HLSPlayer({ animeId, episodeNumber, variant = 0 }) {
    const playerRef = useRef();
    const [isPlaying, setIsPlaying] = useState(false);
    const [showFullDescription, setShowFullDescription] = useState(false);
    const [audioTrack, setAudioTrack] = useState(0); // Audio track state
    const [subtitle, setSubtitle] = useState(0); // Subtitle state
    const [title, setTitle] = useState(''); // Title state
    const [description, setDescription] = useState(''); // Description state

    const videoSrc = `http://localhost:5000/episodes/stream/${animeId}/${episodeNumber}/${audioTrack}`;
    // console.log(animeId,episodeNumber)
    // Fetch episode details
    useEffect(() => {
        const fetchEpisodeDetails = async () => {
            try {
                const response = await fetch(`http://127.0.0.1:5000/episodes/anime/${animeId}/${episodeNumber}`);
                if (response.ok) {
                    const data = await response.json();
                    // console.log(data)

                    setTitle(data.title || 'Untitled Episode');
                    setDescription(`${data.anime_title}: ${data.synopsis}` || 'No description available.');
                } else {
                    console.error('Failed to fetch episode details');
                }
            } catch (error) {
                console.error('Error fetching episode details:', error);
            }
        };

        fetchEpisodeDetails();
    }, [animeId, episodeNumber]);

    useEffect(() => {
        const fetchEpisodeDetails = async () => {
            // Clear previous title and description immediately to avoid stale values
            setTitle('');
            setDescription('');

            try {
                const response = await fetch(`http://127.0.0.1:5000/episodes/anime/${animeId}/${episodeNumber}`);
                if (response.ok) {
                    const data = await response.json();

                    // Update the title and description when new data is fetched
                    setTitle(data.title || 'Untitled Episode');
                    setDescription(`${data.anime_title}: ${data.synopsis}` || 'No description available.');
                } else {
                    console.error('Failed to fetch episode details');
                }
            } catch (error) {
                console.error('Error fetching episode details:', error);
            }
        };

        fetchEpisodeDetails();
    }, [animeId, episodeNumber]);

    const handleToggleDescription = () => {
        setShowFullDescription(!showFullDescription);
    };

    const handleAudioChange = (e) => {
        setAudioTrack(e.target.value);
    };

    const handleSubtitleChange = (e) => {
        setSubtitle(e.target.value);
    };

    return (
        <div className="player-container max-w-4xl mx-auto my-8 bg-[#0a1a2f] p-6 rounded-lg shadow-xl overflow-hidden text-[#f8d7da]">
            <div className="relative group">
                <VideoPlayer playerRef={playerRef} src={videoSrc} />
            </div>

            <div className="mt-4">
                <h2 className="text-3xl font-semibold mb-2 font-poppins text-[#f8d7da]">{title}</h2>

                <div className="flex gap-4 mb-4">
                    <div>
                        <label htmlFor="audioTrack" className="text-white">Select Audio:</label>
                        <select
                            id="audioTrack"
                            value={audioTrack}
                            onChange={handleAudioChange}
                            className="ml-2 p-2 bg-[#0a1a2f] text-[#f8d7da] border border-gray-700 rounded"
                        >
                            <option value="0">Japanese</option>
                            <option value="1" selected>English</option>
                        </select>
                    </div>

                    <div>
                        <label htmlFor="captions" className="text-white">Subtitles:</label>
                        <select
                            id="captions"
                            value={subtitle}
                            onChange={handleSubtitleChange}
                            className="ml-2 p-2 bg-[#0a1a2f] text-[#f8d7da] border border-gray-700 rounded"
                        >
                            <option value="0" selected disabled>Future Implementation</option>
                        </select>
                    </div>
                </div>

                <div className="description-container">
                    <p className={`text-lg ${showFullDescription ? 'block' : 'line-clamp-3'} transition-all duration-300 font-poppins`}>
                        {description}
                    </p>

                    <button
                        onClick={handleToggleDescription}
                        className="text-blue-400 mt-2 hover:underline focus:outline-none font-poppins">
                        {showFullDescription ? "Show Less" : "Show More"}
                    </button>
                </div>
            </div>
        </div>
    );
}

export default HLSPlayer;
