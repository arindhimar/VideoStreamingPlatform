import React from 'react';
import { BrowserRouter, Routes, Route, Navigate } from 'react-router-dom';
import Navbar from './components/Navbar';
import HomePage from './pages/HomePage';
import VideoPage from './pages/VideoPage';
import Footer from './components/Footer';


function App() {
  return (
    <BrowserRouter>
      <Navbar />
      <Routes>
        {/* Redirect any unknown routes to home */}
        <Route path="*" element={<Navigate to="/" replace />} />
        {/* Homepage route */}
        <Route path="/" element={<HomePage />} />
        {/* Video page route with dynamic animeId and episodeNumber */}
        <Route path="/video/:animeId/:episodeNumber" element={<VideoPage />} />
      </Routes>
      <Footer/>
    </BrowserRouter>
  );
}

export default App;
