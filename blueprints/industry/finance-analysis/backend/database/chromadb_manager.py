#!/usr/bin/env python3
"""
Financial Knowledge Store using ChromaDB
Manages financial documents, research reports, and investment knowledge for RAG system
"""

import chromadb
from chromadb.config import Settings
import logging
import json
import os
from typing import List, Dict, Any, Optional
from datetime import datetime
import uuid

logger = logging.getLogger(__name__)

class FinancialKnowledgeStore:
    """
    Manages financial knowledge base using ChromaDB for RAG-powered investment analysis
    Stores financial documents, analyst reports, economic research, and market intelligence
    """
    
    def __init__(self, persist_directory: str = "./financial_knowledge_db"):
        """Initialize ChromaDB for financial knowledge storage"""
        try:
            # Initialize ChromaDB client with persistence
            self.client = chromadb.PersistentClient(
                path=persist_directory,
                settings=Settings(
                    anonymized_telemetry=False,
                    allow_reset=True
                )
            )
            
            # Create collections for different types of financial knowledge
            self._initialize_collections()
            self._populate_sample_knowledge()
            
            logger.info("Financial Knowledge Store initialized successfully")
            
        except Exception as e:
            logger.error(f"Failed to initialize Financial Knowledge Store: {str(e)}")
            raise
    
    def _initialize_collections(self):
        """Initialize ChromaDB collections for different financial knowledge types"""
        try:
            # Collection for company financial documents and filings
            self.company_docs = self.client.get_or_create_collection(
                name="company_financial_docs",
                metadata={
                    "description": "Company financial documents, SEC filings, earnings reports",
                    "created_at": datetime.now().isoformat()
                }
            )
            
            # Collection for analyst reports and research
            self.analyst_reports = self.client.get_or_create_collection(
                name="analyst_reports",
                metadata={
                    "description": "Investment analyst reports and research recommendations",
                    "created_at": datetime.now().isoformat()
                }
            )
            
            # Collection for economic research and market intelligence
            self.market_intelligence = self.client.get_or_create_collection(
                name="market_intelligence",
                metadata={
                    "description": "Economic research, market trends, and sector analysis",
                    "created_at": datetime.now().isoformat()
                }
            )
            
            # Collection for investment strategies and methodologies
            self.investment_strategies = self.client.get_or_create_collection(
                name="investment_strategies",
                metadata={
                    "description": "Investment strategies, portfolio theory, and financial methodologies",
                    "created_at": datetime.now().isoformat()
                }
            )
            
            # Collection for regulatory and compliance knowledge
            self.compliance_knowledge = self.client.get_or_create_collection(
                name="compliance_knowledge",
                metadata={
                    "description": "Financial regulations, compliance requirements, and risk management",
                    "created_at": datetime.now().isoformat()
                }
            )
            
            logger.info("Financial knowledge collections initialized")
            
        except Exception as e:
            logger.error(f"Failed to initialize knowledge collections: {str(e)}")
            raise
    
    def _populate_sample_knowledge(self):
        """Populate knowledge base with sample financial documents"""
        try:
            # Check if sample data already exists
            if self.company_docs.count() > 0:
                return  # Sample data already exists
            
            # Sample company financial documents
            company_documents = [
                {
                    "id": "aapl_10k_2023",
                    "content": "Apple Inc. reported record revenue of $394.3 billion in fiscal 2023, driven by strong iPhone sales and services growth. The company maintains a strong balance sheet with $162.1 billion in cash and marketable securities. Key risks include supply chain dependencies, regulatory challenges in key markets, and intense competition in the smartphone market. Apple's services segment, including the App Store, iCloud, and Apple Music, generated $85.2 billion in revenue, representing 21.6% of total revenue. The company returned $99.9 billion to shareholders through dividends and share repurchases.",
                    "metadata": {
                        "ticker": "AAPL",
                        "company": "Apple Inc.",
                        "document_type": "10-K",
                        "fiscal_year": "2023",
                        "sector": "Technology",
                        "filing_date": "2023-11-02"
                    }
                },
                {
                    "id": "msft_earnings_q4_2023",
                    "content": "Microsoft Corporation delivered strong Q4 2023 results with revenue of $56.2 billion, up 8% year-over-year. Azure and other cloud services revenue grew 26%, driven by AI services adoption. Productivity and Business Processes segment revenue was $18.3 billion, with Microsoft 365 commercial revenue growing 12%. More Personal Computing revenue decreased 4% to $13.9 billion due to PC market weakness. Operating income increased 15% to $24.3 billion, with operating margin expanding to 43%. The company's AI initiatives, including Copilot integration across products, position it well for future growth.",
                    "metadata": {
                        "ticker": "MSFT",
                        "company": "Microsoft Corporation",
                        "document_type": "Earnings Report",
                        "quarter": "Q4 2023",
                        "sector": "Technology",
                        "release_date": "2023-07-25"
                    }
                },
                {
                    "id": "jpm_annual_report_2023",
                    "content": "JPMorgan Chase reported net income of $49.6 billion for 2023, demonstrating the strength of its diversified business model. The firm's CET1 ratio remained strong at 15.0%, well above regulatory minimums. Investment banking revenue faced headwinds with fees down 6% due to market conditions, while trading revenue increased 7%. The Consumer & Community Banking division generated $5.3 billion in net income despite higher credit costs. Net charge-offs increased to $8.1 billion, reflecting normalization from historically low levels. The bank maintained a fortress balance sheet with $3.4 trillion in assets.",
                    "metadata": {
                        "ticker": "JPM",
                        "company": "JPMorgan Chase & Co.",
                        "document_type": "Annual Report",
                        "year": "2023",
                        "sector": "Financial Services",
                        "release_date": "2024-01-12"
                    }
                }
            ]
            
            # Add company documents
            for doc in company_documents:
                self.company_docs.add(
                    documents=[doc["content"]],
                    metadatas=[doc["metadata"]],
                    ids=[doc["id"]]
                )
            
            # Sample analyst reports
            analyst_reports = [
                {
                    "id": "aapl_goldman_buy_2024",
                    "content": "We maintain our BUY rating on Apple (AAPL) with a $200 price target. Key investment highlights include: (1) iPhone 15 cycle showing resilient demand despite macro headwinds, (2) Services business provides recurring revenue stream with 70%+ gross margins, (3) AI capabilities integration expected to drive next upgrade cycle, (4) Strong capital allocation with $110B+ returned to shareholders annually. Key risks include China regulatory concerns and smartphone market saturation. Valuation appears reasonable at 25x forward P/E given growth prospects.",
                    "metadata": {
                        "ticker": "AAPL",
                        "analyst_firm": "Goldman Sachs",
                        "rating": "BUY",
                        "price_target": 200,
                        "analyst": "David Vogt",
                        "publish_date": "2024-01-15"
                    }
                },
                {
                    "id": "tsla_morgan_stanley_overweight",
                    "content": "Tesla (TSLA) remains our top pick in the EV space with an OVERWEIGHT rating and $300 price target. Catalysts include: (1) Model Y refresh cycle driving volume growth, (2) Full Self-Driving (FSD) monetization opportunity worth $100+ per share, (3) Energy storage business inflection with 40%+ growth expected, (4) Manufacturing scale advantages over EV competitors. Near-term headwinds include EV tax credit changes and increased competition. Long-term, we see Tesla as an AI/robotics company trading at EV multiples.",
                    "metadata": {
                        "ticker": "TSLA",
                        "analyst_firm": "Morgan Stanley",
                        "rating": "OVERWEIGHT",
                        "price_target": 300,
                        "analyst": "Adam Jonas",
                        "publish_date": "2024-02-20"
                    }
                }
            ]
            
            # Add analyst reports
            for report in analyst_reports:
                self.analyst_reports.add(
                    documents=[report["content"]],
                    metadatas=[report["metadata"]],
                    ids=[report["id"]]
                )
            
            # Sample market intelligence
            market_intelligence_docs = [
                {
                    "id": "fed_rate_outlook_2024",
                    "content": "The Federal Reserve is expected to maintain a restrictive monetary policy stance through mid-2024, with the federal funds rate likely remaining in the 5.00-5.50% range. Key factors influencing policy decisions include: (1) Core PCE inflation trending toward 2% target but remaining elevated, (2) Labor market showing signs of cooling with unemployment rising to 4.2%, (3) Financial conditions tightening through higher long-term rates. We expect 75-100 basis points of rate cuts in H2 2024, contingent on continued disinflation progress. This environment favors high-quality dividend stocks and shorter-duration fixed income.",
                    "metadata": {
                        "topic": "Federal Reserve Policy",
                        "category": "Monetary Policy",
                        "source": "Fed Research Division",
                        "publish_date": "2024-03-15",
                        "relevance_period": "2024"
                    }
                },
                {
                    "id": "ai_sector_outlook_2024",
                    "content": "The artificial intelligence sector continues to drive significant market returns, with AI-related stocks generating 45%+ returns in 2023. Key investment themes include: (1) Infrastructure plays (NVDA, AMD) benefiting from GPU demand, (2) Software integration opportunities (MSFT, GOOGL) monetizing AI capabilities, (3) Emerging applications in healthcare, finance, and autonomous vehicles. Valuations remain elevated with AI leaders trading at 40-50x forward earnings. Key risks include regulatory oversight, competition from open-source models, and potential hardware supply constraints. We favor companies with sustainable competitive moats and clear monetization strategies.",
                    "metadata": {
                        "topic": "Artificial Intelligence",
                        "category": "Sector Analysis",
                        "source": "Technology Research Team",
                        "publish_date": "2024-01-08",
                        "relevance_period": "2024-2025"
                    }
                }
            ]
            
            # Add market intelligence
            for intel in market_intelligence_docs:
                self.market_intelligence.add(
                    documents=[intel["content"]],
                    metadatas=[intel["metadata"]],
                    ids=[intel["id"]]
                )
            
            # Sample investment strategies
            strategy_docs = [
                {
                    "id": "dividend_growth_strategy",
                    "content": "The Dividend Growth Investment Strategy focuses on companies with sustainable competitive advantages that consistently increase dividend payments over time. Key screening criteria include: (1) Dividend growth rate of 7%+ annually over 10 years, (2) Payout ratio below 60% for sustainability, (3) Free cash flow coverage ratio above 1.2x, (4) Strong balance sheet with debt-to-equity below 0.5x. This strategy typically outperforms during market volatility and provides inflation protection. Suitable for income-focused investors with moderate risk tolerance. Expected returns: 8-10% annually over 10+ year periods.",
                    "metadata": {
                        "strategy_type": "Dividend Growth",
                        "risk_level": "Moderate",
                        "time_horizon": "Long-term",
                        "suitable_for": "Income investors",
                        "expected_return": "8-10%"
                    }
                },
                {
                    "id": "value_investing_framework",
                    "content": "Value investing seeks to identify undervalued securities trading below intrinsic value. Core principles include: (1) Focus on business fundamentals over market sentiment, (2) Margin of safety - buy at significant discount to fair value, (3) Quality management and sustainable competitive advantages, (4) Patient capital - hold until value realization. Key metrics: P/E < 15x, P/B < 2x, debt/equity < 0.4x, ROE > 15%. Works best in inefficient markets and during economic uncertainty. Requires thorough fundamental analysis and contrarian mindset. Historical returns: 10-12% annually over 20+ year periods.",
                    "metadata": {
                        "strategy_type": "Value Investing",
                        "risk_level": "Moderate",
                        "time_horizon": "Long-term",
                        "suitable_for": "Patient investors",
                        "expected_return": "10-12%"
                    }
                }
            ]
            
            # Add investment strategies
            for strategy in strategy_docs:
                self.investment_strategies.add(
                    documents=[strategy["content"]],
                    metadatas=[strategy["metadata"]],
                    ids=[strategy["id"]]
                )
            
            # Sample compliance knowledge
            compliance_docs = [
                {
                    "id": "suitability_requirements",
                    "content": "FINRA Rule 2111 requires broker-dealers to have a reasonable basis to believe that a recommended transaction is suitable for a customer based on: (1) Customer's investment profile including age, financial situation, investment experience, investment objectives, risk tolerance, and liquidity needs, (2) Security's characteristics including liquidity, volatility, credit risk, and tax implications, (3) Investment strategy and concentration levels. Documentation requirements include maintaining records of customer profiles, rationale for recommendations, and periodic suitability reviews. Violations can result in regulatory sanctions, customer restitution, and reputational damage.",
                    "metadata": {
                        "regulation": "FINRA Rule 2111",
                        "category": "Suitability",
                        "compliance_area": "Customer Protection",
                        "severity": "High",
                        "last_updated": "2024-01-01"
                    }
                }
            ]
            
            # Add compliance knowledge
            for compliance in compliance_docs:
                self.compliance_knowledge.add(
                    documents=[compliance["content"]],
                    metadatas=[compliance["metadata"]],
                    ids=[compliance["id"]]
                )
            
            logger.info("Sample financial knowledge populated successfully")
            
        except Exception as e:
            logger.error(f"Failed to populate sample knowledge: {str(e)}")
    
    def search_company_knowledge(self, query: str, ticker: str = None, n_results: int = 5) -> List[Dict]:
        """Search company financial documents and filings"""
        try:
            where_clause = None
            if ticker:
                where_clause = {"ticker": ticker.upper()}
            
            results = self.company_docs.query(
                query_texts=[query],
                n_results=n_results,
                where=where_clause
            )
            
            return self._format_search_results(results, "company_documents")
            
        except Exception as e:
            logger.error(f"Failed to search company knowledge: {str(e)}")
            return []
    
    def search_analyst_reports(self, query: str, ticker: str = None, rating: str = None, n_results: int = 5) -> List[Dict]:
        """Search analyst reports and investment research"""
        try:
            where_clause = {}
            if ticker:
                where_clause["ticker"] = ticker.upper()
            if rating:
                where_clause["rating"] = rating.upper()
            
            where_clause = where_clause if where_clause else None
            
            results = self.analyst_reports.query(
                query_texts=[query],
                n_results=n_results,
                where=where_clause
            )
            
            return self._format_search_results(results, "analyst_reports")
            
        except Exception as e:
            logger.error(f"Failed to search analyst reports: {str(e)}")
            return []
    
    def search_market_intelligence(self, query: str, category: str = None, n_results: int = 5) -> List[Dict]:
        """Search market intelligence and economic research"""
        try:
            where_clause = None
            if category:
                where_clause = {"category": category}
            
            results = self.market_intelligence.query(
                query_texts=[query],
                n_results=n_results,
                where=where_clause
            )
            
            return self._format_search_results(results, "market_intelligence")
            
        except Exception as e:
            logger.error(f"Failed to search market intelligence: {str(e)}")
            return []
    
    def search_investment_strategies(self, query: str, risk_level: str = None, n_results: int = 3) -> List[Dict]:
        """Search investment strategies and methodologies"""
        try:
            where_clause = None
            if risk_level:
                where_clause = {"risk_level": risk_level.title()}
            
            results = self.investment_strategies.query(
                query_texts=[query],
                n_results=n_results,
                where=where_clause
            )
            
            return self._format_search_results(results, "investment_strategies")
            
        except Exception as e:
            logger.error(f"Failed to search investment strategies: {str(e)}")
            return []
    
    def search_compliance_knowledge(self, query: str, regulation: str = None, n_results: int = 3) -> List[Dict]:
        """Search regulatory and compliance knowledge"""
        try:
            where_clause = None
            if regulation:
                where_clause = {"regulation": regulation}
            
            results = self.compliance_knowledge.query(
                query_texts=[query],
                n_results=n_results,
                where=where_clause
            )
            
            return self._format_search_results(results, "compliance_knowledge")
            
        except Exception as e:
            logger.error(f"Failed to search compliance knowledge: {str(e)}")
            return []
    
    def comprehensive_search(self, query: str, context: Dict = None) -> Dict[str, List]:
        """Perform comprehensive search across all knowledge bases"""
        try:
            ticker = context.get('ticker') if context else None
            risk_level = context.get('risk_level') if context else None
            
            results = {
                'company_docs': self.search_company_knowledge(query, ticker=ticker, n_results=3),
                'analyst_reports': self.search_analyst_reports(query, ticker=ticker, n_results=3),
                'market_intelligence': self.search_market_intelligence(query, n_results=2),
                'investment_strategies': self.search_investment_strategies(query, risk_level=risk_level, n_results=2),
                'compliance': self.search_compliance_knowledge(query, n_results=1)
            }
            
            return results
            
        except Exception as e:
            logger.error(f"Failed to perform comprehensive search: {str(e)}")
            return {}
    
    def _format_search_results(self, results: Dict, source_type: str) -> List[Dict]:
        """Format ChromaDB search results for consistent output"""
        try:
            formatted_results = []
            
            if not results['documents'] or not results['documents'][0]:
                return formatted_results
            
            for i, doc in enumerate(results['documents'][0]):
                result = {
                    'id': results['ids'][0][i],
                    'content': doc,
                    'metadata': results['metadatas'][0][i],
                    'distance': results['distances'][0][i] if 'distances' in results else 0,
                    'source_type': source_type,
                    'relevance_score': 1 - (results['distances'][0][i] if 'distances' in results else 0)
                }
                formatted_results.append(result)
            
            return formatted_results
            
        except Exception as e:
            logger.error(f"Failed to format search results: {str(e)}")
            return []
    
    def add_financial_document(self, content: str, metadata: Dict, collection_type: str = "company_docs") -> bool:
        """Add new financial document to knowledge base"""
        try:
            document_id = f"{collection_type}_{uuid.uuid4().hex[:8]}_{int(datetime.now().timestamp())}"
            
            collection_map = {
                "company_docs": self.company_docs,
                "analyst_reports": self.analyst_reports,
                "market_intelligence": self.market_intelligence,
                "investment_strategies": self.investment_strategies,
                "compliance": self.compliance_knowledge
            }
            
            if collection_type not in collection_map:
                raise ValueError(f"Invalid collection type: {collection_type}")
            
            collection = collection_map[collection_type]
            collection.add(
                documents=[content],
                metadatas=[metadata],
                ids=[document_id]
            )
            
            logger.info(f"Financial document added to {collection_type}: {document_id}")
            return True
            
        except Exception as e:
            logger.error(f"Failed to add financial document: {str(e)}")
            return False
    
    def get_collection_stats(self) -> Dict[str, Any]:
        """Get statistics about knowledge base collections"""
        try:
            return {
                'company_docs': self.company_docs.count(),
                'analyst_reports': self.analyst_reports.count(),
                'market_intelligence': self.market_intelligence.count(),
                'investment_strategies': self.investment_strategies.count(),
                'compliance_knowledge': self.compliance_knowledge.count(),
                'total_documents': (
                    self.company_docs.count() + 
                    self.analyst_reports.count() + 
                    self.market_intelligence.count() + 
                    self.investment_strategies.count() + 
                    self.compliance_knowledge.count()
                ),
                'last_updated': datetime.now().isoformat()
            }
            
        except Exception as e:
            logger.error(f"Failed to get collection stats: {str(e)}")
            return {}
    
    def health_check(self) -> bool:
        """Check if knowledge store is functioning properly"""
        try:
            # Test basic search functionality
            test_results = self.company_docs.query(
                query_texts=["revenue growth"],
                n_results=1
            )
            
            return len(test_results['documents'][0]) > 0 if test_results['documents'] else False
            
        except Exception as e:
            logger.error(f"Knowledge store health check failed: {str(e)}")
            return False