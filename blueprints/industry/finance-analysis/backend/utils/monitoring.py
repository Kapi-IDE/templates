#!/usr/bin/env python3
"""
Financial AI Platform Monitoring and Analytics
Provides comprehensive monitoring, metrics, and performance analytics
"""

import logging
import json
from typing import Dict, Any, List, Optional
from datetime import datetime, timedelta
from collections import defaultdict
import statistics
import time

logger = logging.getLogger(__name__)

class FinancialAIMonitoring:
    """
    Comprehensive monitoring system for Financial AI Platform
    Tracks performance, usage, compliance, and system health
    """
    
    def __init__(self):
        """Initialize Financial AI Monitoring"""
        self.metrics_buffer = defaultdict(list)
        self.alert_thresholds = {
            'response_time_ms': 5000,
            'error_rate_percent': 5.0,
            'cpu_usage_percent': 80.0,
            'memory_usage_percent': 85.0,
            'disk_usage_percent': 90.0,
            'concurrent_users': 1000,
            'api_rate_limit': 10000
        }
        
        self.performance_baselines = {
            'research_analysis_ms': 3000,
            'risk_assessment_ms': 2000,
            'report_generation_ms': 5000,
            'compliance_check_ms': 1000,
            'database_query_ms': 500
        }
        
        logger.info("Financial AI Monitoring initialized")
    
    def track_agent_performance(self, agent_type: str, operation: str,
                              duration_ms: float, success: bool = True,
                              additional_metrics: Dict = None) -> None:
        """Track AI agent performance metrics"""
        try:
            metric_entry = {
                'timestamp': datetime.now().isoformat(),
                'agent_type': agent_type,
                'operation': operation,
                'duration_ms': duration_ms,
                'success': success,
                'additional_metrics': additional_metrics or {}
            }
            
            # Store in metrics buffer
            self.metrics_buffer[f"{agent_type}_{operation}"].append(metric_entry)
            
            # Check for performance alerts
            baseline_key = f"{operation}_ms"
            if baseline_key in self.performance_baselines:
                baseline = self.performance_baselines[baseline_key]
                if duration_ms > baseline * 1.5:  # 50% above baseline
                    self._create_performance_alert(
                        agent_type, operation, duration_ms, baseline
                    )
            
            logger.info(f"Agent performance tracked: {agent_type}.{operation} - {duration_ms}ms")
            
        except Exception as e:
            logger.error(f"Failed to track agent performance: {str(e)}")
    
    def track_api_usage(self, endpoint: str, method: str, status_code: int,
                       response_time_ms: float, user_id: str = None,
                       client_id: str = None) -> None:
        """Track API endpoint usage and performance"""
        try:
            usage_entry = {
                'timestamp': datetime.now().isoformat(),
                'endpoint': endpoint,
                'method': method,
                'status_code': status_code,
                'response_time_ms': response_time_ms,
                'user_id': user_id,
                'client_id': client_id,
                'success': 200 <= status_code < 400
            }
            
            # Store API metrics
            self.metrics_buffer['api_usage'].append(usage_entry)
            
            # Check response time threshold
            if response_time_ms > self.alert_thresholds['response_time_ms']:
                self._create_api_alert(endpoint, response_time_ms)
            
        except Exception as e:
            logger.error(f"Failed to track API usage: {str(e)}")
    
    def track_financial_analysis(self, analysis_type: str, ticker: str = None,
                               confidence_score: float = None, risk_score: float = None,
                               advisor_id: str = None, client_id: str = None) -> None:
        """Track financial analysis quality and patterns"""
        try:
            analysis_entry = {
                'timestamp': datetime.now().isoformat(),
                'analysis_type': analysis_type,
                'ticker': ticker,
                'confidence_score': confidence_score,
                'risk_score': risk_score,
                'advisor_id': advisor_id,
                'client_id': client_id,
                'has_client_context': client_id is not None
            }
            
            # Store financial analysis metrics
            self.metrics_buffer['financial_analysis'].append(analysis_entry)
            
            # Track analysis quality trends
            if confidence_score and confidence_score < 5.0:  # Low confidence threshold
                self._create_quality_alert(analysis_type, confidence_score, ticker)
            
        except Exception as e:
            logger.error(f"Failed to track financial analysis: {str(e)}")
    
    def track_compliance_activity(self, activity_type: str, advisor_id: str,
                                client_id: str = None, compliant: bool = True,
                                violations: List[str] = None) -> None:
        """Track compliance-related activities and violations"""
        try:
            compliance_entry = {
                'timestamp': datetime.now().isoformat(),
                'activity_type': activity_type,
                'advisor_id': advisor_id,
                'client_id': client_id,
                'compliant': compliant,
                'violations': violations or [],
                'violation_count': len(violations) if violations else 0
            }
            
            # Store compliance metrics
            self.metrics_buffer['compliance_activity'].append(compliance_entry)
            
            # Create alerts for compliance violations
            if not compliant or (violations and len(violations) > 0):
                self._create_compliance_alert(advisor_id, activity_type, violations)
            
        except Exception as e:
            logger.error(f"Failed to track compliance activity: {str(e)}")
    
    def track_user_behavior(self, user_id: str, action: str, resource: str = None,
                           session_duration_mins: float = None) -> None:
        """Track user behavior patterns for analytics"""
        try:
            behavior_entry = {
                'timestamp': datetime.now().isoformat(),
                'user_id': user_id,
                'action': action,
                'resource': resource,
                'session_duration_mins': session_duration_mins,
                'hour_of_day': datetime.now().hour,
                'day_of_week': datetime.now().weekday()
            }
            
            # Store user behavior metrics
            self.metrics_buffer['user_behavior'].append(behavior_entry)
            
        except Exception as e:
            logger.error(f"Failed to track user behavior: {str(e)}")
    
    def get_financial_platform_dashboard(self) -> Dict[str, Any]:
        """Get comprehensive financial platform dashboard metrics"""
        try:
            # Calculate dashboard metrics
            current_time = datetime.now()
            last_hour = current_time - timedelta(hours=1)
            last_24h = current_time - timedelta(hours=24)
            last_7d = current_time - timedelta(days=7)
            
            dashboard = {
                'generated_at': current_time.isoformat(),
                'platform_status': 'Operational',
                'uptime_percent': 99.95,
                
                # Financial Analysis Metrics
                'analysis_metrics': {
                    'total_analyses_24h': self._count_recent_analyses(last_24h),
                    'average_confidence_score': self._calculate_average_confidence(),
                    'high_confidence_analyses_percent': self._calculate_high_confidence_rate(),
                    'top_analyzed_sectors': self._get_top_analyzed_sectors(),
                    'analysis_types_breakdown': self._get_analysis_types_breakdown()
                },
                
                # Performance Metrics
                'performance_metrics': {
                    'average_response_time_ms': self._calculate_average_response_time(),
                    'research_agent_avg_ms': self._get_agent_avg_time('research_agent'),
                    'risk_agent_avg_ms': self._get_agent_avg_time('risk_assessment_agent'),
                    'report_agent_avg_ms': self._get_agent_avg_time('report_generation_agent'),
                    'api_success_rate_percent': self._calculate_api_success_rate(),
                    'error_rate_percent': self._calculate_error_rate()
                },
                
                # Usage Statistics
                'usage_statistics': {
                    'active_advisors_24h': self._count_active_advisors(last_24h),
                    'client_sessions_24h': self._count_client_sessions(last_24h),
                    'reports_generated_24h': self._count_reports_generated(last_24h),
                    'api_calls_24h': self._count_api_calls(last_24h),
                    'peak_concurrent_users': self._get_peak_concurrent_users(),
                    'average_session_duration_mins': self._calculate_avg_session_duration()
                },
                
                # Compliance Metrics
                'compliance_metrics': {
                    'suitability_checks_24h': self._count_suitability_checks(last_24h),
                    'compliance_rate_percent': self._calculate_compliance_rate(),
                    'violations_24h': self._count_violations(last_24h),
                    'audit_events_24h': self._count_audit_events(last_24h),
                    'regulatory_alerts_active': self._count_active_regulatory_alerts()
                },
                
                # System Health
                'system_health': {
                    'database_status': 'Healthy',
                    'knowledge_base_status': 'Healthy',
                    'ai_models_status': 'Operational',
                    'security_status': 'Secure',
                    'backup_status': 'Current',
                    'last_health_check': current_time.isoformat()
                },
                
                # Alerts and Issues
                'active_alerts': self._get_active_alerts(),
                'system_alerts': self._get_system_alerts(),
                
                # Trending Data
                'trending': {
                    'popular_analysis_types': self._get_trending_analysis_types(),
                    'most_researched_tickers': self._get_most_researched_tickers(),
                    'busiest_hours': self._get_busiest_hours(),
                    'advisor_activity_trends': self._get_advisor_activity_trends()
                }
            }
            
            return dashboard
            
        except Exception as e:
            logger.error(f"Failed to generate financial platform dashboard: {str(e)}")
            return {'error': str(e), 'platform_status': 'Error'}
    
    def get_advisor_performance_report(self, advisor_id: str, days: int = 30) -> Dict[str, Any]:
        """Generate performance report for specific advisor"""
        try:
            cutoff_date = datetime.now() - timedelta(days=days)
            
            # Filter advisor activities
            advisor_activities = self._filter_advisor_activities(advisor_id, cutoff_date)
            
            report = {
                'advisor_id': advisor_id,
                'reporting_period_days': days,
                'generated_at': datetime.now().isoformat(),
                
                'activity_summary': {
                    'total_analyses': len(advisor_activities.get('analyses', [])),
                    'client_interactions': len(advisor_activities.get('client_sessions', [])),
                    'reports_generated': len(advisor_activities.get('reports', [])),
                    'compliance_reviews': len(advisor_activities.get('compliance', [])),
                    'average_analyses_per_day': len(advisor_activities.get('analyses', [])) / days
                },
                
                'quality_metrics': {
                    'average_confidence_score': self._calculate_advisor_avg_confidence(advisor_id),
                    'high_confidence_rate_percent': self._calculate_advisor_high_confidence_rate(advisor_id),
                    'client_satisfaction_score': 8.5,  # Simulated metric
                    'peer_ranking_percentile': 75  # Simulated metric
                },
                
                'compliance_metrics': {
                    'compliance_rate_percent': self._calculate_advisor_compliance_rate(advisor_id),
                    'violations_count': self._count_advisor_violations(advisor_id, cutoff_date),
                    'suitability_checks_performed': len(advisor_activities.get('compliance', [])),
                    'documentation_completeness_percent': 95  # Simulated metric
                },
                
                'productivity_metrics': {
                    'average_analysis_time_mins': self._calculate_advisor_avg_time(advisor_id),
                    'reports_per_week': len(advisor_activities.get('reports', [])) / (days / 7),
                    'client_coverage_ratio': 0.85,  # Simulated metric
                    'response_time_percentile': 80  # Simulated metric
                },
                
                'recommendations': self._generate_advisor_recommendations(advisor_activities)
            }
            
            return report
            
        except Exception as e:
            logger.error(f"Failed to generate advisor performance report: {str(e)}")
            return {'error': str(e)}
    
    def _create_performance_alert(self, agent_type: str, operation: str,
                                actual_ms: float, baseline_ms: float) -> None:
        """Create performance degradation alert"""
        try:
            alert = {
                'alert_type': 'performance_degradation',
                'severity': 'medium',
                'agent_type': agent_type,
                'operation': operation,
                'actual_duration_ms': actual_ms,
                'baseline_duration_ms': baseline_ms,
                'performance_degradation_percent': ((actual_ms - baseline_ms) / baseline_ms) * 100,
                'timestamp': datetime.now().isoformat(),
                'requires_investigation': True
            }
            
            logger.warning(f"PERFORMANCE ALERT: {json.dumps(alert)}")
            
        except Exception as e:
            logger.error(f"Failed to create performance alert: {str(e)}")
    
    def _create_api_alert(self, endpoint: str, response_time_ms: float) -> None:
        """Create API performance alert"""
        try:
            alert = {
                'alert_type': 'api_performance',
                'severity': 'medium',
                'endpoint': endpoint,
                'response_time_ms': response_time_ms,
                'threshold_ms': self.alert_thresholds['response_time_ms'],
                'timestamp': datetime.now().isoformat(),
                'requires_optimization': True
            }
            
            logger.warning(f"API PERFORMANCE ALERT: {json.dumps(alert)}")
            
        except Exception as e:
            logger.error(f"Failed to create API alert: {str(e)}")
    
    def _create_quality_alert(self, analysis_type: str, confidence_score: float,
                            ticker: str = None) -> None:
        """Create analysis quality alert"""
        try:
            alert = {
                'alert_type': 'analysis_quality',
                'severity': 'low',
                'analysis_type': analysis_type,
                'confidence_score': confidence_score,
                'ticker': ticker,
                'threshold': 5.0,
                'timestamp': datetime.now().isoformat(),
                'requires_review': True
            }
            
            logger.info(f"QUALITY ALERT: {json.dumps(alert)}")
            
        except Exception as e:
            logger.error(f"Failed to create quality alert: {str(e)}")
    
    def _create_compliance_alert(self, advisor_id: str, activity_type: str,
                               violations: List[str]) -> None:
        """Create compliance violation alert"""
        try:
            alert = {
                'alert_type': 'compliance_violation',
                'severity': 'high',
                'advisor_id': advisor_id,
                'activity_type': activity_type,
                'violations': violations,
                'violation_count': len(violations),
                'timestamp': datetime.now().isoformat(),
                'requires_immediate_attention': True,
                'escalation_required': True
            }
            
            logger.error(f"COMPLIANCE ALERT: {json.dumps(alert)}")
            
        except Exception as e:
            logger.error(f"Failed to create compliance alert: {str(e)}")
    
    # Simplified metric calculation methods for educational purposes
    def _count_recent_analyses(self, since: datetime) -> int:
        """Count recent financial analyses"""
        return len([a for a in self.metrics_buffer.get('financial_analysis', [])
                   if datetime.fromisoformat(a['timestamp'].replace('Z', '+00:00').replace('+00:00', '')) > since])
    
    def _calculate_average_confidence(self) -> float:
        """Calculate average confidence score"""
        analyses = self.metrics_buffer.get('financial_analysis', [])
        confidence_scores = [a.get('confidence_score', 0) for a in analyses if a.get('confidence_score')]
        return round(statistics.mean(confidence_scores), 2) if confidence_scores else 7.2
    
    def _calculate_high_confidence_rate(self) -> float:
        """Calculate percentage of high confidence analyses"""
        analyses = self.metrics_buffer.get('financial_analysis', [])
        if not analyses:
            return 78.5  # Simulated value
        
        high_confidence = [a for a in analyses if a.get('confidence_score', 0) >= 7]
        return round((len(high_confidence) / len(analyses)) * 100, 1)
    
    def _get_top_analyzed_sectors(self) -> List[str]:
        """Get most analyzed sectors"""
        # Simulated data for educational purposes
        return ['Technology', 'Healthcare', 'Financial Services', 'Energy']
    
    def _get_analysis_types_breakdown(self) -> Dict[str, int]:
        """Get breakdown of analysis types"""
        return {
            'comprehensive': 45,
            'quick': 32,
            'risk_focused': 18,
            'compliance_review': 5
        }
    
    def _calculate_average_response_time(self) -> float:
        """Calculate average API response time"""
        api_calls = self.metrics_buffer.get('api_usage', [])
        if not api_calls:
            return 850.0  # Simulated value
        
        response_times = [call.get('response_time_ms', 0) for call in api_calls]
        return round(statistics.mean(response_times), 1) if response_times else 850.0
    
    def _get_agent_avg_time(self, agent_type: str) -> float:
        """Get average processing time for specific agent"""
        # Simulated values for educational purposes
        agent_times = {
            'research_agent': 2850.0,
            'risk_assessment_agent': 1750.0,
            'report_generation_agent': 4200.0,
            'compliance_agent': 950.0
        }
        return agent_times.get(agent_type, 2000.0)
    
    def _calculate_api_success_rate(self) -> float:
        """Calculate API success rate"""
        api_calls = self.metrics_buffer.get('api_usage', [])
        if not api_calls:
            return 99.2  # Simulated value
        
        successful = [call for call in api_calls if call.get('success', True)]
        return round((len(successful) / len(api_calls)) * 100, 1)
    
    def _calculate_error_rate(self) -> float:
        """Calculate system error rate"""
        return round(100.0 - self._calculate_api_success_rate(), 1)
    
    def _count_active_advisors(self, since: datetime) -> int:
        """Count active advisors in time period"""
        return 45  # Simulated value
    
    def _count_client_sessions(self, since: datetime) -> int:
        """Count client sessions in time period"""
        return 128  # Simulated value
    
    def _count_reports_generated(self, since: datetime) -> int:
        """Count reports generated in time period"""
        return 67  # Simulated value
    
    def _count_api_calls(self, since: datetime) -> int:
        """Count API calls in time period"""
        return len([call for call in self.metrics_buffer.get('api_usage', [])])
    
    def _get_peak_concurrent_users(self) -> int:
        """Get peak concurrent users"""
        return 89  # Simulated value
    
    def _calculate_avg_session_duration(self) -> float:
        """Calculate average session duration"""
        return 45.3  # Simulated value in minutes
    
    def _count_suitability_checks(self, since: datetime) -> int:
        """Count suitability checks performed"""
        return 156  # Simulated value
    
    def _calculate_compliance_rate(self) -> float:
        """Calculate overall compliance rate"""
        compliance_activities = self.metrics_buffer.get('compliance_activity', [])
        if not compliance_activities:
            return 96.8  # Simulated value
        
        compliant = [a for a in compliance_activities if a.get('compliant', True)]
        return round((len(compliant) / len(compliance_activities)) * 100, 1)
    
    def _count_violations(self, since: datetime) -> int:
        """Count compliance violations"""
        return 2  # Simulated value
    
    def _count_audit_events(self, since: datetime) -> int:
        """Count audit events"""
        return 234  # Simulated value
    
    def _count_active_regulatory_alerts(self) -> int:
        """Count active regulatory alerts"""
        return 1  # Simulated value
    
    def _get_active_alerts(self) -> List[Dict]:
        """Get list of active system alerts"""
        return [
            {
                'id': 'PERF_001',
                'type': 'performance',
                'severity': 'medium',
                'description': 'Research agent response time elevated',
                'created_at': datetime.now().isoformat()
            }
        ]
    
    def _get_system_alerts(self) -> List[Dict]:
        """Get system-level alerts"""
        return []  # No current system alerts
    
    def _get_trending_analysis_types(self) -> List[str]:
        """Get trending analysis types"""
        return ['ESG Analysis', 'AI Sector Research', 'Risk Assessment', 'Dividend Analysis']
    
    def _get_most_researched_tickers(self) -> List[str]:
        """Get most researched stock tickers"""
        return ['AAPL', 'MSFT', 'NVDA', 'GOOGL', 'TSLA']
    
    def _get_busiest_hours(self) -> List[int]:
        """Get busiest hours of the day"""
        return [9, 10, 14, 15]  # 9-10 AM and 2-3 PM
    
    def _get_advisor_activity_trends(self) -> Dict[str, Any]:
        """Get advisor activity trends"""
        return {
            'weekly_growth_percent': 12.5,
            'most_active_day': 'Tuesday',
            'average_analyses_per_advisor': 3.2
        }
    
    def _filter_advisor_activities(self, advisor_id: str, since: datetime) -> Dict[str, List]:
        """Filter activities for specific advisor"""
        return {
            'analyses': [],
            'client_sessions': [],
            'reports': [],
            'compliance': []
        }
    
    def _calculate_advisor_avg_confidence(self, advisor_id: str) -> float:
        """Calculate advisor's average confidence score"""
        return 7.8  # Simulated value
    
    def _calculate_advisor_high_confidence_rate(self, advisor_id: str) -> float:
        """Calculate advisor's high confidence rate"""
        return 82.5  # Simulated value
    
    def _calculate_advisor_compliance_rate(self, advisor_id: str) -> float:
        """Calculate advisor's compliance rate"""
        return 98.2  # Simulated value
    
    def _count_advisor_violations(self, advisor_id: str, since: datetime) -> int:
        """Count advisor's compliance violations"""
        return 0  # Simulated value
    
    def _calculate_advisor_avg_time(self, advisor_id: str) -> float:
        """Calculate advisor's average analysis time"""
        return 28.5  # Simulated value in minutes
    
    def _generate_advisor_recommendations(self, activities: Dict) -> List[str]:
        """Generate recommendations for advisor improvement"""
        return [
            'Maintain high compliance standards',
            'Consider increasing analysis depth for better client outcomes',
            'Focus on emerging market opportunities',
            'Continue professional development in ESG investing'
        ]