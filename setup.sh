#!/bin/bash
# Lead Generation System - Setup Script
# Run this to set up your development environment

set -e  # Exit on error

echo "🚀 Lead Generation System - Setup"
echo "=================================="
echo ""

# Check Python version
echo "📋 Checking Python version..."
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 not found. Please install Python 3.11+"
    exit 1
fi

PYTHON_VERSION=$(python3 --version | cut -d' ' -f2)
echo "✅ Found Python $PYTHON_VERSION"
echo ""

# Create virtual environment
echo "📦 Creating virtual environment..."
if [ -d "venv" ]; then
    echo "⚠️  venv/ already exists. Remove it? (y/n)"
    read -r response
    if [ "$response" = "y" ]; then
        rm -rf venv
        python3 -m venv venv
        echo "✅ Recreated venv/"
    else
        echo "ℹ️  Using existing venv/"
    fi
else
    python3 -m venv venv
    echo "✅ Created venv/"
fi
echo ""

# Activate virtual environment
echo "🔌 Activating virtual environment..."
source venv/bin/activate
echo "✅ Virtual environment activated"
echo ""

# Upgrade pip
echo "⬆️  Upgrading pip..."
pip install --upgrade pip
echo ""

# Install dependencies
echo "📥 Installing dependencies..."
if [ -f "requirements.txt" ]; then
    pip install -r requirements.txt
    echo "✅ Dependencies installed"
else
    echo "❌ requirements.txt not found"
    echo "Creating minimal requirements.txt..."
    cat > requirements.txt << EOF
langchain>=0.1.0
langchain-community>=0.0.10
ollama>=0.1.0
sqlalchemy>=2.0.0
psycopg2-binary>=2.9.0
pydantic>=2.0.0
pandas>=2.0.0
requests>=2.31.0
python-dotenv>=1.0.0
EOF
    pip install -r requirements.txt
    echo "✅ Minimal dependencies installed"
fi
echo ""

# Check for PostgreSQL
echo "🗄️  Checking PostgreSQL..."
if command -v psql &> /dev/null; then
    echo "✅ PostgreSQL found"
    
    # Check if leads database exists
    if psql -lqt | cut -d \| -f 1 | grep -qw leads; then
        echo "✅ Database 'leads' already exists"
    else
        echo "📊 Creating database 'leads'..."
        createdb leads
        echo "✅ Database 'leads' created"
    fi
else
    echo "⚠️  PostgreSQL not found"
    echo "   Install with: brew install postgresql"
    echo "   Then run: brew services start postgresql"
fi
echo ""

# Check for Ollama
echo "🤖 Checking Ollama..."
if command -v ollama &> /dev/null; then
    echo "✅ Ollama found"
    
    # Check if model is installed
    if ollama list | grep -q "qwen2.5-coder:32b"; then
        echo "✅ qwen2.5-coder:32b model installed"
    else
        echo "📥 Downloading qwen2.5-coder:32b model..."
        echo "   This may take 10-20 minutes (20GB download)"
        ollama pull qwen2.5-coder:32b
        echo "✅ Model downloaded"
    fi
else
    echo "⚠️  Ollama not found"
    echo "   Install from: https://ollama.ai"
fi
echo ""

# Create .env file template
echo "🔐 Creating .env template..."
if [ ! -f ".env" ]; then
    cat > .env << EOF
# Lead Generation System - Environment Variables

# Database
DATABASE_URL=postgresql://localhost/leads

# Ollama
OLLAMA_BASE_URL=http://localhost:11434
OLLAMA_MODEL=qwen2.5-coder:32b

# HubSpot (Get from: Settings -> Private Apps)
HUBSPOT_API_KEY=pat-na2-your-key-here

# Hunter.io (Optional - Get from: https://hunter.io/api-keys)
HUNTER_API_KEY=

# Scoring Thresholds
HIGH_PRIORITY_SCORE=70
MEDIUM_PRIORITY_SCORE=50
EOF
    echo "✅ Created .env file"
    echo "   ⚠️  Edit .env and add your HUBSPOT_API_KEY"
else
    echo "ℹ️  .env file already exists"
fi
echo ""

# Create project structure
echo "📁 Creating project structure..."
mkdir -p data/{apollo,linkedin,manual}
mkdir -p logs
mkdir -p tests
echo "✅ Project structure created"
echo ""

# Test imports
echo "🧪 Testing imports..."
python3 -c "
try:
    import langchain
    import ollama
    import sqlalchemy
    import pandas
    import pydantic
    print('✅ All imports successful')
except ImportError as e:
    print(f'❌ Import error: {e}')
    exit(1)
"
echo ""

# Summary
echo "✅ Setup Complete!"
echo "=================="
echo ""
echo "📝 Next steps:"
echo ""
echo "1. Activate virtual environment:"
echo "   source venv/bin/activate"
echo ""
echo "2. Edit .env file with your API keys:"
echo "   nano .env"
echo ""
echo "3. Test the system:"
echo "   python lead_gen_system.py --help"
echo ""
echo "4. Process a CSV file:"
echo "   python lead_gen_system.py process --file data/apollo/export.csv --source apollo"
echo ""
echo "5. Sync to HubSpot:"
echo "   python lead_gen_system.py sync --limit 10"
echo ""
echo "📚 Documentation:"
echo "   - README.md (project overview)"
echo "   - AI_LEAD_GENERATION_ARCHITECTURE.md (system design)"
echo "   - APOLLO_ALTERNATIVES.md (data sources)"
echo ""
echo "💡 Tips:"
echo "   - Always activate venv before working: source venv/bin/activate"
echo "   - Deactivate when done: deactivate"
echo "   - Update dependencies: pip install -r requirements.txt --upgrade"
echo ""
echo "🎉 Happy lead generating!"
