import React, { useState, useEffect } from "react";
import {
  VStack,
  Box,
  Button,
  Text,
  Radio,
  RadioGroup,
  Stack,
  useDisclosure,
} from "@chakra-ui/react";
import partyAnimation from "../assets/party_animation.webm";
import { SUBMIT_ANSWER, GET_QUESTION, START_QUIZ, BASE_TITLE } from "../Constants";

const HomePage = () => {
  const [showVideo, setShowVideo] = useState(false);
  const [question, setQuestion] = useState(null);
  const [score, setScore] = useState(null);
  const [quizStarted, setQuizStarted] = useState(false);
  const [currentQuestionId, setCurrentQuestionId] = useState(null);

  useEffect(() => {
    document.title = `Assessment | ${BASE_TITLE}`;
  }, []);

  //Defunct
  const handleStartQuiz = async () => {
    // Reset state
    setShowVideo(false);
    setQuestion(null);

    try {
      const response = await fetch(START_QUIZ, {
        method: "POST",
        headers: {
          Accept: "application/json",
          "Content-Type": "application/json",
        },
      });

      if (response.ok) {
        // If the request was successful, fetch the first question
        fetchQuestion();
      } else {
        // If the request was unsuccessful, alert the user
        alert("Error occurred: Unable to start the quiz.");
      }
    } catch (error) {
      // Handle any errors that occurred during the fetch
      alert(`Error occurred: ${error.message}`);
    }
  };

  const fetchQuestion = async () => {
    const response = await fetch(GET_QUESTION);
    if (response.ok) {
      const data = await response.json();
      setQuestion(data); // Update the state with the fetched question
      setCurrentQuestionId(data.id); // Store the current question ID
      setQuizStarted(true); // Mark the quiz as started
    } else {
      alert("No more questions or quiz not started");
      setQuestion(null); // Reset question state
      setCurrentQuestionId(null); // Reset current question ID
      setQuizStarted(false); // Mark the quiz as not started
    }
  };

  const handleAnswer = async (choice) => {
    const response = await fetch(SUBMIT_ANSWER, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({ question_id: currentQuestionId, choice }), // Use question_id, not questionId
    });
    const data = await response.json();
    if (data.correct) {
      setShowVideo(true); // Show success animation
      setTimeout(() => setShowVideo(false), 5000); // Hide the video after 5 seconds
      fetchQuestion(); // Fetch the next question
    } else {
      alert(data.message); // Show message for wrong answer
    }
  };

  return (
    <VStack spacing={4} align="left" p={5}>
      {!quizStarted && (
        <Button colorScheme="blue" onClick={fetchQuestion}>
          Start Quiz
        </Button>
      )}
      {question && (
        <Box>
          <Text fontSize="xl" mb={4}>
            {question.question}
          </Text>
          <RadioGroup onChange={(value) => handleAnswer(value)}>
            <Stack direction="column">
              {question.choices.map((choice, index) => (
                <Radio key={index} value={choice}>
                  {choice}
                </Radio>
              ))}
            </Stack>
          </RadioGroup>
        </Box>
      )}
      {showVideo && (
        <Box
          position="fixed"
          top="0"
          left="0"
          width="100vw"
          height="100vh"
          zIndex="overlay"
          overflow="hidden"
        >
          <video
            src={partyAnimation}
            autoPlay
            muted
            playsInline
            width="100%"
            height="100%"
            style={{ objectFit: "cover" }}
          >
            Your browser does not support the video tag.
          </video>
        </Box>
      )}
    </VStack>
  );
};

export default HomePage;
