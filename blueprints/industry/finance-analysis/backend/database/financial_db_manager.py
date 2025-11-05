#!/usr/bin/env python3
"""
Financial Data Manager for Investment Research Platform
Handles financial data, portfolios, market data, and compliance audit logs
"""

import sqlite3
import json
import logging
import os
from datetime import datetime, timedelta
from typing import List, Dict, Any, Optional
import uuid
from cryptography.fernet import Fernet

logger = logging.getLogger(__name__)

class FinancialDataManager:
    """
    Manages financial data and investment analysis in SQLite database
    Ensures SOC2 compliance with encryption and comprehensive audit logging
    """
    
    def __init__(self, db_path: str = "./financial_data.db"):
        """Initialize SQLite database and create financial tables"""
        self.db_path = db_path
        self.conn = sqlite3.connect(db_path, check_same_thread=False)
        self.conn.row_factory = sqlite3.Row  # Enable dict-like access
        
        # Initialize encryption for sensitive financial data
        self.encryption_key = os.getenv('ENCRYPTION_KEY')
        if not self.encryption_key:
            # Generate key for demo (DO NOT do this in production)
            self.encryption_key = Fernet.generate_key()
            logger.warning("Generated encryption key for demo - use proper key management in production")
        
        self.cipher = Fernet(self.encryption_key)
        
        self._create_financial_tables()
        self._populate_sample_financial_data()
        logger.info("Financial SQLite database initialized successfully")
    
    def _create_financial_tables(self):
        """Create database tables for financial data and analysis"""
        try:
            # Stocks master table
            self.conn.execute('''
                CREATE TABLE IF NOT EXISTS stocks (
                    ticker TEXT PRIMARY KEY,
                    company_name TEXT NOT NULL,
                    sector TEXT,
                    industry TEXT,
                    market_cap REAL,
                    pe_ratio REAL,
                    dividend_yield REAL,
                    beta REAL,
                    price_to_book REAL,
                    debt_to_equity REAL,
                    roe REAL,
                    profit_margin REAL,
                    description TEXT,
                    exchange TEXT,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            ''')
            
            # Market data table for historical prices and technical indicators
            self.conn.execute('''
                CREATE TABLE IF NOT EXISTS market_data (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    ticker TEXT NOT NULL,
                    date DATE NOT NULL,
                    open_price REAL,
                    high_price REAL,
                    low_price REAL,
                    close_price REAL,
                    volume INTEGER,
                    adjusted_close REAL,
                    rsi REAL,
                    moving_avg_50 REAL,
                    moving_avg_200 REAL,
                    bollinger_upper REAL,
                    bollinger_lower REAL,
                    macd REAL,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (ticker) REFERENCES stocks (ticker)
                )
            ''')
            
            # Client portfolios table
            self.conn.execute('''
                CREATE TABLE IF NOT EXISTS client_portfolios (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    client_id TEXT NOT NULL,
                    advisor_id TEXT NOT NULL,
                    portfolio_name TEXT,
                    encrypted_holdings TEXT NOT NULL,
                    total_value REAL,
                    cash_position REAL,
                    portfolio_beta REAL,
                    risk_score INTEGER,
                    last_rebalanced DATE,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    active BOOLEAN DEFAULT 1
                )
            ''')
            
            # Investment analysis table
            self.conn.execute('''
                CREATE TABLE IF NOT EXISTS investment_analysis (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    analysis_id TEXT UNIQUE NOT NULL,
                    advisor_id TEXT NOT NULL,
                    client_id TEXT,
                    ticker TEXT NOT NULL,
                    analysis_type TEXT,
                    encrypted_analysis_data TEXT NOT NULL,
                    risk_score INTEGER,
                    confidence_score INTEGER,
                    recommendation TEXT,
                    target_price REAL,
                    compliance_approved BOOLEAN DEFAULT 0,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (ticker) REFERENCES stocks (ticker)
                )
            ''')
            
            # Reports table for generated investment reports
            self.conn.execute('''
                CREATE TABLE IF NOT EXISTS investment_reports (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    report_id TEXT UNIQUE NOT NULL,
                    advisor_id TEXT NOT NULL,
                    client_id TEXT NOT NULL,
                    report_type TEXT NOT NULL,
                    encrypted_report_data TEXT NOT NULL,
                    compliance_validated BOOLEAN DEFAULT 0,
                    generated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    expires_at TIMESTAMP,
                    download_count INTEGER DEFAULT 0
                )
            ''')
            
            # Advisor sessions table
            self.conn.execute('''
                CREATE TABLE IF NOT EXISTS advisor_sessions (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    session_id TEXT UNIQUE NOT NULL,
                    advisor_id TEXT NOT NULL,
                    client_id TEXT,
                    session_token TEXT NOT NULL,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    expires_at TIMESTAMP NOT NULL,
                    active BOOLEAN DEFAULT 1,
                    ip_address TEXT,
                    user_agent TEXT
                )
            ''')
            
            # Financial audit log for SOC2 compliance
            self.conn.execute('''
                CREATE TABLE IF NOT EXISTS financial_audit_log (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    advisor_id TEXT,
                    client_id TEXT,
                    action TEXT NOT NULL,
                    ticker TEXT,
                    details TEXT,
                    compliance_data TEXT,
                    ip_address TEXT,
                    user_agent TEXT,
                    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    success BOOLEAN DEFAULT 1,
                    risk_level TEXT,
                    data_classification TEXT
                )
            ''')
            
            # Investment recommendations audit trail
            self.conn.execute('''
                CREATE TABLE IF NOT EXISTS investment_recommendations (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    advisor_id TEXT NOT NULL,
                    client_id TEXT NOT NULL,
                    ticker TEXT NOT NULL,
                    recommendation_type TEXT NOT NULL,
                    recommendation TEXT NOT NULL,
                    reasoning TEXT,
                    risk_assessment TEXT,
                    suitability_analysis TEXT,
                    target_price REAL,
                    stop_loss REAL,
                    time_horizon TEXT,
                    confidence_score INTEGER,
                    compliance_approved BOOLEAN DEFAULT 0,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    expires_at TIMESTAMP,
                    FOREIGN KEY (ticker) REFERENCES stocks (ticker)
                )
            ''')
            
            # Economic indicators table
            self.conn.execute('''
                CREATE TABLE IF NOT EXISTS economic_indicators (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    indicator_name TEXT NOT NULL,
                    date DATE NOT NULL,
                    value REAL NOT NULL,
                    unit TEXT,
                    frequency TEXT,
                    source TEXT,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            ''')
            
            # Create indexes for better query performance
            indexes = [
                'CREATE INDEX IF NOT EXISTS idx_market_data_ticker_date ON market_data(ticker, date)',
                'CREATE INDEX IF NOT EXISTS idx_portfolios_client ON client_portfolios(client_id)',
                'CREATE INDEX IF NOT EXISTS idx_analysis_advisor ON investment_analysis(advisor_id)',
                'CREATE INDEX IF NOT EXISTS idx_analysis_ticker ON investment_analysis(ticker)',
                'CREATE INDEX IF NOT EXISTS idx_audit_advisor ON financial_audit_log(advisor_id)',
                'CREATE INDEX IF NOT EXISTS idx_audit_client ON financial_audit_log(client_id)',
                'CREATE INDEX IF NOT EXISTS idx_audit_timestamp ON financial_audit_log(timestamp)',
                'CREATE INDEX IF NOT EXISTS idx_recommendations_advisor ON investment_recommendations(advisor_id)',
                'CREATE INDEX IF NOT EXISTS idx_recommendations_client ON investment_recommendations(client_id)',
                'CREATE INDEX IF NOT EXISTS idx_sessions_advisor ON advisor_sessions(advisor_id)'
            ]
            
            for index in indexes:
                self.conn.execute(index)
            
            self.conn.commit()
            logger.info("Financial database tables created successfully")
            
        except Exception as e:
            logger.error(f"Failed to create financial database tables: {str(e)}")
            raise
    
    def _encrypt_financial_data(self, data: Any) -> str:
        """Encrypt sensitive financial data"""
        try:
            if isinstance(data, (dict, list)):
                data = json.dumps(data)
            elif not isinstance(data, str):
                data = str(data)
            return self.cipher.encrypt(data.encode()).decode()
        except Exception as e:
            logger.error(f"Failed to encrypt financial data: {str(e)}")
            raise
    
    def _decrypt_financial_data(self, encrypted_data: str) -> str:
        """Decrypt sensitive financial data"""
        try:
            return self.cipher.decrypt(encrypted_data.encode()).decode()
        except Exception as e:
            logger.error(f"Failed to decrypt financial data: {str(e)}")
            raise
    
    def _populate_sample_financial_data(self):
        """Populate database with sample financial data for educational purposes"""
        try:
            # Check if sample data already exists
            cursor = self.conn.execute('SELECT COUNT(*) FROM stocks')
            if cursor.fetchone()[0] > 0:
                return  # Sample data already exists
            
            # Sample stocks data
            sample_stocks = [
                ('AAPL', 'Apple Inc.', 'Technology', 'Consumer Electronics', 3000000000000, 28.5, 0.5, 1.2, 45.2, 1.73, 25.0, 0.266, 'Technology giant focused on consumer electronics', 'NASDAQ'),
                ('MSFT', 'Microsoft Corporation', 'Technology', 'Software', 2800000000000, 32.1, 0.7, 0.9, 12.8, 0.35, 38.0, 0.367, 'Leading software and cloud computing company', 'NASDAQ'),
                ('GOOGL', 'Alphabet Inc.', 'Technology', 'Internet Services', 1700000000000, 24.2, 0.0, 1.1, 5.2, 0.13, 20.0, 0.274, 'Search engine and digital advertising leader', 'NASDAQ'),
                ('AMZN', 'Amazon.com Inc.', 'Consumer Discretionary', 'E-commerce', 1500000000000, 50.5, 0.0, 1.3, 8.1, 0.34, 13.0, 0.076, 'E-commerce and cloud computing giant', 'NASDAQ'),
                ('TSLA', 'Tesla Inc.', 'Consumer Discretionary', 'Electric Vehicles', 800000000000, 65.2, 0.0, 2.1, 12.4, 0.17, 19.0, 0.096, 'Electric vehicle and clean energy company', 'NASDAQ'),
                ('JPM', 'JPMorgan Chase & Co.', 'Financial Services', 'Banking', 450000000000, 12.5, 2.5, 1.0, 1.8, 1.34, 15.0, 0.32, 'Major investment bank and financial services firm', 'NYSE'),
                ('JNJ', 'Johnson & Johnson', 'Healthcare', 'Pharmaceuticals', 400000000000, 15.8, 2.7, 0.7, 5.9, 0.46, 25.0, 0.224, 'Diversified healthcare and pharmaceutical company', 'NYSE'),
                ('V', 'Visa Inc.', 'Financial Services', 'Payment Processing', 500000000000, 35.2, 0.6, 0.8, 14.2, 0.25, 38.0, 0.538, 'Global payment technology company', 'NYSE'),
                ('HD', 'The Home Depot Inc.', 'Consumer Discretionary', 'Home Improvement', 350000000000, 22.1, 2.4, 1.0, 1340.5, 2.56, 45.0, 0.106, 'Home improvement retail chain', 'NYSE'),
                ('PG', 'Procter & Gamble Co.', 'Consumer Staples', 'Household Products', 380000000000, 25.8, 2.4, 0.6, 7.8, 0.49, 25.0, 0.217, 'Consumer goods and household products', 'NYSE')
            ]
            
            # Insert sample stocks
            self.conn.executemany('''
                INSERT INTO stocks (ticker, company_name, sector, industry, market_cap, pe_ratio, 
                                  dividend_yield, beta, price_to_book, debt_to_equity, roe, profit_margin, 
                                  description, exchange)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', sample_stocks)
            
            # Sample economic indicators
            sample_indicators = [
                ('GDP Growth Rate', '2024-03-31', 2.4, 'Percent', 'Quarterly', 'Bureau of Economic Analysis'),
                ('Unemployment Rate', '2024-08-31', 4.2, 'Percent', 'Monthly', 'Bureau of Labor Statistics'),
                ('Federal Funds Rate', '2024-09-01', 5.25, 'Percent', 'Monthly', 'Federal Reserve'),
                ('Inflation Rate (CPI)', '2024-08-31', 2.9, 'Percent', 'Monthly', 'Bureau of Labor Statistics'),
                ('10-Year Treasury Yield', '2024-09-01', 4.30, 'Percent', 'Daily', 'Federal Reserve')
            ]
            
            self.conn.executemany('''
                INSERT INTO economic_indicators (indicator_name, date, value, unit, frequency, source)
                VALUES (?, ?, ?, ?, ?, ?)
            ''', sample_indicators)
            
            self.conn.commit()
            logger.info("Sample financial data populated successfully")
            
        except Exception as e:
            logger.error(f"Failed to populate sample financial data: {str(e)}")
    
    def get_stock_data(self, ticker: str) -> Optional[Dict]:
        """Retrieve comprehensive stock information"""
        try:
            cursor = self.conn.execute('''
                SELECT * FROM stocks WHERE ticker = ? COLLATE NOCASE
            ''', (ticker.upper(),))
            
            row = cursor.fetchone()
            if not row:
                return None
            
            stock_data = dict(row)
            
            # Get latest market data
            market_cursor = self.conn.execute('''
                SELECT * FROM market_data 
                WHERE ticker = ? COLLATE NOCASE 
                ORDER BY date DESC 
                LIMIT 1
            ''', (ticker.upper(),))
            
            market_row = market_cursor.fetchone()
            if market_row:
                stock_data['latest_price'] = market_row['close_price']
                stock_data['latest_volume'] = market_row['volume']
                stock_data['rsi'] = market_row['rsi']
                stock_data['moving_avg_50'] = market_row['moving_avg_50']
                stock_data['moving_avg_200'] = market_row['moving_avg_200']
                stock_data['last_updated'] = market_row['date']
            
            return stock_data
            
        except Exception as e:
            logger.error(f"Failed to retrieve stock data for {ticker}: {str(e)}")
            return None
    
    def store_investment_analysis(self, advisor_id: str, client_id: str, 
                                analysis_data: Dict, compliance_status: Dict) -> bool:
        """Store investment analysis with encryption"""
        try:
            analysis_id = analysis_data.get('analysis_id', str(uuid.uuid4()))
            ticker = analysis_data.get('investment_analysis', {}).get('ticker', '')
            
            # Encrypt sensitive analysis data
            encrypted_data = self._encrypt_financial_data(analysis_data)
            
            # Extract key metrics for indexing
            risk_score = analysis_data.get('risk_assessment', {}).get('overall_risk_score', 0)
            confidence_score = analysis_data.get('investment_analysis', {}).get('confidence_score', 0)
            recommendation = analysis_data.get('investment_analysis', {}).get('ai_recommendation', {}).get('action', '')
            
            # Store in database
            self.conn.execute('''
                INSERT INTO investment_analysis 
                (analysis_id, advisor_id, client_id, ticker, analysis_type, encrypted_analysis_data,
                 risk_score, confidence_score, recommendation, compliance_approved)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (
                analysis_id, advisor_id, client_id, ticker.upper(), 'comprehensive',
                encrypted_data, risk_score, confidence_score, recommendation,
                compliance_status.get('suitability_check', False)
            ))
            
            self.conn.commit()
            logger.info(f"Investment analysis {analysis_id} stored successfully")
            return True
            
        except Exception as e:
            logger.error(f"Failed to store investment analysis: {str(e)}")
            self.conn.rollback()
            return False
    
    def store_portfolio_analysis(self, client_id: str, advisor_id: str, analysis_data: Dict) -> bool:
        """Store portfolio analysis results"""
        try:
            portfolio_data = {
                'holdings': analysis_data.get('portfolio_health', {}).get('asset_allocation', {}),
                'analysis_results': analysis_data,
                'last_analysis': datetime.now().isoformat()
            }
            
            encrypted_holdings = self._encrypt_financial_data(portfolio_data)
            
            total_value = analysis_data.get('portfolio_health', {}).get('total_value', 0)
            portfolio_beta = analysis_data.get('portfolio_health', {}).get('risk_metrics', {}).get('portfolio_beta', 1.0)
            risk_score = analysis_data.get('portfolio_health', {}).get('overall_score', 5)
            
            # Update or insert portfolio record
            self.conn.execute('''
                INSERT OR REPLACE INTO client_portfolios 
                (client_id, advisor_id, portfolio_name, encrypted_holdings, total_value, 
                 portfolio_beta, risk_score, updated_at)
                VALUES (?, ?, ?, ?, ?, ?, ?, CURRENT_TIMESTAMP)
            ''', (
                client_id, advisor_id, f"{client_id}_main_portfolio",
                encrypted_holdings, total_value, portfolio_beta, risk_score
            ))
            
            self.conn.commit()
            logger.info(f"Portfolio analysis for client {client_id} stored successfully")
            return True
            
        except Exception as e:
            logger.error(f"Failed to store portfolio analysis: {str(e)}")
            self.conn.rollback()
            return False
    
    def store_generated_report(self, report_id: str, advisor_id: str, client_id: str,
                             report_data: Dict, compliance_status: Dict) -> bool:
        """Store generated investment report"""
        try:
            encrypted_report = self._encrypt_financial_data(report_data)
            
            # Set report expiration (default: 90 days for compliance)
            expires_at = datetime.now() + timedelta(days=90)
            
            self.conn.execute('''
                INSERT INTO investment_reports 
                (report_id, advisor_id, client_id, report_type, encrypted_report_data,
                 compliance_validated, expires_at)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            ''', (
                report_id, advisor_id, client_id, report_data.get('report_type', 'general'),
                encrypted_report, compliance_status.get('compliant', False), expires_at
            ))
            
            self.conn.commit()
            logger.info(f"Investment report {report_id} stored successfully")
            return True
            
        except Exception as e:
            logger.error(f"Failed to store investment report: {str(e)}")
            self.conn.rollback()
            return False
    
    def store_investment_recommendation_audit(self, advisor_id: str, client_id: str,
                                            ticker: str, recommendation_data: Dict,
                                            agent_reasoning: Dict) -> bool:
        """Store investment recommendation with full audit trail"""
        try:
            recommendation_type = recommendation_data.get('recommendation', {}).get('action', 'hold')
            target_price = recommendation_data.get('recommendation', {}).get('target_price', None)
            confidence_score = recommendation_data.get('confidence_score', 0)
            
            # Set recommendation expiration (default: 30 days)
            expires_at = datetime.now() + timedelta(days=30)
            
            self.conn.execute('''
                INSERT INTO investment_recommendations 
                (advisor_id, client_id, ticker, recommendation_type, recommendation, reasoning,
                 risk_assessment, target_price, confidence_score, expires_at)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (
                advisor_id, client_id, ticker.upper(), recommendation_type,
                json.dumps(recommendation_data.get('recommendation', {})),
                json.dumps(agent_reasoning), 
                json.dumps(recommendation_data.get('risk_assessment', {})),
                target_price, confidence_score, expires_at
            ))
            
            self.conn.commit()
            return True
            
        except Exception as e:
            logger.error(f"Failed to store investment recommendation audit: {str(e)}")
            self.conn.rollback()
            return False
    
    def log_financial_audit_event(self, action: str, advisor_id: str = None, 
                                client_id: str = None, ticker: str = None,
                                details: str = None, compliance_data: Dict = None,
                                ip_address: str = None, user_agent: str = None,
                                success: bool = True, risk_level: str = 'low'):
        """Log financial audit event for SOC2 compliance"""
        try:
            # Classify data for compliance
            data_classification = 'public'
            if client_id:
                data_classification = 'confidential'
            if 'portfolio' in action.lower() or 'personal' in action.lower():
                data_classification = 'restricted'
            
            self.conn.execute('''
                INSERT INTO financial_audit_log 
                (advisor_id, client_id, action, ticker, details, compliance_data, 
                 ip_address, user_agent, success, risk_level, data_classification)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (
                advisor_id, client_id, action, ticker, details,
                json.dumps(compliance_data) if compliance_data else None,
                ip_address, user_agent, success, risk_level, data_classification
            ))
            
            self.conn.commit()
            
        except Exception as e:
            logger.error(f"Failed to log financial audit event: {str(e)}")
    
    def get_market_overview(self) -> Dict[str, Any]:
        """Get market overview and statistics"""
        try:
            # Get sector distribution
            cursor = self.conn.execute('''
                SELECT sector, COUNT(*) as count, AVG(pe_ratio) as avg_pe,
                       AVG(dividend_yield) as avg_dividend_yield
                FROM stocks 
                WHERE sector IS NOT NULL
                GROUP BY sector
                ORDER BY count DESC
            ''')
            
            sector_data = []
            for row in cursor.fetchall():
                sector_data.append({
                    'sector': row['sector'],
                    'stock_count': row['count'],
                    'avg_pe_ratio': round(row['avg_pe'] or 0, 2),
                    'avg_dividend_yield': round(row['avg_dividend_yield'] or 0, 2)
                })
            
            # Get latest economic indicators
            cursor = self.conn.execute('''
                SELECT indicator_name, value, unit, date
                FROM economic_indicators
                WHERE date = (
                    SELECT MAX(date) FROM economic_indicators e2 
                    WHERE e2.indicator_name = economic_indicators.indicator_name
                )
                ORDER BY indicator_name
            ''')
            
            economic_data = [dict(row) for row in cursor.fetchall()]
            
            return {
                'sector_breakdown': sector_data,
                'economic_indicators': economic_data,
                'total_stocks': sum(s['stock_count'] for s in sector_data),
                'last_updated': datetime.now().isoformat()
            }
            
        except Exception as e:
            logger.error(f"Failed to get market overview: {str(e)}")
            return {}
    
    def get_compliance_dashboard(self, days: int = 30) -> Dict[str, Any]:
        """Get compliance dashboard metrics"""
        try:
            since_date = datetime.now() - timedelta(days=days)
            
            # Total recommendations
            cursor = self.conn.execute('''
                SELECT COUNT(*) as total FROM investment_recommendations 
                WHERE created_at > ?
            ''', (since_date,))
            total_recommendations = cursor.fetchone()[0]
            
            # Compliance approved recommendations
            cursor = self.conn.execute('''
                SELECT COUNT(*) as approved FROM investment_recommendations
                WHERE created_at > ? AND compliance_approved = 1
            ''', (since_date,))
            approved_recommendations = cursor.fetchone()[0]
            
            # Risk level distribution
            cursor = self.conn.execute('''
                SELECT risk_level, COUNT(*) as count 
                FROM financial_audit_log 
                WHERE timestamp > ?
                GROUP BY risk_level
            ''', (since_date,))
            risk_distribution = {row[0]: row[1] for row in cursor.fetchall()}
            
            return {
                'total_recommendations': total_recommendations,
                'approved_recommendations': approved_recommendations,
                'approval_rate': (approved_recommendations / max(total_recommendations, 1)) * 100,
                'risk_level_distribution': risk_distribution,
                'date_range': f"{since_date.strftime('%Y-%m-%d')} to {datetime.now().strftime('%Y-%m-%d')}"
            }
            
        except Exception as e:
            logger.error(f"Failed to get compliance dashboard: {str(e)}")
            return {}
    
    def health_check(self) -> bool:
        """Verify financial database is working properly"""
        try:
            cursor = self.conn.execute('SELECT COUNT(*) FROM stocks')
            stock_count = cursor.fetchone()[0]
            
            if stock_count == 0:
                logger.warning("No stock data found in database")
            
            return True
        except Exception as e:
            logger.error(f"Financial database health check failed: {str(e)}")
            return False
    
    def close(self):
        """Close database connection"""
        if self.conn:
            self.conn.close()
            logger.info("Financial database connection closed")