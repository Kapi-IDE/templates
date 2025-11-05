#!/usr/bin/env python3
"""Financial base agent leveraging reusable components from KAPI framework."""

from __future__ import annotations

import logging
import math
import sys
from pathlib import Path
from typing import Any, Dict, List, Optional

# Add components directory to path for imports
templates_dir = Path(__file__).parents[5]  # Get to templates/
components_path = templates_dir / "components" / "backend"
if str(components_path) not in sys.path:
    sys.path.insert(0, str(components_path))

from agent_framework.agent.base import AgentFoundation

logger = logging.getLogger(__name__)


class FinancialBaseAgent(AgentFoundation):
    """Extends AgentFoundation with financial analysis capabilities.

    Provides specialized methods for investment analysis, risk assessment,
    regulatory compliance, and financial metrics calculation.
    """

    # Override BASE_PROMPT with financial-specific guidelines
    BASE_PROMPT = """
You are a professional financial AI assistant specializing in investment research and analysis.

IMPORTANT FINANCIAL GUIDELINES:
- You are NOT a replacement for professional financial advice
- Always include appropriate risk disclosures and disclaimers
- Base recommendations on data analysis and established financial principles
- Consider client suitability and risk tolerance in all recommendations
- Maintain objectivity and avoid conflicts of interest
- Use only factual, verifiable financial data in analysis
- Always disclose the limitations of your analysis

REGULATORY COMPLIANCE:
- All recommendations must be suitable for the client's risk profile
- Include required disclosures for investment advice
- Maintain detailed audit trails of all investment recommendations
- Follow SOC2 security standards for client data protection
- Ensure FINRA, SEC, and other regulatory compliance

FINANCIAL ANALYSIS STANDARDS:
- Use established financial metrics and ratios
- Consider both quantitative and qualitative factors
- Analyze risk-adjusted returns, not just absolute returns
- Account for market conditions, economic indicators, and sector trends
- Provide transparent reasoning for all investment conclusions
- Include stress testing and scenario analysis where appropriate

DATA SOURCES AND ACCURACY:
- Cite all data sources used in analysis
- Verify data accuracy and timeliness
- Use multiple data points to corroborate findings
- Acknowledge data limitations and uncertainties
- Update analysis based on new information
"""

    def __init__(
        self,
        knowledge_store: Any,
        financial_db: Any,
        agent_type: str = "financial_base",
        risk_free_rate: float = 0.045,
        market_return: float = 0.10,
    ):
        """Initialize financial base agent with required dependencies.

        Args:
            knowledge_store: Vector store for financial research/knowledge
            financial_db: Database for client data and audit logs
            agent_type: Identifier for this agent type
            risk_free_rate: Current risk-free rate (default 4.5%)
            market_return: Expected market return (default 10%)
        """
        super().__init__(
            knowledge_store=knowledge_store,
            data_store=financial_db,
            agent_type=agent_type,
        )

        # Keep backward compatibility
        self.financial_db = financial_db

        # Financial analysis constants
        self.RISK_FREE_RATE = risk_free_rate
        self.MARKET_RETURN = market_return

        logger.info("%s financial agent initialized", agent_type.title())

    def fallback_response(self) -> str:
        """Financial-specific fallback message with regulatory disclaimer."""
        return (
            "I apologize, but I'm experiencing technical difficulties with the financial analysis system. "
            "Please consult with a qualified financial advisor for investment guidance. "
            "For urgent matters, please contact your advisor directly."
        )

    # ====================================================================
    # Financial-Specific Utility Methods
    # ====================================================================

    def calculate_sharpe_ratio(
        self, returns: List[float], risk_free_rate: Optional[float] = None
    ) -> float:
        """Calculate Sharpe ratio for risk-adjusted return analysis.

        Args:
            returns: List of historical returns
            risk_free_rate: Optional override for risk-free rate

        Returns:
            Sharpe ratio (higher is better)
        """
        try:
            if not returns or len(returns) < 2:
                return 0.0

            rfr = risk_free_rate if risk_free_rate is not None else self.RISK_FREE_RATE

            # Calculate mean return and standard deviation
            mean_return = sum(returns) / len(returns)
            variance = sum((r - mean_return) ** 2 for r in returns) / len(returns)
            std_deviation = math.sqrt(variance)

            if std_deviation == 0:
                return 0.0

            # Sharpe ratio = (Mean return - Risk-free rate) / Standard deviation
            sharpe_ratio = (mean_return - rfr) / std_deviation
            return round(sharpe_ratio, 3)

        except Exception as exc:
            logger.error("Failed to calculate Sharpe ratio: %s", exc)
            return 0.0

    def calculate_portfolio_beta(
        self, holdings: List[Dict[str, Any]], market_data: Optional[Dict] = None
    ) -> float:
        """Calculate portfolio beta (systematic risk measure).

        Args:
            holdings: List of holdings with 'value' and 'beta' fields
            market_data: Optional market data for beta calculation

        Returns:
            Portfolio beta (1.0 = market average risk)
        """
        try:
            if not holdings:
                return 1.0

            total_value = sum(holding.get("value", 0) for holding in holdings)
            if total_value == 0:
                return 1.0

            weighted_beta = 0.0
            for holding in holdings:
                weight = holding.get("value", 0) / total_value
                beta = holding.get("beta", 1.0)  # Default to market beta
                weighted_beta += weight * beta

            return round(weighted_beta, 3)

        except Exception as exc:
            logger.error("Failed to calculate portfolio beta: %s", exc)
            return 1.0

    def assess_investment_suitability(
        self, investment_data: Dict[str, Any], client_profile: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Assess if investment is suitable for client profile (regulatory requirement).

        Args:
            investment_data: Investment details with risk_score, etc.
            client_profile: Client profile with risk_tolerance, etc.

        Returns:
            Suitability assessment with reasoning and warnings
        """
        try:
            risk_score = investment_data.get("risk_score", 5)
            client_risk_tolerance = client_profile.get("risk_tolerance", "moderate")

            # Map client risk tolerance to numeric scale
            risk_tolerance_map = {
                "conservative": 3,
                "moderate": 5,
                "aggressive": 8,
            }

            client_risk_score = risk_tolerance_map.get(client_risk_tolerance, 5)

            # Investment is suitable if its risk is within client's tolerance
            suitable = risk_score <= client_risk_score + 1  # Allow slight tolerance

            # Generate suitability reasoning
            if suitable:
                reasoning = (
                    f"Investment risk level ({risk_score}/10) aligns with "
                    f"client's {client_risk_tolerance} risk profile."
                )
            else:
                reasoning = (
                    f"Investment risk level ({risk_score}/10) exceeds "
                    f"client's {client_risk_tolerance} risk tolerance."
                )

            # Check additional suitability factors
            warnings = []
            if investment_data.get("liquidity_risk", False):
                warnings.append("This investment may have limited liquidity")
            if investment_data.get("complexity_high", False):
                warnings.append("This is a complex investment product")

            return {
                "suitable": suitable,
                "suitability_score": min(client_risk_score, risk_score),
                "reasoning": reasoning,
                "warnings": warnings,
                "client_risk_tolerance": client_risk_tolerance,
                "investment_risk_level": risk_score,
            }

        except Exception as exc:
            logger.error("Failed to assess investment suitability: %s", exc)
            return {
                "suitable": False,
                "reasoning": "Unable to assess suitability due to insufficient data",
                "warnings": ["Suitability assessment failed - manual review required"],
            }

    def get_regulatory_disclaimer(self) -> str:
        """Standard regulatory disclaimer for investment analysis."""
        return (
            "This analysis is provided for informational purposes only and should not be "
            "construed as investment advice. Past performance does not guarantee future results. "
            "All investments carry risk of loss. Please consult with a qualified financial "
            "advisor before making investment decisions. This analysis was generated by AI "
            "and should be reviewed by a licensed professional."
        )

    def log_financial_interaction(
        self,
        advisor_id: str,
        client_id: str,
        interaction_type: str,
        input_data: Dict[str, Any],
        output_data: Dict[str, Any],
        compliance_status: Optional[Dict] = None,
        processing_time: Optional[float] = None,
    ) -> None:
        """Log financial agent interaction for SOC2/FINRA compliance.

        Args:
            advisor_id: Identifier for the advisor
            client_id: Identifier for the client
            interaction_type: Type of interaction (e.g., 'investment_analysis')
            input_data: Input data dictionary
            output_data: Output data dictionary
            compliance_status: Optional compliance validation results
            processing_time: Optional processing time in seconds
        """
        try:
            # Use base logging with additional financial context
            enhanced_input = {
                **input_data,
                "advisor_id": advisor_id,
                "compliance_status": compliance_status or {},
            }

            enhanced_output = {
                **output_data,
                "regulatory_disclaimer": self.get_regulatory_disclaimer(),
            }

            # Call base log_interaction with mapped parameters
            self.log_interaction(
                user_id=client_id,
                interaction_type=interaction_type,
                input_data=enhanced_input,
                output_data=enhanced_output,
                processing_time=processing_time,
            )

            # Additional financial-specific logging if database supports it
            if hasattr(self.financial_db, "store_investment_recommendation_audit"):
                self.financial_db.store_investment_recommendation_audit(
                    advisor_id=advisor_id,
                    client_id=client_id,
                    ticker=input_data.get("ticker", ""),
                    recommendation_data=output_data,
                    agent_reasoning={
                        "agent_type": self.agent_type,
                        "compliance_status": compliance_status,
                    },
                )

        except Exception as exc:
            logger.error("Failed to log financial interaction: %s", exc)

    def validate_financial_input(
        self, required_fields: List[str], data: Dict[str, Any]
    ) -> tuple[bool, List[str]]:
        """Validate financial analysis input data with domain-specific checks.

        Args:
            required_fields: List of required field names
            data: Input data dictionary

        Returns:
            Tuple of (is_valid, list_of_errors)
        """
        # Check required fields using base validation
        missing_fields = [
            field for field in required_fields if field not in data or not data[field]
        ]

        # Additional financial data validation
        financial_validations = []

        if "ticker" in data:
            ticker = data["ticker"].upper()
            if not ticker.isalpha() or len(ticker) > 5:
                financial_validations.append("Invalid ticker symbol format")

        if "amount" in data:
            try:
                amount = float(data["amount"])
                if amount <= 0:
                    financial_validations.append("Investment amount must be positive")
            except (ValueError, TypeError):
                financial_validations.append("Invalid investment amount")

        if "risk_tolerance" in data:
            valid_risk_levels = ["conservative", "moderate", "aggressive"]
            if data["risk_tolerance"].lower() not in valid_risk_levels:
                financial_validations.append("Invalid risk tolerance level")

        all_validation_errors = missing_fields + financial_validations

        if all_validation_errors:
            logger.error("Financial input validation failed: %s", all_validation_errors)
            return False, all_validation_errors

        return True, []

    def health_check(self) -> bool:
        """Check if financial agent is functioning properly."""
        try:
            # Test base agent health
            if not super().health_check():
                return False

            # Test basic financial calculation
            test_sharpe = self.calculate_sharpe_ratio([0.08, 0.12, 0.06, 0.10])
            if test_sharpe == 0:
                logger.warning("Financial calculation test produced unexpected result")

            return True

        except Exception as exc:
            logger.error("Financial agent health check failed: %s", exc)
            return False

    def agent_info(self) -> Dict[str, Any]:
        """Get information about this financial agent."""
        base_info = super().agent_info()
        base_info.update({
            "capabilities": [
                "investment_analysis",
                "risk_assessment",
                "financial_metrics_calculation",
                "suitability_analysis",
                "regulatory_compliance",
            ],
            "regulatory_compliance": ["SOC2", "FINRA", "SEC"],
            "risk_free_rate": self.RISK_FREE_RATE,
            "expected_market_return": self.MARKET_RETURN,
        })
        return base_info
