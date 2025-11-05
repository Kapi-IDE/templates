/**
 * AMC8 Learning Platform - Dashboard Routes
 * Main dashboard and home page functionality
 */

const express = require('express');
const router = express.Router();

// Import services
const { 
    getDashboardProgress,
    getTopicMastery,
    getCompetitionSchedule,
    getStudyPlan
} = require('../services/dashboard');

const { generateHTMLHead, DASHBOARD_CSS } = require('../views/styles');

/**
 * Dashboard Route (Main Landing Page)
 * Shows comprehensive preparation overview with progress, countdown, and quick actions
 * Integrates all user stories into a central hub
 */
router.get('/', (req, res) => {
    const progress = getDashboardProgress();
    const topics = getTopicMastery();
    const competitions = getCompetitionSchedule();
    const studyPlan = getStudyPlan();
    
    res.send(`
<!DOCTYPE html>
<html lang="en">
${generateHTMLHead('AMC8 2026 Preparation Dashboard', DASHBOARD_CSS)}
<body>
    <div class="container">
        <div class="header">
            <h1>🎯 AMC8 2026 Preparation Dashboard</h1>
            <p class="subtitle">Your Journey to Mathematical Excellence</p>
        </div>

        <div class="dashboard-grid">
            <!-- Competition Countdown -->
            <div class="card">
                <h3>⏰ AMC8 2026 Countdown</h3>
                <div class="countdown">
                    <span class="days" id="countdown-days">${progress.daysRemaining}</span>
                    <span>days remaining</span>
                    <p style="margin-top: 10px; color: #7f8c8d;">January 22-28, 2026</p>
                </div>
            </div>

            <!-- Current Progress -->
            <div class="card">
                <h3>📊 Progress Overview</h3>
                <div class="score-display">
                    <div>
                        <p><strong>Current Best Score</strong></p>
                        <div class="progress-bar">
                            <div class="progress-fill" style="width: ${progress.percentage}%" id="current-progress"></div>
                        </div>
                        <p>${progress.currentScore}/25 points (${progress.percentage}%)</p>
                    </div>
                    <div class="score-circle score-current">${progress.currentScore}</div>
                </div>
                
                <div class="stats-row">
                    <div class="stat-item">
                        <div class="stat-number">${progress.problemsSolved}</div>
                        <div class="stat-label">Problems Solved</div>
                    </div>
                    <div class="stat-item">
                        <div class="stat-number">${progress.practiceTests}</div>
                        <div class="stat-label">Practice Tests</div>
                    </div>
                    <div class="stat-item">
                        <div class="stat-number">${progress.accuracy}%</div>
                        <div class="stat-label">Accuracy</div>
                    </div>
                </div>
            </div>

            <!-- Score Goals -->
            <div class="card">
                <h3>🏆 Achievement Targets</h3>
                <div class="score-display">
                    <div>
                        <strong>Distinguished Honor Roll</strong><br>
                        <small>Top 1% (19-25 points)</small>
                    </div>
                    <div class="score-circle score-dhr">19+</div>
                </div>
                
                <div class="score-display">
                    <div>
                        <strong>Honor Roll</strong><br>
                        <small>Top 5% (15-19 points)</small>
                    </div>
                    <div class="score-circle score-hr">15+</div>
                </div>
                
                <div class="score-display">
                    <div>
                        <strong>Achievement Roll</strong><br>
                        <small>Top 25% (11-14 points)</small>
                    </div>
                    <div class="score-circle score-ar">11+</div>
                </div>
            </div>

            <!-- Topic Mastery -->
            <div class="card">
                <h3>📚 Topic Mastery</h3>
                <div class="topic-grid">
                    ${topics.map(topic => `
                        <div class="topic-item topic-${topic.status}">
                            <strong>${topic.name}</strong><br>
                            <small>${topic.status === 'mastered' ? '✅ Mastered' : 
                                    topic.status === 'learning' ? '📚 Learning' : 
                                    '⚠️ Needs Work'}</small>
                        </div>
                    `).join('')}
                </div>
            </div>

            <!-- Upcoming Competitions -->
            <div class="card">
                <h3>🏁 Competition Schedule</h3>
                <table class="competition-table">
                    <thead>
                        <tr>
                            <th>Competition</th>
                            <th>Date</th>
                            <th>Status</th>
                        </tr>
                    </thead>
                    <tbody>
                        ${competitions.map(comp => `
                            <tr>
                                <td><strong>${comp.name}</strong></td>
                                <td>${comp.date}</td>
                                <td><span class="status-badge status-${comp.status}">
                                    ${comp.status.charAt(0).toUpperCase() + comp.status.slice(1)}
                                </span></td>
                            </tr>
                        `).join('')}
                    </tbody>
                </table>
            </div>

            <!-- Recent Activity -->
            <div class="card">
                <h3>📝 Recent Activity</h3>
                <div style="space-y: 10px;">
                    <p>✅ <strong>Today:</strong> Completed 8 geometry problems</p>
                    <p>📊 <strong>Yesterday:</strong> Practice test score: ${progress.currentScore}/25</p>
                    <p>📚 <strong>This Week:</strong> Focused on coordinate geometry</p>
                    <p>🎯 <strong>Goal:</strong> Master problems 1-15 by end of month</p>
                </div>
            </div>
        </div>

        <!-- Quick Actions -->
        <div class="card">
            <h3>🚀 Quick Actions</h3>
            <div class="quick-actions">
                <a href="/practice" class="btn btn-primary">🎮 Start Practice</a>
                <a href="/test" class="btn btn-warning">⏰ Take Timed Test</a>
                <a href="/study" class="btn btn-info">📚 Study Content</a>
                <a href="/browse" class="btn btn-primary">📊 Browse Problems</a>
            </div>
        </div>

        <!-- Study Plan -->
        <div class="card">
            <h3>📅 This Week's Study Plan</h3>
            <table class="competition-table">
                <thead>
                    <tr>
                        <th>Day</th>
                        <th>Focus Topic</th>
                        <th>Goal</th>
                        <th>Status</th>
                    </tr>
                </thead>
                <tbody>
                    ${studyPlan.map(day => `
                        <tr>
                            <td>${day.day}</td>
                            <td>${day.topic}</td>
                            <td>${day.goal}</td>
                            <td><span class="status-badge status-${day.status === 'completed' ? 'completed' : 'upcoming'}">
                                ${day.status === 'completed' ? '✅ Done' : 'Planned'}
                            </span></td>
                        </tr>
                    `).join('')}
                </tbody>
            </table>
        </div>
    </div>

    <script>
        // Update countdown timer
        function updateCountdown() {
            const targetDate = new Date('2026-01-22');
            const now = new Date();
            const difference = targetDate - now;
            const days = Math.ceil(difference / (1000 * 60 * 60 * 24));
            document.getElementById('countdown-days').textContent = days;
        }
        
        updateCountdown();
        setInterval(updateCountdown, 24 * 60 * 60 * 1000);
        
        console.log('AMC8 Dashboard loaded successfully!');
    </script>
</body>
</html>
    `);
});

module.exports = router;