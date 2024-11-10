import React, { useState, useEffect } from 'react';

const Carousel = () => {
  const [currentSlide, setCurrentSlide] = useState(0);

  const slides = [
    {
      image: "https://i.ibb.co/B3f9zR6/Login-Images-13.jpg",
      title: "Exciting Movie 1",
      link: "#",
    },
    {
      image: "https://i.ibb.co/NxMhkjg/Login-Images-14.jpg",
      title: "Thrilling Movie 2",
      link: "#",
    },
    {
      image: "https://i.ibb.co/N3hjknW/Login-Images-12.jpg",
      title: "Action Packed Movie 3",
      link: "#",
    },
    {
      image: "https://i.ibb.co/WPWvJvt/Login-Images-4.jpg",
      title: "Adventure Movie 4",
      link: "#",
    },
  ];

  const handleNext = () => {
    setCurrentSlide((prev) => (prev + 1) % slides.length);
  };

  const handlePrev = () => {
    setCurrentSlide((prev) => (prev - 1 + slides.length) % slides.length);
  };

  // Automatically change slides every 6 seconds
  useEffect(() => {
    const intervalId = setInterval(() => {
      setCurrentSlide((prev) => (prev + 1) % slides.length);
    }, 6000);

    // Clean up the interval on component unmount
    return () => clearInterval(intervalId);
  }, [slides.length]);

  return (
    <div
      id="carousel-example"
      className="relative w-full flex flex-col items-center mt-20"
    >
      {/* Center the carousel */}
      <div className="w-full sm:w-2/3 mx-auto">
        {/* Carousel wrapper with responsive height */}
        <div className="relative h-56 sm:h-72 md:h-80 lg:h-[350px] xl:h-[600px] overflow-hidden rounded-lg shadow-lg border border-gray-300">
          <div
            className="flex transition-transform duration-700 ease-in-out"
            style={{ transform: `translateX(-${currentSlide * 100}%)` }}
          >
            {slides.map((slide, index) => (
              <div
                key={index}
                className="w-full flex-shrink-0 hover:scale-105 transition-transform duration-300 relative"
              >
                <img
                  src={slide.image}
                  alt={`Slide ${index + 1}`}
                  className="w-full h-full object-cover rounded-lg" // Ensures the image fits the container without distortion
                />
              </div>
            ))}
          </div>
        </div>

        {/* Title and Watch Now Button (Fixed at bottom-left) */}
        <div className="absolute bottom-5 left-55 text-white z-3 bg-opacity-50 px-4 py-2 rounded-md w-4/5 sm:w-3/5 md:w-2/5 lg:w-1/3">
          <h2 className="text-lg sm:text-2xl md:text-3xl font-bold mb-4">{slides[currentSlide].title}</h2>
          <a
            href={slides[currentSlide].link}
            className="bg-gradient-to-r from-blue-500 to-purple-500 text-white py-2 px-6 rounded-full hover:bg-purple-500"
          >
            Watch Now
          </a>
        </div>

        {/* Slider indicators */}
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

        {/* Slider controls */}
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
