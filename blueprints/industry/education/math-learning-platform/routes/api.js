/**
 * AMC8 Learning Platform - API Routes
 * RESTful API endpoints for dashboard data, progress tracking, and problem access
 */

const express = require('express');
const router = express.Router();

// Import services
const { 
    getDashboardProgress, 
    getProgressHistory, 
    getCompetitionSchedule, 
    getStudyPlan, 
    getTopicMastery,
    addTestScore 
} = require('../services/dashboard');

const { 
    getRandomProblems, 
    getProblemsByYear, 
    getStatistics 
} = require('../services/questionBank');

/**
 * API endpoint for dashboard progress data
 * Returns current learning progress, scores, and statistics
 */
router.get('/progress', (req, res) => {
    res.json(getDashboardProgress());
});

/**
 * API endpoint to save practice test scores
 * Accepts POST requests with score data
 */
router.post('/save-score', async (req, res) => {
    try {
        const { score, totalQuestions, timeSpent, topics, mode } = req.body;
        
        await addTestScore({
            score: parseInt(score),
            totalQuestions: parseInt(totalQuestions),
            timeSpent: parseInt(timeSpent),
            topics: topics || [],
            mode: mode || 'practice',
            percentage: Math.round((score / totalQuestions) * 100)
        });
        
        res.json({ success: true, message: 'Score saved successfully' });
    } catch (error) {
        res.status(500).json({ success: false, error: error.message });
    }
});

/**
 * API endpoint for progress history
 * Returns detailed progress data over time
 */
router.get('/progress-history', (req, res) => {
    res.json(getProgressHistory());
});

/**
 * API endpoint for competition schedule data
 * Returns upcoming math competitions and their details
 */
router.get('/competitions', (req, res) => {
    res.json(getCompetitionSchedule());
});

/**
 * API endpoint for weekly study plan data
 * Returns structured daily learning goals and progress
 */
router.get('/study-plan', (req, res) => {
    res.json(getStudyPlan());
});

/**
 * API endpoint for topic mastery data
 * Returns learning status for different AMC8 subject areas
 */
router.get('/topics', (req, res) => {
    res.json(getTopicMastery());
});

/**
 * API endpoint for random problems
 * Returns a specified number of random problems from the question bank
 */
router.get('/problems/random/:count', (req, res) => {
    const count = parseInt(req.params.count) || 5;
    res.json(getRandomProblems(count));
});

/**
 * API endpoint for problems by year
 * Returns all problems from a specific AMC8 year
 */
router.get('/problems/year/:year', (req, res) => {
    const year = parseInt(req.params.year);
    res.json(getProblemsByYear(year));
});

/**
 * API endpoint for question bank statistics
 * Returns comprehensive statistics about available problems
 */
router.get('/statistics', (req, res) => {
    res.json(getStatistics());
});

module.exports = router;