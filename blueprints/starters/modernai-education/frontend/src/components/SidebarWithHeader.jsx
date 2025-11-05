import React from "react";
import {
  IconButton,
  Avatar,
  Box,
  CloseButton,
  Flex,
  HStack,
  VStack,
  Icon,
  useColorModeValue,
  Text,
  Drawer,
  DrawerContent,
  useDisclosure,
  Menu,
  MenuButton,
  MenuDivider,
  MenuItem,
  MenuList,
  Link as ChakraLink,
} from "@chakra-ui/react";

import { 
  FiHome, FiCompass, FiCamera, FiUmbrella, FiStar, 
  FiCoffee, FiTrendingUp, FiBook, FiUsers, FiCode, 
  FiAward, FiBarChart2, FiCalendar, FiMenu, FiBell, FiChevronDown, FiBox
} from 'react-icons/fi';

import {
  Link as ReactRouterLink,
  useResolvedPath,
  useMatch,
  Outlet,
  useNavigate,
  useLocation,
} from "react-router-dom";

import Footer from "./Footer";

import Logo from "./Logo";
import { APP_VERSION } from "../Constants";
import { useAuth } from "../contexts/AuthContext";
import ProfilePic from "../assets/profile-pic.jpg";

import { formatUserInfo } from "../utils/StringUtils";

const notificationCount = 5; //TODO: Replace this with actual count from the DB with an API call

// Main navigation items with sections
const LinkItems = [
  // Main Section
  {
    section: "Main",
    items: [
      { name: "Welcome", icon: FiHome, path: "/" },
      { name: "Dashboard", icon: FiBarChart2, path: "/dashboard" },
    ]
  },
  // Core Learning Experience Section
  { 
    section: "Learning",
    items: [
      { name: "Assessment", icon: FiCompass, path: "/assessment" },
      { name: "Pair Programming", icon: FiUsers, path: "/pair-programming" },
      { name: "Daily Challenges", icon: FiCode, path: "/challenges" },
      { name: "Learning Paths", icon: FiTrendingUp, path: "/learning-paths" },
      { name: "Skills Graph", icon: FiAward, path: "/skills" },
      { name: "Workshops", icon: FiCalendar, path: "/workshops" },
    ]
  },
  // Workshop Tools Section
  {
    section: "Workshop Tools",
    items: [
      { name: "Live Class", icon: FiCamera, path: "/liveclass" },
      { name: "Slides", icon: FiCoffee, path: "/slides" },
      { name: "Poll", icon: FiUmbrella, path: "/poll" },
      { name: "Recordings", icon: FiBook, path: "/recording" },
    ]
  },
  // General Section
  {
    section: "General",
    items: [
      { name: "Landing Page", icon: FiStar, path: "/landing" },
      { name: "Discord Community", icon: FiUsers, path: "/discord" },
    ]
  }
];

const SidebarContent = ({ onClose, ...rest }) => {
  return (
    <Box
      transition="3s ease"
      bg={useColorModeValue("white", "gray.900")}
      borderRight="1px"
      borderRightColor={useColorModeValue("gray.200", "gray.700")}
      w={{ base: "full", md: 60 }}
      pos="fixed"
      h="full"
      {...rest}
    >
      <Flex h="20" alignItems="center" mx="8" justifyContent="space-between">
        <Box p={4} display="flex" justifyContent="center" alignItems="center">
          <Logo fontSize="180px" />
        </Box>
        <CloseButton display={{ base: "flex", md: "none" }} onClick={onClose} />
      </Flex>
      {LinkItems.map((section, sectionIdx) => (
  <Box key={sectionIdx}>
    <Text
      mt={5}
      mb={2}
      mx={8}
      fontSize="xs"
      fontWeight="semibold"
      color="gray.500"
      textTransform="uppercase"
    >
      {section.section}
    </Text>
    {section.items.map((link) => (
      <NavItem key={link.name} icon={link.icon} path={link.path}>
        {link.name}
      </NavItem>
    ))}
  </Box>
))}
      <VStack
        spacing={4}
        align="center"
        justify="end"
        pos="absolute"
        bottom="4"
        w="full"
      >
        <Text fontSize="sm" color="gray.500">
          Version {APP_VERSION}
        </Text>
      </VStack>
    </Box>
  );
};

const NavItem = ({ icon, children, path, ...rest }) => {
  const resolved = useResolvedPath(path);
  const match = useMatch({ path: resolved.pathname, end: true });
  const activeBg = match ? "cyan.500" : undefined;
  const activeColor = match ? "white" : undefined;

  return (
    <ChakraLink
      as={ReactRouterLink}
      to={path}
      style={{ textDecoration: "none" }}
      _focus={{ boxShadow: "none" }}
      _activeLink={{
        bg: activeBg,
        color: activeColor,
      }}
    >
      <Flex
        align="center"
        p="4"
        mx="4"
        borderRadius="lg"
        role="group"
        cursor="pointer"
        _hover={{
          bg: "cyan.400",
          color: "white",
        }}
        bg={activeBg}
        color={activeColor}
        {...rest}
      >
        {icon && (
          <Icon
            mr="4"
            fontSize="16"
            _groupHover={{
              color: "white",
            }}
            as={icon}
          />
        )}
        <Text>{children}</Text>
      </Flex>
    </ChakraLink>
  );
};

const MobileNav = ({ onOpen, ...rest }) => {
  const { logout, isAuthenticated } = useAuth(); // Assuming useAuth includes isAuthenticated
  const navigate = useNavigate();

  const borderColor = useColorModeValue("gray.200", "gray.700");
  const backgroundColor = useColorModeValue("white", "gray.900");

  // If not authenticated, don't render the component
  if (!isAuthenticated) {
    return null;
  }

  const handleLogout = () => {
    console.log("Logout button clicked");
    logout();
    navigate("/login"); // Navigate to the sign-in page after logout
  };

  const firstName = localStorage.getItem("first_name") || "User";
  const lastName = localStorage.getItem("last_name") || "Name";
  const role = localStorage.getItem("role") || "Role";

  //alert(firstName + " " + lastName + " " + role);
  const { formattedName, formattedRole } = formatUserInfo(
    firstName,
    lastName,
    role
  );

  // Render the Flex component only if isAuthenticated is true
  return (
    <Flex
      ml={{ base: 0, md: 60 }}
      px={{ base: 4, md: 4 }}
      height="20"
      alignItems="center"
      bg={backgroundColor}
      borderBottomWidth="1px"
      borderBottomColor={borderColor}
      justifyContent={{ base: "space-between", md: "flex-end" }}
      {...rest}
    >
      {/* Navigation items */}
      <IconButton
        display={{ base: "flex", md: "none" }}
        onClick={onOpen}
        variant="outline"
        aria-label="open menu"
        icon={<FiMenu />}
      />

      <Text
        display={{ base: "flex", md: "none" }}
        fontSize="2xl"
        fontFamily="monospace"
        fontWeight="bold"
      >
        Logo
      </Text>

      <HStack spacing={{ base: "0", md: "6" }}>
        <IconButton
          size="lg"
          variant="ghost"
          aria-label="open menu"
          icon={<FiBell />}
        />
        <Flex alignItems={"center"}>
          <Menu>
            <MenuButton
              py={2}
              transition="all 0.3s"
              _focus={{ boxShadow: "none" }}
            >
              <HStack>
                {/* Avatar and user info */}
                <Avatar size={"sm"} src={ProfilePic} />
                <VStack
                  display={{ base: "none", md: "flex" }}
                  alignItems="flex-start"
                  spacing="1px"
                  ml="2"
                >
                  <Text fontSize="sm">{formattedName}</Text>
                  <Text fontSize="xs" color="gray.600">
                    {formattedRole}
                  </Text>
                </VStack>
                <Box display={{ base: "none", md: "flex" }}>
                  <FiChevronDown />
                </Box>
              </HStack>
            </MenuButton>
            <MenuList>
              <MenuItem>Profile</MenuItem>
              <MenuItem>Settings</MenuItem>
              <MenuDivider />
              <MenuItem onClick={handleLogout}>Logout</MenuItem>
            </MenuList>
          </Menu>
        </Flex>
      </HStack>
    </Flex>
  );
};

const SidebarWithHeader = ({ children }) => {
  const { isOpen, onOpen, onClose } = useDisclosure();
  const location = useLocation();
  const { isAuthenticated } = useAuth();

  return (
    <Box minH="100vh" bg={useColorModeValue("gray.100", "gray.900")}>
      {isAuthenticated && (
        // Only render the sidebar if it's not the sign-in page
        <>
          <SidebarContent
            onClose={() => onClose()}
            display={{ base: "none", md: "block" }}
          />
          <Drawer
            isOpen={isOpen}
            placement="left"
            onClose={onClose}
            returnFocusOnClose={false}
            onOverlayClick={onClose}
            size="full"
          >
            <DrawerContent>
              <SidebarContent onClose={onClose} />
            </DrawerContent>
          </Drawer>
        </>
      )}
      {/* Mobile Nav */}
      <MobileNav onOpen={onOpen} />
      {/* Main content area */}
      <Box ml={{ base: 0, md: !isAuthenticated ? 0 : 60 }} p="4">
        {children ? children : <Outlet />}
        <Box bottom={0} position="fixed" width={"100%"} >
          <Footer/>
        </Box>
      </Box>
    </Box>
  );
};

export default SidebarWithHeader;
