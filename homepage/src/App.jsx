import React from 'react';
import Navbar from './components/Navbar.jsx';  
import HLSPlayer from './components/HLSPlayer.jsx';
import VerticalScrollCard from './components/VerticalScrollCard.jsx';

function App() {
  return (
    <>
      <Navbar />

      {/* Container for the main content, starts below the Navbar */}
      <div className="mt-16 flex flex-col md:flex-row w-full"> {/* Make the container column on small screens and row on large screens */}
        
        {/* Video Player on top or left side on larger screens, full width on small screens */}
        <div className="w-full md:w-8/12 flex justify-center"> {/* Center video player horizontally */}
          <HLSPlayer />
        </div>

        {/* Vertical scroll card or content below on small screens, on the right on large screens */}
        <div className="w-full md:w-4/12 mt-8 md:mt-0">
          <VerticalScrollCard />
        </div>
      </div>
    </>
  );
}

export default App;
