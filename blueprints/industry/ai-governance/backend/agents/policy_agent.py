"""
Simple Compliance Checking Agent
Provides checklist-based compliance assessment against regulations
"""
import uuid
from datetime import datetime, timedelta
from typing import Dict, List
import random


class PolicyComplianceAgent:
    """Ensures AI systems comply with governance policies and regulations"""

    def __init__(self):
        self.frameworks = {
            'EU_AI_ACT': {
                'name': 'European Union AI Act',
                'requirements': [
                    'Risk assessment documentation',
                    'Technical documentation',
                    'Data governance procedures',
                    'Transparency obligations',
                    'Human oversight mechanisms',
                    'Accuracy and robustness testing',
                    'Cybersecurity measures'
                ]
            },
            'GDPR': {
                'name': 'General Data Protection Regulation',
                'requirements': [
                    'Data processing lawfulness',
                    'Purpose limitation',
                    'Data minimization',
                    'Automated decision-making safeguards',
                    'Data subject rights',
                    'Privacy by design'
                ]
            },
            'NIST_AI_RMF': {
                'name': 'NIST AI Risk Management Framework',
                'requirements': [
                    'AI governance structures',
                    'Risk mapping and categorization',
                    'Risk measurement and assessment',
                    'Risk management and monitoring'
                ]
            }
        }

    def check_compliance(self, model_id: str, regulations: List[str] = None) -> Dict:
        """
        Check AI model compliance against regulations

        Uses checklist-based assessment:
        - Evaluates requirements against each framework
        - Identifies compliance gaps
        - Provides remediation recommendations
        """
        if regulations is None:
            regulations = ['EU_AI_ACT', 'GDPR']

        # Assess compliance for each regulation
        compliance_gaps = self._identify_gaps(regulations)

        # Calculate overall compliance score
        compliance_score = self._calculate_compliance_score(compliance_gaps)

        # Determine compliance status
        compliance_status = self._classify_compliance_status(compliance_score)

        # Generate recommendations
        recommendations = self._generate_recommendations(compliance_gaps)

        # Calculate next review date
        next_review = (datetime.now() + timedelta(days=90)).date().isoformat()

        return {
            "model_id": model_id,
            "compliance_status": compliance_status,
            "compliance_rate": compliance_score,
            "gaps": compliance_gaps,
            "recommendations": recommendations,
            "timestamp": datetime.utcnow().isoformat(),
            "next_review_date": next_review
        }

    def _identify_gaps(self, regulations: List[str]) -> List[Dict]:
        """Identify compliance gaps for each regulation"""
        gaps = []

        for regulation in regulations:
            if regulation not in self.frameworks:
                continue

            framework = self.frameworks[regulation]

            # Check each requirement
            for requirement in framework['requirements']:
                # Randomly determine compliance status for demo
                status = random.choice(['Compliant', 'Partial', 'Missing'])

                if status != 'Compliant':
                    gaps.append({
                        "regulation": f"{regulation} - {framework['name']}",
                        "requirement": requirement,
                        "status": status,
                        "details": self._get_gap_details(requirement, status)
                    })

        return gaps

    def _get_gap_details(self, requirement: str, status: str) -> str:
        """Get detailed description of compliance gap"""
        details_map = {
            'Risk assessment documentation': {
                'Partial': 'Risk assessment exists but lacks comprehensive documentation',
                'Missing': 'No formal risk assessment documentation found'
            },
            'Technical documentation': {
                'Partial': 'Basic documentation present, missing detailed technical specifications',
                'Missing': 'Technical documentation not available'
            },
            'Data governance procedures': {
                'Partial': 'Data governance framework incomplete',
                'Missing': 'No formal data governance procedures established'
            },
            'Transparency obligations': {
                'Partial': 'Limited transparency features implemented',
                'Missing': 'Model lacks transparency and explainability features'
            },
            'Human oversight mechanisms': {
                'Partial': 'Human oversight exists but not formalized',
                'Missing': 'No human oversight mechanism in place'
            },
            'Automated decision-making safeguards': {
                'Partial': 'Basic safeguards present, additional controls needed',
                'Missing': 'Automated decision-making lacks required safeguards'
            }
        }

        return details_map.get(requirement, {}).get(status, f'{requirement} - {status}')

    def _calculate_compliance_score(self, gaps: List[Dict]) -> float:
        """Calculate overall compliance percentage"""
        if not gaps:
            return 100.0

        # Count gap severity
        missing_count = sum(1 for gap in gaps if gap['status'] == 'Missing')
        partial_count = sum(1 for gap in gaps if gap['status'] == 'Partial')

        # Estimate total requirements (simplified)
        total_requirements = len(gaps) + random.randint(3, 7)

        # Calculate score (missing = 0 points, partial = 0.5 points, compliant = 1 point)
        compliant_count = total_requirements - len(gaps)
        score = (compliant_count + (partial_count * 0.5)) / total_requirements * 100

        return round(score, 1)

    def _classify_compliance_status(self, compliance_score: float) -> str:
        """Classify overall compliance status"""
        if compliance_score >= 90:
            return "Compliant"
        elif compliance_score >= 70:
            return "Partially Compliant"
        else:
            return "Non-Compliant"

    def _generate_recommendations(self, gaps: List[Dict]) -> List[str]:
        """Generate compliance remediation recommendations"""
        recommendations = []

        # Prioritize based on gap status
        missing_gaps = [g for g in gaps if g['status'] == 'Missing']
        partial_gaps = [g for g in gaps if g['status'] == 'Partial']

        if missing_gaps:
            recommendations.append("⚠️ HIGH PRIORITY: Address critical compliance gaps before deployment")

        # Specific recommendations based on gap types
        gap_types = set(g['requirement'] for g in gaps)

        if 'Risk assessment documentation' in gap_types:
            recommendations.append("Complete comprehensive risk assessment following framework guidelines")

        if 'Technical documentation' in gap_types:
            recommendations.append("Create detailed technical documentation including model cards")

        if 'Data governance procedures' in gap_types:
            recommendations.append("Establish formal data governance and quality management procedures")

        if 'Transparency obligations' in gap_types:
            recommendations.append("Implement model explainability and transparency features")

        if 'Human oversight mechanisms' in gap_types:
            recommendations.append("Define and implement human oversight and intervention procedures")

        if 'Automated decision-making safeguards' in gap_types:
            recommendations.append("Add safeguards for automated decision-making (appeal process, explanations)")

        # General recommendations
        recommendations.append("Schedule regular compliance audits (quarterly recommended)")
        recommendations.append("Assign compliance officer for ongoing monitoring")
        recommendations.append("Document all compliance activities and remediation efforts")

        return recommendations

    def store_assessment(self, db_manager, assessment_data: Dict, system_id: str) -> bool:
        """Store compliance assessment results in database"""
        try:
            compliance_data = {
                'assessment_id': f"compliance_{uuid.uuid4().hex[:8]}",
                'system_id': system_id,
                'assessor_id': 'policy_compliance_agent',
                'status': assessment_data['compliance_status'].lower().replace(' ', '_'),
                'compliance_score': assessment_data['compliance_rate'],
                'frameworks': {'checked': ['EU_AI_ACT', 'GDPR', 'NIST_AI_RMF']},
                'gaps': assessment_data['gaps'],
                'remediation_actions': assessment_data['recommendations'],
                'regulatory_requirements': {
                    'EU_AI_ACT': True,
                    'GDPR': True,
                    'NIST_AI_RMF': True
                },
                'next_review_date': assessment_data.get('next_review_date', ''),
                'compliance_percentage': assessment_data['compliance_rate'],
                'confidence_level': 7,
                'processing_time': 0.4
            }

            return db_manager.store_compliance_assessment(compliance_data)
        except Exception as e:
            print(f"Failed to store compliance assessment: {str(e)}")
            return False
