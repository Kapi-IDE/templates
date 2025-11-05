/**
 * AMC8 Learning Platform - Practice Routes
 * Handles practice sessions, tests, and custom practice configurations
 */

const express = require('express');
const router = express.Router();

// Import services and utilities
const { 
    getRandomProblems, 
    getStatistics,
    getQuestionBank
} = require('../services/questionBank');

const { generatePracticeHTML } = require('../views/generators');
const { shuffleArray } = require('../utils/helpers');

/**
 * Quick Practice Route
 * Generates a practice session with 5 random problems
 * Shows solutions immediately after each answer (practice mode)
 */
router.get('/', (req, res) => {
    const problems = getRandomProblems(5);
    res.send(generatePracticeHTML(problems, '🎮 Practice Mode', false));
});

/**
 * Timed Test Route
 * Generates a test session with 10 random problems and 40-minute timer
 * Shows results only at the end (test mode)
 * Note: This will be accessible as /practice/test
 */
router.get('/test', (req, res) => {
    const problems = getRandomProblems(10);
    res.send(generatePracticeHTML(problems, '⏰ Test Mode', true));
});

/**
 * Custom Practice Setup Route
 * Shows form to customize practice sessions (number of problems, years, mode)
 * Allows filtering by specific years and choosing practice vs test mode
 */
router.get('/custom', (req, res) => {
    const stats = getStatistics();
    res.send(`
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Custom Practice - AMC8 Hub</title>
    <script src="https://polyfill.io/v3/polyfill.min.js?features=es6"></script>
    <script id="MathJax-script" async src="https://cdn.jsdelivr.net/npm/mathjax@3/es5/tex-mml-chtml.js"></script>
    <style>
        body { font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif; line-height: 1.6; margin: 0; padding: 20px; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); min-height: 100vh; }
        .container { max-width: 800px; margin: 0 auto; background: white; padding: 30px; border-radius: 15px; box-shadow: 0 10px 25px rgba(0,0,0,0.1); }
        .header { text-align: center; margin-bottom: 30px; }
        .form-group { margin-bottom: 20px; }
        .form-group label { display: block; margin-bottom: 5px; font-weight: 500; color: #2c3e50; }
        .form-control { width: 100%; padding: 10px; border: 2px solid #ddd; border-radius: 5px; font-size: 16px; }
        .form-control:focus { outline: none; border-color: #3498db; }
        .btn { padding: 12px 25px; background: #3498db; color: white; border: none; border-radius: 6px; cursor: pointer; font-size: 16px; }
        .btn:hover { background: #2980b9; }
        .btn-secondary { background: #95a5a6; color: white; text-decoration: none; display: inline-block; }
        .checkbox-group { display: flex; flex-wrap: wrap; gap: 15px; }
        .checkbox-item { display: flex; align-items: center; }
        .checkbox-item input { margin-right: 8px; }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>🎯 Custom Practice Session</h1>
            <p>Customize your practice experience</p>
        </div>
        
        <form action="/practice/start" method="post">
            <div class="form-group">
                <label for="numProblems">Number of Problems:</label>
                <select id="numProblems" name="numProblems" class="form-control">
                    <option value="5">5 problems (Quick)</option>
                    <option value="10">10 problems (Medium)</option>
                    <option value="15">15 problems (Long)</option>
                    <option value="25">25 problems (Full Test)</option>
                </select>
            </div>
            
            <div class="form-group">
                <label>Select Years (leave unchecked for all years):</label>
                <div class="checkbox-group">
                    ${stats.years.slice().reverse().map(year => `
                        <div class="checkbox-item">
                            <input type="checkbox" id="year${year}" name="years" value="${year}">
                            <label for="year${year}">${year} (${stats.byYear[year]} problems)</label>
                        </div>
                    `).join('')}
                </div>
            </div>
            
            <div class="form-group">
                <label for="mode">Practice Mode:</label>
                <select id="mode" name="mode" class="form-control">
                    <option value="practice">Practice Mode (show answers immediately)</option>
                    <option value="test">Test Mode (show results at end)</option>
                </select>
            </div>
            
            <div style="text-align: center; margin-top: 30px;">
                <button type="submit" class="btn">Start Practice Session</button>
                <a href="/" class="btn btn-secondary">Back to Home</a>
            </div>
        </form>
    </div>
</body>
</html>
    `);
});

/**
 * Custom Practice Start Route (POST)
 * Processes the custom practice form and starts a session with selected parameters
 */
router.post('/start', (req, res) => {
    const { numProblems, years, mode } = req.body;
    const selectedYears = Array.isArray(years) ? years.map(Number) : years ? [Number(years)] : [];
    
    let problems;
    if (selectedYears.length > 0) {
        const questionBank = getQuestionBank();
        problems = questionBank.problems.filter(p => selectedYears.includes(p.year));
        problems = shuffleArray(problems).slice(0, parseInt(numProblems));
    } else {
        problems = getRandomProblems(parseInt(numProblems));
    }
    
    const title = `${mode === 'test' ? '⏰ Test Mode' : '🎮 Practice Mode'}`;
    res.send(generatePracticeHTML(problems, title, mode === 'test'));
});

module.exports = router;