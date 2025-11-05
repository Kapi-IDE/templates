import React, { useState, useEffect } from "react";
import {
  Select,
  Button,
  IconButton,
  HStack,
  Grid,
  GridItem,
  Tooltip,
} from "@chakra-ui/react";
import { FaUpload, FaTrash, FaForward } from "react-icons/fa";

// Mock function to fetch existing surveys
// Replace with your actual data fetching logic
const fetchExistingSurveys = () => [
  { id: 1, name: "Survey 1" },
  { id: 2, name: "Survey 2" },
];

const SelectSurvey = ({ onSurveySelect }) => {
  const [existingSurveys, setExistingSurveys] = useState([]);
  const [selectedSurvey, setSelectedSurvey] = useState("");

  useEffect(() => {
    async function loadSurveys() {
      const surveys = fetchExistingSurveys(); // Simulate fetching surveys
      setExistingSurveys(surveys);
    }
    loadSurveys();
  }, []);

  const handleSurveySelection = (e) => {
    const value = e.target.value;
    setSelectedSurvey(value); // Update local state
    onSurveySelect(value); // Notify parent component
  };

  const handleDelete = () => {
    // Placeholder for save logic
    alert("Delete functionality not implemented yet");
  };

  const handleNext = () => {
    // Placeholder for save logic
    alert("Next functionality not implemented yet");
  };

  const handlePublish = () => {
    // Placeholder for publish logic
    alert("Publish functionality not implemented yet");
  };

  return (
    <Grid templateColumns="repeat(4, 1fr)" gap={6}>
      <GridItem colSpan={3}>
        <Select
          placeholder="Select or create a new survey"
          onChange={handleSurveySelection}
          value={selectedSurvey}
        >
          <option value="new">Create New Survey</option>
          {existingSurveys.map((survey) => (
            <option key={survey.id} value={survey.id}>
              {survey.name}
            </option>
          ))}
        </Select>
      </GridItem>
      <GridItem colSpan={1}>
        <HStack spacing={4}>
          <Tooltip label="Publish this survey">
            <IconButton tool icon={<FaUpload />} onClick={handlePublish} />
          </Tooltip>

          <Tooltip label="Go to the next question">
            <IconButton tool icon={<FaForward />} onClick={handleNext} />
          </Tooltip>

          <Tooltip label="Delete this survey">
            <IconButton tool icon={<FaTrash />} onClick={handleDelete} />
          </Tooltip>
        </HStack>
      </GridItem>
    </Grid>
  );
};

export default SelectSurvey;
