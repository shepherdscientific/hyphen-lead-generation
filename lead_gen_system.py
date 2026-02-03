#!/usr/bin/env python3
"""
Lead Generation System
======================

AI-powered lead generation using local LLMs (Ollama)
Processes multiple data sources into unified format
Enriches, scores, and syncs to HubSpot

Requirements:
    pip install --break-system-packages \
        langchain langchain-community \
        ollama sqlalchemy psycopg2-binary \
        requests pandas pydantic \
        python-dotenv httpx asyncio

Author: Hyphen Partners
Date: 2026-01-11
"""

import asyncio
import json
import os
from datetime import datetime, timedelta
from enum import Enum
from typing import List, Optional, Dict, Any
from pathlib import Path

import pandas as pd
from pydantic import BaseModel, EmailStr, Field, validator
from sqlalchemy import create_engine, Column, Integer, String, DateTime, Float, JSON
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import requests

# Langchain imports
from langchain.llms import Ollama
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain


# =============================================================================
# CONFIGURATION
# =============================================================================

class Config:
    """System configuration"""
    
    # Database
    DATABASE_URL = os.getenv(
        'DATABASE_URL',
        'postgresql://localhost/leads'
    )
    
    # Ollama
    OLLAMA_BASE_URL = os.getenv('OLLAMA_BASE_URL', 'http://localhost:11434')
    OLLAMA_MODEL = os.getenv('OLLAMA_MODEL', 'qwen2.5-coder:32b')
    
    # HubSpot
    HUBSPOT_API_KEY = os.getenv('HUBSPOT_API_KEY', '')
    HUBSPOT_BASE_URL = 'https://api.hubapi.com'
    
    # Hunter.io (email finder)
    HUNTER_API_KEY = os.getenv('HUNTER_API_KEY', '')
    
    # Scoring thresholds
    HIGH_PRIORITY_SCORE = 70
    MEDIUM_PRIORITY_SCORE = 50


# =============================================================================
# DATA MODELS
# =============================================================================

class LeadSource(str, Enum):
    """Lead source types"""
    APOLLO = "apollo"
    LINKEDIN = "linkedin"
    MANUAL = "manual"
    GOOGLE_FORM = "google_form"
    SCRAPED = "scraped"


class PriorityTier(str, Enum):
    """Lead priority classification"""
    HIGH = "High"
    MEDIUM = "Medium"
    LOW = "Low"


class Lead(BaseModel):
    """Unified lead data model"""
    
    # Identity
    first_name: str
    last_name: str
    full_name: Optional[str] = None
    email: Optional[EmailStr] = None
    phone: Optional[str] = None
    
    # Company
    company_name: str
    company_domain: Optional[str] = None
    company_size: Optional[int] = None
    company_industry: Optional[str] = None
    company_location: Optional[str] = None
    
    # Professional
    title: Optional[str] = None
    seniority: Optional[str] = None
    department: Optional[str] = None
    
    # Metadata
    source: LeadSource
    source_id: Optional[str] = None
    source_url: Optional[str] = None
    
    # Enrichment
    linkedin_url: Optional[str] = None
    twitter_url: Optional[str] = None
    
    # Scoring
    lead_score: Optional[int] = Field(default=0, ge=0, le=100)
    priority_tier: Optional[PriorityTier] = None
    score_reasons: Optional[List[str]] = []
    
    # Timestamps
    created_at: datetime = Field(default_factory=datetime.utcnow)
    enriched_at: Optional[datetime] = None
    synced_to_hubspot_at: Optional[datetime] = None
    
    # Raw data
    raw_data: Optional[Dict[str, Any]] = {}
    
    @validator('full_name', always=True)
    def set_full_name(cls, v, values):
        """Auto-generate full name if not provided"""
        if v:
            return v
        return f"{values.get('first_name', '')} {values.get('last_name', '')}".strip()
    
    @validator('phone')
    def normalize_phone(cls, v):
        """Normalize phone numbers to international format"""
        if not v:
            return None
        
        # Remove spaces, dashes, parentheses
        cleaned = ''.join(c for c in v if c.isdigit() or c == '+')
        
        # Handle Nigerian numbers
        if cleaned.startswith('0'):
            cleaned = '+234' + cleaned[1:]
        elif cleaned.startswith('234'):
            cleaned = '+' + cleaned
        elif not cleaned.startswith('+'):
            # Assume Nigerian if no country code
            cleaned = '+234' + cleaned
        
        return cleaned
    
    class Config:
        use_enum_values = True


# SQLAlchemy ORM model
Base = declarative_base()

class LeadDB(Base):
    """Database model for leads"""
    __tablename__ = 'leads'
    
    id = Column(Integer, primary_key=True)
    first_name = Column(String)
    last_name = Column(String)
    email = Column(String, unique=True, index=True)
    phone = Column(String)
    company_name = Column(String, index=True)
    company_domain = Column(String)
    title = Column(String)
    source = Column(String, index=True)
    lead_score = Column(Integer)
    priority_tier = Column(String)
    created_at = Column(DateTime, default=datetime.utcnow)
    enriched_at = Column(DateTime)
    synced_to_hubspot_at = Column(DateTime)
    hubspot_contact_id = Column(String)
    raw_data = Column(JSON)


# =============================================================================
# DATABASE LAYER
# =============================================================================

class Database:
    """Database operations"""
    
    def __init__(self, url: str = Config.DATABASE_URL):
        self.engine = create_engine(url)
        Base.metadata.create_all(self.engine)
        Session = sessionmaker(bind=self.engine)
        self.session = Session()
    
    def save_lead(self, lead: Lead) -> int:
        """Save lead to database"""
        db_lead = LeadDB(
            first_name=lead.first_name,
            last_name=lead.last_name,
            email=lead.email,
            phone=lead.phone,
            company_name=lead.company_name,
            company_domain=lead.company_domain,
            title=lead.title,
            source=lead.source,
            lead_score=lead.lead_score,
            priority_tier=lead.priority_tier if lead.priority_tier else None,
            enriched_at=lead.enriched_at,
            synced_to_hubspot_at=lead.synced_to_hubspot_at,
            raw_data=lead.raw_data
        )
        
        self.session.add(db_lead)
        self.session.commit()
        return db_lead.id
    
    def get_leads_to_enrich(self, limit: int = 10) -> List[LeadDB]:
        """Get leads that need enrichment"""
        return self.session.query(LeadDB)\
            .filter(LeadDB.enriched_at.is_(None))\
            .limit(limit)\
            .all()
    
    def get_leads_to_sync(self, limit: int = 10) -> List[LeadDB]:
        """Get leads that need HubSpot sync"""
        return self.session.query(LeadDB)\
            .filter(LeadDB.synced_to_hubspot_at.is_(None))\
            .filter(LeadDB.enriched_at.isnot(None))\
            .limit(limit)\
            .all()
    
    def mark_enriched(self, lead_id: int):
        """Mark lead as enriched"""
        lead = self.session.query(LeadDB).get(lead_id)
        if lead:
            lead.enriched_at = datetime.utcnow()
            self.session.commit()
    
    def mark_synced(self, lead_id: int, hubspot_contact_id: str):
        """Mark lead as synced to HubSpot"""
        lead = self.session.query(LeadDB).get(lead_id)
        if lead:
            lead.synced_to_hubspot_at = datetime.utcnow()
            lead.hubspot_contact_id = hubspot_contact_id
            self.session.commit()


# =============================================================================
# DATA PARSERS
# =============================================================================

def sanitize(val):
    """Normalise a value from a pandas row into something Pydantic accepts.

    With dtype=str + keep_default_na=False:
      - empty cells  → ''   (we map to None)
      - present cells → str (Pydantic coerces "5200" → int where the model says int)

    Also handles the legacy case where NaN slips through (e.g. from other parsers).
    """
    if val is None or val == '':
        return None
    try:
        if pd.isna(val):          # catches float NaN / NaT
            return None
    except (ValueError, TypeError):
        pass                      # pd.isna blows up on lists/dicts — those are fine
    return val


class ApolloParser:
    """Parse Apollo.io CSV exports"""
    
    @staticmethod
    def parse(file_path: str) -> List[Lead]:
        """Parse Apollo CSV file"""
        # dtype=str  → nothing gets silently cast to float (kills the phone bug)
        # keep_default_na=False → empty cells arrive as '' not NaN
        df = pd.read_csv(file_path, dtype=str, keep_default_na=False)
        leads = []
        
        for _, row in df.iterrows():
            try:
                # ── phone: Corporate Phone is most populated; fall back down the list
                phone = (sanitize(row.get('Corporate Phone'))
                      or sanitize(row.get('Company Phone'))
                      or sanitize(row.get('Work Direct Phone'))
                      or sanitize(row.get('Mobile Phone'))
                      or sanitize(row.get('Other Phone')))

                # ── location: prefer company address over personal
                city    = sanitize(row.get('Company City'))    or sanitize(row.get('City'))
                country = sanitize(row.get('Company Country')) or sanitize(row.get('Country'))
                location = f"{city}, {country}" if city and country else (city or country)

                lead = Lead(
                    # required str fields – `or ''` so sanitize(empty) -> None -> ''
                    first_name   =sanitize(row.get('First Name'))    or '',
                    last_name    =sanitize(row.get('Last Name'))     or '',
                    company_name =sanitize(row.get('Company Name'))  or '',

                    # optional fields (None is fine)
                    email            =sanitize(row.get('Email')),
                    phone            =phone,
                    company_domain   =sanitize(row.get('Website')),
                    company_size     =sanitize(row.get('# Employees')),
                    company_industry =sanitize(row.get('Industry')),
                    company_location =location,
                    title            =sanitize(row.get('Title')),
                    seniority        =sanitize(row.get('Seniority')),
                    department       =sanitize(row.get('Departments')),

                    # social / identifiers
                    linkedin_url     =sanitize(row.get('Person Linkedin Url')),
                    twitter_url      =sanitize(row.get('Twitter Url')),
                    source           =LeadSource.APOLLO,
                    source_id        =sanitize(row.get('Apollo Contact Id')),

                    raw_data={k: sanitize(v) for k, v in row.to_dict().items()}
                )
                leads.append(lead)
            except Exception as e:
                print(f"Error parsing row: {e}")
                continue
        
        return leads


class LinkedInParser:
    """Parse LinkedIn exports"""
    
    @staticmethod
    def parse(file_path: str) -> List[Lead]:
        """Parse LinkedIn CSV file"""
        df = pd.read_csv(file_path, dtype=str, keep_default_na=False)
        leads = []
        
        for _, row in df.iterrows():
            try:
                full_name = sanitize(row.get('Name', '')) or ''
                name_parts = full_name.split(' ', 1)
                
                lead = Lead(
                    first_name=name_parts[0] if len(name_parts) > 0 else '',
                    last_name=name_parts[1] if len(name_parts) > 1 else '',
                    company_name=sanitize(row.get('Company', '')) or '',
                    title=sanitize(row.get('Position')),
                    linkedin_url=sanitize(row.get('Profile URL')),
                    source=LeadSource.LINKEDIN,
                    raw_data={k: sanitize(v) for k, v in row.to_dict().items()}
                )
                leads.append(lead)
            except Exception as e:
                print(f"Error parsing row: {e}")
                continue
        
        return leads


class GoogleFormParser:
    """Parse Google Forms submissions"""
    
    @staticmethod
    def parse(data: Dict[str, Any]) -> Lead:
        """Parse Google Form webhook data"""
        return Lead(
            first_name=data.get('first_name', ''),
            last_name=data.get('last_name', ''),
            email=data.get('email', None),
            phone=data.get('phone', None),
            company_name=data.get('company', ''),
            source=LeadSource.GOOGLE_FORM,
            raw_data=data
        )


# =============================================================================
# ENRICHMENT SERVICES
# =============================================================================

class HunterEmailFinder:
    """Find emails using Hunter.io"""
    
    def __init__(self, api_key: str = Config.HUNTER_API_KEY):
        self.api_key = api_key
        self.base_url = 'https://api.hunter.io/v2'
    
    def find_email(
        self,
        first_name: str,
        last_name: str,
        domain: str
    ) -> Optional[str]:
        """Find email for person at company"""
        
        if not self.api_key:
            return None
        
        url = f"{self.base_url}/email-finder"
        params = {
            'domain': domain,
            'first_name': first_name,
            'last_name': last_name,
            'api_key': self.api_key
        }
        
        try:
            response = requests.get(url, params=params, timeout=10)
            if response.status_code == 200:
                data = response.json()
                return data.get('data', {}).get('email')
        except Exception as e:
            print(f"Hunter.io error: {e}")
        
        return None


class CompanyEnricher:
    """Enrich company data using Clearbit or similar"""
    
    def enrich(self, domain: str) -> Dict[str, Any]:
        """Get company information"""
        # TODO: Implement Clearbit or alternative
        # For now, return empty dict
        return {}


# =============================================================================
# LEAD SCORING
# =============================================================================

class LeadScorer:
    """Score leads using AI"""
    
    def __init__(self, llm: Ollama):
        self.llm = llm
        
        self.prompt = PromptTemplate(
            input_variables=['lead_data', 'icp_criteria'],
            template="""
You are a lead scoring expert. Score this lead from 0-100 based on how well 
they match the Ideal Customer Profile (ICP).

Ideal Customer Profile:
{icp_criteria}

Lead Data:
{lead_data}

Provide:
1. Score (0-100)
2. Priority tier (High: 70+, Medium: 50-69, Low: <50)
3. Reasons for score (list of factors)

Output as JSON:
{{
  "score": <number>,
  "priority": "<High|Medium|Low>",
  "reasons": ["reason 1", "reason 2", ...]
}}
"""
        )
        
        self.chain = LLMChain(llm=self.llm, prompt=self.prompt)
    
    def score(self, lead: Lead, icp_criteria: str = "") -> Lead:
        """Score a lead"""
        
        # Default ICP for B2B SaaS if none provided
        if not icp_criteria:
            icp_criteria = """
            - Tech companies with 10-500 employees
            - Decision makers (CTO, VP Engineering, CEO)
            - Series A-C funded or profitable
            - Growing fast (hiring, revenue growth)
            - Using modern tech stack
            - Located in Nigeria, US, UK, or Canada
            """
        
        # Prepare lead data for LLM
        lead_data = json.dumps({
            'name': lead.full_name,
            'title': lead.title,
            'company': lead.company_name,
            'company_size': lead.company_size,
            'industry': lead.company_industry,
            'location': lead.company_location,
            'seniority': lead.seniority
        }, indent=2)
        
        try:
            # Get AI scoring
            result = self.chain.run(
                lead_data=lead_data,
                icp_criteria=icp_criteria
            )
            
            # Parse JSON response
            # Remove markdown code blocks if present
            result = result.strip()
            if result.startswith('```'):
                result = result.split('```')[1]
                if result.startswith('json'):
                    result = result[4:]
            
            score_data = json.loads(result)
            
            # Update lead
            lead.lead_score = score_data.get('score', 0)
            lead.priority_tier = PriorityTier(score_data.get('priority', 'Low'))
            lead.score_reasons = score_data.get('reasons', [])
            
        except Exception as e:
            print(f"Scoring error: {e}")
            # Fallback to simple scoring
            lead.lead_score = self._simple_score(lead)
            lead.priority_tier = self._get_priority(lead.lead_score)
        
        return lead
    
    @staticmethod
    def _simple_score(lead: Lead) -> int:
        """Simple rule-based scoring fallback"""
        score = 0
        
        # Has email
        if lead.email:
            score += 20
        
        # Has phone
        if lead.phone:
            score += 10
        
        # Decision maker title
        decision_titles = ['cto', 'ceo', 'founder', 'vp', 'director', 'head']
        if lead.title and any(t in lead.title.lower() for t in decision_titles):
            score += 30
        
        # Company size
        if lead.company_size:
            if 10 <= lead.company_size <= 500:
                score += 20
        
        # Has LinkedIn
        if lead.linkedin_url:
            score += 10
        
        # Has company domain
        if lead.company_domain:
            score += 10
        
        return min(score, 100)
    
    @staticmethod
    def _get_priority(score: int) -> PriorityTier:
        """Convert score to priority tier"""
        if score >= Config.HIGH_PRIORITY_SCORE:
            return PriorityTier.HIGH
        elif score >= Config.MEDIUM_PRIORITY_SCORE:
            return PriorityTier.MEDIUM
        else:
            return PriorityTier.LOW


# =============================================================================
# HUBSPOT INTEGRATION
# =============================================================================

class HubSpotSync:
    """Sync leads to HubSpot CRM"""
    
    def __init__(self, api_key: str = Config.HUBSPOT_API_KEY):
        self.api_key = api_key
        self.base_url = Config.HUBSPOT_BASE_URL
        self.headers = {
            'Authorization': f'Bearer {api_key}',
            'Content-Type': 'application/json'
        }
    
    def create_contact(self, lead: Lead) -> Optional[str]:
        """Create contact in HubSpot"""
        
        if not self.api_key:
            print("No HubSpot API key configured")
            return None
        
        url = f"{self.base_url}/crm/v3/objects/contacts"
        
        # Build properties
        properties = {
            'firstname': lead.first_name,
            'lastname': lead.last_name,
            'email': lead.email,
            'phone': lead.phone,
            'company': lead.company_name,
            'website': lead.company_domain,
            'jobtitle': lead.title,
            'hs_lead_status': 'NEW',
        }
        
        # Add custom properties
        if lead.lead_score is not None:
            properties['lead_score__c'] = lead.lead_score
        if lead.priority_tier:
            properties['priority_tier__c'] = lead.priority_tier
        if lead.source:
            properties['lead_source__c'] = lead.source
        if lead.linkedin_url:
            properties['linkedin_url__c'] = lead.linkedin_url
        
        # Remove None values
        properties = {k: v for k, v in properties.items() if v is not None}
        
        data = {'properties': properties}
        
        try:
            response = requests.post(
                url,
                headers=self.headers,
                json=data,
                timeout=10
            )
            
            if response.status_code == 201:
                result = response.json()
                return result.get('id')
            else:
                print(f"HubSpot error: {response.status_code} - {response.text}")
                return None
                
        except Exception as e:
            print(f"HubSpot sync error: {e}")
            return None


# =============================================================================
# LEAD PROCESSOR
# =============================================================================

class LeadProcessor:
    """Main lead processing pipeline"""
    
    def __init__(self):
        self.db = Database()
        self.llm = Ollama(
            base_url=Config.OLLAMA_BASE_URL,
            model=Config.OLLAMA_MODEL,
            temperature=0.1
        )
        self.scorer = LeadScorer(self.llm)
        self.email_finder = HunterEmailFinder()
        self.company_enricher = CompanyEnricher()
        self.hubspot = HubSpotSync()
    
    def process_file(
        self,
        file_path: str,
        source_type: LeadSource = LeadSource.APOLLO
    ) -> List[Lead]:
        """
        Process a file of leads
        
        Args:
            file_path: Path to CSV file
            source_type: Type of source (apollo, linkedin, etc)
        
        Returns:
            List of processed leads
        """
        print(f"📁 Processing file: {file_path}")
        
        # Parse file based on source type
        if source_type == LeadSource.APOLLO:
            leads = ApolloParser.parse(file_path)
        elif source_type == LeadSource.LINKEDIN:
            leads = LinkedInParser.parse(file_path)
        else:
            raise ValueError(f"Unsupported source type: {source_type}")
        
        print(f"📊 Parsed {len(leads)} leads")
        
        # Process each lead
        processed = []
        for i, lead in enumerate(leads, 1):
            print(f"\n🔄 Processing lead {i}/{len(leads)}: {lead.full_name}")
            
            # Enrich
            lead = self.enrich_lead(lead)
            
            # Score
            lead = self.scorer.score(lead)
            
            print(f"   Score: {lead.lead_score} ({lead.priority_tier})")
            
            # Save to database
            lead_id = self.db.save_lead(lead)
            print(f"   💾 Saved to database (ID: {lead_id})")
            
            processed.append(lead)
        
        return processed
    
    def enrich_lead(self, lead: Lead) -> Lead:
        """Enrich a single lead"""
        
        # Find email if missing and we have company domain
        if not lead.email and lead.company_domain:
            email = self.email_finder.find_email(
                lead.first_name,
                lead.last_name,
                lead.company_domain
            )
            if email:
                lead.email = email
                print(f"   📧 Found email: {email}")
        
        # Enrich company data
        if lead.company_domain:
            company_data = self.company_enricher.enrich(lead.company_domain)
            # Update lead with company data
            # (implementation depends on enrichment service used)
        
        lead.enriched_at = datetime.utcnow()
        return lead
    
    def sync_to_hubspot(self, limit: int = 10):
        """Sync enriched leads to HubSpot"""
        leads = self.db.get_leads_to_sync(limit)
        
        print(f"\n🔄 Syncing {len(leads)} leads to HubSpot...")
        
        for lead_db in leads:
            # Convert DB model to Pydantic model
            lead = Lead(
                first_name=lead_db.first_name,
                last_name=lead_db.last_name,
                email=lead_db.email,
                phone=lead_db.phone,
                company_name=lead_db.company_name,
                company_domain=lead_db.company_domain,
                title=lead_db.title,
                source=LeadSource(lead_db.source),
                lead_score=lead_db.lead_score,
                priority_tier=PriorityTier(lead_db.priority_tier) if lead_db.priority_tier else None
            )
            
            # Sync to HubSpot
            contact_id = self.hubspot.create_contact(lead)
            
            if contact_id:
                self.db.mark_synced(lead_db.id, contact_id)
                print(f"✅ Synced: {lead.full_name} (HubSpot ID: {contact_id})")
            else:
                print(f"❌ Failed to sync: {lead.full_name}")


# =============================================================================
# CLI INTERFACE
# =============================================================================

def main():
    """Main CLI interface"""
    import argparse
    
    parser = argparse.ArgumentParser(
        description='Lead Generation System - Process and enrich leads'
    )
    
    parser.add_argument(
        'command',
        choices=['process', 'sync', 'score'],
        help='Command to run'
    )
    
    parser.add_argument(
        '--file',
        help='Path to CSV file to process'
    )
    
    parser.add_argument(
        '--source',
        choices=['apollo', 'linkedin'],
        default='apollo',
        help='Source type of the file'
    )
    
    parser.add_argument(
        '--limit',
        type=int,
        default=10,
        help='Number of leads to process'
    )
    
    args = parser.parse_args()
    
    processor = LeadProcessor()
    
    if args.command == 'process':
        if not args.file:
            print("❌ Error: --file is required for 'process' command")
            return
        
        source = LeadSource(args.source)
        leads = processor.process_file(args.file, source)
        
        print(f"\n✅ Successfully processed {len(leads)} leads")
        print(f"   High priority: {sum(1 for l in leads if l.priority_tier == PriorityTier.HIGH)}")
        print(f"   Medium priority: {sum(1 for l in leads if l.priority_tier == PriorityTier.MEDIUM)}")
        print(f"   Low priority: {sum(1 for l in leads if l.priority_tier == PriorityTier.LOW)}")
    
    elif args.command == 'sync':
        processor.sync_to_hubspot(args.limit)
    
    elif args.command == 'score':
        print("Rescoring leads...")
        # Implement rescoring logic
    
    print("\n✨ Done!")


if __name__ == '__main__':
    main()
