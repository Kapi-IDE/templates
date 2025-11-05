import React, { useState } from "react";
import {
  VStack,
  Input,
  Button,
  Select,
  Grid,
  GridItem,
  Tooltip,
  IconButton,
} from "@chakra-ui/react";
import { surveyTypes } from "../Constants";
import { FaPlus } from "react-icons/fa";
import { CREATE_SURVEY } from "../Constants";

const CreateSurvey = () => {
  const [surveyType, setSurveyType] = useState(surveyTypes[0].value);
  const [surveyName, setSurveyName] = useState("");
  const [question, setQuestion] = useState("How do you feel about this?");
  const [answers, setAnswers] = useState([""]);

  const handleSurveyTypeChange = (e) => setSurveyType(e.target.value);

  const handleQuestionChange = (e) => setQuestion(e.target.value);

  const handleAnswerChange = (index, value) => {
    const updatedAnswers = answers.map((answer, i) =>
      i === index ? value : answer
    );
    setAnswers(updatedAnswers);
  };

  const addAnswerOption = () => setAnswers([...answers, ""]);

  const handleSave = async () => {
    const surveyData = {
      surveyName,
      surveyType,

      question,
      // For types that do not include multiple choices, responses could be omitted or empty
      responses:
        surveyType === "single_word" || surveyType === "single_sentence"
          ? []
          : answers.filter((answer) => answer.trim() !== ""),
    };

    console.log("Saving survey data:", JSON.stringify(surveyData, null, 2));
    try {
      const response = await fetch(CREATE_SURVEY, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          accept: "application/json",
        },
        body: JSON.stringify(surveyData),
      });

      if (response.ok) {
        const responseData = await response.json();
        console.log(responseData);
        alert("Survey saved successfully!");
      } else {
        throw new Error("Network response was not ok.");
      }
    } catch (error) {
      console.error("Failed to save the survey:", error);
      alert("Failed to save the survey.");
    }
  };

  const renderSurveyCreationFields = () => {
    switch (surveyType) {
      case "single_word":
      case "single_sentence":
        return (
          <Input
            placeholder="Enter your question"
            value={question}
            onChange={(e) => setQuestion(e.target.value)}
          />
        );
      case "poll":
      case "quiz":
      case "ranking":
        return (
          <>
            <Input
              placeholder="Enter your question"
              value={question}
              onChange={(e) => setQuestion(e.target.value)}
            />
            {answers.map((answer, index) => (
              <Input
                key={index}
                placeholder={`Option ${index + 1}`}
                value={answer}
                onChange={(e) => handleAnswerChange(index, e.target.value)}
              />
            ))}
            <Tooltip label="Add Option">
              <IconButton tool icon={<FaPlus />} onClick={addAnswerOption} />
            </Tooltip>
          </>
        );
      default:
        return null;
    }
  };

  return (
    <Grid templateColumns="repeat(4, 1fr)" gap={6}>
      <GridItem colSpan={3}>
        <VStack spacing={4} alignItems="start">
          {renderSurveyCreationFields()}
        </VStack>
      </GridItem>
      <GridItem colSpan={1}>
        <VStack spacing={4} alignItems="start">
          <Select onChange={handleSurveyTypeChange}>
            {surveyTypes.map((type) => (
              <option key={type.value} value={type.value}>
                {type.label}
              </option>
            ))}
          </Select>
          <Input
            placeholder="Give a descriptive name for this survey"
            value={surveyName}
            onChange={(e) => setSurveyName(e.target.value)}
          />
          <Button colorScheme="gray" onClick={handleSave}>
            Save
          </Button>
        </VStack>
      </GridItem>
    </Grid>
  );
};

export default CreateSurvey;
