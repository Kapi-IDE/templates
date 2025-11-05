#!/usr/bin/env python3
"""
Legal AI Pod - System Test Script
Comprehensive testing of all legal system components
"""

import os
import sys
import json
import unittest
import logging
from pathlib import Path
from datetime import datetime

# Add backend to path
backend_path = Path(__file__).parent.parent / "backend"
sys.path.append(str(backend_path))

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class TestLegalAISystem(unittest.TestCase):
    """Test suite for Legal AI Pod system"""
    
    @classmethod
    def setUpClass(cls):
        """Set up test environment"""
        try:
            from database.chromadb_legal_manager import LegalKnowledgeStore
            from database.sqlite_legal_manager import LegalDataManager
            from agents.research_agent import LegalResearchAgent
            from agents.case_agent import CaseAnalysisAgent
            from agents.document_agent import DocumentReviewAgent
            from agents.precedent_agent import PrecedentMiningAgent
            
            # Initialize test components
            cls.knowledge_store = LegalKnowledgeStore(persist_directory="./test_chromadb")
            cls.legal_db = LegalDataManager(db_path="./test_legal.db")
            
            # Initialize agents
            cls.research_agent = LegalResearchAgent(cls.knowledge_store, cls.legal_db)
            cls.case_agent = CaseAnalysisAgent(cls.knowledge_store, cls.legal_db)
            cls.document_agent = DocumentReviewAgent(cls.knowledge_store, cls.legal_db)
            cls.precedent_agent = PrecedentMiningAgent(cls.knowledge_store, cls.legal_db)
            
            # Test data
            cls.test_attorney_id = "test_attorney_001"
            cls.test_client_id = "test_client_001"
            
            logger.info("Test environment set up successfully")
            
        except Exception as e:
            logger.error(f"Failed to set up test environment: {e}")
            raise
    
    def test_database_connections(self):
        """Test database connections"""
        logger.info("Testing database connections...")
        
        # Test ChromaDB connection
        try:
            collections = self.knowledge_store.client.list_collections()
            self.assertIsInstance(collections, list)
            logger.info("✓ ChromaDB connection successful")
        except Exception as e:
            self.fail(f"ChromaDB connection failed: {e}")
        
        # Test SQLite connection
        try:
            cursor = self.legal_db.conn.cursor()
            cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
            tables = cursor.fetchall()
            self.assertGreater(len(tables), 0)
            logger.info("✓ SQLite connection successful")
        except Exception as e:
            self.fail(f"SQLite connection failed: {e}")
    
    def test_legal_knowledge_loading(self):
        """Test legal knowledge loading"""
        logger.info("Testing legal knowledge loading...")
        
        # Test case law loading
        sample_case = {
            "case_id": "test_case_001",
            "case_name": "Test v. Case",
            "citation": "123 Test 456 (2023)",
            "court": "Test Court",
            "jurisdiction": "test",
            "decision_date": "2023-01-01",
            "legal_issues": ["Test Issue"],
            "holding": "Test holding",
            "facts": "Test facts",
            "legal_reasoning": "Test reasoning",
            "precedent_weight": 5,
            "binding_authority": "Test authority",
            "related_statutes": ["Test Statute"],
            "full_text": "Test full text"
        }
        
        try:
            self.knowledge_store.add_case_law(sample_case)
            logger.info("✓ Case law loading successful")
        except Exception as e:
            self.fail(f"Case law loading failed: {e}")
        
        # Test statute loading
        sample_statute = {
            "statute_id": "test_statute_001",
            "title": "Test Statute",
            "citation": "Test Code § 123",
            "jurisdiction": "test",
            "effective_date": "2023-01-01",
            "legal_areas": ["Test Area"],
            "summary": "Test summary",
            "key_provisions": ["Test provision"],
            "full_text": "Test statute text",
            "related_cases": ["test_case_001"],
            "amendments": []
        }
        
        try:
            self.knowledge_store.add_statute(sample_statute)
            logger.info("✓ Statute loading successful")
        except Exception as e:
            self.fail(f"Statute loading failed: {e}")
    
    def test_legal_research_agent(self):
        """Test legal research agent"""
        logger.info("Testing legal research agent...")
        
        try:
            results = self.research_agent.conduct_legal_research(
                attorney_id=self.test_attorney_id,
                client_id=self.test_client_id,
                legal_query="test legal query",
                jurisdiction="test"
            )
            
            self.assertIsInstance(results, dict)
            self.assertIn('research_id', results)
            self.assertIn('query', results)
            logger.info("✓ Legal research agent test successful")
            
        except Exception as e:
            self.fail(f"Legal research agent test failed: {e}")
    
    def test_case_analysis_agent(self):
        """Test case analysis agent"""
        logger.info("Testing case analysis agent...")
        
        test_case_facts = {
            "case_type": "test_case",
            "parties": {"plaintiff": "Test Plaintiff", "defendant": "Test Defendant"},
            "facts": "Test case facts",
            "damages_claimed": 100000,
            "jurisdiction": "test"
        }
        
        try:
            results = self.case_agent.analyze_case_strength(
                attorney_id=self.test_attorney_id,
                client_id=self.test_client_id,
                case_facts=test_case_facts
            )
            
            self.assertIsInstance(results, dict)
            self.assertIn('analysis_id', results)
            logger.info("✓ Case analysis agent test successful")
            
        except Exception as e:
            self.fail(f"Case analysis agent test failed: {e}")
    
    def test_document_review_agent(self):
        """Test document review agent"""
        logger.info("Testing document review agent...")
        
        test_document = {
            "document_type": "test_contract",
            "content": "Test contract content",
            "parties": ["Test Party 1", "Test Party 2"],
            "review_focus": ["risk_assessment"]
        }
        
        try:
            results = self.document_agent.review_legal_document(
                attorney_id=self.test_attorney_id,
                client_id=self.test_client_id,
                document_data=test_document
            )
            
            self.assertIsInstance(results, dict)
            self.assertIn('review_id', results)
            logger.info("✓ Document review agent test successful")
            
        except Exception as e:
            self.fail(f"Document review agent test failed: {e}")
    
    def test_precedent_mining_agent(self):
        """Test precedent mining agent"""
        logger.info("Testing precedent mining agent...")
        
        test_legal_issue = {
            "issue_description": "Test legal issue",
            "fact_pattern": "Test fact pattern",
            "jurisdiction": "test",
            "case_type": "test_case_type"
        }
        
        try:
            results = self.precedent_agent.mine_legal_precedents(
                attorney_id=self.test_attorney_id,
                client_id=self.test_client_id,
                legal_issue=test_legal_issue
            )
            
            self.assertIsInstance(results, dict)
            self.assertIn('mining_id', results)
            logger.info("✓ Precedent mining agent test successful")
            
        except Exception as e:
            self.fail(f"Precedent mining agent test failed: {e}")
    
    def test_legal_search_functionality(self):
        """Test legal search functionality"""
        logger.info("Testing legal search functionality...")
        
        try:
            # Test case law search
            case_results = self.knowledge_store.search_case_law("test", limit=5)
            self.assertIsInstance(case_results, list)
            logger.info("✓ Case law search successful")
            
            # Test statute search
            statute_results = self.knowledge_store.search_statutes("test", limit=5)
            self.assertIsInstance(statute_results, list)
            logger.info("✓ Statute search successful")
            
            # Test general legal knowledge search
            general_results = self.knowledge_store.search_legal_knowledge("test", limit=5)
            self.assertIsInstance(general_results, list)
            logger.info("✓ General legal search successful")
            
        except Exception as e:
            self.fail(f"Legal search functionality test failed: {e}")
    
    def test_attorney_client_privilege(self):
        """Test attorney-client privilege protection"""
        logger.info("Testing attorney-client privilege protection...")
        
        try:
            # Test privileged communication storage
            test_communication = {
                "attorney_id": self.test_attorney_id,
                "client_id": self.test_client_id,
                "communication_type": "legal_advice",
                "content": "Test privileged communication",
                "timestamp": datetime.utcnow().isoformat()
            }
            
            # Store privileged communication
            comm_id = self.legal_db.store_privileged_communication(test_communication)
            self.assertIsNotNone(comm_id)
            
            # Retrieve privileged communication
            retrieved = self.legal_db.get_privileged_communications(
                self.test_attorney_id, self.test_client_id
            )
            self.assertIsInstance(retrieved, list)
            logger.info("✓ Attorney-client privilege protection test successful")
            
        except Exception as e:
            self.fail(f"Attorney-client privilege test failed: {e}")
    
    def test_ethics_compliance(self):
        """Test legal ethics compliance"""
        logger.info("Testing legal ethics compliance...")
        
        try:
            from utils.legal_ethics import LegalEthicsMonitoring
            
            ethics_monitor = LegalEthicsMonitoring()
            
            # Test ethics rule loading
            test_ethics_data = {
                "professional_responsibility_rules": [
                    {
                        "rule_id": "test_rule_1_1",
                        "rule_number": "1.1",
                        "rule_title": "Test Competence",
                        "rule_text": "Test rule text",
                        "ai_implications": ["Test implication"],
                        "compliance_requirements": ["Test requirement"],
                        "violation_indicators": ["Test indicator"],
                        "escalation_threshold": "medium"
                    }
                ],
                "ethics_monitoring_rules": [],
                "escalation_procedures": [],
                "compliance_templates": []
            }
            
            ethics_monitor.load_ethics_rules(test_ethics_data)
            logger.info("✓ Legal ethics compliance test successful")
            
        except Exception as e:
            self.fail(f"Legal ethics compliance test failed: {e}")
    
    def test_system_integration(self):
        """Test overall system integration"""
        logger.info("Testing system integration...")
        
        try:
            # Test coordinated workflow
            legal_query = "test integration query"
            
            # Step 1: Legal research
            research_results = self.research_agent.conduct_legal_research(
                attorney_id=self.test_attorney_id,
                client_id=self.test_client_id,
                legal_query=legal_query,
                jurisdiction="test"
            )
            self.assertIsInstance(research_results, dict)
            
            # Step 2: Case analysis
            test_case_facts = {
                "case_type": "integration_test",
                "parties": {"plaintiff": "Test P", "defendant": "Test D"},
                "facts": "Integration test facts",
                "damages_claimed": 50000,
                "jurisdiction": "test"
            }
            
            case_results = self.case_agent.analyze_case_strength(
                attorney_id=self.test_attorney_id,
                client_id=self.test_client_id,
                case_facts=test_case_facts
            )
            self.assertIsInstance(case_results, dict)
            
            logger.info("✓ System integration test successful")
            
        except Exception as e:
            self.fail(f"System integration test failed: {e}")
    
    @classmethod
    def tearDownClass(cls):
        """Clean up test environment"""
        try:
            # Clean up test databases
            test_files = [
                "./test_legal.db",
                "./test_chromadb"
            ]
            
            for file_path in test_files:
                if os.path.exists(file_path):
                    if os.path.isfile(file_path):
                        os.remove(file_path)
                    else:
                        import shutil
                        shutil.rmtree(file_path)
            
            logger.info("Test environment cleaned up")
            
        except Exception as e:
            logger.error(f"Failed to clean up test environment: {e}")

def run_legal_system_tests():
    """Run all legal system tests"""
    print("="*60)
    print("LEGAL AI POD - SYSTEM TESTS")
    print("="*60)
    
    # Create test suite
    test_suite = unittest.TestLoader().loadTestsFromTestCase(TestLegalAISystem)
    
    # Run tests
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(test_suite)
    
    # Print summary
    print("\n" + "="*60)
    print("TEST SUMMARY")
    print("="*60)
    print(f"Tests run: {result.testsRun}")
    print(f"Failures: {len(result.failures)}")
    print(f"Errors: {len(result.errors)}")
    
    if result.failures:
        print("\nFAILURES:")
        for test, traceback in result.failures:
            print(f"- {test}: {traceback}")
    
    if result.errors:
        print("\nERRORS:")
        for test, traceback in result.errors:
            print(f"- {test}: {traceback}")
    
    if result.wasSuccessful():
        print("\n🎉 ALL TESTS PASSED! Legal AI Pod system is working correctly.")
        return True
    else:
        print("\n❌ SOME TESTS FAILED! Please check the system configuration.")
        return False

if __name__ == "__main__":
    success = run_legal_system_tests()
    sys.exit(0 if success else 1)
