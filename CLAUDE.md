# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Common Development Tasks

### Setup
1. Create virtual environment: `python3 -m venv venv`
2. Activate: `source venv/bin/activate`
3. Install dependencies: `pip install -r requirements.txt`
4. Create database: `createdb leads`
5. Setup environment: `cp .env.example .env`
6. Download Ollama model: `ollama pull qwen2.5-coder:32b`

### Testing
- Run full test suite: `python -m pytest`
- Run single test: `python -m pytest tests/test_<filename>.py::test_<name>`

### Linting
- Format code: `black .`
- Check style: `flake8`

## High-Level Architecture

This is an AI-powered lead generation system using:
1. Python backend with virtual environment isolation
2. PostgreSQL database (createdb) for lead storage
3. Local Ollama-hosted Qwen2.5-Coder LLM (32b) for generation

The architecture follows a simple pattern:
1. Command-line interface (lead_gen_system.py)
2. Database interactions through SQLAlchemy
3. LLM integration via Ollama API

Key directory structure:
```text
├── venv/                  # Virtual environment
├── lead_gen_system.py     # Main CLI
├── requirements.txt       # Python dependencies
├── .env                   # Environment variables
├── data/                  # Database files
├── models/                # LLM interaction code
└── tests/                 # Unit tests
```

Database operations are isolated in `data/`, and LLM interactions are encapsulated in `models/`. The CLI handles orchestration between components.