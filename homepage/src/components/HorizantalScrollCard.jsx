import React from "react";
import { ClockIcon, TrendingUpIcon } from "@heroicons/react/outline"; // Importing Heroicons

const HorizantalScrollCard = ({ title }) => {
    const episodes = [
        {
            title: "Episode 1: The Beginning",
            description: "A thrilling start to an exciting adventure.",
            image: "https://i.ibb.co/B3f9zR6/Login-Images-13.jpg",
            label: "Recently Added", // Add label here
        },
        {
            title: "Episode 2: The Journey Continues",
            description: "The adventure intensifies with new challenges.",
            image: "https://i.ibb.co/NxMhkjg/Login-Images-14.jpg",
            label: "Trending", // Add label here
        },
        {
            title: "Episode 3: The Clash",
            description: "A fierce battle awaits the heroes.",
            image: "https://i.ibb.co/N3hjknW/Login-Images-12.jpg",
            label: "Recently Added", // Add label here
        },
        {
            title: "Episode 4: The Conclusion",
            description: "The final showdown that will change everything.",
            image: "https://i.ibb.co/WPWvJvt/Login-Images-4.jpg",
            label: "Trending", // Add label here
        },
        {
            title: "Episode 1: The Beginning",
            description: "A thrilling start to an exciting adventure.",
            image: "https://i.ibb.co/B3f9zR6/Login-Images-13.jpg",
            label: "Recently Added", // Add label here
        },
        {
            title: "Episode 2: The Journey Continues",
            description: "The adventure intensifies with new challenges.",
            image: "https://i.ibb.co/NxMhkjg/Login-Images-14.jpg",
            label: "Trending", // Add label here
        },
    ];

    return (
        <div className="w-full mt-10 px-4">
            {/* Section Heading */}
            <h2 className="text-3xl font-semibold text-white mb-4 font-poppins tracking-wider">
                {title}
            </h2>

            {/* Wrapper Div for Horizontal Scroll */}
            <div className="overflow-x-auto scrollbar-hide">
                {/* Horizontal Scroll Container */}
                <div className="flex space-x-6 py-4 w-max">
                    {episodes.map((episode, index) => (
                        <div
                            key={index}
                            className="relative group overflow-hidden rounded-lg shadow-xl bg-[#1c2a44] transform transition-transform hover:scale-105 hover:shadow-2xl"
                            style={{ width: "24rem", height: "18rem" }}
                        >
                            {/* Label with Icon */}
                            <div className="absolute top-2 right-2 bg-blue-500 text-white text-sm px-3 py-1 rounded-lg shadow-lg z-10 flex items-center">
                                {/* Displaying the icon based on the label */}
                                {episode.label === "Recently Added" ? (
                                    <ClockIcon className="w-4 h-4 mr-2" />
                                ) : (
                                    <TrendingUpIcon className="w-4 h-4 mr-2" />
                                )}
                                {episode.label}
                            </div>

                            {/* Image */}
                            <img
                                src={episode.image}
                                alt={`Episode ${index + 1}`}
                                className="w-full h-72 sm:h-80 object-cover transition-transform duration-500 group-hover:scale-110"
                            />

                            {/* Card Content */}
                            <div className="absolute bottom-0 left-0 right-0 bg-gradient-to-t from-[#0a1a2f] to-transparent p-6 text-white">
                                <h3 className="text-lg sm:text-xl font-semibold mb-2">{episode.title}</h3>
                                <p className="text-sm mb-4">{episode.description}</p>

                                {/* Watch Now Button */}
                                <a
                                    href="#"
                                    className="inline-block bg-gradient-to-r from-blue-500 to-purple-500 text-white py-2 px-6 rounded-full text-sm font-medium transition-all duration-300 group-hover:from-purple-500 group-hover:to-blue-500"
                                >
                                    Watch Now
                                </a>
                            </div>
                        </div>
                    ))}
                </div>
            </div>

            {/* Horizontal Scrollbar Styles (Optional) */}
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
