#!/usr/bin/env python3
"""
Healthcare AI Pod - Main Flask Application
Provides REST API for patient triage and AI agent orchestration
"""

from flask import Flask, request, jsonify, session
from flask_cors import CORS
from dotenv import load_dotenv
import os
import logging
from datetime import datetime
import json

# Import our custom modules
from agents.intake_agent import IntakeAgent
from agents.triage_agent import TriageAgent
from agents.knowledge_agent import KnowledgeAgent
from agents.escalation_agent import EscalationAgent
from database.chromadb_manager import MedicalKnowledgeStore
from database.sqlite_manager import PatientDataManager
from utils.security import HIPAASecurityManager
from utils.monitoring import HealthcareAIMonitoring

# Load environment variables
load_dotenv()

# Initialize Flask app
app = Flask(__name__)
app.secret_key = os.getenv('SECRET_KEY', 'dev-secret-key-change-in-production')
CORS(app, supports_credentials=True)

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('logs/app.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

# Initialize system components
try:
    # Database managers
    knowledge_store = MedicalKnowledgeStore()
    patient_db = PatientDataManager()
    
    # Security and monitoring
    security_manager = HIPAASecurityManager()
    monitoring = HealthcareAIMonitoring()
    
    # AI Agents
    intake_agent = IntakeAgent(knowledge_store, patient_db)
    triage_agent = TriageAgent(knowledge_store, patient_db)
    knowledge_agent = KnowledgeAgent(knowledge_store, patient_db)
    escalation_agent = EscalationAgent(knowledge_store, patient_db)
    
    logger.info("All system components initialized successfully")
    
except Exception as e:
    logger.error(f"Failed to initialize system components: {str(e)}")
    raise

# API Routes

@app.route('/api/health', methods=['GET'])
def health_check():
    """Health check endpoint for monitoring"""
    try:
        # Check database connections
        knowledge_store.health_check()
        patient_db.health_check()
        
        return jsonify({
            'status': 'healthy',
            'timestamp': datetime.now().isoformat(),
            'version': '1.0.0',
            'components': {
                'database': 'ok',
                'agents': 'ok',
                'security': 'ok'
            }
        }), 200
    except Exception as e:
        logger.error(f"Health check failed: {str(e)}")
        return jsonify({
            'status': 'unhealthy',
            'error': str(e)
        }), 500

@app.route('/api/patient/start-session', methods=['POST'])
def start_patient_session():
    """Initialize a new patient session"""
    try:
        data = request.get_json()
        patient_id = data.get('patient_id')
        
        if not patient_id:
            return jsonify({'error': 'Patient ID required'}), 400
        
        # Create secure session
        session_data = security_manager.create_secure_session(patient_id)
        session['patient_id'] = patient_id
        session['session_token'] = session_data['token']
        
        # Log session start for HIPAA compliance
        security_manager.log_patient_access(
            patient_id=patient_id,
            action='session_start',
            ip_address=request.remote_addr
        )
        
        return jsonify({
            'session_id': session_data['session_id'],
            'patient_id': patient_id,
            'message': 'Session started successfully'
        }), 200
        
    except Exception as e:
        logger.error(f"Failed to start patient session: {str(e)}")
        return jsonify({'error': 'Failed to start session'}), 500

@app.route('/api/chat/message', methods=['POST'])
def process_patient_message():
    """Process patient message through AI agent pipeline"""
    try:
        data = request.get_json()
        patient_id = session.get('patient_id')
        message = data.get('message', '')
        conversation_context = data.get('context', {})
        
        if not patient_id:
            return jsonify({'error': 'No active session'}), 401
        
        if not message:
            return jsonify({'error': 'Message is required'}), 400
        
        # Security: Encrypt and audit log the interaction
        encrypted_message = security_manager.encrypt_patient_data(message)
        security_manager.log_patient_interaction(
            patient_id=patient_id,
            message=message,
            ip_address=request.remote_addr
        )
        
        # Step 1: Intake Agent processes the message
        intake_response = intake_agent.process_message(
            patient_id=patient_id,
            message=message,
            context=conversation_context
        )
        
        # Step 2: Triage Agent assesses urgency
        triage_result = triage_agent.assess_urgency(
            patient_id=patient_id,
            symptoms=intake_response['extracted_symptoms'],
            patient_context=intake_response['patient_context']
        )
        
        # Step 3: Knowledge Agent retrieves relevant information
        knowledge_result = knowledge_agent.retrieve_medical_knowledge(
            symptoms=intake_response['extracted_symptoms'],
            patient_context=intake_response['patient_context']
        )
        
        # Step 4: Check if escalation is needed
        escalation_needed = escalation_agent.check_escalation_needed(
            urgency_score=triage_result['urgency_score'],
            symptoms=intake_response['extracted_symptoms'],
            patient_context=intake_response['patient_context']
        )
        
        # Prepare comprehensive response
        response = {
            'agent_response': intake_response['response'],
            'urgency_assessment': {
                'score': triage_result['urgency_score'],
                'level': triage_result['urgency_level'],
                'reasoning': triage_result['reasoning'],
                'recommended_action': triage_result['recommended_action']
            },
            'medical_knowledge': {
                'relevant_conditions': knowledge_result['conditions'],
                'treatment_guidelines': knowledge_result['treatments'],
                'warning_signs': knowledge_result['warning_signs']
            },
            'escalation': escalation_needed,
            'next_questions': intake_response['follow_up_questions'],
            'conversation_id': intake_response['conversation_id'],
            'timestamp': datetime.now().isoformat()
        }
        
        # Store conversation in database
        patient_db.store_conversation(
            patient_id=patient_id,
            conversation_id=response['conversation_id'],
            user_message=message,
            ai_response=response,
            urgency_score=triage_result['urgency_score']
        )
        
        return jsonify(response), 200
        
    except Exception as e:
        logger.error(f"Failed to process patient message: {str(e)}")
        return jsonify({'error': 'Failed to process message'}), 500

@app.route('/api/patient/history', methods=['GET'])
def get_patient_history():
    """Retrieve patient's conversation history"""
    try:
        patient_id = session.get('patient_id')
        
        if not patient_id:
            return jsonify({'error': 'No active session'}), 401
        
        # Security check
        if not security_manager.verify_patient_access(patient_id, session.get('session_token')):
            return jsonify({'error': 'Unauthorized access'}), 403
        
        # Retrieve conversation history
        history = patient_db.get_patient_history(patient_id)
        
        # Decrypt sensitive data
        decrypted_history = security_manager.decrypt_patient_history(history)
        
        return jsonify({
            'patient_id': patient_id,
            'conversations': decrypted_history,
            'total_interactions': len(decrypted_history)
        }), 200
        
    except Exception as e:
        logger.error(f"Failed to retrieve patient history: {str(e)}")
        return jsonify({'error': 'Failed to retrieve history'}), 500

@app.route('/api/triage/dashboard', methods=['GET'])
def get_triage_dashboard():
    """Get dashboard data for healthcare providers"""
    try:
        # This would require provider authentication in production
        dashboard_data = monitoring.get_triage_dashboard_data()
        
        return jsonify(dashboard_data), 200
        
    except Exception as e:
        logger.error(f"Failed to retrieve dashboard data: {str(e)}")
        return jsonify({'error': 'Failed to retrieve dashboard'}), 500

@app.route('/api/admin/metrics', methods=['GET'])
def get_system_metrics():
    """Get system performance metrics for administrators"""
    try:
        # This would require admin authentication in production
        metrics = monitoring.get_system_metrics()
        
        return jsonify(metrics), 200
        
    except Exception as e:
        logger.error(f"Failed to retrieve system metrics: {str(e)}")
        return jsonify({'error': 'Failed to retrieve metrics'}), 500

@app.route('/api/knowledge/search', methods=['POST'])
def search_medical_knowledge():
    """Search medical knowledge base"""
    try:
        data = request.get_json()
        query = data.get('query', '')
        
        if not query:
            return jsonify({'error': 'Search query is required'}), 400
        
        results = knowledge_agent.search_knowledge_base(query)
        
        return jsonify({
            'query': query,
            'results': results,
            'timestamp': datetime.now().isoformat()
        }), 200
        
    except Exception as e:
        logger.error(f"Failed to search knowledge base: {str(e)}")
        return jsonify({'error': 'Search failed'}), 500

# Error handlers

@app.errorhandler(404)
def not_found(error):
    return jsonify({'error': 'Endpoint not found'}), 404

@app.errorhandler(500)
def internal_error(error):
    logger.error(f"Internal server error: {str(error)}")
    return jsonify({'error': 'Internal server error'}), 500

# Application startup

if __name__ == '__main__':
    # Ensure logs directory exists
    os.makedirs('logs', exist_ok=True)
    
    # Start the Flask application
    host = os.getenv('HOST', '0.0.0.0')
    port = int(os.getenv('PORT', 5000))
    debug = os.getenv('DEBUG', 'True').lower() == 'true'
    
    logger.info(f"Starting Healthcare AI Pod on {host}:{port}")
    logger.info(f"Debug mode: {debug}")
    
    app.run(
        host=host,
        port=port,
        debug=debug,
        threaded=True
    )