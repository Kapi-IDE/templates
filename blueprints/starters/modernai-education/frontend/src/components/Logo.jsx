import { Box, Image, useColorMode } from "@chakra-ui/react";
import logoDark from "../assets/logo/logo-dark.png";
import logoWhite from "../assets/logo/logo-white.png";

const Logo = ({ fontSize = "180px", color }) => {
  const { colorMode } = useColorMode();
  // Use color prop if provided, otherwise use the current color mode
  const logoSrc = color === "white" || (!color && colorMode === "dark") 
    ? logoWhite 
    : logoDark;

  return (
    <Box>
      <Image src={logoSrc} alt="Modern AI Pro Logo" maxWidth={fontSize} />
    </Box>
  );
};

export default Logo;
