/**
 * AMC8 Learning Platform - Utility Functions
 * Common helper functions used across the application
 */

/**
 * Shuffles an array using Fisher-Yates algorithm
 * @param {Array} array - Array to shuffle
 * @returns {Array} New shuffled array (original array is not modified)
 */
function shuffleArray(array) {
    const shuffled = [...array];
    for (let i = shuffled.length - 1; i > 0; i--) {
        const j = Math.floor(Math.random() * (i + 1));
        [shuffled[i], shuffled[j]] = [shuffled[j], shuffled[i]];
    }
    return shuffled;
}

/**
 * Generates a breadcrumb navigation component
 * @param {Array} breadcrumbs - Array of breadcrumb objects with {text, url} properties
 * @returns {string} HTML string for breadcrumb navigation
 */
function generateBreadcrumb(breadcrumbs) {
    return `
    <div class="breadcrumb" style="color: #7f8c8d; font-size: 0.9em; margin-bottom: 10px;">
        ${breadcrumbs.map((crumb, index) => {
            const separator = index > 0 ? ' > ' : '';
            return crumb.url ? 
                `${separator}<a href="${crumb.url}" style="color: #3498db; text-decoration: none;">${crumb.text}</a>` :
                `${separator}${crumb.text}`;
        }).join('')}
    </div>`;
}

/**
 * Formats a date to a readable string
 * @param {Date} date - Date to format
 * @returns {string} Formatted date string
 */
function formatDate(date) {
    return date.toLocaleDateString('en-US', {
        year: 'numeric',
        month: 'long',
        day: 'numeric'
    });
}

/**
 * Capitalizes the first letter of a string
 * @param {string} str - String to capitalize
 * @returns {string} Capitalized string
 */
function capitalize(str) {
    return str.charAt(0).toUpperCase() + str.slice(1);
}

/**
 * Calculates percentage and returns formatted string
 * @param {number} value - Numerator value
 * @param {number} total - Denominator value
 * @returns {string} Formatted percentage string
 */
function calculatePercentage(value, total) {
    if (total === 0) return '0%';
    return Math.round((value / total) * 100) + '%';
}

/**
 * Escapes HTML characters to prevent XSS
 * @param {string} text - Text to escape
 * @returns {string} HTML-escaped text
 */
function escapeHtml(text) {
    const map = {
        '&': '&amp;',
        '<': '&lt;',
        '>': '&gt;',
        '"': '&quot;',
        "'": '&#39;'
    };
    return text.replace(/[&<>"']/g, function(m) { return map[m]; });
}

/**
 * Generates a random ID string
 * @param {number} length - Length of the ID (default: 8)
 * @returns {string} Random ID string
 */
function generateRandomId(length = 8) {
    const chars = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789';
    let result = '';
    for (let i = 0; i < length; i++) {
        result += chars.charAt(Math.floor(Math.random() * chars.length));
    }
    return result;
}

/**
 * Truncates text to specified length with ellipsis
 * @param {string} text - Text to truncate
 * @param {number} maxLength - Maximum length
 * @returns {string} Truncated text
 */
function truncateText(text, maxLength) {
    if (text.length <= maxLength) return text;
    return text.substring(0, maxLength - 3) + '...';
}

module.exports = {
    shuffleArray,
    generateBreadcrumb,
    formatDate,
    capitalize,
    calculatePercentage,
    escapeHtml,
    generateRandomId,
    truncateText
};