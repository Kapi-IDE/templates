import React, { useEffect, useRef } from 'react';
import { Box, Flex, Heading, Text, Button } from '@chakra-ui/react';

const TestCelebration = () => {
  const canvasRef = useRef(null);
  
  useEffect(() => {
    const canvas = canvasRef.current;
    if (!canvas) return;
    
    const ctx = canvas.getContext('2d');
    const width = canvas.width = window.innerWidth;
    const height = canvas.height = window.innerHeight;
    
    // Confetti pieces array
    const confetti = [];
    
    // Confetti colors
    const colors = ['#ffffff', '#ff5555', '#1a4789', '#FFA500', '#00CED1'];
    
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
      requestAnimationFrame(animate);
    };
    
    // Initial confetti creation
    createConfetti();
    
    // Start animation
    animate();
    
    // Handle window resize
    const handleResize = () => {
      canvas.width = window.innerWidth;
      canvas.height = window.innerHeight;
    };
    
    window.addEventListener('resize', handleResize);
    
    // Cleanup
    return () => {
      window.removeEventListener('resize', handleResize);
    };
  }, []);

  return (
    <Flex
      direction="column"
      align="center"
      justify="center"
      minH="100vh"
      position="relative"
      bg="#1a4789" // Modern AI Pro blue
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
      
      <Box zIndex={1} textAlign="center" p={8} maxW="800px" mx="auto">
        <Heading as="h1" size="4xl" mb={6} color="white" textShadow="0 0 10px rgba(0,0,0,0.3)">
          Congratulations!!!
        </Heading>
        <Text fontSize="3xl" mb={10} color="white" fontWeight="bold">
          Level Up! You've mastered AI Pair Programming
        </Text>
        
        <Box 
          bg="rgba(255,255,255,0.15)" 
          backdropFilter="blur(10px)" 
          borderRadius="xl" 
          p={6} 
          mb={8}
          boxShadow="0 8px 32px rgba(0,0,0,0.2)"
        >
          <Heading as="h3" size="lg" mb={4} color="white">
            ELO Rating: 1850 (+75)
          </Heading>
          <Text fontSize="xl" color="white" mb={3}>
            You've reached the top 5% of coders in your cohort!
          </Text>
          <Text fontSize="md" color="white" opacity={0.8}>
            Unlock advanced challenges and mentor privileges
          </Text>
        </Box>
        
        <Flex gap={4} mt={8} justify="center" wrap="wrap">
          <Button 
            colorScheme="red" 
            size="lg" 
            boxShadow="0 4px 8px rgba(0,0,0,0.2)"
            _hover={{ transform: 'translateY(-2px)', boxShadow: '0 6px 12px rgba(0,0,0,0.3)' }}
            transition="all 0.2s"
          >
            Practice Now
          </Button>
          <Button 
            bg="rgba(255,255,255,0.2)"
            color="white"
            size="lg" 
            boxShadow="0 4px 8px rgba(0,0,0,0.2)"
            _hover={{ bg: 'rgba(255,255,255,0.3)', transform: 'translateY(-2px)' }}
            transition="all 0.2s"
          >
            Share Achievement
          </Button>
          <Button 
            bg="#ff5555"
            color="white"
            size="lg" 
            boxShadow="0 4px 8px rgba(0,0,0,0.2)"
            _hover={{ bg: '#ff3333', transform: 'translateY(-2px)' }}
            transition="all 0.2s"
          >
            Next Challenge
          </Button>
        </Flex>
      </Box>
    </Flex>
  );
};

export default TestCelebration;
