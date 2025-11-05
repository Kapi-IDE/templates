/**
 * AMC8 Learning Platform - Dashboard Service
 * Handles dashboard data, progress tracking, and related functionality
 */

const fs = require('fs').promises;
const path = require('path');
const { getStatistics } = require('./questionBank');

// Progress data file path
const PROGRESS_FILE = path.join(__dirname, '..', '..', 'manager', 'progress_data.json');

// Progress data structure
let progressData = {
    scores: [],
    topicProgress: {},
    totalProblems: 0,
    practiceTests: 0,
    bestScore: 0
};

/**
 * Loads progress data from JSON file
 * Creates initial structure if file doesn't exist
 */
async function loadProgressData() {
    try {
        const data = await fs.readFile(PROGRESS_FILE, 'utf8');
        progressData = JSON.parse(data);
        console.log('📈 Progress data loaded successfully');
    } catch (error) {
        console.log('📈 Creating new progress tracking file');
        await saveProgressData();
    }
}

/**
 * Saves progress data to JSON file
 */
async function saveProgressData() {
    try {
        await fs.writeFile(PROGRESS_FILE, JSON.stringify(progressData, null, 2));
    } catch (error) {
        console.error('Error saving progress data:', error);
    }
}

/**
 * Adds a new test score to progress tracking
 * @param {Object} scoreData - Score data with details
 */
async function addTestScore(scoreData) {
    progressData.scores.push({
        ...scoreData,
        timestamp: new Date().toISOString()
    });
    
    if (scoreData.score > progressData.bestScore) {
        progressData.bestScore = scoreData.score;
    }
    
    progressData.practiceTests += 1;
    await saveProgressData();
}

/**
 * Gets comprehensive dashboard progress data
 * Combines statistics with progress tracking
 * @returns {Object} Dashboard progress object
 */
function getDashboardProgress() {
    const stats = getStatistics();
    
    // Calculate accuracy from recent scores
    let accuracy = 75; // default
    if (progressData.scores.length > 0) {
        const totalCorrect = progressData.scores.reduce((sum, s) => sum + s.score, 0);
        const totalQuestions = progressData.scores.reduce((sum, s) => sum + s.totalQuestions, 0);
        accuracy = totalQuestions > 0 ? Math.round((totalCorrect / totalQuestions) * 100) : 75;
    }
    
    return {
        currentScore: progressData.bestScore || 16,
        totalProblems: 25,
        percentage: progressData.bestScore ? Math.round((progressData.bestScore / 25) * 100) : 64,
        problemsSolved: stats.total || 127,
        practiceTests: progressData.practiceTests || 0,
        accuracy: accuracy,
        daysRemaining: Math.ceil((new Date('2026-01-22') - new Date()) / (1000 * 60 * 60 * 24))
    };
}

/**
 * Gets topic mastery status for different AMC8 subjects
 * In real implementation, would track actual problem solving by topic
 * @returns {Array} Array of topic mastery objects
 */
function getTopicMastery() {
    // Mock data - in real implementation, would track actual problem solving by topic
    return [
        { name: 'Arithmetic', status: 'mastered', description: 'Mastered' },
        { name: 'Geometry', status: 'learning', description: 'Learning' },
        { name: 'Number Theory', status: 'learning', description: 'Learning' },
        { name: 'Combinatorics', status: 'needs-work', description: 'Needs Work' },
        { name: 'Algebra', status: 'learning', description: 'Learning' },
        { name: 'Word Problems', status: 'needs-work', description: 'Needs Work' }
    ];
}

/**
 * Gets upcoming math competition schedule
 * Helps students plan their preparation timeline
 * @returns {Array} Array of competition objects with name, date, and status
 */
function getCompetitionSchedule() {
    return [
        { name: 'AMC8', date: 'Jan 22-28, 2026', status: 'upcoming' },
        { name: 'MATHCOUNTS School', date: 'Nov 2025 - Jan 2026', status: 'upcoming' },
        { name: 'Math Kangaroo', date: 'March 2026', status: 'upcoming' },
        { name: 'CAML', date: '2025-2026', status: 'upcoming' }
    ];
}

/**
 * Gets weekly study plan with daily goals
 * Provides structure for consistent practice and improvement
 * @returns {Array} Array of daily study plan objects
 */
function getStudyPlan() {
    return [
        { day: 'Monday', topic: 'Coordinate Geometry', goal: '5 problems', status: 'completed' },
        { day: 'Tuesday', topic: 'Number Theory', goal: '8 problems', status: 'completed' },
        { day: 'Wednesday', topic: 'Combinatorics', goal: '6 problems', status: 'upcoming' },
        { day: 'Thursday', topic: 'Word Problems', goal: '7 problems', status: 'upcoming' },
        { day: 'Friday', topic: 'Mixed Review', goal: '10 problems', status: 'upcoming' },
        { day: 'Saturday', topic: 'Practice Test', goal: 'Full test (40 min)', status: 'upcoming' },
        { day: 'Sunday', topic: 'Review & Plan', goal: 'Analyze mistakes', status: 'upcoming' }
    ];
}

/**
 * Gets progress history for charts and analysis
 * @returns {Object} Progress history object with scores and summary
 */
function getProgressHistory() {
    return {
        scores: progressData.scores,
        summary: {
            totalTests: progressData.practiceTests,
            bestScore: progressData.bestScore,
            averageScore: progressData.scores.length > 0 ? 
                progressData.scores.reduce((sum, s) => sum + s.score, 0) / progressData.scores.length : 0,
            improvement: progressData.scores.length >= 2 ? 
                progressData.scores[progressData.scores.length - 1].score - progressData.scores[0].score : 0
        }
    };
}

/**
 * Gets the progress data object (read-only)
 * @returns {Object} Progress data object
 */
function getProgressData() {
    return { ...progressData };
}

module.exports = {
    loadProgressData,
    saveProgressData,
    addTestScore,
    getDashboardProgress,
    getTopicMastery,
    getCompetitionSchedule,
    getStudyPlan,
    getProgressHistory,
    getProgressData
};