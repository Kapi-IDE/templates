import React, { useEffect, useRef, useState } from "react";

const GoogleSlides = ({ 
  width = 640, 
  height = 480, 
  slidesLink, 
  slideDuration = 5, 
  position = 1, 
  showControls = true, 
  loop = true 
}) => {
  const [currentPosition, setCurrentPosition] = useState(position);
  const timerRef = useRef(null);
  const iframeRef = useRef(null);
  
  // Extract presentation ID from the link
  const getPresentationId = (link) => {
    // Extract ID from various Google Slides URL formats
    const regex = /[-\w]{25,}/;
    const match = link.match(regex);
    return match ? match[0] : "";
  };
  
  const presentationId = getPresentationId(slidesLink);
  
  // Format the embed URL with parameters
  const getEmbedUrl = () => {
    let url = `https://docs.google.com/presentation/d/e/${presentationId}/embed?`;
    
    if (currentPosition > 1) {
      url += `start=true&slide=${currentPosition}`;
    } else {
      url += 'start=true';
    }
    
    if (!showControls) {
      url += '&rm=minimal';
    }
    
    if (loop) {
      url += '&loop=true';
    }
    
    return url;
  };
  
  // Handle slide advancement
  useEffect(() => {
    if (slideDuration > 0) {
      timerRef.current = setInterval(() => {
        // Note: We can't directly control slides from iframe due to cross-origin restrictions
        // This will reload the iframe with the next position
        setCurrentPosition(prev => prev + 1);
      }, slideDuration * 1000);
    }
    
    return () => {
      if (timerRef.current) {
        clearInterval(timerRef.current);
      }
    };
  }, [slideDuration]);
  
  return (
    <div className="google-slides-container">
      <iframe
        ref={iframeRef}
        src={getEmbedUrl()}
        width={width}
        height={height}
        frameBorder="0"
        allowFullScreen
        title="Google Slides Presentation"
      />
    </div>
  );
};

// Modified SlideShow component using the custom implementation
const SlideShow = () => {
  return (
    <GoogleSlides
      width={640}
      height={480}
      slidesLink="https://docs.google.com/presentation/d/1hXcru7QqAy7SkvVoNnODCfvb5o9R0wtf4Eik1xGSZJc"
      slideDuration={5}
      position={1}
      showControls={true}
      loop={true}
    />
  );
};

export default SlideShow;