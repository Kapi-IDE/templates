import React, { useEffect, useState } from "react";
import { BASE_TITLE } from "../Constants";
import {
  Heading,
  Text,
  Box,
  Checkbox,
  VStack,
  Button,
} from "@chakra-ui/react";

const OnboardingPage = () => {
  const [stepsCompleted, setStepsCompleted] = useState({
    step1: false,
    step2: false,
    step3: false,
  });

  useEffect(() => {
    document.title = "Onboarding | " + BASE_TITLE;
  }, []);

  const handleCheckboxChange = (e) => {
    const { name, checked } = e.target;
    setStepsCompleted((prev) => ({ ...prev, [name]: checked }));
  };

  const allStepsCompleted = Object.values(stepsCompleted).every(Boolean);

  return (
    <Box p={5}>
      <Heading as="h1" mb={5}>
        Onboarding Instructions
      </Heading>
      <Text mb={4}>Please complete the following steps to get started:</Text>
      <VStack align="start" spacing={3}>
        <Checkbox
          name="step1"
          isChecked={stepsCompleted.step1}
          onChange={handleCheckboxChange}
        >
          Step 1: Read the welcome message
        </Checkbox>
        <Checkbox
          name="step2"
          isChecked={stepsCompleted.step2}
          onChange={handleCheckboxChange}
        >
          Step 2: Set up your profile
        </Checkbox>
        <Checkbox
          name="step3"
          isChecked={stepsCompleted.step3}
          onChange={handleCheckboxChange}
        >
          Step 3: Complete the tutorial
        </Checkbox>
      </VStack>
      <Button
        mt={5}
        colorScheme="teal"
        isDisabled={!allStepsCompleted}
        onClick={() => alert("Onboarding Complete!")}
      >
        Finish Onboarding
      </Button>
    </Box>
  );
};

export default OnboardingPage;
