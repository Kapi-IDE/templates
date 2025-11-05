import React, { useEffect } from "react";
import { BASE_TITLE } from "../Constants";
import { Heading, Image } from "@chakra-ui/react";

import notFoundImage from "../assets/404-landing.jpeg";

const NotFoundPage = () => {
  useEffect(() => {
    document.title = "404 | " + BASE_TITLE;
  }, []);
  return (
    <div>
      <Heading>404: Page Not Found</Heading>
      <p>Sorry, the page you are looking for does not exist.</p>
      <Image
        src={notFoundImage}
        alt="Robot Control Logo"
        width="100%"
        height="100%"
        objectFit="contain" // This prevents distortion if the image aspect ratio doesn't match the element size
      />
    </div>
  );
};

export default NotFoundPage;
