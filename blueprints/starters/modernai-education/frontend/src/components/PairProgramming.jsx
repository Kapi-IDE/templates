import React, { useState, useEffect } from 'react';
import {
  Box,
  Heading,
  Text,
  Button,
  Flex,
  SimpleGrid,
  VStack,
  HStack,
  Icon,
  Avatar,
  AvatarGroup,
  Badge,
  Divider,
  Tag,
  useColorModeValue,
  Tabs,
  TabList,
  TabPanels,
  Tab,
  TabPanel,
  Skeleton,
  Menu,
  MenuButton,
  MenuList,
  MenuItem,
  Modal,
  ModalOverlay,
  ModalContent,
  ModalHeader,
  ModalBody,
  ModalCloseButton,
  ModalFooter,
  useDisclosure,
  Input,
  Select,
  FormControl,
  FormLabel,
  Switch,
} from '@chakra-ui/react';
import { 
  FiCalendar, 
  FiClock, 
  FiCode, 
  FiUsers, 
  FiStar, 
  FiTrendingUp, 
  FiCheck, 
  FiChevronDown,
  FiFilter,
  FiPlus,
  FiVideo,
  FiMessageSquare,
  FiCpu
} from 'react-icons/fi';
import { BASE_TITLE } from '../Constants';

// Mock data that would come from API
const sessionsData = [
  {
    id: 1,
    title: "Implementing a Transformer Model",
    description: "Collaborate on building a transformer-based language model from scratch using PyTorch",
    skillLevel: "Advanced",
    participants: {
      current: 0,
      max: 2
    },
    duration: 60,
    scheduledFor: "2023-06-17T14:00:00",
    tags: ["PyTorch", "NLP", "Transformers"],
    host: {
      id: 101,
      name: "Alex Chen",
      avatar: "https://i.pravatar.cc/150?u=alex",
      rating: 4.8,
      eloRating: 1875
    }
  },
  {
    id: 2,
    title: "Debugging GANs Training Issues",
    description: "Troubleshoot mode collapse and convergence problems in a generative adversarial network",
    skillLevel: "Intermediate",
    participants: {
      current: 1,
      max: 2
    },
    duration: 45,
    scheduledFor: "2023-06-17T16:30:00",
    tags: ["TensorFlow", "GANs", "Debugging"],
    host: {
      id: 102,
      name: "Sarah Johnson",
      avatar: "https://i.pravatar.cc/150?u=sarah",
      rating: 4.6,
      eloRating: 1720
    },
    participants: [
      {
        id: 103,
        name: "Michael Brown",
        avatar: "https://i.pravatar.cc/150?u=michael"
      }
    ]
  },
  {
    id: 3,
    title: "Fine-tuning GPT Models",
    description: "Explore techniques for efficient fine-tuning of large language models on custom datasets",
    skillLevel: "Advanced",
    participants: {
      current: 2,
      max: 4
    },
    duration: 90,
    scheduledFor: "2023-06-18T10:00:00",
    tags: ["GPT", "LLMs", "Fine-tuning"],
    host: {
      id: 104,
      name: "David Park",
      avatar: "https://i.pravatar.cc/150?u=david",
      rating: 4.9,
      eloRating: 1950
    },
    participants: [
      {
        id: 105,
        name: "Emily Wilson",
        avatar: "https://i.pravatar.cc/150?u=emily"
      },
      {
        id: 106,
        name: "Robert Martinez",
        avatar: "https://i.pravatar.cc/150?u=robert"
      }
    ]
  },
  {
    id: 4,
    title: "AI for Graph Neural Networks",
    description: "Implement GNNs for molecular property prediction and social network analysis",
    skillLevel: "Intermediate",
    participants: {
      current: 0,
      max: 3
    },
    duration: 60,
    scheduledFor: "2023-06-19T15:00:00",
    tags: ["GNNs", "PyTorch", "Graph Data"],
    host: {
      id: 107,
      name: "Jennifer Lee",
      avatar: "https://i.pravatar.cc/150?u=jennifer",
      rating: 4.7,
      eloRating: 1820
    }
  }
];

const matchHistoryData = [
  {
    id: 101,
    partner: {
      id: 201,
      name: "Olivia Smith",
      avatar: "https://i.pravatar.cc/150?u=olivia",
      eloRating: 1790
    },
    date: "2023-06-10",
    challenge: "Implementing a CNN for Image Classification",
    duration: 75,
    rating: 5,
    eloChange: "+15"
  },
  {
    id: 102,
    partner: {
      id: 202,
      name: "Noah Johnson",
      avatar: "https://i.pravatar.cc/150?u=noah",
      eloRating: 1840
    },
    date: "2023-06-08",
    challenge: "Building a Recommendation System with Matrix Factorization",
    duration: 60,
    rating: 4,
    eloChange: "+8"
  },
  {
    id: 103,
    partner: {
      id: 203,
      name: "Emma Williams",
      avatar: "https://i.pravatar.cc/150?u=emma",
      eloRating: 1650
    },
    date: "2023-06-05",
    challenge: "Time Series Forecasting with LSTM Networks",
    duration: 90,
    rating: 4,
    eloChange: "+12"
  }
];

const aiAgentsData = [
  {
    id: 501,
    name: "TensorTutor",
    avatar: "/logo192.png",
    specialty: "Neural Network Architectures",
    eloRating: 1900,
    availability: "24/7",
    description: "Specialized in helping with model architecture design and optimization"
  },
  {
    id: 502,
    name: "PyAssist",
    avatar: "/logo192.png",
    specialty: "PyTorch Implementation",
    eloRating: 1850,
    availability: "24/7",
    description: "Expert in translating concepts to PyTorch code and debugging issues"
  },
  {
    id: 503,
    name: "DataSage",
    avatar: "/logo192.png",
    specialty: "Data Processing & Augmentation",
    eloRating: 1820,
    availability: "24/7",
    description: "Focused on efficient data pipelines and preprocessing techniques"
  }
];

// Session Card Component
const SessionCard = ({ session }) => {
  const cardBg = useColorModeValue('white', 'gray.800');
  const borderColor = useColorModeValue('gray.200', 'gray.700');
  
  // Format date and time
  const sessionDate = new Date(session.scheduledFor);
  const formattedDate = sessionDate.toLocaleDateString('en-US', { 
    weekday: 'short', 
    month: 'short', 
    day: 'numeric' 
  });
  const formattedTime = sessionDate.toLocaleTimeString('en-US', { 
    hour: '2-digit', 
    minute: '2-digit' 
  });
  
  // Check if session is full
  const isFull = session.participants && session.participants.current >= session.participants.max;
  
  return (
    <Box
      bg={cardBg}
      borderWidth="1px"
      borderColor={borderColor}
      borderRadius="lg"
      overflow="hidden"
      p={5}
      boxShadow="md"
      transition="all 0.3s"
      _hover={{ transform: 'translateY(-3px)', boxShadow: 'lg' }}
    >
      <VStack align="start" spacing={4}>
        <Flex justify="space-between" width="100%" align="center">
          <Heading as="h3" size="md">{session.title}</Heading>
          <Badge colorScheme={
            session.skillLevel === 'Beginner' ? 'green' : 
            session.skillLevel === 'Intermediate' ? 'blue' : 'purple'
          }>
            {session.skillLevel}
          </Badge>
        </Flex>
        
        <Text color="gray.500" noOfLines={2}>{session.description}</Text>
        
        <HStack>
          <Icon as={FiCalendar} color="gray.500" />
          <Text color="gray.500" fontSize="sm">{formattedDate}</Text>
          <Icon as={FiClock} color="gray.500" />
          <Text color="gray.500" fontSize="sm">{formattedTime}</Text>
          <Text color="gray.500" fontSize="sm">({session.duration} min)</Text>
        </HStack>
        
        <HStack spacing={2} flexWrap="wrap">
          {session.tags.map(tag => (
            <Tag key={tag} size="sm" colorScheme="purple" variant="subtle" mt={1}>
              {tag}
            </Tag>
          ))}
        </HStack>
        
        <Divider />
        
        <Flex justify="space-between" width="100%" align="center">
          <HStack>
            <Avatar size="sm" src={session.host.avatar} name={session.host.name} />
            <Box>
              <Text fontWeight="medium" fontSize="sm">{session.host.name}</Text>
              <HStack spacing={1}>
                <Icon as={FiStar} color="yellow.500" boxSize={3} />
                <Text fontSize="xs">{session.host.rating}</Text>
                <Text fontSize="xs" color="gray.500">•</Text>
                <Text fontSize="xs" color="gray.500">ELO {session.host.eloRating}</Text>
              </HStack>
            </Box>
          </HStack>
          
          <HStack>
            <Icon as={FiUsers} color="gray.500" />
            <Text fontSize="sm" color="gray.500">
              {session.participants ? session.participants.current : 0}/{session.participants.max}
            </Text>
          </HStack>
        </Flex>
        
        <Button 
          colorScheme="purple" 
          size="sm" 
          width="100%" 
          isDisabled={isFull}
        >
          {isFull ? "Session Full" : "Join Session"}
        </Button>
      </VStack>
    </Box>
  );
};

// AI Agent Card Component
const AgentCard = ({ agent }) => {
  const cardBg = useColorModeValue('white', 'gray.800');
  const borderColor = useColorModeValue('gray.200', 'gray.700');
  
  return (
    <Box
      bg={cardBg}
      borderWidth="1px"
      borderColor={borderColor}
      borderRadius="lg"
      overflow="hidden"
      p={5}
      boxShadow="md"
      transition="all 0.3s"
      _hover={{ transform: 'translateY(-3px)', boxShadow: 'lg' }}
    >
      <VStack align="start" spacing={4}>
        <HStack spacing={3}>
          <Avatar 
            size="md" 
            src={agent.avatar} 
            name={agent.name} 
            bg="purple.500"
            icon={<Icon as={FiCpu} color="white" boxSize="1.5rem" />}
          />
          <Box>
            <Heading as="h3" size="md">{agent.name}</Heading>
            <Text color="purple.500" fontSize="sm">{agent.specialty}</Text>
          </Box>
        </HStack>
        
        <Text color="gray.500">{agent.description}</Text>
        
        <HStack width="100%" justify="space-between">
          <Badge colorScheme="purple">AI Partner</Badge>
          <Text fontSize="sm" color="gray.500">ELO {agent.eloRating}</Text>
        </HStack>
        
        <Button 
          colorScheme="purple" 
          variant="outline"
          size="sm" 
          width="100%" 
          leftIcon={<FiCode />}
        >
          Start AI Pairing
        </Button>
      </VStack>
    </Box>
  );
};

// Match History Component
const MatchHistoryItem = ({ match }) => {
  const itemBg = useColorModeValue('white', 'gray.800');
  const borderColor = useColorModeValue('gray.200', 'gray.700');
  
  return (
    <Box 
      p={4} 
      bg={itemBg} 
      borderWidth="1px" 
      borderColor={borderColor}
      borderRadius="md"
      boxShadow="sm"
    >
      <HStack justify="space-between" mb={2}>
        <HStack>
          <Avatar size="sm" src={match.partner.avatar} name={match.partner.name} />
          <Box>
            <Text fontWeight="medium">{match.partner.name}</Text>
            <Text fontSize="xs" color="gray.500">ELO {match.partner.eloRating}</Text>
          </Box>
        </HStack>
        <Badge colorScheme={match.eloChange.startsWith('+') ? 'green' : 'red'}>
          {match.eloChange}
        </Badge>
      </HStack>
      
      <Text noOfLines={1} fontSize="sm" mb={2}>{match.challenge}</Text>
      
      <HStack fontSize="xs" color="gray.500">
        <Icon as={FiCalendar} />
        <Text>{match.date}</Text>
        <Icon as={FiClock} />
        <Text>{match.duration} min</Text>
        <HStack ml="auto">
          {Array(5).fill('').map((_, i) => (
            <Icon 
              key={i} 
              as={FiStar} 
              color={i < match.rating ? 'yellow.500' : 'gray.300'} 
              boxSize={3}
            />
          ))}
        </HStack>
      </HStack>
    </Box>
  );
};

// Main Component
const PairProgramming = () => {
  const [isLoading, setIsLoading] = useState(true);
  const [sessions, setSessions] = useState([]);
  const [matchHistory, setMatchHistory] = useState([]);
  const [aiAgents, setAiAgents] = useState([]);
  const { isOpen, onOpen, onClose } = useDisclosure();
  
  useEffect(() => {
    document.title = `Pair Programming | ${BASE_TITLE}`;
    
    // Simulate API fetch
    setTimeout(() => {
      setSessions(sessionsData);
      setMatchHistory(matchHistoryData);
      setAiAgents(aiAgentsData);
      setIsLoading(false);
    }, 1000);
  }, []);
  
  return (
    <Box p={4}>
      <VStack spacing={8} align="stretch">
        <Box>
          <Heading size="xl" mb={2}>Pair Programming</Heading>
          <Text color="gray.500">Accelerate your learning through collaborative coding</Text>
        </Box>
        
        <Tabs colorScheme="purple" variant="enclosed">
          <TabList>
            <Tab>Upcoming Sessions</Tab>
            <Tab>Match History</Tab>
            <Tab>AI Programming Partners</Tab>
          </TabList>
          
          <TabPanels>
            {/* Upcoming Sessions Tab */}
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
                    </MenuList>
                  </Menu>
                  
                  <Menu>
                    <MenuButton as={Button} rightIcon={<FiChevronDown />} variant="outline" size="sm">
                      Sort By
                    </MenuButton>
                    <MenuList>
                      <MenuItem>Upcoming</MenuItem>
                      <MenuItem>Skill Level</MenuItem>
                      <MenuItem>Host Rating</MenuItem>
                    </MenuList>
                  </Menu>
                </HStack>
                
                <Button colorScheme="purple" leftIcon={<FiPlus />} onClick={onOpen}>
                  Create Session
                </Button>
              </Flex>
              
              {isLoading ? (
                <SimpleGrid columns={{ base: 1, md: 2, lg: 3 }} spacing={6}>
                  {[1, 2, 3].map(i => (
                    <Skeleton key={i} height="320px" borderRadius="lg" />
                  ))}
                </SimpleGrid>
              ) : (
                <SimpleGrid columns={{ base: 1, md: 2, lg: 3 }} spacing={6}>
                  {sessions.map(session => (
                    <SessionCard key={session.id} session={session} />
                  ))}
                </SimpleGrid>
              )}
            </TabPanel>
            
            {/* Match History Tab */}
            <TabPanel px={0}>
              <Box mb={5}>
                <Heading size="md" mb={3}>Your Pair Programming Stats</Heading>
                <SimpleGrid columns={{ base: 2, md: 4 }} gap={4}>
                  <Box p={4} bg={useColorModeValue('white', 'gray.800')} borderRadius="md" boxShadow="sm" borderWidth="1px">
                    <Text color="gray.500" fontSize="sm">Total Sessions</Text>
                    <Heading size="lg">12</Heading>
                  </Box>
                  <Box p={4} bg={useColorModeValue('white', 'gray.800')} borderRadius="md" boxShadow="sm" borderWidth="1px">
                    <Text color="gray.500" fontSize="sm">Current ELO</Text>
                    <Heading size="lg">1765</Heading>
                  </Box>
                  <Box p={4} bg={useColorModeValue('white', 'gray.800')} borderRadius="md" boxShadow="sm" borderWidth="1px">
                    <Text color="gray.500" fontSize="sm">Average Rating</Text>
                    <HStack align="center">
                      <Heading size="lg">4.7</Heading>
                      <Icon as={FiStar} color="yellow.500" boxSize={5} />
                    </HStack>
                  </Box>
                  <Box p={4} bg={useColorModeValue('white', 'gray.800')} borderRadius="md" boxShadow="sm" borderWidth="1px">
                    <Text color="gray.500" fontSize="sm">Skill Growth</Text>
                    <HStack>
                      <Heading size="lg">+22%</Heading>
                      <Icon as={FiTrendingUp} color="green.500" boxSize={5} />
                    </HStack>
                  </Box>
                </SimpleGrid>
              </Box>
              
              <Heading size="md" mb={3}>Recent Pair Programming Sessions</Heading>
              {isLoading ? (
                <VStack spacing={4}>
                  {[1, 2, 3].map(i => (
                    <Skeleton key={i} height="100px" width="100%" borderRadius="md" />
                  ))}
                </VStack>
              ) : (
                <VStack spacing={4}>
                  {matchHistory.map(match => (
                    <MatchHistoryItem key={match.id} match={match} />
                  ))}
                </VStack>
              )}
            </TabPanel>
            
            {/* AI Programming Partners Tab */}
            <TabPanel px={0}>
              <Box mb={5}>
                <Heading size="md" mb={3}>AI-Powered Pair Programming</Heading>
                <Text color="gray.500" mb={5}>
                  Get matched with specialized AI agents that can help you solve specific programming challenges.
                  These AI partners are trained on best practices and can provide guidance when human partners are unavailable.
                </Text>
                
                {isLoading ? (
                  <SimpleGrid columns={{ base: 1, md: 3 }} spacing={6}>
                    {[1, 2, 3].map(i => (
                      <Skeleton key={i} height="220px" borderRadius="lg" />
                    ))}
                  </SimpleGrid>
                ) : (
                  <SimpleGrid columns={{ base: 1, md: 3 }} spacing={6}>
                    {aiAgents.map(agent => (
                      <AgentCard key={agent.id} agent={agent} />
                    ))}
                  </SimpleGrid>
                )}
              </Box>
              
              <Box mt={8} p={5} bg={useColorModeValue('purple.50', 'purple.900')} borderRadius="md">
                <HStack spacing={4} align="flex-start">
                  <Icon as={FiCheck} boxSize={6} color="purple.500" />
                  <Box>
                    <Heading size="sm" mb={1}>Benefits of AI Pair Programming</Heading>
                    <Text fontSize="sm">Practice anytime, receive specialized feedback, and prepare for human pairing sessions with AI-powered code review and recommendations.</Text>
                  </Box>
                </HStack>
              </Box>
            </TabPanel>
          </TabPanels>
        </Tabs>
      </VStack>
      
      {/* Create Session Modal */}
      <Modal isOpen={isOpen} onClose={onClose}>
        <ModalOverlay />
        <ModalContent>
          <ModalHeader>Create Pair Programming Session</ModalHeader>
          <ModalCloseButton />
          <ModalBody>
            <VStack spacing={4}>
              <FormControl>
                <FormLabel>Session Title</FormLabel>
                <Input placeholder="e.g., Building a Recommendation System" />
              </FormControl>
              
              <FormControl>
                <FormLabel>Description</FormLabel>
                <Input placeholder="Briefly describe the programming challenge" />
              </FormControl>
              
              <SimpleGrid columns={2} spacing={4} width="100%">
                <FormControl>
                  <FormLabel>Date</FormLabel>
                  <Input type="date" />
                </FormControl>
                
                <FormControl>
                  <FormLabel>Time</FormLabel>
                  <Input type="time" />
                </FormControl>
              </SimpleGrid>
              
              <SimpleGrid columns={2} spacing={4} width="100%">
                <FormControl>
                  <FormLabel>Duration (min)</FormLabel>
                  <Select defaultValue="60">
                    <option value="30">30</option>
                    <option value="45">45</option>
                    <option value="60">60</option>
                    <option value="90">90</option>
                    <option value="120">120</option>
                  </Select>
                </FormControl>
                
                <FormControl>
                  <FormLabel>Skill Level</FormLabel>
                  <Select defaultValue="intermediate">
                    <option value="beginner">Beginner</option>
                    <option value="intermediate">Intermediate</option>
                    <option value="advanced">Advanced</option>
                  </Select>
                </FormControl>
              </SimpleGrid>
              
              <FormControl>
                <FormLabel>Max Participants</FormLabel>
                <Select defaultValue="2">
                  <option value="2">2</option>
                  <option value="3">3</option>
                  <option value="4">4</option>
                </Select>
              </FormControl>
              
              <FormControl display="flex" alignItems="center">
                <FormLabel mb="0">Enable Video Chat</FormLabel>
                <Switch defaultChecked colorScheme="purple" />
              </FormControl>
            </VStack>
          </ModalBody>

          <ModalFooter>
            <Button variant="ghost" mr={3} onClick={onClose}>
              Cancel
            </Button>
            <Button colorScheme="purple" leftIcon={<FiPlus />}>
              Create Session
            </Button>
          </ModalFooter>
        </ModalContent>
      </Modal>
    </Box>
  );
};

export default PairProgramming;