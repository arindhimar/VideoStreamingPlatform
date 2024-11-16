import React, { useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";

const VerticalScrollCard = ({ animeId, episodeNumber }) => {
    const [episodes, setEpisodes] = useState([]);
    const [loading, setLoading] = useState(true);
    const navigate = useNavigate();

    useEffect(() => {
        const fetchEpisodes = async () => {
            setLoading(true); // Start loading every time we change episodes
            try {
                const response = await fetch(`http://127.0.0.1:5000/episodes/anime/${animeId}`);
                if (!response.ok) {
                    throw new Error("Failed to fetch episodes");
                }
                const allEpisodes = await response.json();

                // Filter out the current episode using the passed episodeNumber
                const filteredEpisodes = allEpisodes.filter(
                    (episode) => episode.episode_number != episodeNumber
                );

                setEpisodes(filteredEpisodes);
            } catch (error) {
                console.error("Error fetching episodes:", error);
            } finally {
                setLoading(false); // End loading once data is fetched
            }
        };

        // Fetch episodes when animeId or episodeNumber changes
        fetchEpisodes();
    }, [animeId, episodeNumber]); // Re-run the effect whenever animeId or episodeNumber changes

    if (loading) {
        return <p className="text-center text-white">Loading episodes...</p>;
    }

    if (episodes.length === 0) {
        return (
            <p className="text-center text-white">
                No other episodes available.
            </p>
        );
    }

    return (
        <div className="w-full mt-10 px-4 max-h-screen overflow-y-auto scrollbar-hide">
            {/* Vertical Scroll Container */}
            <div className="flex flex-col space-y-6 py-4">
                {episodes.map((episode) => (
                    <div
                        key={episode.id}
                        className="relative group overflow-hidden rounded-lg shadow-xl bg-gray-800 transform transition-transform hover:scale-105 hover:shadow-2xl cursor-pointer"
                        onClick={() => navigate(`/video/${animeId}/${episode.episode_number}`)}
                    >
                        {/* Gradient Overlay */}
                        <div className="absolute inset-0 bg-gradient-to-b from-transparent to-gray-900 opacity-40"></div>

                        {/* Image with object-contain */}
                        <img
                            src={episode.thumbnail_url}
                            alt={episode.title}
                            className="w-full h-[35vh] object-contain transition-transform duration-500 group-hover:scale-110"
                        />

                        {/* Content Overlay */}
                        <div className="absolute bottom-0 left-0 right-0 bg-gradient-to-t from-black via-gray-900 to-transparent p-4 text-white">
                            <h3 className="text-lg font-semibold mb-1">
                                Episode {episode.episode_number}: {episode.title}
                            </h3>
                            <p className="text-sm truncate">{episode.description}</p>
                            <button
                                onClick={(e) => {
                                    e.stopPropagation(); // Prevent card click
                                    navigate(`/video/${animeId}/${episode.episode_number}`);
                                }}
                                className="mt-2 bg-gradient-to-r from-blue-500 to-purple-500 text-white py-2 px-6 rounded-full hover:bg-purple-500"
                            >
                                Watch Now
                            </button>
                        </div>
                    </div>
                ))}
            </div>

            {/* Vertical Scrollbar Styles */}
            <style jsx>{`
                .scrollbar-hide::-webkit-scrollbar {
                    display: none;
                }
                .scrollbar-hide {
                    -ms-overflow-style: none;
                    scrollbar-width: none;
                }
            `}</style>
        </div>
    );
};

export default VerticalScrollCard;
