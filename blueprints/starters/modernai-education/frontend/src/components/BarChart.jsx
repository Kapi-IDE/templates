import React, { useEffect, useState } from "react";
import { Bar } from "react-chartjs-2";
import {
  Chart as ChartJS,
  CategoryScale,
  LinearScale,
  BarElement,
  Title,
  Tooltip,
  Legend,
} from "chart.js";

ChartJS.register(
  CategoryScale,
  LinearScale,
  BarElement,
  Title,
  Tooltip,
  Legend
);

const question = "Which algorithm is foundational for modern NLP models?";
const choices = ["RNN", "Transformer", "CNN", "SVM"];

const BarChart = () => {
  const [votes, setVotes] = useState([0, 0, 0, 0]);

  // Function to simulate votes
  const simulateVotes = () => {
    const newVotes = [...votes];
    const voteIndex = Math.floor(Math.random() * choices.length);
    newVotes[voteIndex]++;
    setVotes(newVotes);
  };

  useEffect(() => {
    const intervalId = setInterval(simulateVotes, 1000); // Simulate a vote every second

    return () => clearInterval(intervalId); // Clean up the interval on component unmount
  }, [votes]);

  const data = {
    labels: choices,
    datasets: [
      {
        label: question,
        data: votes,
        backgroundColor: [
          "rgba(255, 99, 132, 0.2)",
          "rgba(54, 162, 235, 0.2)",
          "rgba(255, 206, 86, 0.2)",
          "rgba(75, 192, 192, 0.2)",
        ],
        borderColor: [
          "rgba(255, 99, 132, 1)",
          "rgba(54, 162, 235, 1)",
          "rgba(255, 206, 86, 1)",
          "rgba(75, 192, 192, 1)",
        ],
        borderWidth: 1,
      },
    ],
  };

  const options = {
    scales: {
      y: {
        beginAtZero: true,
      },
    },
  };

  return <Bar data={data} options={options} />;
};

export default BarChart;
