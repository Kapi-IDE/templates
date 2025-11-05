import React, { useState, useEffect } from "react";
import { Heading, VStack, Box, Text, Image } from "@chakra-ui/react";
import { BASE_TITLE } from "../Constants";
import CreateSurvey from "./CreateSurvey";
import SelectSurvey from "./SelectSurvey";
import ZoomPic from "../assets/zoom.png";

const LiveClass = () => {
  const [userRole, setUserRole] = useState(localStorage.getItem("role"));
  const [selectedSurvey, setSelectedSurvey] = useState("");

  useEffect(() => {
    document.title = `Live Class | ${BASE_TITLE}`;
  }, []);

  if (userRole !== "teacher") {
    return (
      <Box p={5}>
        <Text>You must be a teacher to access this page.</Text>
      </Box>
    );
  }

  // Function to handle selection from SelectSurvey component
  const handleSurveySelection = (value) => {
    setSelectedSurvey(value);
  };

  return (
    <VStack spacing={4} align="stretch">
      <SelectSurvey onSurveySelect={handleSurveySelection} />
      {selectedSurvey === "new" && <CreateSurvey />}
      <Image src={ZoomPic} alt="Zoom Pic" />
    </VStack>
  );
};

export default LiveClass;
