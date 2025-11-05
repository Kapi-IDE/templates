/**
 * AMC8 Learning Platform - Browse Routes
 * Handles problem browsing, searching, and year-based filtering
 */

const express = require('express');
const router = express.Router();

// Import services
const { 
    getStatistics,
    getProblemsByYear,
    searchProblems,
    getQuestionBank
} = require('../services/questionBank');

/**
 * Problem Browser Main Route
 * Shows overview of problems organized by year with search functionality
 */
router.get('/', (req, res) => {
    const stats = getStatistics();
    res.send(`
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Problem Browser - AMC8 Hub</title>
    <script src="https://polyfill.io/v3/polyfill.min.js?features=es6"></script>
    <script id="MathJax-script" async src="https://cdn.jsdelivr.net/npm/mathjax@3/es5/tex-mml-chtml.js"></script>
    <style>
        body { font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif; line-height: 1.6; margin: 0; padding: 20px; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); min-height: 100vh; }
        .container { max-width: 1000px; margin: 0 auto; background: white; padding: 30px; border-radius: 15px; box-shadow: 0 10px 25px rgba(0,0,0,0.1); }
        .search-bar { margin-bottom: 30px; }
        .form-control { width: 100%; padding: 12px; border: 2px solid #ddd; border-radius: 6px; font-size: 16px; }
        .years-grid { display: grid; grid-template-columns: repeat(auto-fill, minmax(200px, 1fr)); gap: 15px; margin-top: 20px; }
        .year-card { background: #f8f9fa; padding: 15px; border-radius: 8px; text-align: center; transition: transform 0.3s ease; }
        .year-card:hover { transform: translateY(-3px); box-shadow: 0 5px 15px rgba(0,0,0,0.1); }
        .year-title { font-size: 1.2em; font-weight: bold; color: #2c3e50; }
        .year-count { color: #7f8c8d; margin: 10px 0; }
        .progress-bar { background: #e0e0e0; height: 8px; border-radius: 4px; overflow: hidden; margin: 10px 0; }
        .progress-fill { background: #3498db; height: 100%; border-radius: 4px; }
        .btn { display: inline-block; padding: 8px 15px; background: #3498db; color: white; text-decoration: none; border-radius: 4px; }
        .btn:hover { background: #2980b9; }
        .btn-secondary { background: #95a5a6; }
        .btn-secondary:hover { background: #7f8c8d; }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>📊 Problem Browser</h1>
            <p>Explore problems by year or search for specific topics</p>
        </div>
        
        <div class="search-bar">
            <form action="/browse/search" method="get">
                <input type="text" name="q" class="form-control" placeholder="Search problems by keyword..." value="${req.query.q || ''}">
                <button type="submit" class="btn" style="margin-top: 10px;">Search Problems</button>
            </form>
        </div>
        
        <h3>Browse by Year</h3>
        <div class="years-grid">
            ${stats.years.slice().reverse().map(year => {
                const count = stats.byYear[year];
                const percentage = (count / 25) * 100;
                return `
                <div class="year-card">
                    <div class="year-title">${year}</div>
                    <div class="year-count">${count}/25 problems</div>
                    <div class="progress-bar">
                        <div class="progress-fill" style="width: ${percentage}%"></div>
                    </div>
                    <a href="/browse/year/${year}" class="btn">View Problems</a>
                </div>
                `;
            }).join('')}
        </div>
        
        <div style="text-align: center; margin-top: 30px;">
            <a href="/" class="btn btn-secondary">Back to Home</a>
        </div>
    </div>
</body>
</html>
    `);
});

/**
 * Browse Problems by Year
 * Shows all problems from a specific AMC8 year
 */
router.get('/year/:year', (req, res) => {
    const year = parseInt(req.params.year);
    const problems = getProblemsByYear(year);
    
    if (problems.length === 0) {
        return res.status(404).send(`
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Year ${year} Not Found - AMC8 Hub</title>
    <style>
        body { font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif; text-align: center; padding: 50px; }
        .error { background: #f8d7da; color: #721c24; padding: 20px; border-radius: 8px; margin: 20px auto; max-width: 500px; }
    </style>
</head>
<body>
    <h1>🔍 Year ${year} Not Found</h1>
    <div class="error">No problems found for AMC8 ${year}. This year may not be available in our database yet.</div>
    <a href="/browse" style="color: #3498db; text-decoration: none;">← Back to Problem Browser</a>
</body>
</html>
        `);
    }
    
    res.send(`
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>AMC8 ${year} Problems - AMC8 Hub</title>
    <script src="https://polyfill.io/v3/polyfill.min.js?features=es6"></script>
    <script id="MathJax-script" async src="https://cdn.jsdelivr.net/npm/mathjax@3/es5/tex-mml-chtml.js"></script>
    <style>
        body { font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif; line-height: 1.6; margin: 0; padding: 20px; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); min-height: 100vh; }
        .container { max-width: 900px; margin: 0 auto; background: white; padding: 30px; border-radius: 15px; box-shadow: 0 10px 25px rgba(0,0,0,0.1); }
        .problem-card { background: #f8f9fa; padding: 20px; margin: 15px 0; border-radius: 8px; border-left: 4px solid #3498db; }
        .problem-header { font-weight: bold; color: #2c3e50; margin-bottom: 10px; }
        .problem-statement { margin: 15px 0; line-height: 1.8; }
        .choices { list-style: none; padding: 0; margin: 15px 0; }
        .choices li { background: #e9ecef; padding: 8px; margin: 5px 0; border-radius: 4px; }
        .btn { display: inline-block; padding: 8px 15px; background: #3498db; color: white; text-decoration: none; border-radius: 4px; margin: 5px; }
        .btn:hover { background: #2980b9; }
        .btn-secondary { background: #95a5a6; }
        .btn-secondary:hover { background: #7f8c8d; }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>📝 AMC8 ${year} Problems</h1>
            <p>${problems.length} problems available</p>
        </div>
        
        ${problems.map(problem => `
            <div class="problem-card" style="cursor: pointer; transition: transform 0.2s ease;" onclick="location.href='/browse/problem/${year}/${problem.problem_num}'">
                <div class="problem-header">Problem ${problem.problem_num} ${problem.has_visual ? '🖼️' : ''}</div>
                <div class="problem-statement">${problem.statement}</div>
                <ul class="choices">
                    ${Array.isArray(problem.choices) ? 
                        problem.choices.map(choice => `<li>${choice}</li>`).join('') : 
                        (problem.choices && typeof problem.choices === 'object') ?
                        Object.entries(problem.choices).map(([letter, text]) => `<li><strong>(${letter})</strong> ${text}</li>`).join('') :
                        'No choices available'
                    }
                </ul>
                ${problem.answer ? `<div style="color: #27ae60; font-weight: bold;">Answer: ${problem.answer}</div>` : ''}
                ${problem.solution ? `<div style="background: #e8f5e8; padding: 10px; border-radius: 4px; margin-top: 10px;"><strong>Solution:</strong> ${problem.solution}</div>` : ''}
            </div>
        `).join('')}
        
        <div style="text-align: center; margin-top: 30px;">
            <a href="/practice" class="btn">Practice These Problems</a>
            <a href="/browse" class="btn btn-secondary">Back to Browser</a>
        </div>
    </div>
</body>
</html>
    `);
});

/**
 * Search Problems Route
 * Searches problems by keyword in problem statements
 */
router.get('/search', (req, res) => {
    const query = req.query.q || '';
    const results = query ? searchProblems(query) : [];
    
    res.send(`
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Search Results - AMC8 Hub</title>
    <script src="https://polyfill.io/v3/polyfill.min.js?features=es6"></script>
    <script id="MathJax-script" async src="https://cdn.jsdelivr.net/npm/mathjax@3/es5/tex-mml-chtml.js"></script>
    <style>
        body { font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif; line-height: 1.6; margin: 0; padding: 20px; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); min-height: 100vh; }
        .container { max-width: 900px; margin: 0 auto; background: white; padding: 30px; border-radius: 15px; box-shadow: 0 10px 25px rgba(0,0,0,0.1); }
        .search-bar { margin-bottom: 30px; }
        .form-control { width: 100%; padding: 12px; border: 2px solid #ddd; border-radius: 6px; font-size: 16px; }
        .problem-card { background: #f8f9fa; padding: 20px; margin: 15px 0; border-radius: 8px; border-left: 4px solid #3498db; }
        .problem-header { font-weight: bold; color: #2c3e50; margin-bottom: 10px; }
        .problem-statement { margin: 15px 0; line-height: 1.8; }
        .choices { list-style: none; padding: 0; margin: 15px 0; }
        .choices li { background: #e9ecef; padding: 8px; margin: 5px 0; border-radius: 4px; }
        .btn { display: inline-block; padding: 8px 15px; background: #3498db; color: white; text-decoration: none; border-radius: 4px; margin: 5px; }
        .btn:hover { background: #2980b9; }
        .btn-secondary { background: #95a5a6; }
        .btn-secondary:hover { background: #7f8c8d; }
        .no-results { text-align: center; color: #7f8c8d; padding: 50px; }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>🔍 Search Results</h1>
            ${query ? `<p>Found ${results.length} problems matching "${query}"</p>` : '<p>Enter a search term to find problems</p>'}
        </div>
        
        <div class="search-bar">
            <form action="/browse/search" method="get">
                <input type="text" name="q" class="form-control" placeholder="Search problems by keyword..." value="${query}">
                <button type="submit" class="btn" style="margin-top: 10px;">Search Problems</button>
            </form>
        </div>
        
        ${results.length > 0 ? results.map(problem => `
            <div class="problem-card">
                <div class="problem-header">${problem.year} AMC8 Problem ${problem.problem_num}</div>
                <div class="problem-statement">${problem.statement}</div>
                <ul class="choices">
                    ${Array.isArray(problem.choices) ? 
                        problem.choices.map(choice => `<li>${choice}</li>`).join('') : 
                        (problem.choices && typeof problem.choices === 'object') ?
                        Object.entries(problem.choices).map(([letter, text]) => `<li><strong>(${letter})</strong> ${text}</li>`).join('') :
                        'No choices available'
                    }
                </ul>
                ${problem.answer ? `<div style="color: #27ae60; font-weight: bold;">Answer: ${problem.answer}</div>` : ''}
                ${problem.solution ? `<div style="background: #e8f5e8; padding: 10px; border-radius: 4px; margin-top: 10px;"><strong>Solution:</strong> ${problem.solution}</div>` : ''}
            </div>
        `).join('') : (query ? '<div class="no-results"><h3>No problems found</h3><p>Try different keywords or browse by year instead.</p></div>' : '')}
        
        <div style="text-align: center; margin-top: 30px;">
            <a href="/browse" class="btn btn-secondary">Back to Browser</a>
        </div>
    </div>
</body>
</html>
    `);
});

/**
 * Browse Individual Problem
 * Shows a specific problem with visual components if available
 */
router.get('/problem/:year/:number', (req, res) => {
    const year = parseInt(req.params.year);
    const problemNum = parseInt(req.params.number);
    
    // Get question bank data to find problem
    const questionBank = getQuestionBank();
    const problem = questionBank.problems.find(p => p.year === year && p.problem_num === problemNum);
    
    if (!problem) {
        return res.status(404).send(`
<!DOCTYPE html>
<html>
<head>
    <title>Problem Not Found - AMC8 Hub</title>
    <style>
        body { font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif; line-height: 1.6; margin: 0; padding: 20px; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); min-height: 100vh; }
        .container { max-width: 600px; margin: 50px auto; background: white; padding: 40px; border-radius: 15px; box-shadow: 0 10px 25px rgba(0,0,0,0.1); text-align: center; }
        .btn { display: inline-block; padding: 12px 25px; background: #3498db; color: white; text-decoration: none; border-radius: 6px; margin: 10px; }
        .btn:hover { background: #2980b9; }
    </style>
</head>
<body>
    <div class="container">
        <h2>❌ Problem Not Found</h2>
        <p>Could not find ${year} Problem ${problemNum}</p>
        <a href="/browse" class="btn">← Back to Browse</a>
    </div>
</body>
</html>
        `);
    }
    
    res.send(`
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>${year} Problem ${problemNum} - AMC8 Hub</title>
    <script src="https://polyfill.io/v3/polyfill.min.js?features=es6"></script>
    <script id="MathJax-script" async src="https://cdn.jsdelivr.net/npm/mathjax@3/es5/tex-mml-chtml.js"></script>
    <script>
        window.MathJax = {
            tex: {
                inlineMath: [['$', '$'], ['\\\\(', '\\\\)']],
                displayMath: [['$$', '$$'], ['\\\\[', '\\\\]']]
            }
        };
    </script>
    <style>
        body { font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif; line-height: 1.6; margin: 0; padding: 20px; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); min-height: 100vh; }
        .container { max-width: 900px; margin: 0 auto; }
        .problem-container { background: white; border-radius: 15px; box-shadow: 0 10px 25px rgba(0,0,0,0.1); overflow: hidden; }
        .problem-header { background: linear-gradient(135deg, #007bff, #0056b3); color: white; padding: 30px; text-align: center; }
        .problem-header h1 { margin: 0; font-size: 2.2em; }
        .problem-content { padding: 40px; }
        .problem-statement { background: #f8f9fa; padding: 30px; border-radius: 10px; margin-bottom: 30px; font-size: 18px; line-height: 1.8; border-left: 4px solid #007bff; }
        
        /* Visual Components Styling */
        .visual-image { 
            min-width: 50%;
            max-width: 100%; 
            height: auto; 
            border: 2px solid #e9ecef; 
            border-radius: 8px; 
            margin: 25px 0; 
            display: block; 
            margin-left: auto; 
            margin-right: auto; 
            box-shadow: 0 4px 12px rgba(0,0,0,0.1);
        }
        
        .choices-container { background: #f8f9fa; padding: 30px; border-radius: 10px; margin-bottom: 30px; }
        .choice { display: flex; align-items: center; padding: 15px; margin: 12px 0; border: 2px solid #e9ecef; border-radius: 8px; transition: all 0.3s ease; cursor: pointer; font-size: 16px; }
        .choice:hover { border-color: #007bff; background: #f8f9ff; }
        .choice-letter { background: #007bff; color: white; width: 40px; height: 40px; border-radius: 50%; display: flex; align-items: center; justify-content: center; font-weight: bold; margin-right: 15px; flex-shrink: 0; }
        .choice-text { flex: 1; }
        .navigation-buttons { display: flex; justify-content: space-between; flex-wrap: wrap; gap: 15px; margin-top: 30px; }
        .btn { display: inline-block; padding: 12px 25px; background: #3498db; color: white; text-decoration: none; border-radius: 6px; transition: background 0.3s ease; }
        .btn:hover { background: #2980b9; }
        .btn-secondary { background: #95a5a6; }
        .btn-secondary:hover { background: #7f8c8d; }
        .btn-outline { background: transparent; border: 2px solid #3498db; color: #3498db; }
        .btn-outline:hover { background: #3498db; color: white; }
        
        @media (max-width: 768px) {
            .problem-content { padding: 20px; }
            .navigation-buttons { flex-direction: column; }
            .btn { text-align: center; }
        }
    </style>
</head>
<body>
    <div class="container">
        <div class="problem-container">
            <div class="problem-header">
                <h1>${year} Problem ${problemNum}</h1>
                <p>American Mathematics Competitions 8</p>
            </div>
            
            <div class="problem-content">
                <div class="problem-statement">
                    ${problem.statement}
                </div>
                
                ${problem.has_visual && problem.visual_components ? problem.visual_components
                    .filter(visual => visual.type === 'svg')  // Only show SVG visual components
                    .map(visual => `
                        <img src="/${visual.image_path}" alt="${visual.description}" class="visual-image" />
                `).join('') : ''}
                
                <div class="choices-container">
                    <h3>Answer Choices:</h3>
                    ${Array.isArray(problem.choices) ? 
                        problem.choices.map((choice, index) => {
                            const letter = String.fromCharCode(65 + index); // A, B, C, D, E
                            return `
                                <div class="choice" onclick="selectChoice('${letter}')">
                                    <div class="choice-letter">${letter}</div>
                                    <div class="choice-text">${choice}</div>
                                </div>
                            `;
                        }).join('') : 
                        (problem.choices && typeof problem.choices === 'object') ?
                        Object.entries(problem.choices).map(([letter, text]) => `
                            <div class="choice" onclick="selectChoice('${letter}')">
                                <div class="choice-letter">${letter}</div>
                                <div class="choice-text">${text}</div>
                            </div>
                        `).join('') :
                        '<p>No choices available</p>'
                    }
                </div>
                
                <div class="navigation-buttons">
                    <div>
                        <a href="/browse/year/${year}" class="btn btn-secondary">← Back to ${year}</a>
                        <a href="/browse" class="btn btn-secondary">📊 Browse All</a>
                    </div>
                    <div>
                        ${problemNum > 1 ? `<a href="/browse/problem/${year}/${problemNum - 1}" class="btn btn-outline">← Problem ${problemNum - 1}</a>` : ''}
                        ${problemNum < 25 ? `<a href="/browse/problem/${year}/${problemNum + 1}" class="btn btn-outline">Problem ${problemNum + 1} →</a>` : ''}
                    </div>
                </div>
            </div>
        </div>
    </div>
    
    <script>
        let selectedChoice = null;
        
        function selectChoice(letter) {
            // Remove previous selection
            document.querySelectorAll('.choice').forEach(c => c.classList.remove('selected'));
            
            // Mark current selection
            event.currentTarget.classList.add('selected');
            selectedChoice = letter;
        }
        
        // Add selected styling
        const style = document.createElement('style');
        style.textContent = \`
            .choice.selected {
                border-color: #28a745 !important;
                background: #d4edda !important;
            }
            .choice.selected .choice-letter {
                background: #28a745 !important;
            }
        \`;
        document.head.appendChild(style);
    </script>
</body>
</html>
    `);
});

module.exports = router;