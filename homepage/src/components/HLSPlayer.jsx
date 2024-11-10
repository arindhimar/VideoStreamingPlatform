import React, { useRef, useEffect, useState } from 'react';
import ReactHlsPlayer from 'react-hls-player';

const VideoPlayer = React.memo(({ playerRef }) => {
    return (
        <ReactHlsPlayer
            playerRef={playerRef}
            src="15e76b2e-4e6b-45d6-bfa7-04ec6695f168/index.m3u8"
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

function HLSPlayer() {
    const playerRef = useRef();
    const [isPlaying, setIsPlaying] = useState(false);
    const [showFullDescription, setShowFullDescription] = useState(false); // Control for toggling full description

    // Set up event listeners to handle play and end events
    useEffect(() => {
        const handlePlay = () => console.log("Video started playing");
        const handleEnded = () => {
            console.log("Video ended");
            setIsPlaying(false);
        };

        if (playerRef.current) {
            playerRef.current.addEventListener('play', handlePlay);
            playerRef.current.addEventListener('ended', handleEnded);
        }

        // Cleanup event listeners on unmount
        return () => {
            if (playerRef.current) {
                playerRef.current.removeEventListener('play', handlePlay);
                playerRef.current.removeEventListener('ended', handleEnded);
            }
        };
    }, []);

    const handleToggleDescription = () => {
        setShowFullDescription(!showFullDescription);
    };

    return (
        <div className="player-container max-w-4xl mx-auto my-8 bg-[#0a1a2f] p-6 rounded-lg shadow-xl overflow-hidden">
            <div className="relative group">
                {/* Video Player - Memoized to prevent re-renders */}
                <VideoPlayer playerRef={playerRef} />
            </div>

            {/* Title and Description Below Player */}
            <div className="text-white mt-4">
                {/* Title */}
                <h2 className="text-3xl font-semibold mb-2 font-poppins">Sample Video Title</h2>

                {/* Description */}
                <div className="description-container">
                    <p className={`text-lg ${showFullDescription ? 'block' : 'line-clamp-3'} transition-all duration-300 font-poppins`}>
                        This is a sample video description. It provides a brief overview of the video content. The description should be engaging and informative for the viewers to understand the context of the video they are about to watch. 
                        <br />
                        <br />
                        This part is hidden when the description is collapsed. When you click "Show More," the full description will be displayed.
                    </p>

                    {/* Show More/Show Less Button */}
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
