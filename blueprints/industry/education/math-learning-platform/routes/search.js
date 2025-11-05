#!/usr/bin/env node
/**
 * AMC8 Search Routes - Educational content search using Brave API
 * Provides search capabilities for AMC8 problems, tutorials, and educational resources
 */

const express = require('express');
const { spawn } = require('child_process');
const path = require('path');
const router = express.Router();

/**
 * Call Python Brave Search API wrapper
 */
function callBraveSearch(method, ...args) {
    return new Promise((resolve, reject) => {
        const pythonScript = path.join(__dirname, '../../manager/brave_search_api.py');
        const python = spawn('python3', [pythonScript, method, ...args]);
        
        let stdout = '';
        let stderr = '';
        
        python.stdout.on('data', (data) => {
            stdout += data.toString();
        });
        
        python.stderr.on('data', (data) => {
            stderr += data.toString();
        });
        
        python.on('close', (code) => {
            if (code === 0) {
                try {
                    // Try to parse JSON response
                    const result = JSON.parse(stdout);
                    resolve(result);
                } catch (e) {
                    // If not JSON, return raw output
                    resolve({ output: stdout, success: true });
                }
            } else {
                reject(new Error(`Python script failed: ${stderr || stdout}`));
            }
        });
    });
}

/**
 * GET /search - Main search page
 */
router.get('/', (req, res) => {
    res.render('search', { 
        title: 'Educational Search',
        query: req.query.q || '',
        results: null,
        error: null
    });
});

/**
 * GET /search/api/usage - Get current API usage stats
 */
router.get('/api/usage', async (req, res) => {
    try {
        const pythonScript = path.join(__dirname, '../../manager/brave_search_api.py');
        const python = spawn('python3', ['-c', `
from brave_search_api import BraveSearchAPI
import json
try:
    api = BraveSearchAPI()
    stats = api.get_usage_stats()
    print(json.dumps(stats))
except Exception as e:
    print(json.dumps({"error": str(e)}))
        `]);
        
        let output = '';
        python.stdout.on('data', (data) => output += data.toString());
        
        python.on('close', (code) => {
            try {
                const stats = JSON.parse(output);
                res.json(stats);
            } catch (e) {
                res.status(500).json({ error: 'Failed to get usage stats' });
            }
        });
        
    } catch (error) {
        res.status(500).json({ error: error.message });
    }
});

/**
 * POST /search/educational - Search for educational content
 */
router.post('/educational', async (req, res) => {
    const { topic, level = 'middle school' } = req.body;
    
    if (!topic) {
        return res.status(400).json({ error: 'Topic is required' });
    }
    
    try {
        const pythonScript = path.join(__dirname, '../../manager/brave_search_api.py');
        const python = spawn('python3', ['-c', `
from brave_search_api import BraveSearchAPI
import json
import sys

try:
    api = BraveSearchAPI()
    results = api.search_educational_content("${topic.replace(/"/g, '\\"')}", "${level.replace(/"/g, '\\"')}")
    if results:
        print(json.dumps(results))
    else:
        print(json.dumps({"error": "No results or API limit exceeded"}))
except Exception as e:
    print(json.dumps({"error": str(e)}))
        `]);
        
        let output = '';
        let errorOutput = '';
        
        python.stdout.on('data', (data) => output += data.toString());
        python.stderr.on('data', (data) => errorOutput += data.toString());
        
        python.on('close', (code) => {
            try {
                const results = JSON.parse(output);
                if (results.error) {
                    return res.status(400).json(results);
                }
                
                // Format results for frontend
                const formattedResults = {
                    query: `${topic} ${level}`,
                    results: results.web?.results || [],
                    total: results.web?.results?.length || 0
                };
                
                res.json(formattedResults);
            } catch (e) {
                res.status(500).json({ 
                    error: 'Failed to parse search results',
                    debug: { output, errorOutput }
                });
            }
        });
        
    } catch (error) {
        res.status(500).json({ error: error.message });
    }
});

/**
 * POST /search/competition - Search for competition problems
 */
router.post('/competition', async (req, res) => {
    const { competition = 'AMC8', year } = req.body;
    
    try {
        const pythonScript = path.join(__dirname, '../../manager/brave_search_api.py');
        const yearParam = year ? `, ${year}` : '';
        
        const python = spawn('python3', ['-c', `
from brave_search_api import BraveSearchAPI
import json

try:
    api = BraveSearchAPI()
    results = api.search_competition_problems("${competition.replace(/"/g, '\\"')}"${yearParam})
    if results:
        print(json.dumps(results))
    else:
        print(json.dumps({"error": "No results or API limit exceeded"}))
except Exception as e:
    print(json.dumps({"error": str(e)}))
        `]);
        
        let output = '';
        python.stdout.on('data', (data) => output += data.toString());
        
        python.on('close', (code) => {
            try {
                const results = JSON.parse(output);
                if (results.error) {
                    return res.status(400).json(results);
                }
                
                // Format results for frontend
                const formattedResults = {
                    query: `${competition} ${year || ''}`,
                    results: results.web?.results || [],
                    total: results.web?.results?.length || 0
                };
                
                res.json(formattedResults);
            } catch (e) {
                res.status(500).json({ error: 'Failed to parse search results' });
            }
        });
        
    } catch (error) {
        res.status(500).json({ error: error.message });
    }
});

/**
 * GET /search/web - General web search
 */
router.post('/web', async (req, res) => {
    const { query, count = 10 } = req.body;
    
    if (!query) {
        return res.status(400).json({ error: 'Query is required' });
    }
    
    try {
        const pythonScript = path.join(__dirname, '../../manager/brave_search_api.py');
        
        const python = spawn('python3', ['-c', `
from brave_search_api import BraveSearchAPI
import json

try:
    api = BraveSearchAPI()
    results = api.search_web("${query.replace(/"/g, '\\"')}", ${parseInt(count)})
    if results:
        print(json.dumps(results))
    else:
        print(json.dumps({"error": "No results or API limit exceeded"}))
except Exception as e:
    print(json.dumps({"error": str(e)}))
        `]);
        
        let output = '';
        python.stdout.on('data', (data) => output += data.toString());
        
        python.on('close', (code) => {
            try {
                const results = JSON.parse(output);
                if (results.error) {
                    return res.status(400).json(results);
                }
                
                // Format results for frontend
                const formattedResults = {
                    query: query,
                    results: results.web?.results || [],
                    total: results.web?.results?.length || 0
                };
                
                res.json(formattedResults);
            } catch (e) {
                res.status(500).json({ error: 'Failed to parse search results' });
            }
        });
        
    } catch (error) {
        res.status(500).json({ error: error.message });
    }
});

module.exports = router;