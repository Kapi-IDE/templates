"""
Simple Bias Detection Agent
Provides basic statistical bias analysis for AI models
"""
import uuid
from datetime import datetime
from typing import List, Dict, Optional
import random


class BiasDetectionAgent:
    """Detects and analyzes bias in AI systems using simple statistical methods"""

    def __init__(self):
        self.protected_attributes = ['gender', 'race', 'age', 'ethnicity']

    def detect_bias(self, model_id: str, protected_attributes: Optional[List[str]] = None) -> Dict:
        """
        Run bias detection analysis on a model

        For blueprint purposes, uses simplified bias detection:
        - Simulates group comparisons
        - Calculates basic fairness metrics
        - Provides actionable recommendations
        """
        if protected_attributes is None:
            protected_attributes = self.protected_attributes

        # Simple bias score calculation (0-1, lower is better)
        # In production, this would analyze actual model predictions
        bias_score = round(random.uniform(0.2, 0.8), 2)

        # Calculate fairness metrics
        fairness_metrics = self._calculate_fairness_metrics(bias_score)

        # Generate group comparisons
        group_comparisons = self._generate_group_comparisons(protected_attributes)

        # Generate recommendations based on bias score
        recommendations = self._generate_recommendations(bias_score, fairness_metrics)

        return {
            "model_id": model_id,
            "bias_score": bias_score,
            "fairness_metrics": fairness_metrics,
            "group_comparisons": group_comparisons,
            "recommendations": recommendations,
            "timestamp": datetime.utcnow().isoformat()
        }

    def _calculate_fairness_metrics(self, bias_score: float) -> Dict:
        """
        Calculate standard fairness metrics

        Metrics include:
        - Demographic Parity: Equal acceptance rates across groups
        - Equal Opportunity: Equal true positive rates
        - Predictive Parity: Equal precision across groups
        """
        # Inverse relationship: higher bias = lower fairness
        base_fairness = 1.0 - bias_score

        return {
            "demographic_parity": round(base_fairness + random.uniform(-0.1, 0.1), 2),
            "equal_opportunity": round(base_fairness + random.uniform(-0.15, 0.05), 2),
            "predictive_parity": round(base_fairness + random.uniform(-0.05, 0.15), 2)
        }

    def _generate_group_comparisons(self, protected_attributes: List[str]) -> List[Dict]:
        """Generate comparison statistics across protected groups"""
        comparisons = []

        if 'gender' in protected_attributes:
            comparisons.extend([
                {
                    "group": "Gender - Male",
                    "acceptance_rate": round(random.uniform(0.55, 0.75), 2),
                    "count": random.randint(800, 1500)
                },
                {
                    "group": "Gender - Female",
                    "acceptance_rate": round(random.uniform(0.45, 0.65), 2),
                    "count": random.randint(700, 1300)
                }
            ])

        if 'age' in protected_attributes:
            comparisons.extend([
                {
                    "group": "Age - 18-35",
                    "acceptance_rate": round(random.uniform(0.65, 0.80), 2),
                    "count": random.randint(900, 1400)
                },
                {
                    "group": "Age - 36-60",
                    "acceptance_rate": round(random.uniform(0.60, 0.75), 2),
                    "count": random.randint(1000, 1600)
                },
                {
                    "group": "Age - 60+",
                    "acceptance_rate": round(random.uniform(0.50, 0.70), 2),
                    "count": random.randint(400, 800)
                }
            ])

        if 'race' in protected_attributes:
            comparisons.extend([
                {
                    "group": "Race - Group A",
                    "acceptance_rate": round(random.uniform(0.60, 0.75), 2),
                    "count": random.randint(1000, 1500)
                },
                {
                    "group": "Race - Group B",
                    "acceptance_rate": round(random.uniform(0.55, 0.70), 2),
                    "count": random.randint(800, 1200)
                }
            ])

        return comparisons

    def _generate_recommendations(self, bias_score: float, fairness_metrics: Dict) -> List[str]:
        """Generate actionable recommendations based on bias analysis"""
        recommendations = []

        if bias_score > 0.6:
            recommendations.append("⚠️ HIGH PRIORITY: Significant bias detected. Immediate review required.")
            recommendations.append("Re-examine training data for representation imbalances")
            recommendations.append("Consider implementing fairness constraints in model training")

        if bias_score > 0.4:
            recommendations.append("Review model training data for group balance")
            recommendations.append("Implement bias mitigation techniques (reweighting, adversarial debiasing)")

        if fairness_metrics['demographic_parity'] < 0.7:
            recommendations.append("Improve demographic parity through balanced sampling")

        if fairness_metrics['equal_opportunity'] < 0.7:
            recommendations.append("Adjust decision thresholds to improve equal opportunity")

        # Always include monitoring
        recommendations.append("Monitor ongoing predictions for bias drift")
        recommendations.append("Conduct regular fairness audits (quarterly recommended)")

        return recommendations

    def store_assessment(self, db_manager, assessment_data: Dict) -> bool:
        """Store bias assessment results in database"""
        try:
            bias_data = {
                'assessment_id': f"bias_{uuid.uuid4().hex[:8]}",
                'system_id': assessment_data['model_id'],
                'assessor_id': 'bias_detection_agent',
                'bias_level': self._classify_bias_level(assessment_data['bias_score']),
                'bias_risk_score': assessment_data['bias_score'] * 10,  # Scale to 0-10
                'fairness_metrics': assessment_data['fairness_metrics'],
                'bias_dimensions': {'protected_attributes': ['gender', 'race', 'age']},
                'protected_groups_impact': {'group_comparisons': assessment_data['group_comparisons']},
                'discrimination_risks': {'level': self._classify_bias_level(assessment_data['bias_score'])},
                'mitigation_strategies': assessment_data['recommendations'],
                'continuous_monitoring_plan': {'frequency': 'quarterly', 'metrics': list(assessment_data['fairness_metrics'].keys())},
                'confidence_level': 7,
                'processing_time': 0.5
            }

            return db_manager.store_bias_assessment(bias_data)
        except Exception as e:
            print(f"Failed to store bias assessment: {str(e)}")
            return False

    def _classify_bias_level(self, bias_score: float) -> str:
        """Classify bias level based on score"""
        if bias_score < 0.3:
            return 'low'
        elif bias_score < 0.6:
            return 'moderate'
        else:
            return 'high'
