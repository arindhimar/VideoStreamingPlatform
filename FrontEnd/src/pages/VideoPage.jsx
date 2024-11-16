import React, { useEffect } from 'react';
import HLSPlayer from '../components/HLSPlayer';
import VerticalScrollCard from '../components/VerticalScrollCard';
import { useParams } from 'react-router-dom';
import Navbar from '../components/Navbar.jsx';

const VideoPage = () => {
  const { animeId, episodeNumber } = useParams();

  // Scroll to the top when the component is mounted
  useEffect(() => {
    window.scrollTo(0, 0);
  }, []);  // Empty dependency array ensures this runs once when the component is mounted

  return (
    <div className="mt-16 flex flex-col md:flex-row w-full">
      <div className="w-full md:w-8/12 flex justify-center">
        {/* Pass animeId and episodeNumber as props to HLSPlayer */}
        <HLSPlayer animeId={animeId} episodeNumber={episodeNumber} />
      </div>
      <div className="w-full md:w-4/12 mt-8 md:mt-0">
        <VerticalScrollCard animeId={animeId} episodeNumber={episodeNumber} />
      </div>
    </div>
  );
};

export default VideoPage;
