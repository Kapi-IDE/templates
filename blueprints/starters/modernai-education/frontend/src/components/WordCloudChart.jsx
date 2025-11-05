import React, { useRef, useEffect, useState } from "react"; // Import useState
import { Box } from "@chakra-ui/react";
import { Chart, registerables } from "chart.js";
import { WordCloudController, WordElement } from "chartjs-chart-wordcloud";

// Register Chart.js components and word cloud controller and element
Chart.register(...registerables, WordCloudController, WordElement);

const question = "How do you feel about the course so far?";

// Sample feedback words
const feedbackWords = [
  "insightful",
  "challenging",
  "engaging",
  "difficult",
  "rewarding",
  "intense",
  "informative",
  "overwhelming",
  "motivating",
  "transformative",
];

// Function to simulate receiving new feedback
const getNewFeedback = () => {
  return feedbackWords
    .map((word) => ({
      text: word,
      weight: Math.floor(Math.random() * 50) + 10, // Adjust field to 'weight' for chartjs-chart-wordcloud
    }))
    .filter(() => Math.random() < 0.5); // Random chance to include each word
};

const WordCloudChart = () => {
  const chartRef = useRef(null);
  const [words, setWords] = useState(getNewFeedback()); // Initialize with random feedback

  useEffect(() => {
    const updateChart = () => {
      if (chartRef.current) {
        const ctx = chartRef.current.getContext("2d");

        // Clear existing chart instance if it exists
        if (Chart.instances[chartRef.current]) {
          Chart.instances[chartRef.current].destroy();
        }

        // Create a new chart instance
        new Chart(ctx, {
          type: WordCloudController.id,
          data: {
            labels: words.map((word) => word.text), // Use text from each word
            datasets: [
              {
                label: "Feedback",
                data: words.map((word) => word.weight), // Use weight for data
              },
            ],
          },
          options: {
            plugins: {
              title: {
                display: true,
                text: question,
              },
            },
          },
        });
      }
    };

    updateChart(); // Initialize chart

    const intervalId = setInterval(() => {
      setWords(getNewFeedback()); // Update words state with new feedback
    }, 1000); // Simulate new feedback every 5 seconds

    return () => clearInterval(intervalId); // Cleanup on component unmount
  }, []);

  useEffect(() => {
    // Re-render the chart when the 'words' state updates
    if (words.length > 0) {
      const ctx = chartRef.current.getContext("2d");
      if (ctx) {
        Chart.getChart(ctx)?.destroy(); // Destroy the existing chart
        const newChart = new Chart(ctx, {
          type: WordCloudController.id,
          data: {
            labels: words.map((word) => word.text),
            datasets: [
              {
                label: "Feedback",
                data: words.map((word) => word.weight),
              },
            ],
          },
          options: {
            plugins: {
              title: {
                display: true,
                text: question,
                font: {
                  size: 30,
                  weight: "bold",
                },
                color: "white",
              },
            },
          },
        });
      }
    }
  }, [words]); // This effect depends on 'words' to re-render the chart

  return (
    <Box width="1000px" height="600px">
      <canvas ref={chartRef}></canvas>{" "}
      {/* Removed inline width and height, control via Box */}
    </Box>
  );
};

export default WordCloudChart;
