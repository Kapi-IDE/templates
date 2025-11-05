#!/usr/bin/env python3
"""
Simple demo server to test the Healthcare AI Pod UI
Uses built-in Python libraries only
"""

import http.server
import socketserver
import json
import urllib.parse as urlparse
import os
import sys
from datetime import datetime

PORT = 8083

class HealthcareAIDemoHandler(http.server.SimpleHTTPRequestHandler):
    """Simple demo handler for Healthcare AI API endpoints"""
    
    def do_GET(self):
        """Handle GET requests"""
        path = self.path
        
        if path == '/api-docs' or path == '/docs':
            self.send_api_docs()
        elif path == '/api/health':
            self.send_json_response({
                'status': 'healthy',
                'timestamp': datetime.now().isoformat(),
                'version': '1.0.0-demo',
                'components': {
                    'database': 'demo',
                    'agents': 'demo',
                    'security': 'demo'
                }
            })
        else:
            # Return 404 for unknown endpoints
            self.send_response(404)
            self.send_header('Content-Type', 'text/html')
            self.end_headers()
            self.wfile.write(b'<h1>404 - Endpoint not found</h1><p>Available endpoints: /api/health, /api-docs, /docs</p>')
    
    def do_POST(self):
        """Handle POST requests"""
        path = self.path
        content_length = int(self.headers['Content-Length'])
        post_data = self.rfile.read(content_length)
        
        try:
            data = json.loads(post_data.decode('utf-8'))
        except:
            data = {}
        
        if path == '/api/patient/start-session':
            patient_id = data.get('patient_id', f'demo_patient_{int(datetime.now().timestamp())}')
            self.send_json_response({
                'session_id': f'session_{int(datetime.now().timestamp())}',
                'patient_id': patient_id,
                'message': 'Demo session started successfully'
            })
            
        elif path == '/api/chat/message':
            message = data.get('message', '')
            
            # Simple demo response based on message content
            if any(word in message.lower() for word in ['chest', 'pain', 'heart']):
                urgency_score = 7
                urgency_level = 'high'
                reasoning = 'Chest pain symptoms require urgent medical attention'
                action = 'Seek immediate medical care'
                escalation_required = True
            elif any(word in message.lower() for word in ['headache', 'fever', 'nausea']):
                urgency_score = 4
                urgency_level = 'moderate'
                reasoning = 'Common symptoms that should be monitored'
                action = 'Contact healthcare provider within 24 hours'
                escalation_required = False
            else:
                urgency_score = 2
                urgency_level = 'low'
                reasoning = 'Symptoms appear manageable with self-care'
                action = 'Monitor symptoms and consider self-care measures'
                escalation_required = False
            
            demo_response = {
                'agent_response': f'Thank you for describing your symptoms: "{message}". Based on what you\'ve told me, I\'m assessing your situation. This is a demo response showing how the AI would analyze your symptoms.',
                'urgency_assessment': {
                    'score': urgency_score,
                    'level': urgency_level,
                    'reasoning': reasoning,
                    'recommended_action': action
                },
                'medical_knowledge': {
                    'relevant_conditions': [
                        {'name': 'Demo Condition', 'description': 'This is a demo medical condition for testing'}
                    ],
                    'treatment_guidelines': [
                        {'condition': 'Demo', 'immediate_actions': ['Demo action 1', 'Demo action 2']}
                    ],
                    'warning_signs': ['Demo warning sign']
                },
                'escalation': {
                    'required': escalation_required,
                    'level': urgency_level,
                    'instructions': [
                        'This is a demo instruction',
                        'Contact your healthcare provider',
                        'Monitor your symptoms closely'
                    ]
                },
                'next_questions': [
                    'How long have you been experiencing these symptoms?',
                    'On a scale of 1-10, how would you rate your discomfort?',
                    'Do you have any medical conditions or take medications?'
                ],
                'conversation_id': f'demo_conv_{int(datetime.now().timestamp())}',
                'timestamp': datetime.now().isoformat()
            }
            
            self.send_json_response(demo_response)
        else:
            self.send_json_response({'error': 'Demo endpoint not implemented'}, 404)
    
    def send_json_response(self, data, status_code=200):
        """Send JSON response"""
        self.send_response(status_code)
        self.send_header('Content-Type', 'application/json')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        self.end_headers()
        
        response = json.dumps(data).encode('utf-8')
        self.wfile.write(response)
    
    def do_OPTIONS(self):
        """Handle CORS preflight requests"""
        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        self.end_headers()
    
    def send_api_docs(self):
        """Send API documentation HTML"""
        docs_html = '''
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Healthcare AI Pod - API Documentation</title>
    <style>
        body { font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif; margin: 0; padding: 20px; background: #f8fafc; }
        .container { max-width: 1200px; margin: 0 auto; }
        .header { background: linear-gradient(135deg, #3b82f6, #1e40af); color: white; padding: 2rem; border-radius: 12px; margin-bottom: 2rem; }
        .header h1 { margin: 0; font-size: 2.5rem; display: flex; align-items: center; }
        .header p { margin: 0.5rem 0 0 0; opacity: 0.9; font-size: 1.1rem; }
        .endpoint { background: white; border-radius: 8px; padding: 1.5rem; margin-bottom: 1.5rem; box-shadow: 0 1px 3px rgba(0,0,0,0.1); }
        .method { display: inline-block; padding: 0.25rem 0.75rem; border-radius: 4px; font-weight: bold; font-size: 0.875rem; }
        .method.get { background: #10b981; color: white; }
        .method.post { background: #3b82f6; color: white; }
        .endpoint-path { font-family: 'SF Mono', Monaco, monospace; font-size: 1.25rem; font-weight: 600; color: #374151; margin-left: 1rem; }
        .description { color: #6b7280; margin: 0.75rem 0; }
        .params, .response { margin-top: 1rem; }
        .params h4, .response h4 { margin: 0 0 0.5rem 0; color: #374151; font-size: 0.875rem; font-weight: 600; text-transform: uppercase; }
        .code { background: #f3f4f6; padding: 0.75rem; border-radius: 6px; font-family: 'SF Mono', Monaco, monospace; font-size: 0.875rem; overflow-x: auto; border-left: 4px solid #3b82f6; }
        .status-badge { display: inline-block; padding: 0.25rem 0.5rem; background: #10b981; color: white; border-radius: 12px; font-size: 0.75rem; font-weight: 600; }
        .warning { background: #fef3cd; border: 1px solid #fde68a; border-radius: 6px; padding: 1rem; margin: 1rem 0; }
        .warning-icon { color: #d97706; }
        .example-section { background: #f8fafc; border-radius: 6px; padding: 1rem; margin-top: 1rem; }
        .curl-command { background: #1f2937; color: #f9fafb; padding: 1rem; border-radius: 6px; font-family: 'SF Mono', Monaco, monospace; font-size: 0.875rem; overflow-x: auto; margin-top: 0.5rem; }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>🏥 Healthcare AI Pod API</h1>
            <p>RESTful API for AI-powered patient triage and medical consultation</p>
            <div style="margin-top: 1rem; font-size: 0.875rem;">
                <span class="status-badge">v1.0.0-demo</span>
                <span style="margin-left: 1rem;">Base URL: http://localhost:8083</span>
            </div>
        </div>

        <div class="warning">
            <span class="warning-icon">⚠️</span> <strong>Demo Mode:</strong> This server provides mock responses for testing. 
            For full functionality, configure the real backend with Google Gemini API keys and database connections.
        </div>

        <div class="endpoint">
            <h3>
                <span class="method get">GET</span>
                <span class="endpoint-path">/api/health</span>
            </h3>
            <p class="description">Check the health status of the Healthcare AI system and its components.</p>
            
            <div class="response">
                <h4>Response (200 OK)</h4>
                <div class="code">{
  "status": "healthy",
  "timestamp": "2025-09-14T10:47:35.573499",
  "version": "1.0.0-demo",
  "components": {
    "database": "demo",
    "agents": "demo",
    "security": "demo"
  }
}</div>
            </div>

            <div class="example-section">
                <h4>Try it out:</h4>
                <div class="curl-command">curl http://localhost:8083/api/health</div>
            </div>
        </div>

        <div class="endpoint">
            <h3>
                <span class="method post">POST</span>
                <span class="endpoint-path">/api/patient/start-session</span>
            </h3>
            <p class="description">Initialize a new patient session for medical consultation.</p>
            
            <div class="params">
                <h4>Request Body</h4>
                <div class="code">{
  "patient_id": "string (optional)"
}</div>
            </div>

            <div class="response">
                <h4>Response (200 OK)</h4>
                <div class="code">{
  "session_id": "session_1726311426",
  "patient_id": "demo_patient_1726311426", 
  "message": "Demo session started successfully"
}</div>
            </div>

            <div class="example-section">
                <h4>Try it out:</h4>
                <div class="curl-command">curl -X POST http://localhost:8083/api/patient/start-session \\
  -H "Content-Type: application/json" \\
  -d '{"patient_id": "patient_123"}'</div>
            </div>
        </div>

        <div class="endpoint">
            <h3>
                <span class="method post">POST</span>
                <span class="endpoint-path">/api/chat/message</span>
            </h3>
            <p class="description">Send patient symptoms to AI agents for intelligent triage and medical assessment.</p>
            
            <div class="params">
                <h4>Request Body</h4>
                <div class="code">{
  "message": "string (required) - Patient's symptom description",
  "context": "object (optional) - Additional context"
}</div>
            </div>

            <div class="response">
                <h4>Response (200 OK)</h4>
                <div class="code">{
  "agent_response": "string - AI assessment response",
  "urgency_assessment": {
    "score": "number (0-10) - Urgency level",
    "level": "string - high/moderate/low",
    "reasoning": "string - Assessment reasoning",
    "recommended_action": "string - What patient should do"
  },
  "medical_knowledge": {
    "relevant_conditions": [
      {"name": "string", "description": "string"}
    ],
    "treatment_guidelines": [
      {"condition": "string", "immediate_actions": ["string"]}
    ],
    "warning_signs": ["string"]
  },
  "escalation": {
    "required": "boolean - If immediate care needed",
    "level": "string - Escalation level",
    "instructions": ["string"]
  },
  "next_questions": ["string"],
  "conversation_id": "string",
  "timestamp": "string (ISO 8601)"
}</div>
            </div>

            <div class="example-section">
                <h4>Example Requests:</h4>
                
                <div style="margin: 1rem 0;">
                    <strong>High Urgency (Chest Pain):</strong>
                    <div class="curl-command">curl -X POST http://localhost:8083/api/chat/message \\
  -H "Content-Type: application/json" \\
  -d '{"message": "I have severe chest pain and difficulty breathing"}'</div>
                </div>

                <div style="margin: 1rem 0;">
                    <strong>Moderate Urgency (Headache/Fever):</strong>
                    <div class="curl-command">curl -X POST http://localhost:8083/api/chat/message \\
  -H "Content-Type: application/json" \\
  -d '{"message": "I have a persistent headache and low grade fever for 2 days"}'</div>
                </div>

                <div style="margin: 1rem 0;">
                    <strong>Low Urgency (General symptoms):</strong>
                    <div class="curl-command">curl -X POST http://localhost:8083/api/chat/message \\
  -H "Content-Type: application/json" \\
  -d '{"message": "I feel tired and have a slight cough"}'</div>
                </div>
            </div>
        </div>

        <div style="background: white; border-radius: 8px; padding: 1.5rem; margin-top: 2rem; box-shadow: 0 1px 3px rgba(0,0,0,0.1);">
            <h3 style="margin-top: 0; color: #374151;">🚀 Getting Started</h3>
            <ol style="color: #6b7280; line-height: 1.6;">
                <li><strong>Frontend:</strong> Access the UI at <a href="http://localhost:3000" style="color: #3b82f6;">http://localhost:3000</a></li>
                <li><strong>Backend:</strong> API endpoints available at <a href="http://localhost:8083" style="color: #3b82f6;">http://localhost:8083</a></li>
                <li><strong>Health Check:</strong> Verify system status at <a href="/api/health" style="color: #3b82f6;">/api/health</a></li>
                <li><strong>Test Chat:</strong> Send symptoms to <code>/api/chat/message</code> to see AI triage in action</li>
            </ol>
            
            <div style="background: #f3f4f6; padding: 1rem; border-radius: 6px; margin-top: 1rem;">
                <h4 style="margin: 0 0 0.5rem 0; color: #374151;">🏗️ Architecture Overview</h4>
                <ul style="margin: 0.5rem 0; color: #6b7280; line-height: 1.6;">
                    <li><strong>Multi-Agent System:</strong> Intake → Triage → Knowledge → Escalation</li>
                    <li><strong>AI Engine:</strong> Google Gemini API for medical reasoning</li>
                    <li><strong>Vector Database:</strong> ChromaDB for medical knowledge retrieval</li>
                    <li><strong>Patient Data:</strong> SQLite with HIPAA-compliant encryption</li>
                    <li><strong>Frontend:</strong> React.js with real-time chat interface</li>
                </ul>
            </div>
        </div>

        <div style="text-align: center; margin-top: 2rem; color: #6b7280; font-size: 0.875rem;">
            <p>Healthcare AI Pod - Modern AI Pro Practitioner Course</p>
            <p>Built with React + Flask + ChromaDB + Gemini AI</p>
        </div>
    </div>
</body>
</html>
        '''
        
        self.send_response(200)
        self.send_header('Content-Type', 'text/html')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.end_headers()
        
        self.wfile.write(docs_html.encode('utf-8'))

def main():
    """Start the demo server"""
    # Don't change directory - serve from current location
    
    print(f"🏥 Healthcare AI Pod - Demo Server")
    print(f"=" * 50)
    print(f"Starting demo server on port {PORT}...")
    print(f"API endpoints available:")
    print(f"- GET  /api/health")
    print(f"- POST /api/patient/start-session")
    print(f"- POST /api/chat/message")
    print(f"")
    print(f"Demo server running at: http://localhost:{PORT}")
    print(f"Frontend will be available at: http://localhost:3000 (run 'cd frontend && npm start')")
    print(f"")
    print(f"Note: This is a demo server with mock responses.")
    print(f"For full functionality, install dependencies and run the real backend.")
    print(f"Press Ctrl+C to stop the server")
    
    try:
        with socketserver.TCPServer(("", PORT), HealthcareAIDemoHandler) as httpd:
            httpd.serve_forever()
    except KeyboardInterrupt:
        print(f"\n👋 Demo server stopped")
        return 0

if __name__ == "__main__":
    sys.exit(main())