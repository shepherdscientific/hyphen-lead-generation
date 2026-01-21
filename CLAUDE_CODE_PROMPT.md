# Claude Code Prompt: AI Lead Generation System

## Context

I need a production-ready lead generation system that:
1. Processes leads from multiple sources (Apollo CSV, LinkedIn, Google Forms)
2. Uses local LLMs via Ollama for enrichment and scoring
3. Stores leads in PostgreSQL
4. Syncs to HubSpot CRM
5. Handles all data normalization (especially Nigerian phone numbers)
6. Self-healing and adaptable to changing data formats

## Technical Requirements

**Stack:**
- Python 3.11+
- PostgreSQL database
- Ollama (Qwen 2.5 Coder 32B running locally)
- LangChain for AI orchestration
- SQLAlchemy for ORM
- Pydantic for data validation
- FastAPI for REST API (bonus)

**Environment:**
- Mac Mini M4 Pro (64GB RAM, 20 GPU cores)
- Ollama installed at http://localhost:11434
- PostgreSQL running locally
- HubSpot Private App with Bearer token

## Core Features Needed

### 1. Data Models

**Lead Model:**
```python
- Identity: first_name, last_name, email, phone
- Company: name, domain, size, industry, location
- Professional: title, seniority, department
- Metadata: source, source_url, linkedin_url
- Scoring: lead_score (0-100), priority_tier (High/Medium/Low), score_reasons
- Timestamps: created_at, enriched_at, synced_to_hubspot_at
```

**Support these sources:**
- LeadSource enum: APOLLO, LINKEDIN, GOOGLE_FORM, MANUAL, SCRAPED

**Priority tiers:**
- HIGH: Score >= 70
- MEDIUM: Score 50-69
- LOW: Score < 50

### 2. Data Parsers

**Apollo Parser:**
- Parse Apollo.io CSV exports
- Column mappings: "First Name", "Last Name", "Email", "Company", "Title", "# Employees", etc.
- Handle missing/optional fields gracefully

**LinkedIn Parser:**
- Parse LinkedIn export CSVs
- Extract name (split into first/last)
- Company, position, profile URL

**Google Form Parser:**
- Parse webhook JSON data
- Handle KLS-style education form data

**All parsers must:**
- Return list of Lead objects
- Handle errors gracefully (skip bad rows)
- Log parsing issues

### 3. Data Normalization

**Phone Numbers:**
```python
# Nigerian phone number normalization
Input: "0803 456 7890" → Output: "+234 803 456 7890"
Input: "234803456790" → Output: "+234 803 456 7890"
Input: "+234-803-456-7890" → Output: "+234 803 456 7890"

# Remove all non-digit characters except +
# Handle leading 0 (Nigerian format)
# Add +234 if no country code
# Format with spaces for readability
```

**Email:**
- Lowercase
- Trim whitespace
- Validate format
- Return None if invalid

**Names:**
- Trim whitespace
- Handle multiple word last names
- Generate full_name from first + last if not provided

### 4. Lead Enrichment

**Email Finding (Hunter.io integration):**
```python
class HunterEmailFinder:
    def find_email(first_name: str, last_name: str, domain: str) -> Optional[str]:
        # Call Hunter.io API
        # Return email if found with confidence > 50%
        # Handle rate limits gracefully
        # Return None if not found
```

**Company Enrichment (optional):**
- Clearbit integration (if implemented)
- Or stub for future implementation

### 5. AI Lead Scoring

**Use Ollama LLM for intelligent scoring:**

```python
class LeadScorer:
    # Initialize with Ollama LLM
    # Qwen 2.5 Coder 32B model
    
    def score(lead: Lead, icp_criteria: str) -> Lead:
        # Use LangChain LLMChain
        # Prompt: Compare lead to ICP criteria
        # Output: JSON with score, priority, reasons
        # Update lead object with scoring results
        # Fallback to rule-based scoring if AI fails
```

**Default ICP Criteria:**
```
- Tech companies with 10-500 employees
- Decision makers (CTO, VP Engineering, CEO, Founder)
- Series A-C funded or profitable
- Modern tech stack
- Located in Nigeria, US, UK, or Canada
- Growing (hiring, expanding)
```

**Scoring factors:**
- Has email (+20 points)
- Has phone (+10 points)
- Decision maker title (+30 points)
- Right company size 10-500 (+20 points)
- Has LinkedIn (+10 points)
- Has company domain (+10 points)

**Rule-based fallback if AI fails.**

### 6. Database Layer

**Using SQLAlchemy:**
```python
class Database:
    # PostgreSQL connection
    # LeadDB model (SQLAlchemy ORM)
    
    def save_lead(lead: Lead) -> int:
        # Save to database
        # Return lead ID
        # Handle duplicates (upsert by email)
    
    def get_leads_to_enrich(limit: int) -> List[LeadDB]:
        # Get leads where enriched_at IS NULL
    
    def get_leads_to_sync(limit: int) -> List[LeadDB]:
        # Get leads where synced_to_hubspot_at IS NULL
        # And enriched_at IS NOT NULL
    
    def mark_enriched(lead_id: int):
        # Set enriched_at = now()
    
    def mark_synced(lead_id: int, hubspot_id: str):
        # Set synced_to_hubspot_at = now()
        # Set hubspot_contact_id = hubspot_id
```

**Schema:**
```sql
CREATE TABLE leads (
    id SERIAL PRIMARY KEY,
    first_name VARCHAR,
    last_name VARCHAR,
    email VARCHAR UNIQUE,
    phone VARCHAR,
    company_name VARCHAR,
    company_domain VARCHAR,
    title VARCHAR,
    source VARCHAR,
    lead_score INTEGER,
    priority_tier VARCHAR,
    created_at TIMESTAMP,
    enriched_at TIMESTAMP,
    synced_to_hubspot_at TIMESTAMP,
    hubspot_contact_id VARCHAR,
    raw_data JSONB
);

CREATE INDEX idx_email ON leads(email);
CREATE INDEX idx_company ON leads(company_name);
CREATE INDEX idx_source ON leads(source);
```

### 7. HubSpot Integration

**Using Private App (Bearer token):**
```python
class HubSpotSync:
    # Bearer token authentication
    # Base URL: https://api.hubapi.com
    
    def create_contact(lead: Lead) -> Optional[str]:
        # POST /crm/v3/objects/contacts
        # Map Lead fields to HubSpot properties
        # Handle custom properties (lead_score__c, priority_tier__c, etc.)
        # Return contact ID if successful
        # Return None if failed
        # Log errors
```

**Property mappings:**
```python
{
    'firstname': lead.first_name,
    'lastname': lead.last_name,
    'email': lead.email,
    'phone': lead.phone,
    'company': lead.company_name,
    'website': lead.company_domain,
    'jobtitle': lead.title,
    'hs_lead_status': 'NEW',
    'lead_score__c': lead.lead_score,
    'priority_tier__c': lead.priority_tier,
    'lead_source__c': lead.source,
    'linkedin_url__c': lead.linkedin_url
}
```

### 8. Main Pipeline

**LeadProcessor class:**
```python
class LeadProcessor:
    def __init__(self):
        # Initialize all components
        self.db = Database()
        self.llm = Ollama(model="qwen2.5-coder:32b")
        self.scorer = LeadScorer(self.llm)
        self.email_finder = HunterEmailFinder()
        self.hubspot = HubSpotSync()
    
    def process_file(file_path: str, source_type: LeadSource) -> List[Lead]:
        # 1. Parse file based on source type
        # 2. For each lead:
        #    a. Enrich (find email if missing)
        #    b. Score using AI
        #    c. Save to database
        # 3. Return processed leads
        # 4. Print summary (high/medium/low counts)
    
    def enrich_lead(lead: Lead) -> Lead:
        # Find email if missing (Hunter.io)
        # Enrich company data (optional)
        # Set enriched_at timestamp
        # Return enriched lead
    
    def sync_to_hubspot(limit: int = 10):
        # Get leads ready to sync
        # For each lead:
        #   - Create HubSpot contact
        #   - Mark as synced in database
        # Print sync results
```

### 9. CLI Interface

**Commands:**
```bash
# Process Apollo CSV
python lead_gen.py process --file apollo_leads.csv --source apollo

# Process LinkedIn export
python lead_gen.py process --file linkedin_export.csv --source linkedin

# Sync leads to HubSpot
python lead_gen.py sync --limit 50

# Rescore existing leads
python lead_gen.py score --limit 100
```

**Using argparse for CLI.**

### 10. Configuration

**Environment variables:**
```bash
# .env file
DATABASE_URL=postgresql://localhost/leads
OLLAMA_BASE_URL=http://localhost:11434
OLLAMA_MODEL=qwen2.5-coder:32b
HUBSPOT_API_KEY=pat-na2-xxxxx
HUNTER_API_KEY=your_hunter_key
```

**Config class to load env vars.**

## Code Quality Requirements

1. **Type hints everywhere** (use typing module)
2. **Docstrings for all classes and methods**
3. **Error handling** (try/except with logging)
4. **Validation** (use Pydantic validators)
5. **Clean separation of concerns**
6. **Single responsibility principle**
7. **DRY (Don't Repeat Yourself)**

## File Structure

```
lead_gen_system/
├── lead_gen.py              # Main script (single file for now)
├── requirements.txt         # Dependencies
├── .env.example            # Example environment variables
├── README.md               # Usage instructions
└── tests/
    ├── test_parsers.py
    ├── test_scoring.py
    └── test_hubspot.py
```

## Dependencies

```
# requirements.txt
langchain>=0.1.0
langchain-community>=0.0.10
ollama>=0.1.0
sqlalchemy>=2.0.0
psycopg2-binary>=2.9.0
pydantic>=2.0.0
python-dotenv>=1.0.0
requests>=2.31.0
pandas>=2.0.0
httpx>=0.25.0
```

## Testing Data

**Provide sample CSV for testing:**
```csv
First Name,Last Name,Email,Phone,Company,Website,Title,# Employees,Industry,City
John,Doe,john@example.com,08012345678,TechCorp,techcorp.com,CTO,50,Technology,Lagos
Jane,Smith,,08087654321,FinTech Inc,fintech.com,CEO,100,Financial Services,Abuja
```

## Special Requirements

1. **Nigerian phone numbers:** Must handle all formats correctly
2. **Missing data:** Must be resilient to missing fields
3. **Duplicate handling:** Upsert by email (update if exists)
4. **Async operations:** Use asyncio where appropriate for API calls
5. **Rate limiting:** Respect API rate limits (Hunter.io, HubSpot)
6. **Logging:** Log all operations for debugging
7. **Progress indicators:** Show progress during processing

## Success Criteria

The system should:
1. ✅ Process 100 leads from Apollo CSV in < 5 minutes
2. ✅ Correctly normalize all phone numbers
3. ✅ Score leads intelligently using AI
4. ✅ Sync to HubSpot without errors
5. ✅ Handle missing data gracefully
6. ✅ Log all operations clearly
7. ✅ Be maintainable and extendable

## Example Usage

```python
# Initialize processor
processor = LeadProcessor()

# Process Apollo CSV
leads = processor.process_file('apollo_export.csv', LeadSource.APOLLO)

# Results:
# 📁 Processing file: apollo_export.csv
# 📊 Parsed 25 leads
#
# 🔄 Processing lead 1/25: John Doe
#    📧 Found email: john@example.com
#    Score: 85 (High)
#    💾 Saved to database (ID: 1)
#
# [... processing continues ...]
#
# ✅ Successfully processed 25 leads
#    High priority: 8
#    Medium priority: 12
#    Low priority: 5

# Sync to HubSpot
processor.sync_to_hubspot(limit=25)

# 🔄 Syncing 25 leads to HubSpot...
# ✅ Synced: John Doe (HubSpot ID: 12345678)
# ✅ Synced: Jane Smith (HubSpot ID: 87654321)
# [...]
# ✨ Done!
```

## Additional Notes

- **Ollama must be running** before starting
- **PostgreSQL must be running** and database created
- **HubSpot custom properties** must exist (lead_score__c, priority_tier__c, etc.)
- **Hunter.io API key** is optional (will skip email finding if not provided)
- **Start simple,** add complexity later (no need for FastAPI in v1)

## Build This

Please create a complete, production-ready implementation following these specifications. Use best practices, include comprehensive error handling, and make it maintainable.

Focus on:
1. **Robustness** - Handle errors gracefully
2. **Clarity** - Code should be self-documenting
3. **Extensibility** - Easy to add new parsers/enrichers
4. **Performance** - Efficient batch processing

Thank you!
