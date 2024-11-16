import React, { useState, useEffect } from "react";

const Navbar = () => {
  const [isMenuOpen, setIsMenuOpen] = useState(false); // To toggle mobile menu visibility
  const [currentTime, setCurrentTime] = useState(""); // State to hold the current time

  // Function to update the clock
  const updateClock = () => {
    const now = new Date();
    const formattedTime = now.toLocaleTimeString(); // Format the time as HH:MM:SS
    setCurrentTime(formattedTime);
  };

  useEffect(() => {
    // Update the clock every second
    const intervalId = setInterval(updateClock, 1000);

    // Cleanup interval on component unmount
    return () => clearInterval(intervalId);
  }, []);

  const handleMenuToggle = () => {
    setIsMenuOpen(!isMenuOpen);
  };

  return (
    <div style={{ backgroundColor: "#0a1a2f" }} className="fixed top-0 w-full z-50">
      <div style={{ backgroundColor: "#0a1a2f" }} className="p-4 w-full">
        <div className="p-4 text-gray-200 bg-gray-900 rounded-lg shadow-lg font-medium capitalize flex items-center justify-between">
          <span className="px-2 mr-2 border-r border-gray-700 flex items-center">
            <img
              src="https://i.ibb.co/j8PqcbH/Logo-No-Backgroud.png"
              alt="ANIMEX"
              className="w-8 h-8 -mt-1"
            />
          </span>

          {/* Hamburger Menu Button (for Mobile) */}
          <button
            className="block md:hidden px-2 py-1 cursor-pointer text-gray-300"
            onClick={handleMenuToggle}
          >
            <i className="fas fa-bars"></i>
          </button>

          {/* Main Navbar Content */}
          <div className="hidden md:flex items-center justify-between w-full">
            <span className="px-2 py-1 cursor-pointer hover:bg-gray-800 hover:text-gray-200 text-gray-300 text-sm rounded flex items-center ml-4">
              <i className="fas fa-stream p-2 text-gray-400 bg-gray-800 rounded-full"></i>
              <span className="mx-1">Categories</span>
            </span>

            <span className="px-1 hover:text-white cursor-pointer flex items-center bg-gray-800 w-1/3 rounded-md mx-auto focus-within:text-white">
              <i className="fas fa-search p-2 text-gray-400"></i>
              <input
                type="text"
                placeholder="Search..."
                className="bg-transparent border-none text-gray-300 placeholder-gray-500 w-full p-2 focus:outline-none focus:text-white"
              />
            </span>

            <div className="flex ml-auto space-x-4 items-center">
              <span className="px-1 hover:text-white cursor-pointer relative flex items-center space-x-2">
                <i className="fas fa-clock p-2 text-gray-400 bg-gray-800 rounded-full"></i>
                <span className="text-gray-300 ml-2 hover:text-white font-jura">
                  {currentTime}
                </span>
              </span>

              <span className="px-1 hover:text-white cursor-pointer relative">
                <i className="fas fa-bell p-2 text-gray-400 bg-gray-800 rounded-full hover:bg-white-700 hover:text-white"></i>
                <span className="absolute right-0 top-0 -mt-2 -mr-1 text-xs bg-red-500 text-white font-medium px-2 shadow-lg rounded-full">
                  3
                </span>
              </span>

              <a href="./login.html">
                <span className="hover:text-white cursor-pointer relative flex items-center space-x-2">
                  <i className="fas fa-user p-2 text-gray-400 bg-gray-800 rounded-full hover:bg-white-700 hover:text-white"></i>
                  <span className="text-sm text-gray-300 hover:text-white">Login</span>
                </span>
              </a>
            </div>
          </div>
        </div>
      </div>

      {/* Mobile Menu */}
      <div
        className={`${isMenuOpen ? "block" : "hidden"
          } md:hidden bg-gray-800 text-gray-200 px-4 py-2 space-y-4 transition-all duration-500 ease-out transform ${isMenuOpen
            ? "max-h-screen opacity-100 scale-100 translate-y-0"
            : "max-h-0 opacity-0 scale-95 translate-y-10"
          }`}
      >
        <span className="px-2 py-1 cursor-pointer hover:bg-gray-800 hover:text-gray-200 text-gray-300 text-sm rounded flex items-center">
          <i className="fas fa-stream p-2 text-gray-400 bg-gray-800 rounded-full"></i>
          <span className="mx-1">Categories</span>
        </span>

        <span className="px-2 py-1 cursor-pointer hover:bg-gray-800 hover:text-gray-200 text-gray-300 text-sm rounded flex items-center">
          <i className="fas fa-search p-2 text-gray-400 bg-gray-800 rounded-full"></i>
          <span className="mx-1">Search</span>
        </span>

        <span className="px-2 py-1 cursor-pointer hover:bg-gray-800 hover:text-gray-200 text-gray-300 text-sm rounded flex items-center">
          <i className="fas fa-clock p-2 text-gray-400 bg-gray-800 rounded-full"></i>
          <span className="mx-1">{currentTime}</span>
        </span>

        <span className="px-2 py-1 cursor-pointer hover:bg-gray-800 hover:text-gray-200 text-gray-300 text-sm rounded flex items-center">
          <i className="fas fa-bell p-2 text-gray-400 bg-gray-800 rounded-full"></i>
          <span className="mx-1">Notifications</span>
        </span>

        <span className="px-2 py-1 cursor-pointer hover:bg-gray-800 hover:text-gray-200 text-gray-300 text-sm rounded flex items-center">
          <i className="fas fa-user p-2 text-gray-400 bg-gray-800 rounded-full"></i>
          <span className="mx-1">Login</span>
        </span>
      </div>
    </div>
  );
};

export default Navbar;
