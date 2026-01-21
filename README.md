# Lead Generation System

AI-powered lead generation using local LLMs and Python.

## Quick Start (5 Minutes)

### Option 1: Automated Setup (Recommended)

```bash
# Download the setup script
chmod +x setup.sh

# Run setup
./setup.sh

# Activate virtual environment
source venv/bin/activate

# You're ready!
```

### Option 2: Manual Setup

```bash
# 1. Create virtual environment
python3 -m venv venv

# 2. Activate it
source venv/bin/activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Create database
createdb leads

# 5. Setup environment variables
cp .env.example .env
nano .env  # Add your API keys

# 6. Download Ollama model
ollama pull qwen2.5-coder:32b
```

## ⚠️ IMPORTANT: Virtual Environments

### Never Use --break-system-packages!

**DON'T DO THIS:**
```bash
❌ pip3 install --break-system-packages package
```

**DO THIS:**
```bash
✅ python3 -m venv venv
✅ source venv/bin/activate
✅ pip install package
```

### Why Virtual Environments?

| System-Wide Install | Virtual Environment |
|-------------------|-------------------|
| ❌ Can break macOS | ✅ Isolated & safe |
| ❌ Package conflicts | ✅ No conflicts |
| ❌ Hard to uninstall | ✅ Just delete venv/ |
| ❌ Need sudo | ✅ No sudo needed |
| ❌ One version only | ✅ Different versions per project |

### Daily Workflow

```bash
# Start working
cd ~/projects/lead_generation
source venv/bin/activate  # ← Do this EVERY TIME

# Your prompt shows (venv):
# (venv) user@macmini ~/projects/lead_generation $

# Work normally
python lead_gen_system.py --help

# Done? Deactivate
deactivate
```

## Usage

See README.md for complete documentation.
