import React, { useEffect, useState, useRef } from "react";
import {
  Box,
  Button,
  Container,
  Flex,
  Heading,
  Stack,
  Text,
  Icon,
  SimpleGrid,
  VStack,
  useColorModeValue,
  Image,
  Badge,
  Link,
} from "@chakra-ui/react";
import { Link as RouterLink } from "react-router-dom";
import { BASE_TITLE } from "../Constants";
import Logo from "./Logo";
import { FaCode, FaUsers, FaTrophy, FaRocket, FaChartLine, FaLaptopCode } from "react-icons/fa";
import { useAuth } from "../contexts/AuthContext";

const Feature = ({ title, text, icon }) => {
  return (
    <Stack 
      bg="gray.800" 
      borderRadius="lg" 
      p={6} 
      border="1px solid" 
      borderColor="purple.600"
      boxShadow="lg"
      transition="all 0.3s"
      _hover={{ transform: "translateY(-5px)", boxShadow: "xl" }}
    >
      <Flex
        w={16}
        h={16}
        align="center"
        justify="center"
        color="white"
        rounded="full"
        bg="purple.500"
        mb={4}
      >
        <Icon as={icon} w={10} h={10} />
      </Flex>
      <Heading fontSize="xl" color="white">{title}</Heading>
      <Text color="gray.400" fontSize="md">{text}</Text>
    </Stack>
  );
};

const PricingCard = ({ title, price, features, buttonText, isPopular }) => {
  return (
    <Box
      maxW="330px"
      w="full"
      bg="gray.800"
      boxShadow="lg"
      rounded="lg"
      overflow="hidden"
      position="relative"
      border="1px solid"
      borderColor={isPopular ? "purple.500" : "gray.700"}
    >
      {isPopular && (
        <Badge
          position="absolute"
          top={0}
          right={0}
          bg="purple.500"
          color="white"
          fontWeight="bold"
          p={2}
          borderBottomLeftRadius="lg"
          fontSize="sm"
        >
          POPULAR
        </Badge>
      )}
      <Box p={6}>
        <Stack spacing={0} align="center" mb={5}>
          <Heading size="md" fontWeight="500" color="white">
            {title}
          </Heading>
          <Stack direction="row" align="center" justify="center">
            <Text fontSize="5xl" fontWeight="900" color="white">
              ${price}
            </Text>
            {price > 0 && (
              <Text color="gray.400" fontSize="lg">
                {title === "Premium" ? "/3 months" : "/month"}
              </Text>
            )}
          </Stack>
        </Stack>
        <VStack spacing={4}>
          {features.map((feature, index) => (
            <Text key={index} textAlign="center" color="gray.400" fontSize="sm">
              {feature}
            </Text>
          ))}
        </VStack>
        <Button
          as={RouterLink}
          to="/login"
          mt={10}
          w="full"
          bg={isPopular ? "purple.500" : "gray.700"}
          color="white"
          rounded="md"
          _hover={{
            bg: isPopular ? "purple.600" : "gray.600",
          }}
        >
          {buttonText}
        </Button>
      </Box>
    </Box>
  );
};

const LandingPage = () => {
  const { isAuthenticated } = useAuth();
  const featuresRef = useRef(null);
  const pricingRef = useRef(null);
  const aboutRef = useRef(null);
  
  useEffect(() => {
    document.title = BASE_TITLE;
  }, []);

  const scrollToSection = (ref) => {
    ref.current.scrollIntoView({ behavior: 'smooth' });
  };

  const bgGradient = "linear(to-b, gray.900, purple.900)";

  return (
    <Box bgGradient={bgGradient} minH="100vh" color="white">
      {/* Navigation */}
      <Flex
        as="nav"
        align="center"
        justify="space-between"
        wrap="wrap"
        w="100%"
        py={4}
        px={8}
        bg="gray.900"
        position="sticky"
        top={0}
        zIndex={10}
        boxShadow="md"
      >
        <Flex align="center">
          <Logo fontSize="160px" color="white" />
        </Flex>
        <Stack
          direction="row"
          spacing={6}
          display={{ base: "none", md: "flex" }}
          alignItems="center"
        >
          <Link 
            color="gray.300" 
            _hover={{ color: "white", cursor: "pointer" }}
            onClick={() => scrollToSection(featuresRef)}
          >
            Features
          </Link>
          <Link 
            color="gray.300" 
            _hover={{ color: "white", cursor: "pointer" }}
            onClick={() => scrollToSection(pricingRef)}
          >
            Pricing
          </Link>
          <Link 
            color="gray.300" 
            _hover={{ color: "white", cursor: "pointer" }}
            onClick={() => scrollToSection(aboutRef)}
          >
            About
          </Link>
          {isAuthenticated ? (
            <Button
              as={RouterLink}
              to="/"
              colorScheme="purple"
              variant="solid"
              size="md"
            >
              Dashboard
            </Button>
          ) : (
            <Button
              as={RouterLink}
              to="/login"
              colorScheme="purple"
              variant="solid"
              size="md"
            >
              Sign In
            </Button>
          )}
        </Stack>
        {isAuthenticated ? (
          <Button
            as={RouterLink}
            to="/"
            display={{ base: "flex", md: "none" }}
            colorScheme="purple"
            variant="solid"
            size="sm"
          >
            Dashboard
          </Button>
        ) : (
          <Button
            as={RouterLink}
            to="/login"
            display={{ base: "flex", md: "none" }}
            colorScheme="purple"
            variant="solid"
            size="sm"
          >
            Sign In
          </Button>
        )}
      </Flex>

      {/* Hero Section */}
      <Box 
        position="relative" 
        overflow="hidden"
        py={{ base: 20, md: 28 }}
        px={8}
      >
        <Container maxW="container.xl" zIndex={2} position="relative">
          <Stack
            textAlign="center"
            align="center"
            spacing={{ base: 6, md: 8 }}
            py={{ base: 10, md: 18 }}
          >
            <Heading
              fontWeight={700}
              fontSize={{ base: "3xl", sm: "4xl", md: "5xl" }}
              lineHeight="shorter"
              bgGradient="linear(to-r, purple.400, pink.400)"
              bgClip="text"
            >
              Master AI Skills Through Real Collaboration
            </Heading>
            <Text
              color="gray.300"
              maxW="2xl"
              fontSize={{ base: "lg", md: "xl" }}
            >
              Modern AI Pro revolutionizes professional upskilling through intelligent pairing and adaptive learning,
              creating an unprecedented collaborative coding ecosystem where professionals grow together.
            </Text>
            <Stack
              direction={{ base: "column", sm: "row" }}
              spacing={4}
              justify="center"
            >
              <Button
                as={RouterLink}
                to="/login"
                rounded="full"
                size="lg"
                fontWeight="bold"
                px={6}
                colorScheme="purple"
                bg="purple.500"
                _hover={{ bg: "purple.600" }}
              >
                Get Started
              </Button>
              <Button
                rounded="full"
                size="lg"
                fontWeight="bold"
                px={6}
                leftIcon={<FaCode />}
                colorScheme="whiteAlpha"
                variant="outline"
                onClick={() => scrollToSection(featuresRef)}
              >
                Learn More
              </Button>
            </Stack>
          </Stack>
        </Container>
      </Box>

      {/* Features Section */}
      <Box py={20} bg="gray.900" ref={featuresRef}>
        <Container maxW="container.xl">
          <VStack spacing={12}>
            <VStack spacing={2} textAlign="center">
              <Heading 
                as="h2" 
                size="xl" 
                bgGradient="linear(to-r, purple.400, pink.400)"
                bgClip="text"
              >
                Why Choose Modern AI Pro?
              </Heading>
              <Text fontSize="lg" color="gray.400">
                Accelerate your AI skills with our innovative platform
              </Text>
            </VStack>
            <SimpleGrid columns={{ base: 1, md: 2, lg: 3 }} spacing={10}>
              <Feature
                icon={FaLaptopCode}
                title="Pair Programming"
                text="Built-in collaborative coding environment with real-time video/audio communication."
              />
              <Feature
                icon={FaTrophy}
                title="ELO Rating System"
                text="Chess-like competitive ranking with smart pairing algorithm for skill comparison."
              />
              <Feature
                icon={FaChartLine}
                title="Personalized Learning"
                text="AI-driven curriculum customization based on your strengths and areas for improvement."
              />
              <Feature
                icon={FaRocket}
                title="Daily Challenges"
                text="Time-bound coding challenges with difficulty adaptation for continuous skill improvement."
              />
              <Feature
                icon={FaUsers}
                title="Learning Pods"
                text="Form groups of 3-5 users for collaborative projects and enhanced learning experiences."
              />
              <Feature
                icon={FaCode}
                title="Comprehensive Courses"
                text="Complete library of courses, guides, and implementation plans for AI mastery."
              />
            </SimpleGrid>
          </VStack>
        </Container>
      </Box>

      {/* Pricing Section */}
      <Box py={20} bg={useColorModeValue("gray.800", "gray.900")} ref={pricingRef}>
        <Container maxW="container.xl">
          <VStack spacing={12}>
            <VStack spacing={2} textAlign="center">
              <Heading 
                as="h2" 
                size="xl" 
                bgGradient="linear(to-r, purple.400, pink.400)"
                bgClip="text"
              >
                Choose Your Plan
              </Heading>
              <Text fontSize="lg" color="gray.400">
                Simple, transparent pricing to fit your learning needs
              </Text>
            </VStack>
            <SimpleGrid columns={{ base: 1, md: 3 }} spacing={10} alignItems="flex-start">
              <PricingCard
                title="Free"
                price="0"
                features={[
                  "AI Search Interface",
                  "Limited Content Access",
                  "Skills Assessment",
                  "Basic Progress Tracking",
                  "Usage Quota",
                ]}
                buttonText="Start Free"
              />
              <PricingCard
                title="Basic"
                price="30"
                features={[
                  "Full Course Access",
                  "Pair Programming",
                  "AI Challenges",
                  "ELO Rating System",
                  "Skills Visualization",
                  "Community Features",
                ]}
                buttonText="Subscribe Now"
                isPopular={true}
              />
              <PricingCard
                title="Premium"
                price="500"
                features={[
                  "Live Workshops",
                  "Priority Matching",
                  "Advanced Projects",
                  "Personalized Learning Path",
                  "Live Polling",
                  "Recorded Sessions",
                ]}
                buttonText="Go Premium"
              />
            </SimpleGrid>
          </VStack>
        </Container>
      </Box>

      {/* CTA Section */}
      <Box py={16} bgGradient="linear(to-b, purple.900, gray.900)">
        <Container maxW="container.xl">
          <Stack
            direction={{ base: "column", md: "row" }}
            spacing={10}
            align="center"
            justify="space-between"
            bg="gray.800"
            p={8}
            rounded="xl"
            boxShadow="xl"
          >
            <VStack align="flex-start" spacing={4} maxW="lg">
              <Heading size="lg" color="white">
                Ready to accelerate your AI career?
              </Heading>
              <Text color="gray.400">
                Join over 10,000 professionals already transforming their skills with our platform.
              </Text>
            </VStack>
            <Button
              as={RouterLink}
              to="/login"
              colorScheme="purple"
              size="lg"
              rounded="full"
              px={8}
              _hover={{ transform: "translateY(-2px)" }}
            >
              Get Started Today
            </Button>
          </Stack>
        </Container>
      </Box>

      {/* Footer */}
      <Box bg="gray.900" color="gray.400" py={8} ref={aboutRef}>
        <Container maxW="container.xl">
          <SimpleGrid columns={{ base: 1, md: 3 }} spacing={8}>
            <VStack align="flex-start">
              <Heading size="md" color="white" mb={2}>
                Modern AI Pro
              </Heading>
              <Text>Revolutionizing AI education through collaboration and competition.</Text>
            </VStack>
            <VStack align="flex-start">
              <Heading size="md" color="white" mb={2}>
                Quick Links
              </Heading>
              <Link _hover={{ color: "white", cursor: "pointer" }} onClick={() => scrollToSection(featuresRef)}>Features</Link>
              <Link _hover={{ color: "white", cursor: "pointer" }} onClick={() => scrollToSection(pricingRef)}>Pricing</Link>
              <Link _hover={{ color: "white", cursor: "pointer" }} onClick={() => scrollToSection(aboutRef)}>About Us</Link>
              <Text _hover={{ color: "white" }}>Contact</Text>
            </VStack>
            <VStack align="flex-start">
              <Heading size="md" color="white" mb={2}>
                Connect With Us
              </Heading>
              <Text _hover={{ color: "white" }}>Twitter</Text>
              <Text _hover={{ color: "white" }}>LinkedIn</Text>
              <Text _hover={{ color: "white" }}>Discord</Text>
              <Text _hover={{ color: "white" }}>GitHub</Text>
            </VStack>
          </SimpleGrid>
          <Text mt={12} textAlign="center">
            © {new Date().getFullYear()} Modern AI Pro. All rights reserved.
          </Text>
        </Container>
      </Box>
    </Box>
  );
};

export default LandingPage;