#!/usr/bin/env python3
"""
Legal AI Pod Database Setup Script
Initializes SQLite database with sample legal data and ChromaDB with legal knowledge
"""

import os
import sys
import logging
from datetime import datetime, timedelta
from typing import Dict, Any, List
import uuid
import json
from faker import Faker

# Add backend to path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from database.sqlite_legal_manager import LegalDataManager
from database.chromadb_legal_manager import LegalKnowledgeStore

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize Faker for generating sample data
fake = Faker()

class LegalDatabaseSeeder:
    """Seeds legal database with sample data for development and testing"""
    
    def __init__(self):
        """Initialize database managers"""
        self.legal_db = LegalDataManager()
        self.knowledge_store = LegalKnowledgeStore()
        
    def seed_attorneys(self, count: int = 10) -> List[str]:
        """Create sample attorney records"""
        attorney_ids = []
        
        for i in range(count):
            attorney_data = {
                'attorney_id': f"attorney_{i+1:03d}",
                'bar_number': f"BAR{fake.random_int(10000, 99999)}",
                'first_name': fake.first_name(),
                'last_name': fake.last_name(),
                'law_firm': fake.company() + " Law Firm",
                'email': fake.email(),
                'phone': fake.phone_number(),
                'practice_areas': fake.random_elements(
                    elements=['Corporate Law', 'Litigation', 'Real Estate', 'Employment Law', 
                             'Family Law', 'Criminal Law', 'Immigration', 'Intellectual Property'],
                    length=fake.random_int(1, 3)
                ),
                'jurisdiction': fake.random_element(['Federal', 'California', 'New York', 'Texas', 'Florida']),
                'bar_admission_date': fake.date_between(start_date='-20y', end_date='-2y')
            }
            
            if self.legal_db.create_attorney(attorney_data):
                attorney_ids.append(attorney_data['attorney_id'])
                logger.info(f"Created attorney: {attorney_data['first_name']} {attorney_data['last_name']}")
        
        return attorney_ids
    
    def seed_clients(self, count: int = 25) -> List[str]:
        """Create sample client records"""
        client_ids = []
        
        for i in range(count):
            client_type = fake.random_element(['individual', 'corporate'])
            
            if client_type == 'individual':
                client_data = {
                    'client_id': f"client_{i+1:03d}",
                    'client_type': 'individual',
                    'first_name': fake.first_name(),
                    'last_name': fake.last_name(),
                    'email': fake.email(),
                    'phone': fake.phone_number(),
                    'address': fake.address(),
                    'case_matter_type': fake.random_element(['Civil Litigation', 'Family Law', 'Criminal Defense', 'Personal Injury']),
                    'retainer_status': fake.random_element(['paid', 'pending', 'overdue']),
                    'conflict_checked': True
                }
            else:
                client_data = {
                    'client_id': f"client_{i+1:03d}",
                    'client_type': 'corporate',
                    'company_name': fake.company(),
                    'email': fake.company_email(),
                    'phone': fake.phone_number(),
                    'address': fake.address(),
                    'case_matter_type': fake.random_element(['Corporate Transactions', 'Employment Law', 'Intellectual Property', 'Regulatory Compliance']),
                    'retainer_status': fake.random_element(['paid', 'pending']),
                    'conflict_checked': True
                }
            
            if self.legal_db.create_client(client_data):
                client_ids.append(client_data['client_id'])
                logger.info(f"Created client: {client_data.get('company_name') or client_data.get('first_name', '') + ' ' + client_data.get('last_name', '')}")
        
        return client_ids
    
    def seed_attorney_client_relationships(self, attorney_ids: List[str], client_ids: List[str], count: int = 20):
        """Create attorney-client relationships"""
        for i in range(count):
            attorney_id = fake.random_element(attorney_ids)
            client_id = fake.random_element(client_ids)
            
            # Avoid duplicate relationships
            try:
                relationship_data = {
                    'matter_description': fake.text(max_nb_chars=200),
                    'engagement_date': fake.date_between(start_date='-2y', end_date='today'),
                    'relationship_status': 'active',
                    'privilege_status': 'privileged',
                    'retainer_amount': fake.pydecimal(left_digits=5, right_digits=2, positive=True),
                    'billing_rate': fake.pydecimal(left_digits=3, right_digits=2, positive=True)
                }
                
                relationship_id = self.legal_db.create_attorney_client_relationship(
                    attorney_id, client_id, relationship_data
                )
                logger.info(f"Created relationship {relationship_id} between {attorney_id} and {client_id}")
                
            except Exception as e:
                logger.debug(f"Relationship already exists or conflict detected: {str(e)}")
                continue
    
    def seed_case_law_knowledge(self, count: int = 100):
        """Seed ChromaDB with sample case law"""
        logger.info("Seeding case law knowledge...")
        
        legal_issues_pool = [
            "Contract interpretation", "Negligence liability", "Constitutional rights", 
            "Employment discrimination", "Intellectual property infringement", "Corporate governance",
            "Criminal procedure", "Evidence admissibility", "Jurisdiction disputes", "Standing to sue",
            "Due process violations", "First Amendment rights", "Search and seizure",
            "Miranda rights", "Double jeopardy", "Statute of limitations", "Breach of fiduciary duty",
            "Securities fraud", "Antitrust violations", "Environmental liability"
        ]
        
        courts_pool = [
            "Supreme Court", "9th Circuit Court of Appeals", "2nd Circuit Court of Appeals",
            "District Court for SDNY", "District Court for NDCA", "California Supreme Court",
            "New York Court of Appeals", "Texas Supreme Court", "Florida Supreme Court"
        ]
        
        for i in range(count):
            case_data = {
                'case_name': f"{fake.last_name()} v. {fake.last_name()}",
                'citation': f"{fake.random_int(100, 999)} F.{fake.random_int(2, 3)}d {fake.random_int(1, 1500)}",
                'court': fake.random_element(courts_pool),
                'jurisdiction': fake.random_element(['Federal', 'California', 'New York', 'Texas', 'Florida']),
                'decision_date': fake.date_between(start_date='-50y', end_date='today'),
                'legal_issues': fake.random_elements(legal_issues_pool, length=fake.random_int(1, 3)),
                'holding': fake.paragraph(nb_sentences=3),
                'key_facts': fake.paragraph(nb_sentences=4),
                'legal_reasoning': fake.paragraph(nb_sentences=5),
                'precedent_type': fake.random_element(['binding', 'persuasive']),
                'practice_areas': fake.random_elements(
                    ['Corporate Law', 'Litigation', 'Constitutional Law', 'Criminal Law', 'Civil Rights'],
                    length=fake.random_int(1, 2)
                ),
                'summary': fake.paragraph(nb_sentences=2),
                'citation_count': fake.random_int(0, 150),
                'overruled': fake.boolean(chance_of_getting_true=5)
            }
            
            if self.knowledge_store.add_case_law(case_data):
                if (i + 1) % 20 == 0:
                    logger.info(f"Added {i + 1} case law entries")
    
    def seed_statutes_knowledge(self, count: int = 50):
        """Seed ChromaDB with sample statutes"""
        logger.info("Seeding statutes knowledge...")
        
        statute_titles = [
            "Civil Rights Act", "Americans with Disabilities Act", "Securities Exchange Act",
            "Fair Labor Standards Act", "Clean Air Act", "Sarbanes-Oxley Act",
            "Employee Retirement Income Security Act", "Immigration and Nationality Act",
            "Telecommunications Act", "Copyright Act", "Patent Act", "Trademark Act"
        ]
        
        for i in range(count):
            title_base = fake.random_element(statute_titles)
            statute_data = {
                'title': f"{title_base} of {fake.random_int(1950, 2023)}",
                'citation': f"{fake.random_int(10, 50)} U.S.C. § {fake.random_int(100, 9999)}",
                'jurisdiction': fake.random_element(['Federal', 'California', 'New York', 'Texas']),
                'chapter': str(fake.random_int(1, 50)),
                'section': str(fake.random_int(100, 9999)),
                'effective_date': fake.date_between(start_date='-30y', end_date='today'),
                'statute_text': fake.paragraph(nb_sentences=8),
                'summary': fake.paragraph(nb_sentences=3),
                'keywords': fake.random_elements(
                    ['regulation', 'compliance', 'enforcement', 'liability', 'procedure', 'rights'],
                    length=fake.random_int(2, 4)
                ),
                'practice_areas': fake.random_elements(
                    ['Corporate Law', 'Employment Law', 'Environmental Law', 'Securities Law'],
                    length=fake.random_int(1, 2)
                )
            }
            
            if self.knowledge_store.add_statute(statute_data):
                if (i + 1) % 10 == 0:
                    logger.info(f"Added {i + 1} statute entries")
    
    def seed_precedents_knowledge(self, count: int = 75):
        """Seed ChromaDB with sample legal precedents"""
        logger.info("Seeding legal precedents knowledge...")
        
        legal_principles = [
            "Duty of care in negligence", "Reasonable expectation of privacy", "Freedom of speech protection",
            "Due process requirements", "Equal protection under law", "Commerce Clause authority",
            "Executive privilege limitations", "Judicial review scope", "Contract formation requirements",
            "Good faith and fair dealing", "Fiduciary duty standards", "Corporate veil piercing"
        ]
        
        for i in range(count):
            precedent_data = {
                'legal_principle': fake.random_element(legal_principles),
                'precedent_weight': fake.random_int(5, 10),
                'binding_authority': fake.random_element(['Supreme Court', 'Circuit Court', 'State Supreme Court']),
                'jurisdiction': fake.random_element(['Federal', 'California', 'New York', 'Texas']),
                'practice_area': fake.random_element(['Constitutional Law', 'Corporate Law', 'Civil Rights', 'Criminal Law']),
                'fact_pattern': fake.paragraph(nb_sentences=3),
                'legal_standard': fake.paragraph(nb_sentences=2),
                'overruled': fake.boolean(chance_of_getting_true=3)
            }
            
            if self.knowledge_store.add_precedent(precedent_data):
                if (i + 1) % 15 == 0:
                    logger.info(f"Added {i + 1} precedent entries")
    
    def seed_contract_templates(self, count: int = 25):
        """Seed ChromaDB with sample contract templates"""
        logger.info("Seeding contract templates...")
        
        contract_types = [
            'Employment Agreement', 'Non-Disclosure Agreement', 'Service Agreement',
            'Purchase Agreement', 'Lease Agreement', 'Partnership Agreement',
            'License Agreement', 'Merger Agreement', 'Loan Agreement'
        ]
        
        for i in range(count):
            contract_type = fake.random_element(contract_types)
            template_data = {
                'template_name': f"Standard {contract_type}",
                'contract_type': contract_type.lower().replace(' ', '_'),
                'jurisdiction': fake.random_element(['Federal', 'California', 'New York', 'Delaware']),
                'practice_area': fake.random_element(['Corporate Law', 'Employment Law', 'Real Estate']),
                'template_content': fake.paragraph(nb_sentences=10),
                'standard_clauses': fake.random_elements(
                    ['Termination', 'Confidentiality', 'Governing Law', 'Dispute Resolution', 'Force Majeure'],
                    length=fake.random_int(3, 5)
                ),
                'optional_clauses': fake.random_elements(
                    ['Non-Compete', 'Indemnification', 'Assignment', 'Amendment'],
                    length=fake.random_int(1, 3)
                ),
                'risk_level': fake.random_element(['low', 'medium', 'high']),
                'complexity_level': fake.random_element(['simple', 'medium', 'complex'])
            }
            
            if self.knowledge_store.add_contract_template(template_data):
                if (i + 1) % 5 == 0:
                    logger.info(f"Added {i + 1} contract templates")
    
    def create_sample_interactions(self, attorney_ids: List[str], client_ids: List[str], count: int = 50):
        """Create sample AI interactions for testing"""
        logger.info("Creating sample AI interactions...")
        
        agent_types = ['legal_research', 'case_analysis', 'document_review', 'precedent_mining']
        
        for i in range(count):
            attorney_id = fake.random_element(attorney_ids)
            client_id = fake.random_element(client_ids)
            agent_type = fake.random_element(agent_types)
            
            interaction_data = {
                'agent_type': agent_type,
                'interaction_type': f'{agent_type}_query',
                'query': fake.sentence(nb_words=10),
                'response': {'result': fake.paragraph(nb_sentences=3), 'confidence': fake.pyfloat(min_value=0.7, max_value=0.99)},
                'confidence_score': fake.pyfloat(min_value=0.7, max_value=0.99),
                'processing_time_seconds': fake.pyfloat(min_value=0.5, max_value=5.0),
                'privilege_protected': True,
                'session_id': str(uuid.uuid4())
            }
            
            try:
                self.legal_db.store_ai_interaction(attorney_id, client_id, interaction_data)
                if (i + 1) % 10 == 0:
                    logger.info(f"Created {i + 1} AI interactions")
            except Exception as e:
                logger.debug(f"Failed to create interaction: {str(e)}")
    
    def run_full_seed(self):
        """Run complete database seeding process"""
        logger.info("Starting Legal AI Pod database seeding...")
        
        try:
            # Seed attorneys and clients first
            attorney_ids = self.seed_attorneys(15)
            client_ids = self.seed_clients(30)
            
            # Create relationships
            self.seed_attorney_client_relationships(attorney_ids, client_ids, 25)
            
            # Seed knowledge base
            self.seed_case_law_knowledge(100)
            self.seed_statutes_knowledge(50)
            self.seed_precedents_knowledge(75)
            self.seed_contract_templates(25)
            
            # Create sample interactions
            self.create_sample_interactions(attorney_ids, client_ids, 50)
            
            logger.info("Legal AI Pod database seeding completed successfully!")
            
            # Print stats
            db_stats = self.legal_db.get_database_stats()
            knowledge_stats = self.knowledge_store.get_collection_stats()
            
            logger.info("Database Statistics:")
            for table, count in db_stats.items():
                logger.info(f"  {table}: {count} records")
            
            logger.info("Knowledge Base Statistics:")
            for collection, count in knowledge_stats.items():
                if '_count' in collection:
                    logger.info(f"  {collection}: {count} documents")
            
        except Exception as e:
            logger.error(f"Database seeding failed: {str(e)}")
            raise

def main():
    """Main execution function"""
    print("Legal AI Pod Database Setup")
    print("===========================")
    
    # Create seeder and run
    seeder = LegalDatabaseSeeder()
    seeder.run_full_seed()
    
    print("\nSetup completed successfully!")
    print("You can now run the Legal AI Pod application with sample data.")

if __name__ == "__main__":
    main()