#!/usr/bin/env node
/**
 * AMC8 Learning Platform - Main Application
 * Modular web-based learning platform for AMC8 math practice
 * 
 * ARCHITECTURE OVERVIEW:
 * ====================
 * This platform is organized into modular components for better maintainability:
 * 
 * 1. ROUTES:
 *    - /routes/dashboard.js: Main dashboard with progress tracking
 *    - /routes/study.js: Study guides and educational content
 *    - /routes/practice.js: Practice sessions and tests
 *    - /routes/browse.js: Problem browsing and search
 *    - /routes/api.js: RESTful API endpoints
 * 
 * 2. SERVICES:
 *    - /services/questionBank.js: Question data access and filtering
 *    - /services/dashboard.js: Progress tracking and dashboard data
 * 
 * 3. VIEWS:
 *    - /views/styles.js: CSS styling and HTML head generation
 *    - /views/generators.js: HTML page generation functions
 * 
 * 4. UTILITIES:
 *    - /utils/helpers.js: Common helper functions
 * 
 * @author AMC8 Learning Platform
 * @version 3.0 - Modular Architecture
 */

const express = require('express');
const path = require('path');

// Initialize Express app
const app = express();
const PORT = process.env.PORT || 3000;

// ================================================================
// MIDDLEWARE CONFIGURATION
// ================================================================
app.use(express.json());
app.use(express.static(path.join(__dirname, 'public')));
app.use('/manager', express.static(path.join(__dirname, 'manager')));
app.use(express.urlencoded({ extended: true }));

// ================================================================
// IMPORT SERVICES AND INITIALIZE DATA
// ================================================================
const { loadQuestionBank } = require('./services/questionBank');
const { loadProgressData } = require('./services/dashboard');
const { generatePracticeHTML } = require('./views/generators');
const { getRandomProblems } = require('./services/questionBank');

// ================================================================
// IMPORT ROUTE MODULES
// ================================================================
const dashboardRoutes = require('./routes/dashboard');
const studyRoutes = require('./routes/study');
const practiceRoutes = require('./routes/practice');
const browseRoutes = require('./routes/browse');
const searchRoutes = require('./routes/search');
const apiRoutes = require('./routes/api');

// ================================================================
// MOUNT ROUTE MODULES
// ================================================================
app.use('/', dashboardRoutes);          // Dashboard routes (/, etc.)
app.use('/study', studyRoutes);         // Study routes (/study/*, etc.)
app.use('/practice', practiceRoutes);   // Practice routes (/practice/*, etc.)
app.use('/browse', browseRoutes);       // Browse routes (/browse/*, etc.)
app.use('/search', searchRoutes);       // Search routes (/search/*, etc.)
app.use('/api', apiRoutes);             // API routes (/api/*, etc.)

// ================================================================
// STANDALONE ROUTES (not in modules)
// ================================================================

/**
 * Standalone Test Route
 * Provides direct access to test mode at /test for backwards compatibility
 * This is separate from /practice/test to maintain existing user bookmarks
 */
app.get('/test', (req, res) => {
    const problems = getRandomProblems(10);
    res.send(generatePracticeHTML(problems, '⏰ Test Mode', true));
});

/**
 * Health Check Route
 * Simple endpoint to verify server is running
 */
app.get('/health', (req, res) => {
    res.json({ 
        status: 'OK', 
        timestamp: new Date().toISOString(),
        version: '3.0.0',
        architecture: 'modular'
    });
});

// ================================================================
// ERROR HANDLING
// ================================================================

/**
 * 404 Error Handler
 * Shows a friendly error page for non-existent routes
 */
app.use((req, res) => {
    res.status(404).send(`
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Page Not Found - AMC8 Hub</title>
    <style>
        body { 
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif; 
            text-align: center; 
            padding: 50px; 
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
            color: white;
        }
        .error-container {
            background: rgba(255, 255, 255, 0.95);
            color: #333;
            padding: 40px;
            border-radius: 15px;
            max-width: 500px;
            margin: 0 auto;
            box-shadow: 0 10px 25px rgba(0,0,0,0.1);
        }
        .error-icon { font-size: 4em; margin-bottom: 20px; }
        h1 { color: #2c3e50; margin-bottom: 10px; }
        p { color: #7f8c8d; margin-bottom: 30px; }
        .btn { 
            display: inline-block;
            padding: 12px 25px;
            background: #3498db;
            color: white;
            text-decoration: none;
            border-radius: 6px;
            margin: 5px;
        }
        .btn:hover { background: #2980b9; }
    </style>
</head>
<body>
    <div class="error-container">
        <div class="error-icon">🔍</div>
        <h1>Page Not Found</h1>
        <p>The page you're looking for doesn't exist. Let's get you back on track!</p>
        <a href="/" class="btn">🏠 Go to Dashboard</a>
        <a href="/practice" class="btn">🎮 Start Practice</a>
        <a href="/study" class="btn">📚 Study Guide</a>
    </div>
</body>
</html>
    `);
});

/**
 * General Error Handler
 * Catches and displays server errors in a user-friendly way
 */
app.use((err, req, res, next) => {
    console.error('Server Error:', err);
    res.status(500).send(`
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Server Error - AMC8 Hub</title>
    <style>
        body { 
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif; 
            text-align: center; 
            padding: 50px; 
            background: linear-gradient(135deg, #e74c3c 0%, #c0392b 100%);
            min-height: 100vh;
            color: white;
        }
        .error-container {
            background: rgba(255, 255, 255, 0.95);
            color: #333;
            padding: 40px;
            border-radius: 15px;
            max-width: 500px;
            margin: 0 auto;
            box-shadow: 0 10px 25px rgba(0,0,0,0.1);
        }
    </style>
</head>
<body>
    <div class="error-container">
        <h1>⚠️ Server Error</h1>
        <p>Something went wrong on our end. Please try again later.</p>
        <a href="/" style="color: #3498db; text-decoration: none;">← Back to Dashboard</a>
    </div>
</body>
</html>
    `);
});

// ================================================================
// SERVER INITIALIZATION
// ================================================================

/**
 * Initialize the server with all required data loading
 * Loads question bank and progress data before starting the server
 */
async function startServer() {
    try {
        console.log('🚀 Starting AMC8 Learning Platform v3.0...');
        
        // Load question bank and progress data
        await loadQuestionBank();
        await loadProgressData();
        
        // Start the server
        app.listen(PORT, () => {
            console.log('✅ AMC8 Learning Platform is running!');
            console.log(`🌐 Dashboard: http://localhost:${PORT}`);
            console.log(`📚 Study Guide: http://localhost:${PORT}/study`);
            console.log(`🎮 Practice: http://localhost:${PORT}/practice`);
            console.log(`📊 Browse Problems: http://localhost:${PORT}/browse`);
            console.log(`🔗 API: http://localhost:${PORT}/api`);
            console.log('');
            console.log('📁 Modular Architecture:');
            console.log('   ├── routes/        (Route handlers)');
            console.log('   ├── services/      (Business logic)');
            console.log('   ├── views/         (HTML generation)');
            console.log('   └── utils/         (Helper functions)');
        });
        
    } catch (error) {
        console.error('❌ Failed to start server:', error);
        process.exit(1);
    }
}

// ================================================================
// GRACEFUL SHUTDOWN
// ================================================================

/**
 * Handle graceful shutdown on SIGINT (Ctrl+C)
 */
process.on('SIGINT', () => {
    console.log('\n🛑 Received SIGINT. Shutting down gracefully...');
    console.log('👋 Thanks for using AMC8 Learning Platform!');
    process.exit(0);
});

// Start the server
startServer().catch(error => {
    console.error('Failed to start server:', error);
    process.exit(1);
});

module.exports = app;