import React, { useState } from "react";

const Sidebar = () => {
  const [isOpen, setIsOpen] = useState(false); // For mobile toggle

  const handleToggle = () => {
    setIsOpen(!isOpen);
  };

  return (
    <div className="flex">
      {/* Sidebar for Mobile */}
      <div
        className={`md:hidden fixed top-0 left-0 w-full h-full bg-gray-900 bg-opacity-75 z-50 transition-transform transform ${
          isOpen ? "translate-x-0" : "translate-x-full"
        }`}
        onClick={handleToggle}
      >
        <div className="w-64 bg-gray-800 text-white p-4">
          <img
            src="https://www.freepnglogos.com/uploads/spotify-logo-png/file-spotify-logo-png-4.png"
            alt="Placeholder"
            className="w-8 h-8 mx-auto mb-5"
          />
          <span className="cursor-pointer hover:text-white px-2 block mb-5">
            <i className="fas fa-home"></i> Home
          </span>
          <span className="cursor-pointer hover:text-white px-2 block mb-5">
            <i className="fas fa-th-list"></i> Categories
          </span>
          <span className="cursor-pointer hover:text-white px-2 block mb-5">
            <i className="fas fa-search p-2 bg-gray-800 rounded-full"></i> Search
          </span>
          <span className="cursor-pointer hover:text-white px-2 block mb-5">
            <i className="fas fa-user"></i> Profile
          </span>
          <span className="cursor-pointer hover:text-white px-2 block mb-5">
            <i className="fas fa-cogs"></i> Settings
          </span>
        </div>
      </div>

      {/* Sidebar for Desktop */}
      <div className="hidden md:block p-4 w-64 bg-gray-800 text-white">
        <div className="w-full py-4 px-2 text-gray-700 bg-gray-900 rounded-lg text-left capitalize font-medium shadow-lg">
          <img
            src="https://www.freepnglogos.com/uploads/spotify-logo-png/file-spotify-logo-png-4.png"
            alt="Placeholder"
            className="w-8 h-8 mx-auto mb-5"
          />
          <span className="cursor-pointer px-2 py-1 hover:bg-gray-800 hover:text-gray-300 rounded block mb-5">
            <i className="w-8 fas fa-home p-2 bg-gray-800 rounded-full"></i>
            <span className="mx-2">Home</span>
          </span>
          <span className="cursor-pointer px-2 py-1 hover:bg-gray-800 hover:text-gray-300 rounded block mb-5">
            <i className="w-8 fas fa-th-list p-2 bg-gray-800 rounded-full"></i>
            <span className="mx-2">Categories</span>
          </span>
          <span className="cursor-pointer px-2 py-1 hover:bg-gray-800 hover:text-gray-300 rounded block mb-5">
            <i className="w-8 fas fa-search p-2 bg-gray-800 rounded-full"></i>
            <span className="mx-2">Search</span>
          </span>
          <span className="cursor-pointer px-2 py-1 hover:bg-gray-800 hover:text-gray-300 rounded block mb-5">
            <i className="w-8 fas fa-user p-2 bg-gray-800 rounded-full"></i>
            <span className="mx-2">Profile</span>
          </span>
          <span className="cursor-pointer px-2 py-1 hover:bg-gray-800 hover:text-gray-300 rounded block mb-5">
            <i className="w-8 fas fa-cogs p-2 bg-gray-800 rounded-full"></i>
            <span className="mx-2">Settings</span>
          </span>
        </div>
      </div>

      {/* Hamburger Icon for Mobile */}
      <button
        className="md:hidden p-4 absolute top-4 left-4 text-white"
        onClick={handleToggle}
      >
        <i className="fas fa-bars"></i>
      </button>
    </div>
  );
};

export default Sidebar;
