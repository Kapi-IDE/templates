import React, { useState, useEffect } from 'react';
import {
  Box,
  Heading,
  Text,
  SimpleGrid,
  VStack,
  HStack,
  Button,
  Badge,
  Tag,
  Flex,
  Icon,
  Image,
  Divider,
  Avatar,
  AvatarGroup,
  useColorModeValue,
  Tabs,
  TabList,
  TabPanels,
  Tab,
  TabPanel,
  Menu,
  MenuButton,
  MenuList,
  MenuItem,
  Skeleton,
} from '@chakra-ui/react';
import { 
  FiCalendar, 
  FiMapPin, 
  FiClock, 
  FiUsers, 
  FiDollarSign, 
  FiStar, 
  FiVideo, 
  FiFilter, 
  FiChevronDown,
  FiCheck,
  FiX,
  FiBookmark,
  FiGlobe,
  FiDownload
} from 'react-icons/fi';
import { BASE_TITLE } from '../Constants';

// Mock data - would come from API
const workshopsData = [
  {
    id: 1,
    title: "Building Production-Ready LLM Applications",
    banner: "https://images.unsplash.com/photo-1524419986249-348e8fa6ad4a?w=800&auto=format&fit=crop",
    description: "Learn how to develop, deploy, and maintain large language model applications at scale with industry best practices",
    startDate: "2023-07-10T09:00:00",
    endDate: "2023-07-12T17:00:00",
    geography: "Virtual",
    isVirtual: true,
    cost: 149.99,
    capacity: 50,
    enrolled: 38,
    tags: ["LLMs", "Production", "Deployment"],
    level: "Advanced",
    instructors: [
      {
        id: 101,
        name: "Dr. Maya Chen",
        title: "AI Research Lead at TechCorp",
        avatar: "https://i.pravatar.cc/150?u=maya"
      },
      {
        id: 102,
        name: "James Wilson",
        title: "Senior ML Engineer",
        avatar: "https://i.pravatar.cc/150?u=james"
      }
    ],
    rating: 4.9,
    reviews: 42,
    recorded: true,
    status: "open"
  },
  {
    id: 2,
    title: "Data Engineering for ML Pipelines",
    banner: "https://images.unsplash.com/photo-1581092918056-0c4c3acd3789?w=800&auto=format&fit=crop",
    description: "Master the art of building robust data pipelines for training and serving machine learning models",
    startDate: "2023-07-15T10:00:00",
    endDate: "2023-07-16T16:00:00",
    geography: "New York, NY",
    isVirtual: false,
    cost: 299.99,
    capacity: 30,
    enrolled: 27,
    tags: ["Data Engineering", "ETL", "MLOps"],
    level: "Intermediate",
    instructors: [
      {
        id: 103,
        name: "Sophia Rodriguez",
        title: "Principal Data Engineer",
        avatar: "https://i.pravatar.cc/150?u=sophia"
      }
    ],
    rating: 4.8,
    reviews: 36,
    recorded: true,
    status: "almost-full"
  },
  {
    id: 3,
    title: "Reinforcement Learning from Human Feedback",
    banner: "https://images.unsplash.com/photo-1591696331111-ef9586a5b17a?w=800&auto=format&fit=crop",
    description: "Explore RLHF techniques used to train and align large language models with human preferences",
    startDate: "2023-08-05T09:00:00",
    endDate: "2023-08-07T17:00:00",
    geography: "Virtual",
    isVirtual: true,
    cost: 199.99,
    capacity: 40,
    enrolled: 18,
    tags: ["RLHF", "LLMs", "Alignment"],
    level: "Advanced",
    instructors: [
      {
        id: 104,
        name: "Dr. Marcus Johnson",
        title: "AI Researcher",
        avatar: "https://i.pravatar.cc/150?u=marcus"
      },
      {
        id: 105,
        name: "Olivia Park",
        title: "ML Engineer",
        avatar: "https://i.pravatar.cc/150?u=olivia"
      }
    ],
    rating: 4.7,
    reviews: 12,
    recorded: true,
    status: "open"
  },
  {
    id: 4,
    title: "Computer Vision for Autonomous Systems",
    banner: "https://images.unsplash.com/photo-1555661059-7e755c1c3c1d?w=800&auto=format&fit=crop",
    description: "Implement state-of-the-art vision algorithms for robotics and autonomous vehicle applications",
    startDate: "2023-07-22T09:00:00",
    endDate: "2023-07-24T17:00:00",
    geography: "San Francisco, CA",
    isVirtual: false,
    cost: 399.99,
    capacity: 25,
    enrolled: 25,
    tags: ["Computer Vision", "Robotics", "Object Detection"],
    level: "Advanced",
    instructors: [
      {
        id: 106,
        name: "Dr. Takashi Kim",
        title: "Vision Research Lead",
        avatar: "https://i.pravatar.cc/150?u=takashi"
      }
    ],
    rating: 4.9,
    reviews: 28,
    recorded: false,
    status: "full"
  },
  {
    id: 5,
    title: "Introduction to Deep Learning",
    banner: "https://images.unsplash.com/photo-1501854140801-50d01698950b?w=800&auto=format&fit=crop",
    description: "A comprehensive introduction to neural networks, backpropagation, and popular architectures",
    startDate: "2023-08-12T10:00:00",
    endDate: "2023-08-13T16:00:00",
    geography: "Virtual",
    isVirtual: true,
    cost: 99.99,
    capacity: 100,
    enrolled: 58,
    tags: ["Deep Learning", "Neural Networks", "Beginner"],
    level: "Beginner",
    instructors: [
      {
        id: 107,
        name: "Sarah Johnson",
        title: "AI Educator",
        avatar: "https://i.pravatar.cc/150?u=sarah"
      }
    ],
    rating: 4.8,
    reviews: 86,
    recorded: true,
    status: "open"
  }
];

const myWorkshopsData = [
  {
    id: 101,
    title: "Advanced NLP Techniques",
    date: "May 15-17, 2023",
    status: "completed",
    certificate: true,
    recordingsAvailable: true
  },
  {
    id: 102,
    title: "Data Engineering for ML Pipelines",
    date: "July 15-16, 2023",
    status: "upcoming",
    paymentComplete: true
  },
  {
    id: 103,
    title: "Introduction to Deep Learning",
    date: "August 12-13, 2023",
    status: "upcoming",
    paymentComplete: true
  }
];

// Workshop Card Component
const WorkshopCard = ({ workshop }) => {
  const cardBg = useColorModeValue('white', 'gray.800');
  const borderColor = useColorModeValue('gray.200', 'gray.700');
  
  // Format dates
  const startDate = new Date(workshop.startDate);
  const endDate = new Date(workshop.endDate);
  
  const formatDate = (date) => {
    return date.toLocaleDateString('en-US', {
      month: 'short',
      day: 'numeric',
      year: 'numeric'
    });
  };
  
  const formattedDateRange = `${formatDate(startDate)} - ${formatDate(endDate)}`;
  
  // Status badge
  const getStatusProps = (status) => {
    switch(status) {
      case 'open':
        return { colorScheme: 'green', text: 'Open for Registration' };
      case 'almost-full':
        return { colorScheme: 'yellow', text: 'Almost Full' };
      case 'full':
        return { colorScheme: 'red', text: 'Sold Out' };
      default:
        return { colorScheme: 'gray', text: status };
    }
  };
  
  const statusProps = getStatusProps(workshop.status);
  
  return (
    <Box
      bg={cardBg}
      borderWidth="1px"
      borderColor={borderColor}
      borderRadius="lg"
      overflow="hidden"
      boxShadow="md"
      transition="all 0.3s"
      _hover={{ transform: 'translateY(-5px)', boxShadow: 'lg' }}
    >
      <Box position="relative">
        <Image
          src={workshop.banner}
          alt={workshop.title}
          objectFit="cover"
          height="180px"
          width="100%"
        />
        <HStack
          position="absolute"
          top="10px"
          right="10px"
          spacing={2}
        >
          {workshop.isVirtual && (
            <Badge colorScheme="blue" borderRadius="full" px={2}>
              <HStack spacing={1}>
                <Icon as={FiVideo} boxSize={3} />
                <Text>Virtual</Text>
              </HStack>
            </Badge>
          )}
          {workshop.recorded && (
            <Badge colorScheme="purple" borderRadius="full" px={2}>
              <HStack spacing={1}>
                <Icon as={FiDownload} boxSize={3} />
                <Text>Recorded</Text>
              </HStack>
            </Badge>
          )}
        </HStack>
        <Badge
          position="absolute"
          bottom="10px"
          left="10px"
          colorScheme={
            workshop.level === 'Beginner' ? 'green' :
            workshop.level === 'Intermediate' ? 'blue' : 'purple'
          }
          fontSize="xs"
          borderRadius="full"
          px={2}
        >
          {workshop.level}
        </Badge>
      </Box>
      
      <Box p={5}>
        <Heading as="h3" size="md" mb={2} noOfLines={1}>
          {workshop.title}
        </Heading>
        
        <Text color="gray.500" fontSize="sm" noOfLines={2} mb={3}>
          {workshop.description}
        </Text>
        
        <HStack mb={3}>
          <Icon as={FiCalendar} color="gray.500" />
          <Text fontSize="sm" color="gray.500">{formattedDateRange}</Text>
        </HStack>
        
        <HStack mb={3}>
          <Icon as={workshop.isVirtual ? FiGlobe : FiMapPin} color="gray.500" />
          <Text fontSize="sm" color="gray.500">{workshop.geography}</Text>
        </HStack>
        
        <HStack spacing={4} mb={4}>
          <HStack>
            <Icon as={FiDollarSign} color="gray.500" />
            <Text fontWeight="bold">${workshop.cost}</Text>
          </HStack>
          
          <HStack>
            <Icon as={FiUsers} color="gray.500" />
            <Text fontSize="sm" color="gray.500">
              {workshop.enrolled}/{workshop.capacity}
            </Text>
          </HStack>
          
          <HStack>
            <Icon as={FiStar} color="yellow.500" />
            <Text fontSize="sm">{workshop.rating} ({workshop.reviews})</Text>
          </HStack>
        </HStack>
        
        <Divider mb={4} />
        
        <HStack justify="space-between" mb={4}>
          <AvatarGroup size="sm" max={2}>
            {workshop.instructors.map(instructor => (
              <Avatar 
                key={instructor.id}
                name={instructor.name} 
                src={instructor.avatar} 
                title={instructor.name}
              />
            ))}
          </AvatarGroup>
          
          <Badge colorScheme={statusProps.colorScheme}>
            {statusProps.text}
          </Badge>
        </HStack>
        
        <Button 
          colorScheme="purple" 
          size="sm" 
          width="100%"
          isDisabled={workshop.status === 'full'}
        >
          {workshop.status === 'full' ? 'Sold Out' : 'Register Now'}
        </Button>
      </Box>
    </Box>
  );
};

// My Workshops List Item Component
const MyWorkshopItem = ({ workshop }) => {
  const itemBg = useColorModeValue('white', 'gray.800');
  const borderColor = useColorModeValue('gray.200', 'gray.700');
  
  const getStatusProps = (status) => {
    switch(status) {
      case 'completed':
        return { icon: FiCheck, color: 'green.500', text: 'Completed' };
      case 'upcoming':
        return { icon: FiCalendar, color: 'blue.500', text: 'Upcoming' };
      case 'in-progress':
        return { icon: FiClock, color: 'yellow.500', text: 'In Progress' };
      default:
        return { icon: FiX, color: 'gray.500', text: status };
    }
  };
  
  const statusProps = getStatusProps(workshop.status);
  
  return (
    <Flex
      bg={itemBg}
      borderWidth="1px"
      borderColor={borderColor}
      borderRadius="lg"
      p={4}
      boxShadow="sm"
      justify="space-between"
      align="center"
    >
      <HStack spacing={4}>
        <Icon as={statusProps.icon} color={statusProps.color} boxSize={5} />
        <Box>
          <Heading as="h4" size="sm">{workshop.title}</Heading>
          <Text fontSize="sm" color="gray.500">{workshop.date}</Text>
        </Box>
      </HStack>
      
      <HStack>
        {workshop.status === 'completed' && (
          <>
            {workshop.certificate && (
              <Button size="sm" colorScheme="green" variant="outline">
                Certificate
              </Button>
            )}
            
            {workshop.recordingsAvailable && (
              <Button size="sm" colorScheme="purple" variant="outline">
                Recordings
              </Button>
            )}
          </>
        )}
        
        {workshop.status === 'upcoming' && (
          <Badge colorScheme="blue">
            {workshop.paymentComplete ? 'Confirmed' : 'Payment Due'}
          </Badge>
        )}
        
        <Button size="sm" variant="ghost">
          Details
        </Button>
      </HStack>
    </Flex>
  );
};

// Main Workshops Component
const Workshops = () => {
  const [isLoading, setIsLoading] = useState(true);
  const [workshops, setWorkshops] = useState([]);
  const [myWorkshops, setMyWorkshops] = useState([]);
  
  useEffect(() => {
    document.title = `Workshops | ${BASE_TITLE}`;
    
    // Simulate API fetch
    setTimeout(() => {
      setWorkshops(workshopsData);
      setMyWorkshops(myWorkshopsData);
      setIsLoading(false);
    }, 1000);
  }, []);
  
  return (
    <Box p={4}>
      <VStack spacing={8} align="stretch">
        <Box>
          <Heading size="xl" mb={2}>AI Workshops</Heading>
          <Text color="gray.500">Learn from industry experts in interactive sessions</Text>
        </Box>
        
        <Tabs colorScheme="purple" variant="enclosed">
          <TabList>
            <Tab>Upcoming Workshops</Tab>
            <Tab>My Workshops</Tab>
          </TabList>
          
          <TabPanels>
            {/* Upcoming Workshops Tab */}
            <TabPanel px={0}>
              <Flex justify="space-between" align="center" mb={4}>
                <HStack>
                  <Menu>
                    <MenuButton as={Button} rightIcon={<FiFilter />} variant="outline" size="sm">
                      Filter
                    </MenuButton>
                    <MenuList>
                      <MenuItem>All Levels</MenuItem>
                      <MenuItem>Beginner</MenuItem>
                      <MenuItem>Intermediate</MenuItem>
                      <MenuItem>Advanced</MenuItem>
                      <MenuItem>Virtual Only</MenuItem>
                      <MenuItem>In-Person Only</MenuItem>
                    </MenuList>
                  </Menu>
                  
                  <Menu>
                    <MenuButton as={Button} rightIcon={<FiChevronDown />} variant="outline" size="sm">
                      Sort By
                    </MenuButton>
                    <MenuList>
                      <MenuItem>Date (Soonest)</MenuItem>
                      <MenuItem>Date (Latest)</MenuItem>
                      <MenuItem>Price (Low to High)</MenuItem>
                      <MenuItem>Price (High to Low)</MenuItem>
                      <MenuItem>Rating</MenuItem>
                    </MenuList>
                  </Menu>
                </HStack>
                
                <HStack>
                  <Button colorScheme="purple" variant="outline" leftIcon={<FiBookmark />}>
                    Saved Workshops
                  </Button>
                </HStack>
              </Flex>
              
              {isLoading ? (
                <SimpleGrid columns={{ base: 1, md: 2, lg: 3 }} spacing={6}>
                  {[1, 2, 3].map(i => (
                    <Skeleton key={i} height="450px" borderRadius="lg" />
                  ))}
                </SimpleGrid>
              ) : (
                <SimpleGrid columns={{ base: 1, md: 2, lg: 3 }} spacing={6}>
                  {workshops.map(workshop => (
                    <WorkshopCard key={workshop.id} workshop={workshop} />
                  ))}
                </SimpleGrid>
              )}
            </TabPanel>
            
            {/* My Workshops Tab */}
            <TabPanel px={0}>
              <Box mb={6}>
                <Heading size="md" mb={4}>Your Workshop Journey</Heading>
                <SimpleGrid columns={{ base: 1, md: 3 }} spacing={6}>
                  <Box bg={useColorModeValue('purple.50', 'purple.900')} p={4} borderRadius="lg">
                    <Text color="gray.500" fontSize="sm">Workshops Completed</Text>
                    <Heading size="xl">1</Heading>
                  </Box>
                  
                  <Box bg={useColorModeValue('blue.50', 'blue.900')} p={4} borderRadius="lg">
                    <Text color="gray.500" fontSize="sm">Upcoming Workshops</Text>
                    <Heading size="xl">2</Heading>
                  </Box>
                  
                  <Box bg={useColorModeValue('green.50', 'green.900')} p={4} borderRadius="lg">
                    <Text color="gray.500" fontSize="sm">Certificates Earned</Text>
                    <Heading size="xl">1</Heading>
                  </Box>
                </SimpleGrid>
              </Box>
              
              <Heading size="md" mb={4}>Your Workshops</Heading>
              {isLoading ? (
                <VStack spacing={4}>
                  {[1, 2, 3].map(i => (
                    <Skeleton key={i} height="80px" width="100%" borderRadius="lg" />
                  ))}
                </VStack>
              ) : (
                <VStack spacing={4}>
                  {myWorkshops.map(workshop => (
                    <MyWorkshopItem key={workshop.id} workshop={workshop} />
                  ))}
                </VStack>
              )}
              
              <Box 
                mt={8} 
                p={5} 
                borderRadius="md" 
                bg={useColorModeValue('gray.100', 'gray.700')}
                borderWidth="1px"
                borderColor={useColorModeValue('gray.200', 'gray.600')}
              >
                <Heading size="md" mb={2}>Workshop Recommendations</Heading>
                <Text mb={4}>Based on your learning path and interests, we recommend these upcoming workshops:</Text>
                <SimpleGrid columns={{ base: 1, md: 2 }} spacing={4}>
                  <HStack 
                    p={3} 
                    bg={useColorModeValue('white', 'gray.800')} 
                    borderRadius="md"
                    borderWidth="1px"
                    borderColor={useColorModeValue('gray.200', 'gray.700')}
                  >
                    <Icon as={FiVideo} color="purple.500" boxSize={5} />
                    <Box>
                      <Text fontWeight="bold">Reinforcement Learning from Human Feedback</Text>
                      <Text fontSize="sm" color="gray.500">August 5-7, 2023</Text>
                    </Box>
                  </HStack>
                  
                  <HStack 
                    p={3} 
                    bg={useColorModeValue('white', 'gray.800')} 
                    borderRadius="md"
                    borderWidth="1px"
                    borderColor={useColorModeValue('gray.200', 'gray.700')}
                  >
                    <Icon as={FiMapPin} color="blue.500" boxSize={5} />
                    <Box>
                      <Text fontWeight="bold">Computer Vision for Medical Applications</Text>
                      <Text fontSize="sm" color="gray.500">September 10-12, 2023</Text>
                    </Box>
                  </HStack>
                </SimpleGrid>
              </Box>
            </TabPanel>
          </TabPanels>
        </Tabs>
      </VStack>
    </Box>
  );
};

export default Workshops;