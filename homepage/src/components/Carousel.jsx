import React, { useState } from 'react';

const Carousel = () => {
  const [currentSlide, setCurrentSlide] = useState(0);
  
  const slides = [
    "https://i.ibb.co/B3f9zR6/Login-Images-13.jpg",
    "https://i.ibb.co/NxMhkjg/Login-Images-14.jpg",
    "https://i.ibb.co/N3hjknW/Login-Images-12.jpg",
    "https://i.ibb.co/WPWvJvt/Login-Images-4.jpg",
  ];

  const handleNext = () => {
    setCurrentSlide((prev) => (prev + 1) % slides.length);
  };

  const handlePrev = () => {
    setCurrentSlide((prev) => (prev - 1 + slides.length) % slides.length);
  };

  return (
    <div id="carousel-example" className="relative w-full">
      {/* Carousel wrapper */}
      <div className="relative h-56 overflow-hidden rounded-lg sm:h-64 xl:h-80 2xl:h-96">
        <div className="relative flex transition-all duration-700 ease-in-out">
          {slides.map((slide, index) => (
            <div
              key={index}
              className={`w-full flex-shrink-0 transition-transform duration-700 ease-in-out transform ${
                currentSlide === index
                  ? "translate-x-0"
                  : currentSlide > index
                  ? "-translate-x-full"
                  : "translate-x-full"
              }`}
            >
              <img
                src={slide}
                alt={`Slide ${index + 1}`}
                className="w-full h-full object-cover"
              />
            </div>
          ))}
        </div>
      </div>
      
      {/* Slider indicators */}
      <div className="absolute bottom-5 left-1/2 z-30 flex -translate-x-1/2 space-x-3 rtl:space-x-reverse">
        {slides.map((_, index) => (
          <button
            key={index}
            type="button"
            className={`h-3 w-3 rounded-full ${currentSlide === index ? 'bg-white' : 'bg-gray-400'}`}
            onClick={() => setCurrentSlide(index)}
            aria-current={currentSlide === index ? 'true' : 'false'}
            aria-label={`Slide ${index + 1}`}
          ></button>
        ))}
      </div>
      
      {/* Slider controls */}
      <button
        type="button"
        className="group absolute left-0 top-0 z-30 flex h-full cursor-pointer items-center justify-center px-4 focus:outline-none"
        onClick={handlePrev}
      >
        <span className="inline-flex h-10 w-10 items-center justify-center rounded-full bg-white/30 group-hover:bg-white/50 group-focus:outline-none group-focus:ring-4 group-focus:ring-white dark:bg-gray-800/30 dark:group-hover:bg-gray-800/60 dark:group-focus:ring-gray-800/70">
          <svg className="h-4 w-4 text-white dark:text-gray-800" aria-hidden="true" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 6 10">
            <path stroke="currentColor" strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M5 1L1 5l4 4" />
          </svg>
          <span className="hidden">Previous</span>
        </span>
      </button>

      <button
        type="button"
        className="group absolute right-0 top-0 z-30 flex h-full cursor-pointer items-center justify-center px-4 focus:outline-none"
        onClick={handleNext}
      >
        <span className="inline-flex h-10 w-10 items-center justify-center rounded-full bg-white/30 group-hover:bg-white/50 group-focus:outline-none group-focus:ring-4 group-focus:ring-white dark:bg-gray-800/30 dark:group-hover:bg-gray-800/60 dark:group-focus:ring-gray-800/70">
          <svg className="h-4 w-4 text-white dark:text-gray-800" aria-hidden="true" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 6 10">
            <path stroke="currentColor" strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M1 9l4-4-4-4" />
          </svg>
          <span className="hidden">Next</span>
        </span>
      </button>
    </div>
  );
};

export default Carousel;
