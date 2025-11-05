import React from "react";
import { ChakraProvider, extendTheme } from "@chakra-ui/react";
import { BrowserRouter as Router, Routes, Route, Navigate } from "react-router-dom";
import { AuthProvider } from "./contexts/AuthContext";
import SidebarWithHeader from "./components/SidebarWithHeader";
import HomePage from "./components/HomePage";
import LandingPage from "./components/LandingPage";
import WelcomeDashboard from "./components/WelcomeDashboard";
import LearningPaths from "./components/LearningPaths";
import PairProgramming from "./components/PairProgramming";
import Workshops from "./components/Workshops";
import BarChart from "./components/BarChart";
import WordCloudChart from "./components/WordCloudChart";
import SlideShow from "./components/SlideShow";
import Recordings from "./components/Recordings";
import Login from "./components/Login";
import NotFoundPage from "./components/NotFoundPage";
import ProtectedRoute from "./components/ProtectedRoute";
import Discord from "./components/Discord";
import LiveClass from "./components/LiveClass";
import OnboardingPage from "./components/Onboarding";
import TestCelebration from "./components/TestCelebration";
import { useAuth } from "./contexts/AuthContext";

const theme = extendTheme({
  config: {
    initialColorMode: "dark",
    useSystemColorMode: false,
  },
  colors: {
    brand: {
      50: "#f3e8ff",
      100: "#e9d5ff",
      200: "#d8b4fe",
      300: "#c084fc",
      400: "#a855f7",
      500: "#9333ea",
      600: "#7e22ce",
      700: "#6b21a8",
      800: "#581c87",
      900: "#4c1d95",
    },
  },
});

// Layout wrapper component that handles authenticated vs non-authenticated views
const AppLayout = () => {
  const { isAuthenticated } = useAuth();

  // For authenticated users: show dashboard with protected content 
  // For non-authenticated users: show the landing page and login
  return isAuthenticated ? (
    <Routes>
      {/* Landing page is always accessible */}
      <Route path="/landing" element={<LandingPage />} />
      
      {/* Dashboard routes with sidebar */}
      <Route path="/" element={<WelcomeDashboard />} />
      <Route path="/dashboard" element={
        <SidebarWithHeader>
          <HomePage />
        </SidebarWithHeader>
      } />
      <Route path="/learning-paths" element={
        <SidebarWithHeader>
          <LearningPaths />
        </SidebarWithHeader>
      } />
      <Route path="/pair-programming" element={
        <SidebarWithHeader>
          <PairProgramming />
        </SidebarWithHeader>
      } />
      <Route path="/workshops" element={
        <SidebarWithHeader>
          <Workshops />
        </SidebarWithHeader>
      } />
      <Route path="/liveclass" element={
        <SidebarWithHeader>
          <LiveClass />
        </SidebarWithHeader>
      } />
      <Route path="/onboarding" element={
        <SidebarWithHeader>
          <OnboardingPage />
        </SidebarWithHeader>
      } />
      <Route path="/poll" element={
        <SidebarWithHeader>
          <BarChart />
        </SidebarWithHeader>
      } />
      <Route path="/word-cloud" element={
        <SidebarWithHeader>
          <WordCloudChart />
        </SidebarWithHeader>
      } />
      <Route path="/slides" element={
        <SidebarWithHeader>
          <SlideShow />
        </SidebarWithHeader>
      } />
      <Route path="/recording" element={
        <SidebarWithHeader>
          <Recordings />
        </SidebarWithHeader>
      } />
      <Route path="/discord" element={
        <SidebarWithHeader>
          <Discord />
        </SidebarWithHeader>
      } />
      
      <Route path="/login" element={<Navigate to="/" replace />} />
      <Route path="*" element={<NotFoundPage />} />
    </Routes>
  ) : (
    <Routes>
      <Route path="/landing" element={<LandingPage />} />
      <Route path="/" element={<LandingPage />} />
      <Route path="/login" element={<Login />} />
      <Route path="*" element={<NotFoundPage />} />
    </Routes>
  );
};

function App() {
  return (
    <ChakraProvider theme={theme}>
      <Router>
        <AuthProvider>
          <Routes>
            <Route path="/celebration" element={<TestCelebration />} />
            <Route path="/*" element={<AppLayout />} />
          </Routes>
        </AuthProvider>
      </Router>
    </ChakraProvider>
  );
}

export default App;
