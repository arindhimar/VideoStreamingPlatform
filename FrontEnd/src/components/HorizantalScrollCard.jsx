import React, { useState, useEffect, useRef } from "react";
import { useNavigate } from "react-router-dom";
import { ClockIcon, TrendingUpIcon, ChevronLeftIcon, ChevronRightIcon } from "@heroicons/react/outline";
import axios from "axios";  // Assuming you are using Axios for fetching data

const HorizantalScrollCard = ({ title }) => {
  const navigate = useNavigate();
  const scrollRef = useRef(null);

  const [episodes, setEpisodes] = useState([]);

  // Fetch latest episodes on component mount
  useEffect(() => {
    const fetchEpisodes = async () => {
      try {
        const response = await axios.get("http://127.0.0.1:5000/episodes/latest");  // Assuming this endpoint fetches the latest 5 episodes
        setEpisodes(response.data);
      } catch (error) {
        console.error("Error fetching episodes:", error);
      }
    };

    fetchEpisodes();
  }, []);

  const handleVideoClick = (animeId, episodeNumber) => {
    navigate(`/video/${animeId}/${episodeNumber}`);
    // console.log(animeId,episodeNumber)
  };

  const scrollLeft = () => {
    scrollRef.current.scrollBy({
      left: -300,
      behavior: "smooth",
    });
  };

  const scrollRight = () => {
    scrollRef.current.scrollBy({
      left: 300,
      behavior: "smooth",
    });
  };

  return (
    <div className="w-full mt-10 px-4 relative">
      <h2 className="text-3xl font-semibold text-white mb-4 font-poppins tracking-wider">{title}</h2>

      {/* Wrapping the scroll area and buttons */}
      <div className="relative" style={{ height: "18rem" }}>
        {/* Left scroll button */}
        <button
          onClick={scrollLeft}
          className="absolute left-4 top-1/2 transform -translate-y-1/2 bg-gray-800 text-white p-3 rounded-full shadow-lg hover:bg-gray-700 z-10"
        >
          <ChevronLeftIcon className="w-6 h-6" />
        </button>

        {/* Right scroll button */}
        <button
          onClick={scrollRight}
          className="absolute right-4 top-1/2 transform -translate-y-1/2 bg-gray-800 text-white p-3 rounded-full shadow-lg hover:bg-gray-700 z-10"
        >
          <ChevronRightIcon className="w-6 h-6" />
        </button>

        {/* Horizontal Scroll Container */}
        <div className="overflow-x-auto scrollbar-hide" ref={scrollRef} style={{ height: "100%" }}>
          <div className="flex space-x-6 py-4 w-max h-full">
            {episodes.map((episode) => (
              <div
                key={episode.episode_id}
                onClick={() => handleVideoClick(episode.anime_id,episode.episode_number)}  // Use episode_id for navigation

                className="relative group overflow-hidden rounded-lg shadow-xl bg-[#1c2a44] transform transition-transform hover:scale-105 hover:shadow-2xl"
                style={{ width: "24rem", height: "100%" }}
              >
                <div className="absolute top-2 right-2 bg-blue-500 text-white text-sm px-3 py-1 rounded-lg shadow-lg z-10 flex items-center">
                  {episode.status === "uploaded" ? (
                    <ClockIcon className="w-4 h-4 mr-2" />
                  ) : (
                    <ClockIcon className="w-4 h-4 mr-2" />
                  )}
                  {episode.status === "uploaded" ? "Recently Added" : "Recently Added"}
                </div>
                <img
                  src={episode.thumbnail_url}  // Using the thumbnail_url from the episode data
                  alt={`Episode ${episode.episode_number}`}
                  className="w-full h-72 sm:h-80 object-cover transition-transform duration-500 group-hover:scale-110"
                />
                <div className="absolute bottom-0 left-0 right-0 bg-gradient-to-t from-[#0a1a2f] to-transparent p-6 text-white">
                  <h3 className="text-lg sm:text-xl font-semibold mb-2">{episode.title}</h3>
                  <p className="text-sm mb-4">{episode.description || "No description available"}</p>
                  <button
                    onClick={() => handleVideoClick(episode.anime_id,episode.episode_number)}  // Use episode_id for navigation
                    className="inline-block bg-gradient-to-r from-blue-500 to-purple-500 text-white py-2 px-6 rounded-full text-sm font-medium transition-all duration-300 group-hover:from-purple-500 group-hover:to-blue-500"
                  >
                    Watch Now
                  </button>
                </div>
              </div>
            ))}
          </div>
        </div>
      </div>

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

export default HorizantalScrollCard;
