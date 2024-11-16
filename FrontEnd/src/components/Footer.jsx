import React from "react";
import reactLogo from "../assets/techStack/react.svg";
import viteLogo from "../assets/techStack/vite.svg";
import flaskLogo from "../assets/techStack/flask.svg";
import tailwindLogo from "../assets/techStack/tailwind.svg";
import bootstrapLogo from "../assets/techStack/bootstrap.svg";
import mysqlLogo from "../assets/techStack/mysql.svg";

const Footer = () => {
    return (
        <footer className="bg-[#0a1a2f] py-16 px-8 text-gray-200">
            <div className="max-w-7xl mx-auto grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-10">
                
                {/* Company Branding */}
                <div>
                    <h2 className="text-2xl font-bold text-white">
                        <img src="./src/assets/Logo-NoBackgroud.png" alt="Animex Logo" className="w-24 h-auto" />
                    </h2>
                    <p className="mt-4 text-gray-400 text-sm leading-relaxed">
                        Elevate your experience with the latest anime episodes, curated collections, and exclusive content.
                    </p>
                </div>
                
                {/* Navigation Links */}
                <div>
                    <h2 className="text-xl font-semibold text-white mb-4">Quick Links</h2>
                    <ul className="space-y-2 text-gray-400">
                        {['Home', 'Episodes', 'Popular Series', 'Contact Us'].map((link) => (
                            <li key={link}>
                                <a href={`/${link.toLowerCase().replace(' ', '-')}`} className="hover:text-white transition duration-300" aria-label={`Go to ${link}`}>
                                    {link}
                                </a>
                            </li>
                        ))}
                    </ul>
                </div>

                {/* Tech Stack Section */}
                <div>
                    <h2 className="text-xl font-semibold text-white mb-4">Tech Stack</h2>
                    <div className="flex flex-wrap gap-4 mt-4">
                        {[reactLogo, viteLogo, flaskLogo, tailwindLogo, bootstrapLogo, mysqlLogo].map((tech, index) => (
                            <div key={index} className="w-12 h-12 flex items-center justify-center bg-[#1c2a44] rounded-lg p-2 transition-transform transform hover:scale-105">
                                <img src={tech} alt={`Tech logo`} title={`Tech`} className="w-8 h-8 opacity-80 hover:opacity-100" />
                            </div>
                        ))}
                    </div>
                </div>

                {/* About the Developer */}
                <div>
                    <h2 className="text-xl font-semibold text-white mb-4">About the Developer</h2>
                    <p className="text-sm text-gray-400 mb-4">
                        Hi, I’m <b>Arin Dhimar</b>, the developer behind <b>ANIMEX</b>. I’m passionate about creating immersive anime experiences. 
                        Connect with me on social media!
                    </p>
                    <div className="flex space-x-3 mt-4">
                        {['github', 'linkedin', 'instagram'].map((platform) => (
                            <a href={`https://www.${platform}.com/arindhimar`} key={platform} className="hover:scale-105 transform transition duration-300" aria-label={`Visit my ${platform}`}>
                                <img 
                                    src={`./src/assets/socialMedia/${platform}.svg`} 
                                    alt={`${platform} icon`} 
                                    className="w-6 h-6 opacity-75 hover:opacity-100 filter invert"
                                />
                            </a>
                        ))}
                    </div>
                </div>
            </div>

            <div className="border-t border-gray-700 mt-12 pt-8 text-center text-sm text-gray-500">
                <p>&copy; 2024 Animex. All rights reserved.</p>
            </div>
        </footer>
    );
};

export default Footer;
