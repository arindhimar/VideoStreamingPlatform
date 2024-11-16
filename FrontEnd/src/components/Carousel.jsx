import React, { useState, useEffect } from 'react';
import axios from 'axios';
import { useNavigate } from 'react-router-dom';

const Carousel = () => {
  const navigate = useNavigate();
  const [currentSlide, setCurrentSlide] = useState(0);
  const [slides, setSlides] = useState([]);

  // Fetch slides data from backend API and pick 4 random slides
  useEffect(() => {
    const fetchSlides = async () => {
      try {
        const response = await axios.get('http://127.0.0.1:5000/anime/');
        // Get 4 random slides
        const randomSlides = response.data
          .sort(() => 0.5 - Math.random()) // Shuffle array randomly
          .slice(0, 4); // Select first 4 items after shuffle

        setSlides(randomSlides);
      } catch (error) {
        console.error('Error fetching slides:', error);
      }
    };

    fetchSlides();
  }, []);

  const handleNext = () => {
    setCurrentSlide((prev) => (prev + 1) % slides.length);
  };

  const handlePrev = () => {
    setCurrentSlide((prev) => (prev - 1 + slides.length) % slides.length);
  };

  const handleVideoClick = (animeId, episodeNumber) => {
    navigate(`/video/${animeId}/${episodeNumber}`);
    // console.log(animeId,episodeNumber)
  };

  // Automatically change slides every 6 seconds
  useEffect(() => {
    const intervalId = setInterval(() => {
      setCurrentSlide((prev) => (prev + 1) % slides.length);
    }, 6000);

    return () => clearInterval(intervalId);
  }, [slides.length]);

  if (!slides.length) {
    return <div>Loading slides...</div>;
  }

  return (
    <div id="carousel-example" className="relative w-full flex flex-col items-center mt-20">
      <div className="w-full sm:w-2/3 mx-auto">
        <div className="relative h-56 sm:h-72 md:h-80 lg:h-[350px] xl:h-[560px] overflow-hidden rounded-lg shadow-lg border border-gray-300">
          <div className="flex transition-transform duration-700 ease-in-out" style={{ transform: `translateX(-${currentSlide * 100}%)` }}>
            {slides.map((slide, index) => (
              <div
                key={slide.anime_id}
                onClick={() => handleVideoClick(slide.anime_id, 1)}
                className="w-full flex-shrink-0 relative hover:scale-105 transition-transform duration-300 bg-gray-900 aspect-[16/9] cursor-pointer"
              >
                {/* Optional gradient overlay to blend background edges */}
                <div className="absolute inset-0 bg-gradient-to-b from-transparent to-gray-900 opacity-30"></div>

                {/* Image with object-contain to avoid excessive zoom */}
                <img
                  src={slide.banner_url}
                  alt={`Slide ${index + 1}`}
                  className="w-full h-full object-contain object-center rounded-lg bg-gray-800"
                />
              </div>
            ))}
          </div>
        </div>

        <div className="absolute bottom-5 left-5 text-white z-10 bg-opacity-50 px-4 py-2 rounded-md w-4/5 sm:w-3/5 md:w-2/5 lg:w-1/3">
          <h2 className="text-lg sm:text-2xl md:text-3xl font-bold mb-4">
            {slides[currentSlide]?.title}
          </h2>
          <button
            onClick={() => handleVideoClick(slides[currentSlide].anime_id,1)}
            className="bg-gradient-to-r from-blue-500 to-purple-500 text-white py-2 px-6 rounded-full hover:bg-purple-500"
          >
            Watch Now
          </button>
        </div>

        <div className="absolute bottom-5 left-1/2 transform -translate-x-1/2 flex space-x-2">
          {slides.map((_, index) => (
            <button
              key={index}
              type="button"
              className={`h-3 w-3 rounded-full transition-colors duration-300 ${currentSlide === index ? 'bg-white' : 'bg-gray-400'}`}
              onClick={() => setCurrentSlide(index)}
              aria-current={currentSlide === index ? 'true' : 'false'}
              aria-label={`Slide ${index + 1}`}
            ></button>
          ))}
        </div>

        <button
          type="button"
          className="absolute left-5 sm:left-10 top-1/2 transform -translate-y-1/2 z-30 flex h-12 w-12 items-center justify-center rounded-full bg-gradient-to-r from-blue-500 to-purple-500 hover:from-purple-500 hover:to-blue-500 focus:outline-none"
          onClick={handlePrev}
        >
          <svg className="h-6 w-6 text-white" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 6 10">
            <path stroke="currentColor" strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M5 1L1 5l4 4" />
          </svg>
        </button>

        <button
          type="button"
          className="absolute right-5 sm:right-10 top-1/2 transform -translate-y-1/2 z-30 flex h-12 w-12 items-center justify-center rounded-full bg-gradient-to-r from-blue-500 to-purple-500 hover:from-purple-500 hover:to-blue-500 focus:outline-none"
          onClick={handleNext}
        >
          <svg className="h-6 w-6 text-white" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 6 10">
            <path stroke="currentColor" strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M1 9l4-4-4-4" />
          </svg>
        </button>
      </div>
    </div>
  );
};

export default Carousel;
