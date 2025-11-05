#!/usr/bin/env python3
"""
Healthcare AI Triage System - Production Backend API
KAPI Template Implementation

This backend provides:
- Multi-agent AI orchestration for patient triage
- HIPAA-compliant data handling and audit logging
- Real-time patient assessment and provider notifications
- Comprehensive medical knowledge retrieval
- Production-ready security and monitoring

Architecture: Flask + FastAPI hybrid with microservices design
Security: End-to-end encryption, RBAC, comprehensive audit trails
Performance: Sub-2-second response times, auto-scaling ready
Compliance: HIPAA, HITECH, FDA clinical decision support guidelines
"""

from flask import Flask, request, jsonify
from flask_cors import CORS
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from dotenv import load_dotenv
import os
import logging
import sys
from datetime import datetime, timedelta
import json
import uuid
from typing import Dict, List, Optional, Any
import asyncio
from concurrent.futures import ThreadPoolExecutor
import traceback

# Security and monitoring imports
from werkzeug.security import generate_password_hash, check_password_hash
from jwt import encode as jwt_encode, decode as jwt_decode, InvalidTokenError
from cryptography.fernet import Fernet
import redis
from prometheus_client import Counter, Histogram, generate_latest, CollectorRegistry

# Import application modules
from services.agent_orchestrator import HealthcareAgentOrchestrator
from services.authentication import AuthenticationService
from services.patient_service import PatientService
from services.triage_service import TriageService
from services.knowledge_service import KnowledgeService
from services.monitoring_service import MonitoringService
from database.connection_manager import DatabaseConnectionManager
from utils.security import HIPAASecurityManager, SecurityAuditLogger
from utils.validators import RequestValidator, DataSanitizer
from utils.error_handlers import CustomErrorHandler
from config.settings import ProductionConfig, DevelopmentConfig, TestingConfig

# Load environment variables
load_dotenv()

# Initialize configuration based on environment
config_mapping = {
    'production': ProductionConfig,
    'development': DevelopmentConfig,
    'testing': TestingConfig
}

ENV = os.getenv('FLASK_ENV', 'development')
config = config_mapping.get(ENV, DevelopmentConfig)

# Initialize Flask application with production settings
app = Flask(__name__)
app.config.from_object(config)

# Security configurations
app.config['SESSION_COOKIE_SECURE'] = ENV == 'production'
app.config['SESSION_COOKIE_HTTPONLY'] = True
app.config['SESSION_COOKIE_SAMESITE'] = 'Strict'
app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(minutes=30)

# CORS configuration for healthcare environment
cors_origins = os.getenv('CORS_ORIGINS', 'http://localhost:3000').split(',')
CORS(app, 
     origins=cors_origins,
     supports_credentials=True,
     methods=['GET', 'POST', 'PUT', 'DELETE', 'OPTIONS'],
     allow_headers=['Content-Type', 'Authorization', 'X-HIPAA-Audit-Token'])

# Rate limiting for API protection
limiter = Limiter(
    app,
    key_func=get_remote_address,
    default_limits=["1000 per hour", "100 per minute"],
    storage_uri=os.getenv('REDIS_URL', 'redis://localhost:6379')
)

# Prometheus metrics setup
REGISTRY = CollectorRegistry()
REQUEST_COUNT = Counter('http_requests_total', 'Total HTTP requests', 
                       ['method', 'endpoint', 'status'], registry=REGISTRY)
REQUEST_DURATION = Histogram('http_request_duration_seconds', 'HTTP request duration',
                           ['method', 'endpoint'], registry=REGISTRY)
AGENT_RESPONSE_TIME = Histogram('agent_response_duration_seconds', 'AI agent response time',
                               ['agent_type'], registry=REGISTRY)
TRIAGE_ACCURACY = Counter('triage_accuracy_total', 'Triage accuracy measurements',
                         ['accuracy_level'], registry=REGISTRY)

# Configure comprehensive logging
def setup_logging():
    """Configure HIPAA-compliant logging with proper security measures"""
    log_level = getattr(logging, os.getenv('LOG_LEVEL', 'INFO').upper())
    
    # Create logs directory
    log_dir = os.path.join(os.path.dirname(__file__), 'logs')
    os.makedirs(log_dir, exist_ok=True)
    
    # Configure formatters
    detailed_formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(funcName)s:%(lineno)d - %(message)s'
    )
    
    audit_formatter = logging.Formatter(
        '%(asctime)s - AUDIT - %(levelname)s - %(message)s'
    )
    
    # Application logger
    app_handler = logging.handlers.RotatingFileHandler(
        os.path.join(log_dir, 'application.log'),
        maxBytes=10485760,  # 10MB
        backupCount=10
    )
    app_handler.setFormatter(detailed_formatter)
    app_handler.setLevel(log_level)
    
    # Security audit logger (separate file for compliance)
    audit_handler = logging.handlers.RotatingFileHandler(
        os.path.join(log_dir, 'security_audit.log'),
        maxBytes=10485760,
        backupCount=50  # Keep more audit logs
    )
    audit_handler.setFormatter(audit_formatter)
    audit_handler.setLevel(logging.INFO)
    
    # Error logger
    error_handler = logging.handlers.RotatingFileHandler(
        os.path.join(log_dir, 'errors.log'),
        maxBytes=10485760,
        backupCount=20
    )
    error_handler.setFormatter(detailed_formatter)
    error_handler.setLevel(logging.ERROR)
    
    # Configure loggers
    app.logger.setLevel(log_level)
    app.logger.addHandler(app_handler)
    app.logger.addHandler(error_handler)
    
    # Audit logger
    audit_logger = logging.getLogger('security_audit')
    audit_logger.setLevel(logging.INFO)
    audit_logger.addHandler(audit_handler)
    
    # Console handler for development
    if ENV == 'development':
        console_handler = logging.StreamHandler(sys.stdout)
        console_handler.setFormatter(detailed_formatter)
        console_handler.setLevel(log_level)
        app.logger.addHandler(console_handler)

setup_logging()

# Initialize core services
try:
    # Database connection manager
    db_manager = DatabaseConnectionManager(config)
    
    # Security services
    security_manager = HIPAASecurityManager(config)
    audit_logger = SecurityAuditLogger(config)
    
    # Core business services
    auth_service = AuthenticationService(db_manager, security_manager)
    patient_service = PatientService(db_manager, security_manager, audit_logger)
    triage_service = TriageService(db_manager, security_manager, audit_logger)
    knowledge_service = KnowledgeService(db_manager, security_manager)
    monitoring_service = MonitoringService(db_manager, REGISTRY)
    
    # AI agent orchestrator
    agent_orchestrator = HealthcareAgentOrchestrator(
        patient_service=patient_service,
        knowledge_service=knowledge_service,
        security_manager=security_manager,
        config=config
    )
    
    # Request validation and sanitization
    request_validator = RequestValidator()
    data_sanitizer = DataSanitizer()
    
    # Error handling
    error_handler = CustomErrorHandler(app, audit_logger)
    
    app.logger.info("All system components initialized successfully")
    
except Exception as e:
    app.logger.error(f"Failed to initialize system components: {str(e)}")
    app.logger.error(f"Traceback: {traceback.format_exc()}")
    sys.exit(1)

# Request middleware for security and monitoring
@app.before_request
def before_request():
    """Process all requests for security, validation, and monitoring"""
    request.start_time = datetime.utcnow()
    request.request_id = str(uuid.uuid4())
    
    # Security headers
    if request.endpoint and request.endpoint.startswith('api.'):
        # Validate HIPAA audit token for protected endpoints
        audit_token = request.headers.get('X-HIPAA-Audit-Token')
        if not audit_token:
            return jsonify({'error': 'HIPAA audit token required'}), 400
        
        # Rate limiting for authenticated endpoints
        if hasattr(request, 'limiter_exempt'):
            pass  # Skip rate limiting for exempt endpoints
        
        # Request validation
        if request.method in ['POST', 'PUT', 'PATCH']:
            validation_result = request_validator.validate_request(request)
            if not validation_result.is_valid:
                audit_logger.log_security_event(
                    event_type='invalid_request',
                    details={'errors': validation_result.errors},
                    ip_address=request.remote_addr
                )
                return jsonify({'error': 'Invalid request', 'details': validation_result.errors}), 400

@app.after_request
def after_request(response):
    """Process response for monitoring and security logging"""
    if hasattr(request, 'start_time'):
        duration = (datetime.utcnow() - request.start_time).total_seconds()
        
        # Record metrics
        REQUEST_COUNT.labels(
            method=request.method,
            endpoint=request.endpoint or 'unknown',
            status=response.status_code
        ).inc()
        
        REQUEST_DURATION.labels(
            method=request.method,
            endpoint=request.endpoint or 'unknown'
        ).observe(duration)
        
        # Log request details for audit
        if response.status_code >= 400:
            audit_logger.log_request(
                method=request.method,
                endpoint=request.endpoint,
                status_code=response.status_code,
                duration_ms=duration * 1000,
                ip_address=request.remote_addr,
                user_agent=request.headers.get('User-Agent'),
                request_id=getattr(request, 'request_id', 'unknown')
            )
    
    # Security headers
    response.headers['X-Content-Type-Options'] = 'nosniff'
    response.headers['X-Frame-Options'] = 'DENY'
    response.headers['X-XSS-Protection'] = '1; mode=block'
    response.headers['Strict-Transport-Security'] = 'max-age=31536000; includeSubDomains'
    response.headers['Referrer-Policy'] = 'strict-origin-when-cross-origin'
    response.headers['X-Request-ID'] = getattr(request, 'request_id', 'unknown')
    
    return response

# =============================================================================
# AUTHENTICATION AND SESSION MANAGEMENT
# =============================================================================

@app.route('/api/v1/auth/login', methods=['POST'])
@limiter.limit("5 per minute")
def login():
    """Authenticate healthcare provider"""
    try:
        data = request.get_json()
        employee_id = data_sanitizer.sanitize_string(data.get('employee_id', ''))
        password = data.get('password', '')
        mfa_token = data_sanitizer.sanitize_string(data.get('mfa_token', ''))
        
        # Validate required fields
        if not all([employee_id, password, mfa_token]):
            audit_logger.log_security_event(
                event_type='login_attempt_missing_fields',
                details={'employee_id': employee_id},
                ip_address=request.remote_addr
            )
            return jsonify({'error': 'Employee ID, password, and MFA token required'}), 400
        
        # Authenticate user
        auth_result = auth_service.authenticate(
            employee_id=employee_id,
            password=password,
            mfa_token=mfa_token,
            ip_address=request.remote_addr,
            user_agent=request.headers.get('User-Agent', '')
        )
        
        if auth_result.success:
            audit_logger.log_security_event(
                event_type='login_success',
                details={'employee_id': employee_id, 'role': auth_result.user.role},
                ip_address=request.remote_addr,
                user_id=auth_result.user.id
            )
            
            return jsonify({
                'access_token': auth_result.access_token,
                'refresh_token': auth_result.refresh_token,
                'user': {
                    'id': auth_result.user.id,
                    'employee_id': auth_result.user.employee_id,
                    'name': f"{auth_result.user.first_name} {auth_result.user.last_name}",
                    'role': auth_result.user.role,
                    'department': auth_result.user.department,
                    'permissions': auth_result.user.permissions
                },
                'expires_in': auth_result.expires_in
            }), 200
        else:
            audit_logger.log_security_event(
                event_type='login_failure',
                details={'employee_id': employee_id, 'reason': auth_result.error},
                ip_address=request.remote_addr
            )
            return jsonify({'error': auth_result.error}), 401
            
    except Exception as e:
        app.logger.error(f"Login error: {str(e)}")
        return jsonify({'error': 'Authentication failed'}), 500

@app.route('/api/v1/auth/logout', methods=['POST'])
def logout():
    """Logout and invalidate tokens"""
    try:
        auth_header = request.headers.get('Authorization', '')
        token = auth_header.replace('Bearer ', '') if auth_header.startswith('Bearer ') else ''
        
        if token:
            auth_service.logout(token)
            audit_logger.log_security_event(
                event_type='logout',
                ip_address=request.remote_addr
            )
        
        return jsonify({'message': 'Logged out successfully'}), 200
        
    except Exception as e:
        app.logger.error(f"Logout error: {str(e)}")
        return jsonify({'error': 'Logout failed'}), 500

# =============================================================================
# PATIENT MANAGEMENT ENDPOINTS
# =============================================================================

@app.route('/api/v1/patients', methods=['POST'])
@auth_service.require_permission('patient:create')
def create_patient():
    """Create new patient record with HIPAA compliance"""
    try:
        data = request.get_json()
        
        # Validate required patient data
        required_fields = ['medical_record_number', 'demographics']
        validation_result = request_validator.validate_required_fields(data, required_fields)
        if not validation_result.is_valid:
            return jsonify({'error': 'Missing required fields', 'details': validation_result.errors}), 400
        
        # Sanitize patient data
        sanitized_data = data_sanitizer.sanitize_patient_data(data)
        
        # Create patient record
        patient = patient_service.create_patient(
            patient_data=sanitized_data,
            created_by=request.current_user.id
        )
        
        audit_logger.log_patient_access(
            patient_id=patient.id,
            action='patient_created',
            user_id=request.current_user.id,
            ip_address=request.remote_addr
        )
        
        return jsonify({
            'id': patient.id,
            'medical_record_number': patient.medical_record_number,
            'created_at': patient.created_at.isoformat(),
            'message': 'Patient created successfully'
        }), 201
        
    except patient_service.PatientExistsError as e:
        return jsonify({'error': str(e)}), 409
    except Exception as e:
        app.logger.error(f"Patient creation error: {str(e)}")
        return jsonify({'error': 'Failed to create patient'}), 500

@app.route('/api/v1/patients', methods=['GET'])
@auth_service.require_permission('patient:read')
def search_patients():
    """Search patients with proper access controls"""
    try:
        # Get search parameters
        mrn = data_sanitizer.sanitize_string(request.args.get('medical_record_number', ''))
        last_name = data_sanitizer.sanitize_string(request.args.get('last_name', ''))
        dob = data_sanitizer.sanitize_date(request.args.get('date_of_birth', ''))
        limit = min(int(request.args.get('limit', 20)), 100)  # Max 100 results
        
        # Perform search
        search_results = patient_service.search_patients(
            medical_record_number=mrn,
            last_name=last_name,
            date_of_birth=dob,
            limit=limit,
            requesting_user=request.current_user
        )
        
        # Log search for audit
        audit_logger.log_patient_search(
            search_criteria={'mrn': mrn, 'last_name': last_name, 'dob': dob},
            results_count=len(search_results.patients),
            user_id=request.current_user.id,
            ip_address=request.remote_addr
        )
        
        return jsonify({
            'patients': [patient.to_summary_dict() for patient in search_results.patients],
            'total_count': search_results.total_count,
            'has_more': search_results.has_more
        }), 200
        
    except Exception as e:
        app.logger.error(f"Patient search error: {str(e)}")
        return jsonify({'error': 'Search failed'}), 500

@app.route('/api/v1/patients/<patient_id>', methods=['GET'])
@auth_service.require_permission('patient:read')
def get_patient(patient_id):
    """Retrieve detailed patient information"""
    try:
        # Validate UUID format
        try:
            uuid.UUID(patient_id)
        except ValueError:
            return jsonify({'error': 'Invalid patient ID format'}), 400
        
        # Check patient access permissions
        if not patient_service.check_patient_access(patient_id, request.current_user):
            audit_logger.log_security_event(
                event_type='unauthorized_patient_access',
                details={'patient_id': patient_id},
                user_id=request.current_user.id,
                ip_address=request.remote_addr
            )
            return jsonify({'error': 'Access denied'}), 403
        
        # Retrieve patient data
        patient = patient_service.get_patient(patient_id)
        if not patient:
            return jsonify({'error': 'Patient not found'}), 404
        
        # Log access for audit
        audit_logger.log_patient_access(
            patient_id=patient_id,
            action='patient_viewed',
            user_id=request.current_user.id,
            ip_address=request.remote_addr
        )
        
        return jsonify(patient.to_detailed_dict()), 200
        
    except Exception as e:
        app.logger.error(f"Patient retrieval error: {str(e)}")
        return jsonify({'error': 'Failed to retrieve patient'}), 500

# =============================================================================
# TRIAGE SESSION ENDPOINTS
# =============================================================================

@app.route('/api/v1/triage/sessions', methods=['POST'])
@auth_service.require_permission('triage:create')
def start_triage_session():
    """Initialize new triage assessment session"""
    try:
        data = request.get_json()
        
        # Validate required fields
        required_fields = ['patient_id', 'department', 'chief_complaint']
        validation_result = request_validator.validate_required_fields(data, required_fields)
        if not validation_result.is_valid:
            return jsonify({'error': 'Missing required fields', 'details': validation_result.errors}), 400
        
        # Sanitize triage data
        sanitized_data = data_sanitizer.sanitize_triage_data(data)
        
        # Create triage session
        triage_session = triage_service.create_session(
            patient_id=sanitized_data['patient_id'],
            triage_nurse_id=request.current_user.id,
            session_data=sanitized_data
        )
        
        audit_logger.log_patient_access(
            patient_id=sanitized_data['patient_id'],
            action='triage_session_started',
            user_id=request.current_user.id,
            ip_address=request.remote_addr,
            additional_data={'session_id': triage_session.id}
        )
        
        return jsonify({
            'id': triage_session.id,
            'patient_id': triage_session.patient_id,
            'department': triage_session.department,
            'status': triage_session.status,
            'session_start': triage_session.session_start.isoformat(),
            'message': 'Triage session started successfully'
        }), 201
        
    except Exception as e:
        app.logger.error(f"Triage session creation error: {str(e)}")
        return jsonify({'error': 'Failed to start triage session'}), 500

@app.route('/api/v1/agents/interact', methods=['POST'])
@auth_service.require_permission('triage:update')
@limiter.limit("60 per minute")  # Rate limit AI interactions
def interact_with_agents():
    """Process message through AI agent pipeline"""
    try:
        data = request.get_json()
        
        # Validate required fields
        required_fields = ['session_id', 'agent_type', 'message']
        validation_result = request_validator.validate_required_fields(data, required_fields)
        if not validation_result.is_valid:
            return jsonify({'error': 'Missing required fields', 'details': validation_result.errors}), 400
        
        session_id = data_sanitizer.sanitize_string(data['session_id'])
        agent_type = data_sanitizer.sanitize_string(data['agent_type'])
        message = data_sanitizer.sanitize_text(data['message'])
        context = data.get('context', {})
        
        # Validate agent type
        valid_agents = ['intake', 'triage', 'knowledge', 'escalation']
        if agent_type not in valid_agents:
            return jsonify({'error': f'Invalid agent type. Must be one of: {valid_agents}'}), 400
        
        # Verify session access
        session = triage_service.get_session(session_id)
        if not session:
            return jsonify({'error': 'Triage session not found'}), 404
        
        if not triage_service.check_session_access(session_id, request.current_user):
            return jsonify({'error': 'Access denied to this session'}), 403
        
        # Process through AI agents with performance monitoring
        start_time = datetime.utcnow()
        
        agent_response = agent_orchestrator.process_interaction(
            session_id=session_id,
            agent_type=agent_type,
            message=message,
            context=context,
            user=request.current_user
        )
        
        processing_time = (datetime.utcnow() - start_time).total_seconds()
        AGENT_RESPONSE_TIME.labels(agent_type=agent_type).observe(processing_time)
        
        # Log interaction for audit and monitoring
        audit_logger.log_agent_interaction(
            session_id=session_id,
            agent_type=agent_type,
            message_length=len(message),
            processing_time_ms=processing_time * 1000,
            confidence_score=agent_response.confidence_score,
            user_id=request.current_user.id,
            ip_address=request.remote_addr
        )
        
        return jsonify({
            'agent_type': agent_response.agent_type,
            'response_type': agent_response.response_type,
            'message': agent_response.message,
            'confidence_score': agent_response.confidence_score,
            'suggested_actions': agent_response.suggested_actions,
            'assessment': agent_response.assessment,
            'processing_time_ms': int(processing_time * 1000),
            'timestamp': datetime.utcnow().isoformat()
        }), 200
        
    except agent_orchestrator.AgentError as e:
        app.logger.error(f"Agent interaction error: {str(e)}")
        return jsonify({'error': str(e)}), 400
    except Exception as e:
        app.logger.error(f"Unexpected agent error: {str(e)}")
        return jsonify({'error': 'Agent interaction failed'}), 500

# =============================================================================
# MEDICAL KNOWLEDGE ENDPOINTS
# =============================================================================

@app.route('/api/v1/knowledge/search', methods=['POST'])
@auth_service.require_permission('clinical:read')
def search_medical_knowledge():
    """Search medical knowledge base with semantic search"""
    try:
        data = request.get_json()
        
        query = data_sanitizer.sanitize_text(data.get('query', ''))
        if not query:
            return jsonify({'error': 'Search query is required'}), 400
        
        filters = data.get('filters', {})
        limit = min(int(data.get('limit', 10)), 50)  # Max 50 results
        
        # Perform semantic search
        search_results = knowledge_service.search_knowledge(
            query=query,
            filters=filters,
            limit=limit,
            user=request.current_user
        )
        
        # Log search for analytics
        audit_logger.log_knowledge_search(
            query=query,
            filters=filters,
            results_count=len(search_results.results),
            user_id=request.current_user.id,
            ip_address=request.remote_addr
        )
        
        return jsonify({
            'query': query,
            'results': [result.to_dict() for result in search_results.results],
            'total_count': search_results.total_count,
            'search_time_ms': search_results.search_time_ms,
            'timestamp': datetime.utcnow().isoformat()
        }), 200
        
    except Exception as e:
        app.logger.error(f"Knowledge search error: {str(e)}")
        return jsonify({'error': 'Search failed'}), 500

@app.route('/api/v1/knowledge/drug-interactions', methods=['POST'])
@auth_service.require_permission('clinical:read')
def check_drug_interactions():
    """Check for drug interactions and contraindications"""
    try:
        data = request.get_json()
        
        medications = data.get('medications', [])
        if not medications:
            return jsonify({'error': 'Medication list is required'}), 400
        
        # Sanitize medication list
        sanitized_medications = [data_sanitizer.sanitize_string(med) for med in medications]
        
        # Check for interactions
        interaction_results = knowledge_service.check_drug_interactions(
            medications=sanitized_medications,
            user=request.current_user
        )
        
        # Log drug interaction check
        audit_logger.log_drug_interaction_check(
            medications=sanitized_medications,
            interactions_found=len(interaction_results.interactions),
            user_id=request.current_user.id,
            ip_address=request.remote_addr
        )
        
        return jsonify({
            'medications': sanitized_medications,
            'interactions': [interaction.to_dict() for interaction in interaction_results.interactions],
            'warnings': interaction_results.warnings,
            'contraindications': interaction_results.contraindications,
            'timestamp': datetime.utcnow().isoformat()
        }), 200
        
    except Exception as e:
        app.logger.error(f"Drug interaction check error: {str(e)}")
        return jsonify({'error': 'Drug interaction check failed'}), 500

# =============================================================================
# ANALYTICS AND REPORTING
# =============================================================================

@app.route('/api/v1/analytics/dashboard', methods=['GET'])
@auth_service.require_permission('analytics:read')
def get_triage_dashboard():
    """Get real-time triage analytics dashboard"""
    try:
        # Get time range parameter
        time_range = request.args.get('time_range', 'day')
        department = request.args.get('department', 'all')
        
        # Validate parameters
        valid_ranges = ['hour', 'day', 'week', 'month']
        if time_range not in valid_ranges:
            return jsonify({'error': f'Invalid time range. Must be one of: {valid_ranges}'}), 400
        
        # Get dashboard data
        dashboard_data = monitoring_service.get_triage_dashboard(
            time_range=time_range,
            department=department,
            user=request.current_user
        )
        
        return jsonify(dashboard_data.to_dict()), 200
        
    except Exception as e:
        app.logger.error(f"Dashboard data error: {str(e)}")
        return jsonify({'error': 'Failed to retrieve dashboard data'}), 500

# =============================================================================
# SYSTEM HEALTH AND MONITORING
# =============================================================================

@app.route('/api/v1/health', methods=['GET'])
def health_check():
    """Basic health check for load balancers"""
    try:
        # Quick health check
        health_status = monitoring_service.get_basic_health()
        
        if health_status.is_healthy:
            return jsonify({
                'status': 'healthy',
                'timestamp': datetime.utcnow().isoformat(),
                'version': config.VERSION,
                'uptime_seconds': health_status.uptime_seconds
            }), 200
        else:
            return jsonify({
                'status': 'unhealthy',
                'issues': health_status.issues,
                'timestamp': datetime.utcnow().isoformat()
            }), 503
            
    except Exception as e:
        app.logger.error(f"Health check error: {str(e)}")
        return jsonify({
            'status': 'unhealthy',
            'error': 'Health check failed'
        }), 503

@app.route('/api/v1/health/detailed', methods=['GET'])
@auth_service.require_permission('admin:read')
def detailed_health_check():
    """Comprehensive health check for administrators"""
    try:
        health_details = monitoring_service.get_detailed_health()
        
        return jsonify({
            'overall_status': health_details.overall_status,
            'components': health_details.components,
            'metrics': health_details.metrics,
            'timestamp': datetime.utcnow().isoformat()
        }), 200
        
    except Exception as e:
        app.logger.error(f"Detailed health check error: {str(e)}")
        return jsonify({'error': 'Detailed health check failed'}), 500

@app.route('/metrics', methods=['GET'])
def metrics():
    """Prometheus metrics endpoint"""
    return generate_latest(REGISTRY), 200, {'Content-Type': 'text/plain; charset=utf-8'}

# =============================================================================
# ERROR HANDLERS
# =============================================================================

@app.errorhandler(400)
def bad_request(error):
    audit_logger.log_error(
        error_type='bad_request',
        message=str(error),
        ip_address=request.remote_addr,
        endpoint=request.endpoint
    )
    return jsonify({'error': 'Bad request', 'message': str(error)}), 400

@app.errorhandler(401)
def unauthorized(error):
    audit_logger.log_security_event(
        event_type='unauthorized_access',
        details={'endpoint': request.endpoint},
        ip_address=request.remote_addr
    )
    return jsonify({'error': 'Unauthorized', 'message': 'Authentication required'}), 401

@app.errorhandler(403)
def forbidden(error):
    audit_logger.log_security_event(
        event_type='forbidden_access',
        details={'endpoint': request.endpoint},
        ip_address=request.remote_addr,
        user_id=getattr(request, 'current_user', {}).get('id')
    )
    return jsonify({'error': 'Forbidden', 'message': 'Insufficient permissions'}), 403

@app.errorhandler(404)
def not_found(error):
    return jsonify({'error': 'Not found', 'message': 'Resource not found'}), 404

@app.errorhandler(429)
def rate_limit_exceeded(error):
    audit_logger.log_security_event(
        event_type='rate_limit_exceeded',
        details={'limit': str(error.description)},
        ip_address=request.remote_addr
    )
    return jsonify({
        'error': 'Rate limit exceeded',
        'message': 'Too many requests, please slow down'
    }), 429

@app.errorhandler(500)
def internal_error(error):
    app.logger.error(f"Internal server error: {str(error)}")
    audit_logger.log_error(
        error_type='internal_server_error',
        message=str(error),
        ip_address=request.remote_addr,
        endpoint=request.endpoint
    )
    return jsonify({'error': 'Internal server error'}), 500

# =============================================================================
# APPLICATION STARTUP
# =============================================================================

def create_app(config_name=None):
    """Application factory for testing and deployment"""
    if config_name:
        app.config.from_object(config_mapping[config_name])
    return app

if __name__ == '__main__':
    # Ensure required directories exist
    os.makedirs('logs', exist_ok=True)
    
    # Get configuration
    host = os.getenv('HOST', '0.0.0.0')
    port = int(os.getenv('PORT', 5000))
    debug = ENV == 'development'
    
    app.logger.info(f"Starting Healthcare AI Triage System")
    app.logger.info(f"Environment: {ENV}")
    app.logger.info(f"Host: {host}:{port}")
    app.logger.info(f"Debug mode: {debug}")
    app.logger.info(f"Configuration: {config.__name__}")
    
    # Security warning for development
    if ENV == 'development':
        app.logger.warning("Running in development mode - DO NOT USE IN PRODUCTION")
    
    # Start application
    if ENV == 'production':
        # Production mode - use WSGI server
        app.logger.info("Production mode: Use WSGI server (gunicorn/uWSGI)")
    else:
        # Development mode
        app.run(
            host=host,
            port=port,
            debug=debug,
            threaded=True,
            use_reloader=True
        )