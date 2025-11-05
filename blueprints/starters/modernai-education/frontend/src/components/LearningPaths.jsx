import React, { useState, useEffect } from 'react';
import {
  Box,
  Heading,
  Text,
  SimpleGrid,
  VStack,
  HStack,
  Badge,
  Progress,
  Button,
  useColorModeValue,
  Flex,
  Icon,
  Divider,
  Tag,
  TagLabel,
  TagLeftIcon,
  Skeleton,
} from '@chakra-ui/react';
import { FiActivity, FiAward, FiBarChart2, FiLock, FiUnlock, FiCheckCircle, FiClock, FiArrowRight } from 'react-icons/fi';
import { BASE_TITLE } from '../Constants';

// Mock data - would come from API
const learningPathsMock = [
  {
    id: 1,
    title: "AI Fundamentals",
    description: "Master the core concepts of artificial intelligence and machine learning",
    progress: 75,
    level: "Beginner",
    estimatedHours: 20,
    topicsCount: 8,
    completedTopics: 6,
    tags: ["Fundamentals", "Python", "ML Basics"],
    lastActivity: "2 days ago",
    unlocked: true
  },
  {
    id: 2,
    title: "Deep Learning Specialization",
    description: "Explore neural networks, computer vision, and natural language processing",
    progress: 30,
    level: "Intermediate",
    estimatedHours: 40,
    topicsCount: 12,
    completedTopics: 4,
    tags: ["Deep Learning", "TensorFlow", "PyTorch"],
    lastActivity: "1 week ago",
    unlocked: true
  },
  {
    id: 3,
    title: "Generative AI Applications",
    description: "Build practical applications with LLMs, Stable Diffusion, and more",
    progress: 10,
    level: "Advanced",
    estimatedHours: 35,
    topicsCount: 10,
    completedTopics: 1,
    tags: ["LLMs", "Diffusion Models", "Fine-Tuning"],
    lastActivity: "3 days ago",
    unlocked: true
  },
  {
    id: 4,
    title: "Reinforcement Learning",
    description: "Learn the principles of RL and implement algorithms from scratch",
    progress: 0,
    level: "Advanced",
    estimatedHours: 45,
    topicsCount: 15,
    completedTopics: 0,
    tags: ["RL", "PyTorch", "Gymnasium"],
    lastActivity: null,
    unlocked: false
  },
];

// Learning path card component
const LearningPathCard = ({ path }) => {
  const cardBg = useColorModeValue('white', 'gray.800');
  const borderColor = useColorModeValue('gray.200', 'gray.700');
  const progressColor = path.progress > 70 ? "green.400" : path.progress > 30 ? "blue.400" : "purple.400";
  
  return (
    <Box
      bg={cardBg}
      borderWidth="1px"
      borderColor={borderColor}
      borderRadius="lg"
      overflow="hidden"
      p={5}
      boxShadow="md"
      position="relative"
      transition="all 0.3s"
      _hover={{ transform: 'translateY(-5px)', boxShadow: 'lg' }}
    >
      {!path.unlocked && (
        <Box
          position="absolute"
          top="10px"
          right="10px"
          zIndex="1"
        >
          <Icon as={FiLock} color="gray.500" />
        </Box>
      )}
      
      <VStack align="start" spacing={4}>
        <Heading as="h3" size="md">{path.title}</Heading>
        <Text color="gray.500" noOfLines={2}>{path.description}</Text>
        
        <HStack spacing={2} flexWrap="wrap">
          {path.tags.map(tag => (
            <Tag key={tag} size="sm" colorScheme="purple" variant="subtle" mt={1}>
              <TagLabel>{tag}</TagLabel>
            </Tag>
          ))}
        </HStack>
        
        <Box w="100%">
          <Flex justify="space-between" mb={1}>
            <Text fontSize="sm" fontWeight="bold">{path.progress}% Complete</Text>
            <Text fontSize="sm">{path.completedTopics}/{path.topicsCount} Topics</Text>
          </Flex>
          <Progress value={path.progress} colorScheme={path.progress > 70 ? "green" : path.progress > 30 ? "blue" : "purple"} size="sm" borderRadius="full" />
        </Box>
        
        <Divider />
        
        <HStack justify="space-between" w="100%">
          <Tag size="sm" variant="subtle" colorScheme={path.level === "Beginner" ? "green" : path.level === "Intermediate" ? "blue" : "purple"}>
            <TagLeftIcon as={FiBarChart2} />
            <TagLabel>{path.level}</TagLabel>
          </Tag>
          
          <HStack>
            <Icon as={FiClock} color="gray.500" />
            <Text fontSize="xs" color="gray.500">{path.estimatedHours}h</Text>
          </HStack>
        </HStack>
        
        <Button 
          rightIcon={<FiArrowRight />} 
          colorScheme="purple" 
          size="sm" 
          isFullWidth
          disabled={!path.unlocked}
        >
          {path.progress > 0 ? "Continue" : "Start"} Learning
        </Button>
      </VStack>
    </Box>
  );
};

// Recommended next steps component
const RecommendedNextSteps = () => {
  const cardBg = useColorModeValue('white', 'gray.800');
  const borderColor = useColorModeValue('gray.200', 'gray.700');
  
  return (
    <Box
      bg={cardBg}
      borderWidth="1px"
      borderColor={borderColor}
      borderRadius="lg"
      p={5}
      boxShadow="md"
    >
      <Heading as="h3" size="md" mb={4}>Recommended Next Steps</Heading>
      
      <VStack align="start" spacing={4} w="100%">
        <HStack w="100%" justify="space-between" p={2} bg="purple.50" _dark={{ bg: "purple.900" }} borderRadius="md">
          <HStack>
            <Icon as={FiActivity} color="purple.500" boxSize={5} />
            <Text fontWeight="medium">Complete "Neural Networks Basics"</Text>
          </HStack>
          <Button size="sm" colorScheme="purple" variant="outline">Resume</Button>
        </HStack>
        
        <HStack w="100%" justify="space-between" p={2} bg="blue.50" _dark={{ bg: "blue.900" }} borderRadius="md">
          <HStack>
            <Icon as={FiBarChart2} color="blue.500" boxSize={5} />
            <Text fontWeight="medium">Take Weekly Assessment Quiz</Text>
          </HStack>
          <Button size="sm" colorScheme="blue" variant="outline">Start</Button>
        </HStack>
        
        <HStack w="100%" justify="space-between" p={2} bg="green.50" _dark={{ bg: "green.900" }} borderRadius="md">
          <HStack>
            <Icon as={FiAward} color="green.500" boxSize={5} />
            <Text fontWeight="medium">Schedule Pair Programming Session</Text>
          </HStack>
          <Button size="sm" colorScheme="green" variant="outline">Schedule</Button>
        </HStack>
      </VStack>
    </Box>
  );
};

// Learning stats component
const LearningStats = () => {
  const statBg = useColorModeValue('white', 'gray.800');
  const borderColor = useColorModeValue('gray.200', 'gray.700');
  
  return (
    <SimpleGrid columns={{ base: 1, md: 4 }} gap={4}>
      <Box bg={statBg} p={4} borderRadius="lg" borderWidth="1px" borderColor={borderColor} boxShadow="sm">
        <Text color="gray.500" fontSize="sm">Current Streak</Text>
        <HStack>
          <Heading size="lg">7</Heading>
          <Text color="gray.500">days</Text>
        </HStack>
      </Box>
      
      <Box bg={statBg} p={4} borderRadius="lg" borderWidth="1px" borderColor={borderColor} boxShadow="sm">
        <Text color="gray.500" fontSize="sm">Topics Completed</Text>
        <HStack>
          <Heading size="lg">11</Heading>
          <Text color="gray.500">of 45</Text>
        </HStack>
      </Box>
      
      <Box bg={statBg} p={4} borderRadius="lg" borderWidth="1px" borderColor={borderColor} boxShadow="sm">
        <Text color="gray.500" fontSize="sm">Hours Invested</Text>
        <HStack>
          <Heading size="lg">28</Heading>
          <Text color="gray.500">hours</Text>
        </HStack>
      </Box>
      
      <Box bg={statBg} p={4} borderRadius="lg" borderWidth="1px" borderColor={borderColor} boxShadow="sm">
        <Text color="gray.500" fontSize="sm">Skill Growth</Text>
        <HStack>
          <Heading size="lg">+34%</Heading>
          <Icon as={FiActivity} color="green.500" />
        </HStack>
      </Box>
    </SimpleGrid>
  );
};

// Main Component
const LearningPaths = () => {
  const [isLoading, setIsLoading] = useState(true);
  const [learningPaths, setLearningPaths] = useState([]);
  
  useEffect(() => {
    document.title = `Learning Paths | ${BASE_TITLE}`;
    
    // Simulate API call
    setTimeout(() => {
      setLearningPaths(learningPathsMock);
      setIsLoading(false);
    }, 1000);
  }, []);
  
  return (
    <Box p={4}>
      <VStack spacing={8} align="stretch">
        <Box>
          <Heading size="xl" mb={2}>Your Learning Journey</Heading>
          <Text color="gray.500">Continue your personalized learning path to AI mastery</Text>
        </Box>
        
        <LearningStats />
        
        <Divider />
        
        <Box>
          <Flex justify="space-between" align="center" mb={4}>
            <Heading size="lg">Learning Paths</Heading>
            <Button variant="ghost" rightIcon={<FiArrowRight />}>View All</Button>
          </Flex>
          
          {isLoading ? (
            <SimpleGrid columns={{ base: 1, md: 2, lg: 3 }} spacing={6}>
              {[1, 2, 3].map(i => (
                <Box key={i}>
                  <Skeleton height="300px" borderRadius="lg" />
                </Box>
              ))}
            </SimpleGrid>
          ) : (
            <SimpleGrid columns={{ base: 1, md: 2, lg: 3 }} spacing={6}>
              {learningPaths.map(path => (
                <LearningPathCard key={path.id} path={path} />
              ))}
            </SimpleGrid>
          )}
        </Box>
        
        <SimpleGrid columns={{ base: 1, md: 2 }} spacing={6}>
          <RecommendedNextSteps />
          
          <Box>
            <Heading as="h3" size="md" mb={4}>Learning Achievements</Heading>
            <VStack align="start" spacing={4} bg={useColorModeValue('white', 'gray.800')} p={5} borderRadius="lg" borderWidth="1px" boxShadow="md">
              <HStack>
                <Icon as={FiCheckCircle} color="green.500" />
                <Text>Completed "Introduction to AI" path</Text>
              </HStack>
              <HStack>
                <Icon as={FiCheckCircle} color="green.500" />
                <Text>7-day learning streak</Text>
              </HStack>
              <HStack>
                <Icon as={FiCheckCircle} color="green.500" />
                <Text>First pair programming session</Text>
              </HStack>
              <Button colorScheme="purple" variant="ghost" size="sm" alignSelf="flex-end">
                View All Achievements
              </Button>
            </VStack>
          </Box>
        </SimpleGrid>
      </VStack>
    </Box>
  );
};

export default LearningPaths;