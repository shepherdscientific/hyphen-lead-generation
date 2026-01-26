# AI-Native Lead Generation Architecture
## Leveraging Your M4 Pro + Ollama

---

## The Vision

**Instead of:**
```
❌ Manual CSV exports → n8n workflows → brittle processing
```

**Build:**
```
✅ Prompt → AI Agent → Leads Database → Auto-enrichment → CRM
```

**Example:**
```
You: "Find me 50 fintech companies in Nigeria that raised Series A in 
      the last 2 years and have 10-50 employees"

AI Agent:
  1. Searches LinkedIn, Crunchbase, local sources
  2. Validates against criteria
  3. Enriches with contact data
  4. Scores leads
  5. Adds to HubSpot
  6. Generates outreach sequences

Result: 50 qualified leads in HubSpot with full context
```

---

## Architecture Overview

```
┌─────────────────────────────────────────────────────────────┐
│                     USER INTERFACE                           │
│  Terminal / Web UI / Chat Interface                         │
└─────────────────────────────────────────────────────────────┘
                            ↓
┌─────────────────────────────────────────────────────────────┐
│                    AI ORCHESTRATOR                           │
│  Local LLM (Ollama) on Mac Mini M4 Pro                     │
│  - Qwen 2.5 Coder 32B (for tool use)                       │
│  - Llama 3.3 70B (for reasoning)                           │
└─────────────────────────────────────────────────────────────┘
                            ↓
        ┌───────────────────┼───────────────────┐
        ↓                   ↓                   ↓
┌──────────────┐   ┌──────────────┐   ┌──────────────┐
│   SEARCH     │   │  ENRICHMENT  │   │    OUTPUT    │
│   TOOLS      │   │    TOOLS     │   │    TOOLS     │
└──────────────┘   └──────────────┘   └──────────────┘
        ↓                   ↓                   ↓
┌──────────────┐   ┌──────────────┐   ┌──────────────┐
│ - LinkedIn   │   │ - Apollo API │   │ - HubSpot    │
│ - Crunchbase │   │ - Hunter.io  │   │ - PostgreSQL │
│ - Google     │   │ - Clearbit   │   │ - Airtable   │
│ - Local DBs  │   │ - Enrichment │   │ - CSV        │
└──────────────┘   └──────────────┘   └──────────────┘
```

---

## Stack Recommendation

### Core Components

**1. AI Orchestration: LangChain + Ollama**
```python
# Why:
- Local LLMs (no API costs, full privacy)
- Tool/function calling built-in
- Agent framework for complex workflows
- Python ecosystem (robust, testable)

# Models to use:
- Qwen 2.5 Coder 32B: Tool use, structured output
- Llama 3.3 70B: Complex reasoning
- Both run on your M4 Pro easily
```

**2. Data Storage: PostgreSQL + Vector DB**
```python
# Why:
- PostgreSQL: Reliable, mature, SQL
- pgvector extension: Semantic search
- Local on Mac Mini
- No vendor lock-in

# Use cases:
- Store all leads
- Semantic search ("similar companies to X")
- Historical tracking
- Analytics
```

**3. Task Queue: Celery + Redis**
```python
# Why:
- Background processing
- Retry logic built-in
- Scale across both Macs
- Production-proven

# Use cases:
- Enrichment tasks (slow)
- Batch processing
- Scheduled jobs
```

**4. Web Interface: FastAPI + Streamlit**
```python
# Why:
- FastAPI: Modern Python API framework
- Streamlit: Quick dashboards
- Both lightweight
- Easy to deploy

# Use cases:
- API for integrations
- Dashboard for monitoring
- Chat interface for prompts
```

---

## Component 1: AI Lead Generation Agent

### How It Works

**User prompt:**
```
"Find Nigerian fintech companies, Series A, 10-50 employees"
```

**Agent workflow:**
```python
1. UNDERSTAND
   - Parse criteria
   - Validate requirements
   - Plan search strategy

2. SEARCH
   - LinkedIn: Search companies
   - Crunchbase: Filter by funding
   - Google: Validate existence
   - Cross-reference results

3. FILTER
   - Apply size criteria (10-50 employees)
   - Check funding stage (Series A)
   - Verify location (Nigeria)
   - Remove duplicates

4. ENRICH
   - Find decision makers (LinkedIn)
   - Get contact info (Apollo/Hunter)
   - Company website, tech stack
   - Social media presence

5. SCORE
   - Lead quality (0-100)
   - Fit with your ICP
   - Contact data completeness
   - Recent activity signals

6. OUTPUT
   - Save to PostgreSQL
   - Push to HubSpot
   - Generate outreach sequences
   - Create summary report
```

---

## Component 2: Multi-Source Lead Processing

### Unified Data Pipeline

**Instead of separate workflows for each source:**

```python
# Single pipeline handles ALL sources

class LeadProcessor:
    """
    Processes leads from ANY source into unified format
    """
    
    def process(self, source: str, data: Any) -> Lead:
        """
        Universal lead processing
        
        Supports:
        - Apollo CSV
        - LinkedIn export
        - Google Sheets
        - Manual entry
        - API calls
        - Web scraping results
        """
        
        # 1. Detect source format
        format = self.detect_format(data)
        
        # 2. Parse into standard schema
        raw_lead = self.parse(data, format)
        
        # 3. Normalize data
        normalized = self.normalize(raw_lead)
        
        # 4. Enrich missing fields
        enriched = self.enrich(normalized)
        
        # 5. Score lead
        scored = self.score(enriched)
        
        # 6. Return unified Lead object
        return scored

# Use it:
processor = LeadProcessor()

# Apollo CSV
leads_apollo = processor.process('apollo', apollo_csv)

# LinkedIn scrape
leads_linkedin = processor.process('linkedin', linkedin_data)

# Manual entry
leads_manual = processor.process('manual', form_data)

# All become same format!
```

**Benefits:**
- ✅ One codebase
- ✅ Easy to add new sources
- ✅ Consistent normalization
- ✅ Version controllable
- ✅ Testable

---

## Component 3: Apollo Integration

### How Apollo Actually Works

**Apollo.io is:**
- B2B contact database (275M+ contacts)
- Company intelligence platform
- Email finder and verifier
- Outreach sequences

**Free tier:**
- 25 email credits/month
- Unlimited searches
- Basic filters
- CSV export (25 at a time)

**Paid tiers:**
```
Basic: $49/month
  - 500 email credits
  - Better filters
  - Chrome extension

Professional: $99/month
  - 1000 credits
  - API access (IMPORTANT!)
  - Sequences
  - Integrations

Organization: $149/month
  - 2000 credits
  - Team features
  - Advanced filters
```

**API is KEY:**
```python
# With API, you can:
import apollo

# Search companies
companies = apollo.search_companies(
    q_organization_locations=['Nigeria'],
    organization_num_employees_ranges=['10,50'],
    organization_latest_funding_stage_cd=['series_a']
)

# Get contacts
contacts = apollo.get_contacts(
    organization_ids=[c.id for c in companies],
    person_titles=['CTO', 'VP Engineering', 'CEO']
)

# Enrich in bulk
enriched = apollo.enrich_people(
    contact_ids=[c.id for c in contacts]
)

# No CSV export/import needed!
```

**Recommended approach:**
- Use API (Professional tier, $99/mo)
- Or build web scraper (free but slower)
- Or use alternative: Hunter.io, Clearbit, RocketReach

---

## Component 4: Local LLM Setup

### Models to Run on M4 Pro

**Your M4 Pro 64GB can handle:**

**1. Qwen 2.5 Coder 32B** ⭐ PRIMARY
```bash
# Best for tool use and structured output
ollama pull qwen2.5-coder:32b

# Performance on M4 Pro:
- Speed: ~20-30 tokens/sec
- RAM: ~35GB
- Quality: Excellent for coding, tool calling
```

**2. Llama 3.3 70B** (If needed)
```bash
# For complex reasoning
ollama pull llama3.3:70b

# Performance on M4 Pro:
- Speed: ~10-15 tokens/sec
- RAM: ~55GB
- Quality: GPT-4 level reasoning
```

**3. Mistral Small** (Fast alternative)
```bash
# For speed-critical tasks
ollama pull mistral-small:latest

# Performance:
- Speed: ~50-60 tokens/sec
- RAM: ~15GB
- Quality: Good for most tasks
```

**Recommendation:**
- **Primary:** Qwen 2.5 Coder 32B (best balance)
- **Backup:** Mistral Small (for speed)
- **Reasoning:** Use Claude API when needed (complex planning)

---

## Component 5: Example Implementation

### Prompt-to-Leads System

**File structure:**
```
lead_generation/
├── agents/
│   ├── search_agent.py      # AI search orchestrator
│   ├── enrichment_agent.py  # Data enrichment
│   └── scoring_agent.py     # Lead scoring
├── tools/
│   ├── apollo.py            # Apollo integration
│   ├── linkedin.py          # LinkedIn scraper
│   ├── hunter.py            # Email finder
│   └── clearbit.py          # Company enrichment
├── models/
│   ├── lead.py              # Lead data model
│   ├── company.py           # Company data model
│   └── contact.py           # Contact data model
├── storage/
│   ├── postgres.py          # Database layer
│   └── hubspot.py           # CRM sync
├── api/
│   ├── main.py              # FastAPI app
│   └── routes.py            # API endpoints
├── ui/
│   └── dashboard.py         # Streamlit dashboard
└── cli/
    └── generate.py          # Command line interface
```

**Example usage:**

```bash
# Command line
python cli/generate.py "Find Nigerian fintech, Series A, 10-50 people"

# Output:
Searching... ━━━━━━━━━━━━━━━━━━━━━━━━━━ 100%
Found 127 companies matching criteria
Filtering... ━━━━━━━━━━━━━━━━━━━━━━━━━━ 100%
67 companies pass filters
Enriching... ━━━━━━━━━━━━━━━━━━━━━━━━━━ 100%
Found contacts for 54 companies
Scoring... ━━━━━━━━━━━━━━━━━━━━━━━━━━━ 100%
Identified 31 high-quality leads

Top 5 leads:
1. Flutterwave (Score: 95)
   - CEO: Olugbenga Agboola
   - Email: gb@flutterwave.com
   - Reason: Series C, 200+ employees, perfect fit

2. Paystack (Score: 92)
   - CTO: Ezra Olubi
   - Email: ezra@paystack.com
   - Reason: Acquired by Stripe, strong tech team

[...]

Added 31 leads to HubSpot
Generated outreach sequences
Summary saved to reports/2026-01-11_fintech_search.pdf
```

---

## Real Code Example

### Simple Lead Generation Agent

```python
# lead_agent.py

from langchain.agents import initialize_agent, Tool
from langchain.llms import Ollama
from langchain.prompts import PromptTemplate
import asyncio

class LeadGenerationAgent:
    """
    AI agent that generates leads from natural language prompts
    """
    
    def __init__(self):
        # Initialize Ollama with Qwen 2.5 Coder
        self.llm = Ollama(
            model="qwen2.5-coder:32b",
            temperature=0.1
        )
        
        # Define tools agent can use
        self.tools = [
            Tool(
                name="search_linkedin",
                func=self.search_linkedin,
                description="Search LinkedIn for companies matching criteria"
            ),
            Tool(
                name="search_crunchbase",
                func=self.search_crunchbase,
                description="Search Crunchbase for funding/company data"
            ),
            Tool(
                name="enrich_contact",
                func=self.enrich_contact,
                description="Find email and contact info for a person"
            ),
            Tool(
                name="save_to_crm",
                func=self.save_to_crm,
                description="Save lead to HubSpot CRM"
            )
        ]
        
        # Initialize agent
        self.agent = initialize_agent(
            self.tools,
            self.llm,
            agent="zero-shot-react-description",
            verbose=True
        )
    
    async def generate_leads(self, prompt: str):
        """
        Main entry point - takes natural language prompt,
        returns qualified leads
        """
        
        # Let AI agent figure out the workflow
        result = await self.agent.arun(f"""
        Generate leads based on this request:
        {prompt}
        
        Your workflow:
        1. Parse the criteria from the request
        2. Search for companies matching criteria
        3. Find decision makers at those companies
        4. Enrich with contact information
        5. Score each lead (0-100)
        6. Save high-scoring leads (>70) to CRM
        7. Return summary
        """)
        
        return result
    
    def search_linkedin(self, criteria: str):
        """Search LinkedIn - implement with Selenium/Playwright"""
        # Your implementation
        pass
    
    def search_crunchbase(self, criteria: str):
        """Search Crunchbase - use their API"""
        # Your implementation
        pass
    
    def enrich_contact(self, name: str, company: str):
        """Find email using Hunter.io or Apollo"""
        # Your implementation
        pass
    
    def save_to_crm(self, lead_data: dict):
        """Save to HubSpot"""
        # Your implementation
        pass

# Use it:
agent = LeadGenerationAgent()
leads = await agent.generate_leads(
    "Find Nigerian fintech companies, Series A, 10-50 employees"
)
```

---

## Benefits of This Approach

### vs n8n

**n8n:**
```
❌ Visual workflows (hard to version control)
❌ Security vulnerabilities (CVE-2025-68613)
❌ Brittle (manual changes for each source)
❌ Limited testing
❌ Vendor lock-in
```

**This approach:**
```
✅ Pure Python (git-friendly)
✅ No security issues (you control everything)
✅ Flexible (one pipeline handles all sources)
✅ Fully testable
✅ No vendor lock-in
✅ Local AI (no API costs)
✅ Leverages your hardware
```

---

## Apollo Alternatives

### If You Don't Want to Pay $99/month

**1. Hunter.io** (Email finder)
- Free: 25 searches/month
- $49/mo: 500 searches
- Best for email finding

**2. RocketReach**
- Free: 5 lookups/month
- $49/mo: 170 lookups
- Good for phone numbers too

**3. Clearbit** (Enrichment)
- Pay per lookup (~$0.50)
- No monthly fee
- Good data quality

**4. Scraping + DIY**
- Free (just your time)
- Full control
- Need to build scrapers
- Slower but works

**5. PhantomBuster** (Automation)
- $56/mo: Cloud automation
- LinkedIn, Twitter scrapers
- Pre-built extractors

**Recommendation:**
- Start with free tiers + scraping
- Upgrade to Apollo Pro ($99) when proven
- ROI: 10 deals from better leads = pays for itself

---

## Hardware Utilization Strategy

### Mac Mini M4 Pro (Primary Workhorse)

**Use for:**
```
1. Ollama LLM hosting
   - Qwen 2.5 Coder 32B (always running)
   - Fast inference server
   
2. PostgreSQL database
   - All leads data
   - Vector embeddings
   
3. Redis + Celery
   - Background job processing
   - Task queue
   
4. FastAPI server
   - REST API
   - Webhook receiver
   
5. Long-running agents
   - Search agents (hours)
   - Enrichment jobs (background)
```

**Why M4 Pro:**
- 64GB RAM: Can run large models + database
- 20 GPU cores: Fast LLM inference
- Always-on: Server role

---

### iMac (Development + UI)

**Use for:**
```
1. Development environment
   - VSCode
   - Testing
   - Git
   
2. Streamlit dashboard
   - Visual interface
   - Monitoring
   
3. Ollama (smaller models)
   - Mistral Small for quick tests
   - Development iterations
   
4. Client work
   - Presentations
   - Demos
```

**Why iMac:**
- 8GB RAM: Enough for dev work
- Good display: UI development
- Your daily driver: Convenient

---

## Implementation Roadmap

### Phase 1: Foundation (Week 1)

**Goals:**
- Replace n8n brittleness
- Get basic automation working
- Prove local LLM approach

**Tasks:**
```
Day 1-2: Setup
  - PostgreSQL on Mac Mini
  - Ollama + Qwen 2.5 Coder
  - Python environment
  - Git repo structure

Day 3-4: Core Pipeline
  - Lead data model
  - Apollo CSV importer
  - Normalization logic
  - HubSpot sync

Day 5-7: Basic Agent
  - LangChain setup
  - Simple search tools
  - CLI interface
  - Test with manual prompts
```

**Deliverable:** Python script that processes Apollo CSV better than n8n

---

### Phase 2: AI Agent (Week 2)

**Goals:**
- Prompt-to-leads working
- Multi-source support
- Automated enrichment

**Tasks:**
```
Day 8-10: Search Tools
  - LinkedIn scraper (Selenium)
  - Crunchbase API integration
  - Google search automation
  - Cross-referencing logic

Day 11-12: Enrichment
  - Email finding (Hunter.io)
  - Company data (Clearbit)
  - Validation logic
  - Scoring algorithm

Day 13-14: Agent Integration
  - Tool calling working
  - Multi-step workflows
  - Error handling
  - Batch processing
```

**Deliverable:** Natural language → qualified leads in HubSpot

---

### Phase 3: Production (Week 3)

**Goals:**
- Robust, maintainable
- Dashboard
- KLS integration

**Tasks:**
```
Day 15-17: Infrastructure
  - Background jobs (Celery)
  - Scheduled tasks
  - Monitoring
  - Error alerting

Day 18-19: UI
  - Streamlit dashboard
  - FastAPI endpoints
  - Webhook handlers

Day 20-21: KLS Integration
  - Google Forms → Agent
  - Auto-enrichment
  - Deal creation
  - Testing
```

**Deliverable:** Production system replacing all n8n workflows

---

## Cost Comparison

### Current Approach (n8n)

```
n8n Cloud: $20-50/month
Apollo (manual CSV): Free (limited)
Time spent on maintenance: 5-10 hours/month
Security risk: HIGH (CVE-2025-68613)

Total: $20-50/month + high maintenance + security issues
```

---

### Proposed Approach

```
Hardware: Already owned ✅
Ollama: Free ✅
PostgreSQL: Free ✅
Python ecosystem: Free ✅

Optional:
Apollo API: $99/month (if needed)
Hunter.io: $49/month (if needed)
OR: Build scrapers: Free (your time)

Total: $0-150/month, zero maintenance overhead, no security issues
```

**Better, cheaper, more secure!**

---

## Next Steps

### This Week

1. **Decide on n8n:**
   - Keep for KLS only? (short-term)
   - Migrate to Python? (recommended)
   - Timeline?

2. **Apollo decision:**
   - Try free tier + scraping first?
   - Upgrade to Pro ($99) when proven?
   - Use alternatives?

3. **Start local setup:**
   - PostgreSQL on Mac Mini
   - Test Qwen 2.5 Coder performance
   - Build simple lead processor

4. **Prove concept:**
   - Process one Apollo CSV with Python
   - Better than n8n?
   - Measure time saved

### Want me to:**
- Build the Python lead processor?
- Set up the Mac Mini stack?
- Create the AI agent scaffolding?
- Compare Apollo vs alternatives in detail?

**Let me know where you want to start!** 🚀
