/**
 * AMC8 Learning Platform - Question Bank Service  
 * Handles all question data access and filtering operations
 */

const fs = require('fs').promises;
const path = require('path');
const { shuffleArray } = require('../utils/helpers');

// Question bank data loaded from JSON file
let questionBank = { problems: [], total_count: 0, years_available: [] };
const QUESTION_BANK_FILE = path.join(__dirname, '..', '..', 'manager', 'amc8_question_bank.json');

/**
 * Loads the question bank from the JSON file
 * This should be called once when the server starts
 */
async function loadQuestionBank() {
    try {
        const data = await fs.readFile(QUESTION_BANK_FILE, 'utf-8');
        questionBank = JSON.parse(data);
        console.log(`📚 Loaded ${questionBank.total_count} problems from question bank`);
    } catch (error) {
        console.error('❌ Error loading question bank:', error.message);
        // Initialize with empty data if file doesn't exist
        questionBank = { problems: [], total_count: 0, years_available: [] };
    }
}

/**
 * Gets a random selection of problems from the question bank
 * @param {number} count - Number of problems to return (default: 5)
 * @returns {Array} Array of random problem objects
 */
function getRandomProblems(count = 5) {
    const shuffled = shuffleArray(questionBank.problems);
    return shuffled.slice(0, Math.min(count, shuffled.length));
}

/**
 * Retrieves all problems from a specific year
 * Useful for focused practice on particular AMC8 competitions
 * @param {number} year - The year to filter problems by
 * @returns {Array} Array of problem objects from the specified year
 */
function getProblemsByYear(year) {
    return questionBank.problems.filter(p => p.year == year);
}

/**
 * Gets problems from recent years for current practice
 * Helps students focus on more recent problem styles and trends
 * @param {number} yearsBack - Number of recent years to include (default: 5)
 * @returns {Array} Array of problem objects from recent years
 */
function getRecentProblems(yearsBack = 5) {
    const maxYear = Math.max(...questionBank.years_available);
    const minYear = maxYear - yearsBack + 1;
    return questionBank.problems.filter(p => p.year >= minYear && p.year <= maxYear);
}

/**
 * Searches problems by keyword in the problem statement
 * Great for finding problems on specific topics like "geometry" or "fractions"
 * @param {string} keyword - The keyword to search for
 * @returns {Array} Array of problem objects containing the keyword
 */
function searchProblems(keyword) {
    return questionBank.problems.filter(p => 
        p.statement.toLowerCase().includes(keyword.toLowerCase())
    );
}

/**
 * Filters problems by topic using keyword matching
 * @param {string} topic - Topic name (geometry, algebra, arithmetic, etc.)
 * @returns {Array} Array of problems matching the topic
 */
function getProblemsByTopic(topic) {
    const topicKeywords = {
        'geometry': ['area', 'perimeter', 'triangle', 'circle', 'rectangle', 'square', 'polygon', 'angle', 'diameter', 'radius'],
        'algebra': ['equation', 'variable', 'solve', 'expression', 'polynomial', 'factor'],
        'arithmetic': ['addition', 'subtraction', 'multiplication', 'division', 'fraction', 'decimal', 'percentage'],
        'number-theory': ['prime', 'factor', 'divisible', 'remainder', 'gcd', 'lcm', 'integer'],
        'combinatorics': ['combination', 'permutation', 'ways', 'arrange', 'choose', 'probability'],
        'word-problems': ['age', 'distance', 'speed', 'time', 'work', 'rate']
    };
    
    const keywords = topicKeywords[topic.toLowerCase()] || [];
    if (keywords.length === 0) return [];
    
    return questionBank.problems.filter(problem => {
        const statement = problem.statement.toLowerCase();
        return keywords.some(keyword => statement.includes(keyword));
    });
}

/**
 * Gets a specific problem by year and problem number
 * @param {number} year - Problem year
 * @param {number} problemNum - Problem number
 * @returns {Object|null} Problem object or null if not found
 */
function getProblem(year, problemNum) {
    return questionBank.problems.find(p => p.year == year && p.problem_num == problemNum) || null;
}

/**
 * Generates comprehensive statistics about the question bank
 * Provides insights into problem distribution and availability
 * @returns {Object} Statistics object with counts, years, and averages
 */
function getStatistics() {
    const problemsByYear = {};
    questionBank.problems.forEach(p => {
        if (!problemsByYear[p.year]) problemsByYear[p.year] = 0;
        problemsByYear[p.year]++;
    });
    
    const years = Object.keys(problemsByYear).map(Number).sort();
    
    return {
        total: questionBank.total_count,
        years: years,
        yearsCount: years.length,
        byYear: problemsByYear,
        avgPerYear: years.length > 0 ? questionBank.total_count / years.length : 0,
        mostRecentYear: years.length > 0 ? Math.max(...years) : null,
        oldestYear: years.length > 0 ? Math.min(...years) : null
    };
}

/**
 * Gets all available years
 * @returns {Array} Array of available years sorted in ascending order
 */
function getAvailableYears() {
    return [...questionBank.years_available].sort();
}

/**
 * Gets the question bank object (read-only access)
 * @returns {Object} Question bank object
 */
function getQuestionBank() {
    return { ...questionBank };
}

module.exports = {
    loadQuestionBank,
    getRandomProblems,
    getProblemsByYear,
    getRecentProblems,
    searchProblems,
    getProblemsByTopic,
    getProblem,
    getStatistics,
    getAvailableYears,
    getQuestionBank
};