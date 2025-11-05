/**
 * AMC8 Learning Platform - Study Routes
 * Handles study guide, topic-specific study content, and educational resources
 */

const express = require('express');
const router = express.Router();

// Import utilities
const { generateHTMLHead, generatePageCSS } = require('../views/styles');
const { generateBreadcrumb } = require('../utils/helpers');
const { getProblemsByTopic } = require('../services/questionBank');

// AMC8 Topics Data Structure
const AMC8_TOPICS = {
    'Arithmetic': {
        description: 'Basic operations, fractions, decimals, and percentages',
        skills: ['Integer operations', 'Fraction arithmetic', 'Decimal calculations', 'Percentage problems', 'Order of operations', 'Estimation techniques']
    },
    'Geometry': {
        description: 'Shapes, area, perimeter, and coordinate geometry',
        skills: ['Area and perimeter', 'Volume and surface area', 'Coordinate geometry', 'Similar triangles', 'Angle relationships', 'Geometric transformations']
    },
    'Number Theory': {
        description: 'Divisibility, prime numbers, and number properties',
        skills: ['Prime factorization', 'GCD and LCM', 'Divisibility rules', 'Modular arithmetic', 'Diophantine equations', 'Number patterns']
    },
    'Algebra': {
        description: 'Variables, equations, and algebraic expressions',
        skills: ['Solving linear equations', 'Systems of equations', 'Algebraic manipulation', 'Word problems', 'Inequalities', 'Functions']
    },
    'Combinatorics': {
        description: 'Counting, probability, and logical reasoning',
        skills: ['Counting principles', 'Permutations and combinations', 'Probability basics', 'Logical reasoning', 'Casework', 'Pigeonhole principle']
    },
    'Word Problems': {
        description: 'Real-world applications and problem-solving strategies',
        skills: ['Rate and time problems', 'Money and business', 'Age problems', 'Distance and travel', 'Mixture problems', 'Logic puzzles']
    }
};

/**
 * Study Guide Main Route - Unified Learning Experience
 * Shows engaging module cards with colorful UX for interactive learning
 * Combines the best of /modules UX with /study content depth
 */
router.get('/', (req, res) => {
    res.send(`
<!DOCTYPE html>
<html lang="en">
${generateHTMLHead('🧠 Math Learning Hub', generatePageCSS(`
    .container {
        max-width: 900px;
        margin: 0 auto;
        background: rgba(255, 255, 255, 0.95);
        border-radius: 20px;
        padding: 30px;
        box-shadow: 0 15px 35px rgba(0, 0, 0, 0.1);
    }
    .header p {
        font-size: 1.3em;
    }
    .module-icon {
        font-size: 4em;
        margin-bottom: 15px;
    }
    .module-title {
        font-size: 1.5em;
        font-weight: bold;
        color: #2c3e50;
        margin-bottom: 10px;
    }
    .module-description {
        color: #7f8c8d;
        margin-bottom: 20px;
    }
    .start-btn {
        background: linear-gradient(135deg, #3498db, #2980b9);
        color: white;
        border: none;
        padding: 15px 30px;
        border-radius: 25px;
        font-size: 1.1em;
        font-weight: bold;
        cursor: pointer;
        transition: all 0.3s ease;
        text-decoration: none;
        display: inline-block;
    }
    .start-btn:hover {
        transform: translateY(-2px);
        box-shadow: 0 8px 20px rgba(52, 152, 219, 0.4);
    }
    .footer {
        text-align: center;
        margin-top: 40px;
        padding-top: 20px;
        border-top: 2px solid #ecf0f1;
    }
    .footer h3 {
        color: #27ae60;
        margin-bottom: 10px;
    }
`))}
<body>
    <div class="container">
        <div class="header">
            <h1>🧠 Math Learning Hub</h1>
            <p>Interactive learning modules designed just for you!</p>
        </div>
        
        <div class="modules-grid">
            ${Object.entries(AMC8_TOPICS).map(([topic, info]) => {
                const icons = {
                    'Arithmetic': '🔢',
                    'Geometry': '📐', 
                    'Number Theory': '🔍',
                    'Algebra': '📊',
                    'Combinatorics': '🎲',
                    'Word Problems': '📝'
                };
                const difficulties = {
                    'Arithmetic': 'beginner',
                    'Geometry': 'intermediate',
                    'Number Theory': 'intermediate', 
                    'Algebra': 'intermediate',
                    'Combinatorics': 'advanced',
                    'Word Problems': 'beginner'
                };
                
                return `
                <div class="module-card" onclick="location.href='/study/${encodeURIComponent(topic.toLowerCase())}'">
                    <div class="module-icon">${icons[topic] || '📚'}</div>
                    <div class="module-title">${topic}</div>
                    <div class="module-description">${info.description}</div>
                    <div class="difficulty-badge difficulty-${difficulties[topic] || 'beginner'}">
                        ${(difficulties[topic] || 'beginner').charAt(0).toUpperCase() + (difficulties[topic] || 'beginner').slice(1)}
                    </div>
                    <div class="lesson-count">${info.skills.length} lessons</div><br>
                    <a href="/study/${encodeURIComponent(topic.toLowerCase())}" class="start-btn">Start Learning! 🚀</a>
                </div>
                `;
            }).join('')}
        </div>
        
        <div class="footer">
            <h3>🌟 Ready to become a math superstar? 🌟</h3>
            <p>Pick any module above to start your amazing math journey!</p>
        </div>
    </div>
</body>
</html>
    `);
});

/**
 * Individual Topic Module Route
 * Shows engaging module interface with lessons, videos, and practice problems
 * Unified learning experience combining modules UX with study content
 */
router.get('/:topicId', (req, res) => {
    const topicId = req.params.topicId;
    
    // Handle geometry module specifically with enhanced experience
    if (topicId === 'geometry') {
        const geometryProblems = getProblemsByTopic('geometry');
        
        const module = {
            id: 'geometry',
            title: '📐 Geometry Mastery',
            description: 'Master shapes, areas, perimeters, and coordinate geometry step by step!',
            difficulty: 'intermediate',
            totalLessons: 8,
            contents: [
                { id: 1, type: "learn", title: "Geometry Fundamentals", description: "Basic shapes and properties" },
                { id: 2, type: "video", title: "Area and Perimeter Magic", description: "Visual explanations of area and perimeter" },
                { id: 3, type: "question", title: "Shape Practice", description: "Practice with basic geometric shapes" },
                { id: 4, type: "learn", title: "Coordinate Geometry", description: "Working with the coordinate plane" },
                { id: 5, type: "question", title: "Coordinate Challenges", description: "Advanced coordinate geometry problems" },
                { id: 6, type: "video", title: "Volume and Surface Area", description: "3D geometry concepts" },
                { id: 7, type: "question", title: "Real AMC8 Problems", description: `Practice with ${geometryProblems.length} geometry problems` },
                { id: 8, type: "quiz", title: "Geometry Mastery Test", description: "Test your complete understanding" }
            ]
        };
        
        res.send(`
<!DOCTYPE html>
<html lang="en">
${generateHTMLHead('📐 Geometry Mastery Module', generatePageCSS(`
    .container {
        max-width: 800px;
        margin: 0 auto;
        background: rgba(255, 255, 255, 0.95);
        border-radius: 20px;
        padding: 30px;
        box-shadow: 0 15px 35px rgba(0, 0, 0, 0.1);
    }
    .module-header {
        text-align: center;
        margin-bottom: 30px;
        padding-bottom: 20px;
        border-bottom: 3px solid #e3f2fd;
    }
    .module-title {
        font-size: 2.5em;
        color: #2c3e50;
        margin-bottom: 10px;
    }
    .module-description {
        font-size: 1.2em;
        color: #7f8c8d;
        margin-bottom: 20px;
    }
    .progress-section {
        background: #e8f5e8;
        padding: 20px;
        border-radius: 15px;
        margin-bottom: 30px;
        text-align: center;
    }
    .progress-bar {
        background: #ddd;
        height: 20px;
        border-radius: 10px;
        overflow: hidden;
        margin: 15px 0;
    }
    .progress-fill {
        background: linear-gradient(90deg, #2ecc71, #27ae60);
        height: 100%;
        border-radius: 10px;
        transition: width 0.3s ease;
    }
    .lessons-list {
        list-style: none;
        padding: 0;
    }
    .lesson-item {
        background: #f8f9fa;
        margin: 15px 0;
        padding: 20px;
        border-radius: 15px;
        border-left: 5px solid #3498db;
        transition: all 0.3s ease;
        cursor: pointer;
    }
    .lesson-item:hover {
        transform: translateX(10px);
        background: #e3f2fd;
        border-left-color: #2196f3;
    }
    .lesson-number {
        font-size: 1.5em;
        font-weight: bold;
        color: #3498db;
        margin-bottom: 8px;
    }
    .lesson-title {
        font-size: 1.2em;
        font-weight: bold;
        color: #2c3e50;
        margin-bottom: 5px;
    }
    .lesson-description {
        color: #7f8c8d;
        font-size: 0.9em;
        margin-bottom: 10px;
    }
    .lesson-type {
        display: inline-block;
        padding: 4px 12px;
        border-radius: 12px;
        font-size: 0.8em;
        font-weight: bold;
        margin-bottom: 10px;
    }
    .type-learn { background: #e3f2fd; color: #1976d2; }
    .type-video { background: #fce4ec; color: #c2185b; }
    .type-question { background: #fff3e0; color: #f57c00; }
    .type-quiz { background: #f3e5f5; color: #7b1fa2; }
`))}
<body>
    <div class="container">
        <div class="module-header">
            <h1 class="module-title">${module.title}</h1>
            <p class="module-description">${module.description}</p>
            <div class="difficulty-badge difficulty-${module.difficulty}">
                ${module.difficulty.charAt(0).toUpperCase() + module.difficulty.slice(1)} Level
            </div>
        </div>
        
        <div class="progress-section">
            <h3>📊 Your Progress</h3>
            <div class="progress-bar">
                <div class="progress-fill" style="width: 0%"></div>
            </div>
            <p>0 of ${module.totalLessons} lessons completed</p>
        </div>
        
        <h3>📚 Learning Path:</h3>
        <ul class="lessons-list">
            ${module.contents.map(content => `
            <li class="lesson-item" onclick="location.href='/study/${module.id}/lesson/${content.id}'">
                <div class="lesson-number">Lesson ${content.id}</div>
                <div class="lesson-title">${content.title}</div>
                <div class="lesson-description">${content.description}</div>
                <span class="lesson-type type-${content.type}">
                    ${content.type === 'learn' ? '📖 Learn' : 
                      content.type === 'video' ? '🎥 Video' :
                      content.type === 'question' ? '❓ Practice' :
                      content.type === 'quiz' ? '🏆 Quiz' : content.type}
                </span>
            </li>
            `).join('')}
        </ul>
        
        <div style="text-align: center; margin-top: 30px;">
            <a href="/study" class="btn btn-secondary">← Back to Learning Hub</a>
        </div>
    </div>
</body>
</html>
        `);
        return;
    }
    
    // Handle other topics with the original format
    const topicData = Object.entries(AMC8_TOPICS).find(
        ([key]) => key.toLowerCase() === topicId
    );
    
    if (!topicData) {
        return res.status(404).send('Topic not found');
    }
    
    const [displayName, info] = topicData;
    
    res.send(`
<!DOCTYPE html>
<html lang="en">
${generateHTMLHead(`Study ${displayName}`, generatePageCSS())}
<body>
    <div class="container">
        ${generateBreadcrumb([
            {text: 'Dashboard', url: '/'},
            {text: 'Study Guide', url: '/study'},
            {text: displayName}
        ])}
        
        <div class="header">
            <h1>📚 ${displayName}</h1>
            <p>${info.description}</p>
        </div>
        
        <div class="card">
            <h3>🎯 Key Skills to Master</h3>
            <ul>
                ${info.skills.map(skill => `<li>${skill}</li>`).join('')}
            </ul>
        </div>
        
        <div class="card">
            <h3>📖 Study Resources</h3>
            <p>Curated external resources for mastering ${displayName}:</p>
            <ul>
                <li><a href="https://artofproblemsolving.com/wiki/index.php/AMC_8_Problems_and_Solutions" target="_blank">🏆 AoPS AMC8 Problem Database</a> - Official past problems and solutions</li>
                <li><a href="https://www.khanacademy.org/" target="_blank">📚 Khan Academy - ${displayName}</a> - Free video lessons and practice</li>
                <li><a href="https://brilliant.org/" target="_blank">💡 Brilliant Problem Solving</a> - Interactive math challenges</li>
                <li><a href="https://www.omegalearn.org/mastering-amc8" target="_blank">📖 Mastering AMC8 (Free PDF)</a> - Comprehensive preparation guide</li>
                <li><a href="https://www.thethinkacademy.com/amc-8" target="_blank">🎯 Think Academy AMC8 Prep</a> - Structured competition training</li>
                <li><a href="https://alphastar.academy/amc-8/" target="_blank">⭐ AlphaStar Academy</a> - Advanced AMC8 preparation courses</li>
            </ul>
        </div>
        
        <div class="card">
            <h3>🎮 Practice Problems</h3>
            <p>Ready to practice ${displayName.toLowerCase()} problems?</p>
            <div style="text-align: center; margin-top: 20px;">
                <a href="/practice" class="btn btn-large btn-primary">Start Practice Session</a>
                <a href="/browse" class="btn btn-large btn-secondary">Browse Problem Bank</a>
            </div>
        </div>
        
        <div style="text-align: center; margin-top: 30px;">
            <a href="/study" class="btn btn-secondary">← Back to Study Guide</a>
        </div>
    </div>
</body>
</html>
    `);
});

/**
 * Individual Lesson Route for Enhanced Modules
 * Shows detailed lesson content with navigation and interactive elements
 */
router.get('/:topicId/lesson/:lessonId', (req, res) => {
    const { topicId, lessonId } = req.params;
    
    if (topicId === 'geometry') {
        const lessonNum = parseInt(lessonId);
        const geometryProblems = getProblemsByTopic('geometry');
        
        const lessons = {
            1: {
                title: "Geometry Fundamentals 📐",
                type: "learn",
                content: `
                    <h2>Welcome to Geometry! 🎉</h2>
                    <p>Geometry is the study of shapes, sizes, and the properties of space. Let's start with the basics!</p>
                    
                    <h3>Basic Shapes 🔺</h3>
                    <ul>
                        <li><strong>Triangle:</strong> A shape with 3 sides and 3 angles</li>
                        <li><strong>Rectangle:</strong> A shape with 4 sides and 4 right angles</li>
                        <li><strong>Circle:</strong> A round shape where all points are the same distance from the center</li>
                        <li><strong>Square:</strong> A special rectangle where all sides are equal</li>
                    </ul>
                    
                    <h3>Key Formulas 📊</h3>
                    <div style="background: #f0f8ff; padding: 15px; border-radius: 8px; margin: 15px 0;">
                        <p><strong>Area of Rectangle:</strong> $A = length \\times width$</p>
                        <p><strong>Area of Triangle:</strong> $A = \\frac{1}{2} \\times base \\times height$</p>
                        <p><strong>Area of Circle:</strong> $A = \\pi r^2$</p>
                        <p><strong>Perimeter of Rectangle:</strong> $P = 2(length + width)$</p>
                    </div>
                    
                    <h3>Practice Problem 🎯</h3>
                    <div style="background: #fff3e0; padding: 15px; border-radius: 8px; margin: 15px 0;">
                        <p><strong>Example:</strong> Find the area of a rectangle with length 8 cm and width 5 cm.</p>
                        <p><strong>Solution:</strong> $A = 8 \\times 5 = 40$ square cm</p>
                    </div>
                `
            },
            7: {
                title: "Real AMC8 Geometry Problems 🏆",
                type: "question", 
                content: `
                    <h2>Practice with Real AMC8 Problems! 🎯</h2>
                    <p>Now let's practice with actual geometry problems from past AMC8 competitions.</p>
                    
                    <div class="problems-section">
                        <h3>Available Geometry Problems: ${geometryProblems.length}</h3>
                        ${geometryProblems.slice(0, 3).map(problem => `
                            <div style="background: #f8f9fa; padding: 20px; margin: 15px 0; border-radius: 10px; border-left: 4px solid #28a745;">
                                <h4>${problem.year} AMC8 Problem ${problem.problem_num}</h4>
                                <p style="margin: 15px 0; line-height: 1.6;">${problem.statement}</p>
                                <div style="margin: 10px 0;">
                                    ${Object.entries(problem.choices).map(([letter, choice]) => 
                                        `<div style="margin: 5px 0;"><strong>(${letter})</strong> ${choice}</div>`
                                    ).join('')}
                                </div>
                                ${problem.answer ? `<div style="color: #28a745; font-weight: bold; margin-top: 15px;">Answer: ${problem.answer}</div>` : ''}
                                ${problem.solution ? `<div style="background: #e8f5e8; padding: 10px; border-radius: 5px; margin-top: 10px;"><strong>Solution:</strong> ${problem.solution}</div>` : ''}
                            </div>
                        `).join('')}
                        
                        <div style="text-align: center; margin: 20px 0;">
                            <a href="/practice" style="background: #007bff; color: white; padding: 10px 20px; text-decoration: none; border-radius: 5px; display: inline-block;">
                                🎮 Practice All Geometry Problems
                            </a>
                        </div>
                    </div>
                `
            }
        };
        
        const lesson = lessons[lessonNum] || {
            title: "Coming Soon! 🚧",
            type: "learn",
            content: `
                <h2>This lesson is being developed! 🛠️</h2>
                <p>We're working hard to create amazing content for this lesson.</p>
                <p>Check back soon for interactive learning experiences!</p>
            `
        };
        
        res.send(`
<!DOCTYPE html>
<html lang="en">
${generateHTMLHead(lesson.title, generatePageCSS(`
    .lesson-container {
        max-width: 900px;
        margin: 0 auto;
        background: rgba(255, 255, 255, 0.95);
        border-radius: 20px;
        padding: 30px;
        box-shadow: 0 15px 35px rgba(0, 0, 0, 0.1);
    }
    .lesson-header {
        text-align: center;
        margin-bottom: 30px;
        padding-bottom: 20px;
        border-bottom: 3px solid #e3f2fd;
    }
    .lesson-content {
        line-height: 1.8;
        color: #333;
    }
    .lesson-content h2 {
        color: #2c3e50;
        margin-top: 30px;
        margin-bottom: 15px;
    }
    .lesson-content h3 {
        color: #3498db;
        margin-top: 25px;
        margin-bottom: 10px;
    }
    .navigation-buttons {
        display: flex;
        justify-content: space-between;
        align-items: center;
        margin-top: 40px;
        padding-top: 20px;
        border-top: 2px solid #ecf0f1;
    }
    .nav-btn {
        display: inline-block;
        padding: 12px 24px;
        background: #3498db;
        color: white;
        text-decoration: none;
        border-radius: 8px;
        font-weight: bold;
        transition: all 0.3s ease;
    }
    .nav-btn:hover {
        background: #2980b9;
        transform: translateY(-2px);
    }
    .nav-btn.secondary {
        background: #95a5a6;
    }
    .nav-btn.secondary:hover {
        background: #7f8c8d;
    }
`))}
<body>
    <div class="lesson-container">
        <div class="lesson-header">
            <h1>${lesson.title}</h1>
            <p>Lesson ${lessonId} of 8 • Geometry Mastery Module</p>
        </div>
        
        <div class="lesson-content">
            ${lesson.content}
        </div>
        
        <div class="navigation-buttons">
            <div>
                ${lessonNum > 1 ? 
                    `<a href="/study/geometry/lesson/${lessonNum - 1}" class="nav-btn">← Previous Lesson</a>` :
                    `<a href="/study/geometry" class="nav-btn secondary">← Back to Module</a>`
                }
            </div>
            
            <div style="text-align: center; color: #7f8c8d; font-weight: bold;">
                ${lessonNum} / 8
            </div>
            
            <div>
                ${lessonNum < 8 ? 
                    `<a href="/study/geometry/lesson/${lessonNum + 1}" class="nav-btn">Next Lesson →</a>` :
                    `<a href="/study/geometry" class="nav-btn secondary">Module Complete! 🎉</a>`
                }
            </div>
        </div>
    </div>
    
    <script>
        // Initialize MathJax if present
        if (window.MathJax) {
            MathJax.typesetPromise();
        }
    </script>
</body>
</html>
        `);
        return;
    }
    
    // Default lesson route for other topics
    res.status(404).send('Lesson not found');
});

/**
 * API route for geometry problems
 * Returns filtered geometry problems for the module
 */
router.get('/api/problems/geometry', (req, res) => {
    const geometryProblems = getProblemsByTopic('geometry');
    res.json({
        topic: 'geometry',
        count: geometryProblems.length,
        problems: geometryProblems
    });
});

module.exports = router;