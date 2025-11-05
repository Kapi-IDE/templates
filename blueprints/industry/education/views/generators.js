/**
 * AMC8 Learning Platform - HTML Generators
 * Functions for generating complete HTML pages and components
 */

const { generatePageCSS, generateHTMLHead } = require('./styles');
const { generateBreadcrumb } = require('../utils/helpers');

/**
 * Generates interactive practice session HTML
 * Creates a full practice/test interface with timer, navigation, and scoring
 * Supports both practice mode (show solutions immediately) and test mode (timed)
 * @param {Array} problems - Array of problem objects to display
 * @param {string} title - Title for the practice session
 * @param {boolean} isTestMode - Whether this is a timed test (default: false)
 * @returns {string} Complete interactive HTML page with JavaScript
 */
function generatePracticeHTML(problems, title, isTestMode = false) {
    return `
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>${title} - AMC8 Hub</title>
    <script src="https://polyfill.io/v3/polyfill.min.js?features=es6"></script>
    <script id="MathJax-script" async src="https://cdn.jsdelivr.net/npm/mathjax@3/es5/tex-mml-chtml.js"></script>
    <style>
        body { font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif; line-height: 1.6; margin: 0; padding: 20px; background: #f5f7fa; }
        .container { max-width: 800px; margin: 0 auto; }
        .header { background: white; padding: 25px; border-radius: 10px; box-shadow: 0 2px 10px rgba(0,0,0,0.1); margin-bottom: 20px; text-align: center; }
        .progress { background: #e0e0e0; height: 8px; border-radius: 4px; margin: 20px 0; }
        .progress-bar { background: #3498db; height: 100%; border-radius: 4px; transition: width 0.3s ease; }
        .problem-card { background: white; padding: 30px; border-radius: 10px; box-shadow: 0 2px 10px rgba(0,0,0,0.1); margin-bottom: 20px; }
        .problem-header { font-size: 1.1em; color: #7f8c8d; margin-bottom: 15px; }
        .problem-statement { font-size: 1.2em; margin-bottom: 25px; line-height: 1.8; color: #2c3e50; }
        .choices { list-style: none; padding: 0; }
        .choice { background: #f8f9fa; margin: 8px 0; padding: 15px; border-radius: 8px; cursor: pointer; transition: all 0.3s ease; border: 2px solid transparent; }
        .choice:hover { background: #e3f2fd; }
        .choice.selected { background: #bbdefb; border-color: #2196f3; }
        .choice.correct { background: #c8e6c9; border-color: #4caf50; }
        .choice.incorrect { background: #ffcdd2; border-color: #f44336; }
        .solution { background: #e8f5e8; padding: 20px; border-radius: 8px; margin-top: 20px; display: none; }
        .solution.show { display: block; }
        .solution-title { font-weight: bold; color: #2e7d32; margin-bottom: 10px; }
        .controls { text-align: center; margin-top: 30px; }
        .btn { display: inline-block; padding: 12px 25px; margin: 0 10px; background: #3498db; color: white; text-decoration: none; border: none; border-radius: 6px; cursor: pointer; font-size: 16px; }
        .btn:hover { background: #2980b9; }
        .btn:disabled { background: #bdc3c7; cursor: not-allowed; }
        .btn-success { background: #27ae60; }
        .btn-success:hover { background: #229954; }
        .results { background: white; padding: 30px; border-radius: 10px; box-shadow: 0 2px 10px rgba(0,0,0,0.1); text-align: center; }
        .score { font-size: 3em; font-weight: bold; color: #3498db; margin: 20px 0; }
        .hidden { display: none; }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>${title}</h1>
            <div class="progress">
                <div class="progress-bar" id="progressBar" style="width: 0%"></div>
            </div>
            <div id="progressText">Problem 1 of ${problems.length}</div>
            ${isTestMode ? '<div id="timer" style="font-size: 1.2em; color: #e74c3c; margin-top: 10px;">40:00</div>' : ''}
        </div>
        
        <div id="problemArea">
            ${problems.map((problem, index) => `
                <div class="problem-card ${index === 0 ? '' : 'hidden'}" data-index="${index}">
                    <div class="problem-header">Problem ${index + 1} (${problem.year} AMC8 #${problem.problem_num})</div>
                    <div class="problem-statement">${problem.statement}</div>
                    <ul class="choices">
                        ${Object.entries(problem.choices).map(([letter, text]) => `
                            <li class="choice" data-answer="${letter}" onclick="selectChoice(${index}, '${letter}')">
                                <strong>(${letter})</strong> ${text}
                            </li>
                        `).join('')}
                    </ul>
                    <div class="solution" id="solution${index}">
                        <div class="solution-title">💡 Solution:</div>
                        <div>${problem.solution}</div>
                    </div>
                </div>
            `).join('')}
        </div>
        
        <div class="controls">
            <button class="btn" onclick="previousProblem()" id="prevBtn" disabled>← Previous</button>
            <button class="btn" onclick="submitAnswer()" id="submitBtn" disabled>Submit Answer</button>
            <button class="btn hidden" onclick="nextProblem()" id="nextBtn">Next →</button>
            <button class="btn btn-success hidden" onclick="showResults()" id="finishBtn">Finish Session</button>
        </div>
        
        <div class="results hidden" id="results">
            <h2>🎉 Session Complete!</h2>
            <div class="score" id="scoreDisplay">0/0</div>
            <div id="scoreMessage"></div>
            <div style="margin-top: 30px;">
                <a href="/practice" class="btn">New Practice Session</a>
                <a href="/" class="btn">Back to Home</a>
            </div>
        </div>
    </div>
    
    <script>
        const problems = ${JSON.stringify(problems)};
        const isTestMode = ${isTestMode};
        let currentProblem = 0;
        let userAnswers = new Array(problems.length).fill(null);
        let startTime = Date.now();
        let timerInterval;
        
        function updateProgress() {
            const progress = ((currentProblem + 1) / problems.length) * 100;
            document.getElementById('progressBar').style.width = progress + '%';
            document.getElementById('progressText').textContent = \`Problem \${currentProblem + 1} of \${problems.length}\`;
        }
        
        function selectChoice(problemIndex, answer) {
            if (problemIndex !== currentProblem) return;
            
            // Clear previous selections
            document.querySelectorAll(\`.problem-card[data-index="\${problemIndex}"] .choice\`).forEach(choice => {
                choice.classList.remove('selected');
            });
            
            // Mark selected choice
            document.querySelector(\`.problem-card[data-index="\${problemIndex}"] .choice[data-answer="\${answer}"]\`).classList.add('selected');
            
            userAnswers[problemIndex] = answer;
            document.getElementById('submitBtn').disabled = false;
        }
        
        function submitAnswer() {
            const problem = problems[currentProblem];
            const userAnswer = userAnswers[currentProblem];
            const correctAnswer = problem.answer;
            
            // Show correct/incorrect styling
            document.querySelectorAll(\`.problem-card[data-index="\${currentProblem}"] .choice\`).forEach(choice => {
                const choiceAnswer = choice.dataset.answer;
                if (choiceAnswer === correctAnswer) {
                    choice.classList.add('correct');
                } else if (choiceAnswer === userAnswer && userAnswer !== correctAnswer) {
                    choice.classList.add('incorrect');
                }
            });
            
            // Show solution in practice mode
            if (!isTestMode) {
                document.getElementById(\`solution\${currentProblem}\`).classList.add('show');
            }
            
            // Update buttons
            document.getElementById('submitBtn').classList.add('hidden');
            if (currentProblem < problems.length - 1) {
                document.getElementById('nextBtn').classList.remove('hidden');
            } else {
                document.getElementById('finishBtn').classList.remove('hidden');
            }
        }
        
        function nextProblem() {
            if (currentProblem < problems.length - 1) {
                // Hide current problem
                document.querySelector(\`.problem-card[data-index="\${currentProblem}"]\`).classList.add('hidden');
                currentProblem++;
                
                // Show next problem
                document.querySelector(\`.problem-card[data-index="\${currentProblem}"]\`).classList.remove('hidden');
                
                // Reset buttons
                document.getElementById('nextBtn').classList.add('hidden');
                document.getElementById('submitBtn').classList.remove('hidden');
                document.getElementById('submitBtn').disabled = userAnswers[currentProblem] === null;
                
                // Update prev button
                document.getElementById('prevBtn').disabled = currentProblem === 0;
                
                updateProgress();
                MathJax.typesetPromise();
            }
        }
        
        function previousProblem() {
            if (currentProblem > 0) {
                // Hide current problem
                document.querySelector(\`.problem-card[data-index="\${currentProblem}"]\`).classList.add('hidden');
                currentProblem--;
                
                // Show previous problem
                document.querySelector(\`.problem-card[data-index="\${currentProblem}"]\`).classList.remove('hidden');
                
                // Update buttons based on previous problem state
                if (userAnswers[currentProblem] !== null) {
                    // Answer was already submitted for this problem
                    document.getElementById('submitBtn').classList.add('hidden');
                    if (currentProblem < problems.length - 1) {
                        document.getElementById('nextBtn').classList.remove('hidden');
                    } else {
                        document.getElementById('finishBtn').classList.remove('hidden');
                    }
                } else {
                    // No answer submitted yet
                    document.getElementById('submitBtn').classList.remove('hidden');
                    document.getElementById('submitBtn').disabled = true;
                    document.getElementById('nextBtn').classList.add('hidden');
                    document.getElementById('finishBtn').classList.add('hidden');
                }
                
                document.getElementById('prevBtn').disabled = currentProblem === 0;
                updateProgress();
                MathJax.typesetPromise();
            }
        }
        
        function showResults() {
            clearInterval(timerInterval);
            
            // Calculate score
            let correct = 0;
            problems.forEach((problem, index) => {
                if (userAnswers[index] === problem.answer) {
                    correct++;
                }
            });
            
            // Hide problem area and show results
            document.getElementById('problemArea').classList.add('hidden');
            document.querySelector('.controls').classList.add('hidden');
            document.getElementById('results').classList.remove('hidden');
            
            // Display score
            const percentage = Math.round((correct / problems.length) * 100);
            document.getElementById('scoreDisplay').textContent = \`\${correct}/\${problems.length}\`;
            
            let message = '';
            if (percentage >= 80) {
                message = '🌟 Excellent work! You\\'re ready for the AMC8!';
            } else if (percentage >= 60) {
                message = '👍 Good job! Keep practicing to improve your score.';
            } else {
                message = '📚 Keep studying! Review the solutions and try again.';
            }
            document.getElementById('scoreMessage').textContent = message;
            
            // Save score to backend
            const timeSpent = Math.round((Date.now() - startTime) / 1000);
            fetch('/api/save-score', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({
                    score: correct,
                    totalQuestions: problems.length,
                    timeSpent: timeSpent,
                    mode: isTestMode ? 'test' : 'practice'
                })
            });
        }
        
        // Timer for test mode
        if (isTestMode) {
            let timeLeft = 40 * 60; // 40 minutes in seconds
            timerInterval = setInterval(() => {
                timeLeft--;
                const minutes = Math.floor(timeLeft / 60);
                const seconds = timeLeft % 60;
                document.getElementById('timer').textContent = \`\${minutes}:\${seconds.toString().padStart(2, '0')}\`;
                
                if (timeLeft <= 0) {
                    clearInterval(timerInterval);
                    showResults();
                }
            }, 1000);
        }
        
        updateProgress();
    </script>
</body>
</html>
    `;
}

/**
 * Generates a simple HTML page with title and content
 * @param {string} title - Page title
 * @param {string} content - HTML content for the page body
 * @param {string} additionalCSS - Optional additional CSS
 * @returns {string} Complete HTML page
 */
function generateSimplePage(title, content, additionalCSS = '') {
    return `
<!DOCTYPE html>
<html lang="en">
${generateHTMLHead(title, generatePageCSS(additionalCSS))}
<body>
    <div class="container">
        ${content}
    </div>
</body>
</html>`;
}

/**
 * Generates a page with header and navigation
 * @param {string} title - Page title
 * @param {string} content - HTML content for the page body
 * @param {Array} breadcrumbs - Breadcrumb navigation items
 * @param {string} additionalCSS - Optional additional CSS
 * @returns {string} Complete HTML page with navigation
 */
function generatePageWithNav(title, content, breadcrumbs = [], additionalCSS = '') {
    const breadcrumbHTML = breadcrumbs.length > 0 ? generateBreadcrumb(breadcrumbs) : '';
    
    return `
<!DOCTYPE html>
<html lang="en">
${generateHTMLHead(title, generatePageCSS(additionalCSS))}
<body>
    <div class="container">
        <div class="card">
            ${breadcrumbHTML}
            <div class="header">
                <h1>${title}</h1>
            </div>
            ${content}
        </div>
    </div>
</body>
</html>`;
}

module.exports = {
    generatePracticeHTML,
    generateSimplePage,
    generatePageWithNav
};