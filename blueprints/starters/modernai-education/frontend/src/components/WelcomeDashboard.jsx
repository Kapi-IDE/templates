import React, { useEffect, useRef } from 'react';
import { Box, Flex, Heading, Text, Button, VStack, HStack, Image } from '@chakra-ui/react';
import { useNavigate } from 'react-router-dom';
import { BASE_TITLE } from '../Constants';
import Logo from './Logo';

const WelcomeDashboard = () => {
  const canvasRef = useRef(null);
  const navigate = useNavigate();
  
  // Get user's first name from localStorage
  const firstName = localStorage.getItem('first_name') || 'Modern AI Pro Learner';
  
  useEffect(() => {
    document.title = `Welcome | ${BASE_TITLE}`;
    
    const canvas = canvasRef.current;
    if (!canvas) return;
    
    const ctx = canvas.getContext('2d');
    const width = canvas.width = window.innerWidth;
    const height = canvas.height = window.innerHeight;
    
    // Confetti pieces array
    const confetti = [];
    
    // Animation control
    let animationFrameId;
    let isAnimating = true;
    
    // Confetti colors - using our theme colors (purple tones)
    const colors = ['#ffffff', '#9333ea', '#6b21a8', '#a855f7', '#c084fc'];
    
    // Create confetti pieces
    const createConfetti = () => {
      for (let i = 0; i < 200; i++) {
        confetti.push({
          x: Math.random() * width,
          y: Math.random() * height - height,
          width: Math.random() * 10 + 5,
          height: Math.random() * 10 + 5,
          speed: Math.random() * 3 + 2,
          color: colors[Math.floor(Math.random() * colors.length)],
          rotation: Math.random() * 360,
          rotationSpeed: (Math.random() - 0.5) * 2,
          oscillationSpeed: Math.random() * 0.5 + 0.5,
          oscillationAmplitude: Math.random() * 5
        });
      }
    };
    
    // Animation loop
    const animate = () => {
      if (!isAnimating) {
        ctx.clearRect(0, 0, width, height);
        return;
      }
      
      ctx.clearRect(0, 0, width, height);
      
      confetti.forEach((piece, index) => {
        // Update position
        piece.y += piece.speed;
        piece.x += Math.sin(piece.y * piece.oscillationSpeed) * piece.oscillationAmplitude;
        piece.rotation += piece.rotationSpeed;
        
        // Draw confetti piece
        ctx.save();
        ctx.translate(piece.x, piece.y);
        ctx.rotate((piece.rotation * Math.PI) / 180);
        
        ctx.fillStyle = piece.color;
        ctx.fillRect(-piece.width / 2, -piece.height / 2, piece.width, piece.height);
        
        ctx.restore();
        
        // Remove pieces that are out of screen
        if (piece.y > height) {
          // Put the piece back at the top
          piece.y = -piece.height;
          piece.x = Math.random() * width;
        }
      });
      
      // Continue animation
      animationFrameId = requestAnimationFrame(animate);
    };
    
    // Initial confetti creation
    createConfetti();
    
    // Start animation
    animate();
    
    // Stop confetti after 10 seconds
    const confettiTimer = setTimeout(() => {
      isAnimating = false;
      cancelAnimationFrame(animationFrameId);
      ctx.clearRect(0, 0, width, height);
    }, 10000);
    
    // Handle window resize
    const handleResize = () => {
      canvas.width = window.innerWidth;
      canvas.height = window.innerHeight;
    };
    
    window.addEventListener('resize', handleResize);
    
    // Cleanup
    return () => {
      window.removeEventListener('resize', handleResize);
      clearTimeout(confettiTimer);
      cancelAnimationFrame(animationFrameId);
      isAnimating = false;
    };
  }, []);

  const handleContinueLearning = () => {
    navigate('/learning-paths');
  };

  const handlePairProgramming = () => {
    navigate('/pair-programming');
  };

  const handleExploreWorkshops = () => {
    navigate('/workshops');
  };

  return (
    <Flex
      direction="column"
      align="center"
      justify="center"
      minH="100vh"
      position="relative"
      bg="gray.900" // Dark background
      color="white"
      overflow="hidden"
    >
      <canvas
        ref={canvasRef}
        style={{
          position: "absolute",
          width: "100%",
          height: "100%",
          zIndex: 0
        }}
      />
      
      <Box zIndex={1} textAlign="center" p={8} maxW="900px" mx="auto">
        <VStack spacing={6} mb={10}>
          <Logo fontSize="100px" color="white" />
          <Heading as="h1" size="2xl" color="white" textShadow="0 0 10px rgba(0,0,0,0.3)">
            Welcome back, {firstName}!
          </Heading>
          <Text fontSize="xl" color="white">
            Ready to continue your AI mastery journey?
          </Text>
        </VStack>
        
        <Box 
          bg="rgba(255,255,255,0.05)" 
          backdropFilter="blur(10px)" 
          borderRadius="xl" 
          p={6} 
          mb={8}
          boxShadow="0 8px 32px rgba(0,0,0,0.2)"
          borderWidth="1px"
          borderColor="purple.700"
        >
          <VStack spacing={4} align="stretch">
            <Heading as="h3" size="lg" mb={4} color="white">
              Your Learning Dashboard
            </Heading>
            
            <HStack justify="space-between" flexWrap="wrap">
              <VStack align="flex-start" minW="200px" p={3}>
                <Text fontSize="md" color="gray.400">Current ELO Rating</Text>
                <Text fontSize="2xl" color="white" fontWeight="bold">1250</Text>
              </VStack>
              
              <VStack align="flex-start" minW="200px" p={3}>
                <Text fontSize="md" color="gray.400">Challenges Completed</Text>
                <Text fontSize="2xl" color="white" fontWeight="bold">12</Text>
              </VStack>
              
              <VStack align="flex-start" minW="200px" p={3}>
                <Text fontSize="md" color="gray.400">Current Streak</Text>
                <Text fontSize="2xl" color="white" fontWeight="bold">3 days</Text>
              </VStack>
            </HStack>
          </VStack>
        </Box>
        
        <Flex gap={5} mt={10} justify="center" wrap="wrap">
          <Button 
            colorScheme="purple" 
            size="lg"
            height="70px"
            width="200px"
            boxShadow="0 4px 8px rgba(0,0,0,0.3)"
            _hover={{ transform: 'translateY(-3px)', boxShadow: '0 6px 12px rgba(0,0,0,0.4)' }}
            transition="all 0.2s"
            onClick={handleContinueLearning}
          >
            Continue Learning
          </Button>
          
          <Button 
            bg="#4c1d95"
            color="white"
            size="lg"
            height="70px"
            width="200px"
            boxShadow="0 4px 8px rgba(0,0,0,0.3)"
            _hover={{ bg: '#6b21a8', transform: 'translateY(-3px)' }}
            transition="all 0.2s"
            onClick={handlePairProgramming}
          >
            Pair Programming
          </Button>
          
          <Button 
            bg="rgba(255,255,255,0.15)"
            color="white"
            size="lg"
            height="70px"
            width="200px"
            boxShadow="0 4px 8px rgba(0,0,0,0.3)"
            _hover={{ bg: 'rgba(255,255,255,0.25)', transform: 'translateY(-3px)' }}
            transition="all 0.2s"
            onClick={handleExploreWorkshops}
          >
            Explore Workshops
          </Button>
        </Flex>
        
        <Text mt={16} fontSize="sm" color="gray.400">
          Your personalized learning path is updated based on your recent activity
        </Text>
      </Box>
    </Flex>
  );
};

export default WelcomeDashboard;