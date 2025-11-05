/**
 * AMC8 Learning Platform - CSS Styles
 * Centralized styling for consistent design across the application
 */

/**
 * Base CSS styles used across all pages
 * Consolidated to reduce duplication and ensure consistent styling
 */
const BASE_CSS = `
* {
    margin: 0;
    padding: 0;
    box-sizing: border-box;
}

body {
    font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
    line-height: 1.6;
    color: #333;
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    min-height: 100vh;
}

.container {
    max-width: 1200px;
    margin: 0 auto;
    padding: 20px;
}

.card {
    background: rgba(255, 255, 255, 0.95);
    border-radius: 15px;
    padding: 20px;
    box-shadow: 0 8px 32px rgba(0, 0, 0, 0.1);
    backdrop-filter: blur(10px);
    transition: transform 0.3s ease;
}

.card:hover {
    transform: translateY(-5px);
}

.header {
    text-align: center;
    margin-bottom: 30px;
}

.header h1 {
    color: #2c3e50;
    font-size: 2.5em;
    margin-bottom: 10px;
}

.header .subtitle {
    color: #7f8c8d;
    font-size: 1.2em;
}
`;

/**
 * Button styles for consistent button appearance across the app
 */
const BUTTON_CSS = `
.btn {
    display: inline-block;
    padding: 12px 25px;
    border: none;
    border-radius: 8px;
    cursor: pointer;
    font-weight: bold;
    text-decoration: none;
    font-size: 16px;
    transition: all 0.3s ease;
    text-align: center;
}

.btn:hover {
    transform: translateY(-2px);
}

.btn-primary { background: #3498db; color: white; }
.btn-primary:hover { background: #2980b9; }
.btn-success { background: #2ecc71; color: white; }
.btn-success:hover { background: #27ae60; }
.btn-warning { background: #f39c12; color: white; }
.btn-warning:hover { background: #e67e22; }
.btn-secondary { background: #95a5a6; color: white; }
.btn-secondary:hover { background: #7f8c8d; }
.btn-large {
    padding: 15px 30px;
    font-size: 1.1em;
    border-radius: 25px;
}
`;

/**
 * Form styles for consistent form appearance
 */
const FORM_CSS = `
.form-group {
    margin-bottom: 20px;
}

.form-group label {
    display: block;
    margin-bottom: 5px;
    font-weight: 500;
    color: #2c3e50;
}

.form-control {
    width: 100%;
    padding: 12px;
    border: 2px solid #ddd;
    border-radius: 6px;
    font-size: 16px;
    transition: border-color 0.3s ease;
}

.form-control:focus {
    outline: none;
    border-color: #3498db;
}
`;

/**
 * Kid-friendly module/learning specific styles
 */
const MODULE_CSS = `
.modules-grid {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
    gap: 25px;
    margin: 30px 0;
}

.module-card {
    background: linear-gradient(135deg, #f8f9fa 0%, #e9ecef 100%);
    border-radius: 20px;
    padding: 30px;
    text-align: center;
    transition: all 0.3s ease;
    border: 3px solid transparent;
    cursor: pointer;
}

.module-card:hover {
    transform: translateY(-10px);
    border-color: #3498db;
    box-shadow: 0 15px 30px rgba(52, 152, 219, 0.3);
}

.difficulty-badge {
    display: inline-block;
    padding: 5px 15px;
    border-radius: 15px;
    font-size: 0.9em;
    font-weight: bold;
    margin-bottom: 15px;
}

.difficulty-beginner { background: #d4edda; color: #155724; }
.difficulty-intermediate { background: #fff3cd; color: #856404; }
.difficulty-advanced { background: #f8d7da; color: #721c24; }

.lesson-count {
    background: #e3f2fd;
    color: #1565c0;
    padding: 8px 16px;
    border-radius: 20px;
    font-weight: bold;
    margin-bottom: 20px;
    display: inline-block;
}
`;

/**
 * Responsive design for mobile devices
 */
const RESPONSIVE_CSS = `
@media (max-width: 768px) {
    .container {
        padding: 15px;
    }
    
    .header h1 {
        font-size: 2em;
    }
    
    .modules-grid {
        grid-template-columns: 1fr;
    }
    
    .btn {
        width: 100%;
        margin-bottom: 10px;
    }
}
`;

/**
 * Dashboard-specific styles
 */
const DASHBOARD_CSS = `
* {
    margin: 0;
    padding: 0;
    box-sizing: border-box;
}

body {
    font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
    line-height: 1.6;
    color: #333;
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    min-height: 100vh;
}

.container {
    max-width: 1200px;
    margin: 0 auto;
    padding: 20px;
}

.header {
    background: rgba(255, 255, 255, 0.95);
    padding: 20px;
    border-radius: 15px;
    margin-bottom: 20px;
    box-shadow: 0 8px 32px rgba(0, 0, 0, 0.1);
    backdrop-filter: blur(10px);
}

.header h1 {
    color: #2c3e50;
    text-align: center;
    font-size: 2.5em;
    margin-bottom: 10px;
}

.header .subtitle {
    text-align: center;
    color: #7f8c8d;
    font-size: 1.2em;
}

.dashboard-grid {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
    gap: 20px;
    margin-bottom: 20px;
}

.card {
    background: rgba(255, 255, 255, 0.95);
    padding: 20px;
    border-radius: 15px;
    box-shadow: 0 8px 32px rgba(0, 0, 0, 0.1);
    backdrop-filter: blur(10px);
    transition: transform 0.3s ease;
}

.card:hover {
    transform: translateY(-5px);
}

.card h3 {
    color: #2c3e50;
    margin-bottom: 15px;
    font-size: 1.3em;
    border-bottom: 2px solid #3498db;
    padding-bottom: 5px;
}

.countdown {
    text-align: center;
    font-size: 1.1em;
}

.countdown .days {
    font-size: 3em;
    font-weight: bold;
    color: #e74c3c;
    display: block;
}

.progress-bar {
    background: #ecf0f1;
    border-radius: 10px;
    height: 20px;
    margin: 10px 0;
    overflow: hidden;
}

.progress-fill {
    height: 100%;
    background: linear-gradient(90deg, #2ecc71, #27ae60);
    border-radius: 10px;
    transition: width 0.3s ease;
}

.score-display {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin: 10px 0;
}

.score-circle {
    width: 80px;
    height: 80px;
    border-radius: 50%;
    display: flex;
    align-items: center;
    justify-content: center;
    font-weight: bold;
    font-size: 1.4em;
    color: white;
}

.score-dhr { background: linear-gradient(45deg, #f39c12, #e67e22); }
.score-hr { background: linear-gradient(45deg, #3498db, #2980b9); }
.score-ar { background: linear-gradient(45deg, #2ecc71, #27ae60); }
.score-current { background: linear-gradient(45deg, #9b59b6, #8e44ad); }

.competition-table {
    width: 100%;
    border-collapse: collapse;
    margin-top: 10px;
}

.competition-table th,
.competition-table td {
    padding: 12px;
    text-align: left;
    border-bottom: 1px solid #ddd;
}

.competition-table th {
    background: #f8f9fa;
    font-weight: bold;
    color: #2c3e50;
}

.status-badge {
    padding: 4px 8px;
    border-radius: 12px;
    font-size: 0.8em;
    font-weight: bold;
}

.status-upcoming { background: #fff3cd; color: #856404; }
.status-registered { background: #d4edda; color: #155724; }
.status-completed { background: #d1ecf1; color: #0c5460; }

.topic-grid {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(150px, 1fr));
    gap: 10px;
    margin-top: 10px;
}

.topic-item {
    background: #f8f9fa;
    padding: 10px;
    border-radius: 8px;
    text-align: center;
    border-left: 4px solid #3498db;
}

.topic-mastered { border-left-color: #2ecc71; background: #d4edda; }
.topic-learning { border-left-color: #f39c12; background: #fff3cd; }
.topic-needs-work { border-left-color: #e74c3c; background: #f8d7da; }

.quick-actions {
    display: flex;
    gap: 10px;
    margin-top: 15px;
    flex-wrap: wrap;
}

.btn {
    padding: 10px 20px;
    border: none;
    border-radius: 8px;
    cursor: pointer;
    font-weight: bold;
    text-decoration: none;
    display: inline-block;
    transition: transform 0.2s ease;
}

.btn:hover {
    transform: translateY(-2px);
}

.btn-primary { background: #3498db; color: white; }
.btn-success { background: #2ecc71; color: white; }
.btn-warning { background: #f39c12; color: white; }
.btn-info { background: #17a2b8; color: white; }
.btn-secondary { background: #95a5a6; color: white; }
.btn-secondary:hover { background: #7f8c8d; }

.stats-row {
    display: flex;
    justify-content: space-around;
    text-align: center;
    margin: 15px 0;
}

.stat-item {
    flex: 1;
}

.stat-number {
    font-size: 2em;
    font-weight: bold;
    color: #2c3e50;
}

.stat-label {
    color: #7f8c8d;
    font-size: 0.9em;
}

@media (max-width: 768px) {
    .dashboard-grid {
        grid-template-columns: 1fr;
    }
    
    .header h1 {
        font-size: 2em;
    }
    
    .quick-actions {
        flex-direction: column;
    }
    
    .btn {
        text-align: center;
    }
}
`;

/**
 * Generates the complete CSS for a page by combining base styles with additional styles
 * @param {string} additionalCSS - Any page-specific CSS to append
 * @returns {string} Complete CSS string
 */
function generatePageCSS(additionalCSS = '') {
    return `${BASE_CSS}\n${BUTTON_CSS}\n${FORM_CSS}\n${MODULE_CSS}\n${RESPONSIVE_CSS}\n${additionalCSS}`;
}

/**
 * Generates HTML head section with CSS
 * @param {string} title - Page title
 * @param {string} css - CSS content to include
 * @returns {string} HTML head section
 */
function generateHTMLHead(title, css = '') {
    return `
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>${title}</title>
    <script src="https://polyfill.io/v3/polyfill.min.js?features=es6"></script>
    <script id="MathJax-script" async src="https://cdn.jsdelivr.net/npm/mathjax@3/es5/tex-mml-chtml.js"></script>
    <style>
        ${css}
    </style>
</head>`;
}

module.exports = {
    BASE_CSS,
    BUTTON_CSS,
    FORM_CSS,
    MODULE_CSS,
    RESPONSIVE_CSS,
    DASHBOARD_CSS,
    generatePageCSS,
    generateHTMLHead
};