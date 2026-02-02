## Problem Statement

The current lead generation workflow relies on brittle n8n workflows with CSV exports, leading to:
```
❌ Manual CSV exports → n8n workflows → brittle processing
```
This results in:
- High maintenance overhead
- Security vulnerabilities (CVE-2025-68613 in n8n)
- Inflexible architecture
- Poor testability

## Solution Overview

Replace the n8n-based workflow with an AI-native lead generation system:
```
✅ Prompt → AI Agent → Leads Database → Auto-enrichment → CRM
```
Key architectural components:
1. **LangChain + Ollama orchestration**
2. **PostgreSQL + vector DB**
3. **Celery + Redis for background tasks**
4. **FastAPI + Streamlit for interface**

## Technical Requirements

### Core Stack
1. **AI Orchestration**
   - Qwen 2.5 Coder 32B (tool use, structured output)
   - Llama 3.3 70B (complex reasoning)
   - LangChain agent framework

2. **Data Storage**
   - PostgreSQL with pgvector extension
   - Local deployment on Mac Mini

3. **Task Processing**
   - Celery + Redis
   - Background task queue

4. **Web Interface**
   - FastAPI for API endpoints
   - Streamlit for dashboard

### Lead Generation Agent
1. **Workflow Stages**:
   ```python
   1. UNDERSTAND
   2. SEARCH
   3. FILTER
   4. ENRICH
   5. SCORE
   6. OUTPUT
   ````
2. **Tools Required**:
   - LinkedIn scraper (Selenium)
   - Crunchbase API integration
   - Apollo/Hunter.io for contact enrichment

## Implementation Plan

### Phase 1: Foundation (Week 1)
1. **Mac Mini Setup**
   - `python3 -m venv venv`
   - `createdb leads`
   - `ollama pull qwen2.5-coder:32b`
   - `pip install -r requirements.txt`

2. **Core Pipeline**
   - Create `lead.py` data model
   - Implement Apollo CSV importer in `tools/apollo.py`
   - Build PostgreSQL ORM in `storage/postgres.py`
   - Create HubSpot sync in `storage/hubspot.py`

3. **CLI Interface**
   - Implement `cli/generate.py`
   - Add basic validation logic

### Phase 2: AI Agent (Week 2)
1. **Search Tools**
   - Develop `tools/linkedin.py` scraper
   - Implement Crunchbase API in `tools/crunchbase.py`
   - Add Google search automation

2. **Enrichment System**
   - Create `tools/hunter.py` for email finding
   - Build Clearbit integration in `tools/clearbit.py`
   - Develop scoring algorithm in `scoring_agent.py`

3. **Agent Integration**
   - Implement LangChain agent in `agents/search_agent.py`
   - Add multi-step workflow logic
   - Create error handling system

### Phase 3: Production (Week 3)
1. **Background Processing**
   - Configure Celery in `tasks/celery.py`
   - Add task scheduling
   - Implement error alerting

2. **Dashboard**
   - Develop FastAPI endpoints in `api/main.py`
   - Create Streamlit dashboard in `ui/dashboard.py`

3. **KLS Integration**
   - Add Google Forms webhook in `api/webhooks.py`
   - Build auto-enrichment system
   - Implement deal creation logic

## Testing Strategy

1. **Unit Tests**
   - Test individual tools with `pytest tests/test_apollo.py`
   - Validate search results formatting

2. **Integration Tests**
   - Run full workflow from prompt to CRM in `tests/test_end_to_end.py`
   - Test Apollo CSV conversion in `tests/test_csv_importer.py`

3. **Manual Verification**
   - Run validation commands:
     ```bash
     python -m pytest
     psql leads -c "SELECT * FROM leads"
     streamlit run ui/dashboard.py
     ```

## Files to Modify
1. Create new files:
   - `agents/search_agent.py`
   - `tools/linkedin.py`
   - `storage/postgres.py`

2. Update:
   - `requirements.txt`
   - `.env`
   - `README.md`

3. Remove:
   - `n8n/workflows/leads_workflow.json`

## Dependencies
- Apollo API ($99/month or build scraper)
- PostgreSQL installation
- Mac Mini as primary server

## Validation
1. Run initial validation:
   ```bash
   # Test basic database connection
   python -c "import psycopg2; psycopg2.connect(database='leads')"

   # Verify Ollama model
   ollama list | grep qwen2.5-coder

   # Run simple lead processor test
   python cli/generate.py "Test prompt"
   ```
