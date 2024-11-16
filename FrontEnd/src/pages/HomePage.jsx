import React from 'react';
import Carousel from '../components/Carousel';
import HorizantalScrollCard from '../components/HorizantalScrollCard';
import Footer from '../components/Footer';

const HomePage = () => {
  return (
    <>
      <br />
      <br />
      <Carousel />
      {/* <HorizantalScrollCard title="Trending Now" /> */}
      <HorizantalScrollCard title="Recently Added" />
      {/* <Footer /> */}
    </>
  );
};

export default HomePage;
