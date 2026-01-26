#!/bin/bash

# Claude Code Automation Template Setup Script
# This script helps you copy and customize the template for your project

set -e  # Exit on error

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Configuration
TEMPLATE_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
TARGET_DIR=""
EXCLUDE_README=false
AUTOMATION_LEVEL="safe"

# Print functions
print_header() {
    echo ""
    echo -e "${BLUE}================================================${NC}"
    echo -e "${BLUE}  Claude Code Automation Template Setup${NC}"
    echo -e "${BLUE}================================================${NC}"
    echo ""
}

print_success() {
    echo -e "${GREEN}✓${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}⚠${NC} $1"
}

print_error() {
    echo -e "${RED}✗${NC} $1"
}

print_info() {
    echo -e "${BLUE}ℹ${NC} $1"
}

# Usage information
usage() {
    echo "Usage: $0 [OPTIONS]"
    echo ""
    echo "Options:"
    echo "  -t, --target DIR          Target directory (default: current directory)"
    echo "  -e, --exclude-readme      Exclude copying README.md (for existing projects)"
    echo "  -a, --automation LEVEL    Set automation level: safe, recommended, high, experimental"
    echo "  -h, --help                Show this help message"
    echo ""
    echo "Examples:"
    echo "  # Setup in current directory"
    echo "  ./setup-template.sh"
    echo ""
    echo "  # Copy to existing project"
    echo "  ./setup-template.sh --target ../my-project --exclude-readme"
    echo ""
    echo "  # Setup with high automation"
    echo "  ./setup-template.sh --automation high"
    exit 1
}

# Parse command line arguments
while [[ $# -gt 0 ]]; do
    case $1 in
        -t|--target)
            TARGET_DIR="$2"
            shift 2
            ;;
        -e|--exclude-readme)
            EXCLUDE_README=true
            shift
            ;;
        -a|--automation)
            AUTOMATION_LEVEL="$2"
            shift 2
            ;;
        -h|--help)
            usage
            ;;
        *)
            print_error "Unknown option: $1"
            usage
            ;;
    esac
done

# Set default target directory if not specified
if [ -z "$TARGET_DIR" ]; then
    TARGET_DIR="$(pwd)"
fi

# Create absolute path
TARGET_DIR="$(cd "$TARGET_DIR" 2>/dev/null && pwd)" || {
    print_error "Target directory does not exist: $TARGET_DIR"
    exit 1
}

# Main setup function
main() {
    print_header

    print_info "Template directory: $TEMPLATE_DIR"
    print_info "Target directory: $TARGET_DIR"
    print_info "Automation level: $AUTOMATION_LEVEL"
    echo ""

    # Confirm if target is not empty
    if [ "$(ls -A "$TARGET_DIR" 2>/dev/null | grep -v '^\.git$')" ]; then
        print_warning "Target directory is not empty"
        read -p "Continue? (y/n): " -n 1 -r
        echo
        if [[ ! $REPLY =~ ^[Yy]$ ]]; then
            print_info "Setup cancelled"
            exit 0
        fi
    fi

    echo ""
    print_info "Starting setup..."
    echo ""

    # Step 1: Copy .claude directory
    copy_claude_dir

    # Step 2: Copy ai-docs directory
    copy_ai_docs

    # Step 3: Copy specs directory
    copy_specs

    # Step 4: Copy documentation files
    copy_docs

    # Step 5: Create settings.local.json based on automation level
    create_settings_file

    # Step 6: Initialize git if needed
    init_git_if_needed

    # Step 7: Print next steps
    print_next_steps
}

copy_claude_dir() {
    print_info "Copying .claude directory..."

    if [ -d "$TARGET_DIR/.claude" ]; then
        print_warning ".claude directory already exists, skipping"
        return
    fi

    cp -r "$TEMPLATE_DIR/.claude" "$TARGET_DIR/.claude"
    print_success ".claude directory copied"
}

copy_ai_docs() {
    print_info "Copying ai-docs directory..."

    if [ -d "$TARGET_DIR/ai-docs" ]; then
        print_warning "ai-docs directory already exists"
        read -p "Overwrite? (y/n): " -n 1 -r
        echo
        if [[ $REPLY =~ ^[Yy]$ ]]; then
            rm -rf "$TARGET_DIR/ai-docs"
            cp -r "$TEMPLATE_DIR/ai-docs" "$TARGET_DIR/ai-docs"
            print_success "ai-docs directory replaced"
        else
            print_warning "Skipping ai-docs"
        fi
    else
        cp -r "$TEMPLATE_DIR/ai-docs" "$TARGET_DIR/ai-docs"
        print_success "ai-docs directory copied"
    fi
}

copy_specs() {
    print_info "Copying specs directory..."

    if [ -d "$TARGET_DIR/specs" ]; then
        print_warning "specs directory already exists, skipping"
        return
    fi

    cp -r "$TEMPLATE_DIR/specs" "$TARGET_DIR/specs"
    print_success "specs directory copied"
}

copy_docs() {
    print_info "Copying documentation files..."

    # Always copy these
    cp "$TEMPLATE_DIR/AI-WORKFLOW-QUICKSTART.md" "$TARGET_DIR/" 2>/dev/null && \
        print_success "Copied AI-WORKFLOW-QUICKSTART.md"

    cp "$TEMPLATE_DIR/README-TEMPLATE-SECTION.md" "$TARGET_DIR/" 2>/dev/null && \
        print_success "Copied README-TEMPLATE-SECTION.md"

    # Copy README.md unless excluded
    if [ "$EXCLUDE_README" = false ]; then
        if [ -f "$TARGET_DIR/README.md" ]; then
            print_warning "README.md already exists"
            read -p "Overwrite? (y/n): " -n 1 -r
            echo
            if [[ $REPLY =~ ^[Yy]$ ]]; then
                cp "$TEMPLATE_DIR/README.md" "$TARGET_DIR/"
                print_success "README.md replaced"
            else
                print_warning "Skipping README.md"
            fi
        else
            cp "$TEMPLATE_DIR/README.md" "$TARGET_DIR/"
            print_success "Copied README.md"
        fi
    else
        print_info "Skipping README.md (--exclude-readme flag set)"
    fi
}

create_settings_file() {
    print_info "Creating settings.local.json for automation level: $AUTOMATION_LEVEL"

    local settings_file="$TARGET_DIR/.claude/settings.local.json"

    # Check if already exists
    if [ -f "$settings_file" ]; then
        print_warning "settings.local.json already exists, skipping"
        return
    fi

    case $AUTOMATION_LEVEL in
        safe)
            create_safe_settings "$settings_file"
            ;;
        recommended)
            create_recommended_settings "$settings_file"
            ;;
        high)
            create_high_settings "$settings_file"
            ;;
        experimental)
            create_experimental_settings "$settings_file"
            ;;
        *)
            print_error "Unknown automation level: $AUTOMATION_LEVEL"
            exit 1
            ;;
    esac

    print_success "Created settings.local.json ($AUTOMATION_LEVEL mode)"
}

create_safe_settings() {
    cat > "$1" << 'EOF'
{
  "// INFO": "Safe mode - Manual approval for all edits",
  "// LEVEL": "Safe - Requires manual approval for most operations",
  "permissions": {
    "allow": [
      "Read(specs/**)",
      "Read(ai-docs/**)",
      "Read(package.json)",
      "Read(*.config.*)",
      "Bash(git status)",
      "Bash(git log *)",
      "Bash(git diff *)"
    ]
  }
}
EOF
}

create_recommended_settings() {
    cat > "$1" << 'EOF'
{
  "// INFO": "Recommended mode - Auto-approve safe operations",
  "// LEVEL": "Recommended - Good balance of safety and automation",
  "permissions": {
    "allow": [
      "Read(**/*.{js,ts,jsx,tsx,py,go,rb,java,c,cpp,h,hpp,rs,php,cs})",
      "Read(specs/**)",
      "Read(ai-docs/**)",
      "Read(package.json)",
      "Read(*.config.*)",
      "Read(README.md)",
      "Edit(specs/**)",
      "Edit(ai-docs/**)",
      "Bash(npm run test)",
      "Bash(npm run lint)",
      "Bash(npm run build)",
      "Bash(git status)",
      "Bash(git log *)",
      "Bash(git diff *)"
    ],
    "deny": [
      "Read(.env*)",
      "Read(**/secrets/**)",
      "Edit(.env*)",
      "Bash(rm -rf *)",
      "Bash(git push *)"
    ]
  }
}
EOF
}

create_high_settings() {
    cat > "$1" << 'EOF'
{
  "// INFO": "High automation mode - Auto-approve most development operations",
  "// LEVEL": "High - Use with caution, monitor initial runs",
  "// WARNING": "This allows automatic file edits. Review changes carefully.",
  "permissions": {
    "allow": [
      "Read(**)",
      "Edit(src/**)",
      "Edit(lib/**)",
      "Edit(components/**)",
      "Edit(tests/**)",
      "Edit(__tests__/**)",
      "Edit(specs/**)",
      "Edit(ai-docs/**)",
      "Bash(npm *)",
      "Bash(yarn *)",
      "Bash(pnpm *)",
      "Bash(git status)",
      "Bash(git log *)",
      "Bash(git diff *)",
      "Bash(git add *)",
      "Bash(git commit *)"
    ],
    "deny": [
      "Read(.env*)",
      "Read(**/secrets/**)",
      "Read(**/credentials/**)",
      "Edit(.env*)",
      "Edit(*.key)",
      "Edit(*.pem)",
      "Bash(rm -rf *)",
      "Bash(git push *force*)",
      "Bash(git reset --hard*)"
    ]
  }
}
EOF
}

create_experimental_settings() {
    cat > "$1" << 'EOF'
{
  "// INFO": "Experimental mode - Maximum automation (USE WITH EXTREME CAUTION)",
  "// LEVEL": "Experimental - For overnight autonomous runs",
  "// WARNING": "This bypasses most permission checks. Only use in isolated environments.",
  "// RECOMMENDATION": "Use in development branches only, never in production",
  "permissions": {
    "allow": [
      "Read(**)",
      "Edit(**/*.{js,ts,jsx,tsx,py,go,rb,java,c,cpp,h,hpp,rs,php,cs})",
      "Edit(specs/**)",
      "Edit(ai-docs/**)",
      "Edit(tests/**)",
      "Edit(__tests__/**)",
      "Write(**)",
      "Bash(*)"
    ],
    "deny": [
      "Read(.env*)",
      "Edit(.env*)",
      "Edit(*.key)",
      "Edit(*.pem)",
      "Edit(**/secrets/**)",
      "Bash(rm -rf /)",
      "Bash(sudo *)",
      "Bash(git push *force*)"
    ]
  }
}
EOF
}

init_git_if_needed() {
    if [ ! -d "$TARGET_DIR/.git" ]; then
        print_info "No git repository found"
        read -p "Initialize git repository? (y/n): " -n 1 -r
        echo
        if [[ $REPLY =~ ^[Yy]$ ]]; then
            cd "$TARGET_DIR"
            git init

            # Create .gitignore if it doesn't exist
            if [ ! -f ".gitignore" ]; then
                cat > .gitignore << 'EOF'
# Claude Code local settings
.claude/settings.local.json

# Dependencies
node_modules/
vendor/

# Environment variables
.env
.env.local
.env.*.local

# Build outputs
dist/
build/
*.log

# IDE
.vscode/
.idea/
*.swp
*.swo
*~

# OS
.DS_Store
Thumbs.db
EOF
                print_success "Created .gitignore"
            fi

            print_success "Git repository initialized"
        fi
    else
        print_success "Git repository already exists"
    fi
}

print_next_steps() {
    echo ""
    echo -e "${GREEN}================================================${NC}"
    echo -e "${GREEN}  Setup Complete! 🎉${NC}"
    echo -e "${GREEN}================================================${NC}"
    echo ""
    echo -e "${BLUE}Next Steps:${NC}"
    echo ""
    echo "1. ${YELLOW}Customize the template${NC}:"
    echo "   • Update .claude/claude_code_rules.md with your tech stack"
    echo "   • Populate ai-docs/ with your project specifics"
    echo "   • Adjust .claude/commands/context-prime.md if needed"
    echo ""
    echo "2. ${YELLOW}Open in Claude Code${NC}:"
    echo "   cd $TARGET_DIR"
    echo "   # Then open Claude Code in this directory"
    echo ""
    echo "3. ${YELLOW}Run customization helper${NC}:"
    echo "   /template-adapt"
    echo ""
    echo "4. ${YELLOW}Prime the AI context${NC}:"
    echo "   /context-prime"
    echo ""
    echo "5. ${YELLOW}Create your first spec${NC}:"
    echo "   /plan-draft"
    echo ""
    echo -e "${BLUE}Automation Level: ${YELLOW}$AUTOMATION_LEVEL${NC}"
    case $AUTOMATION_LEVEL in
        safe)
            echo "   • Manual approval required for most operations"
            echo "   • Safest option for getting started"
            ;;
        recommended)
            echo "   • Auto-approves safe operations (reads, tests, docs)"
            echo "   • Good balance for most projects"
            ;;
        high)
            echo "   • Auto-approves most development operations"
            echo "   • Monitor initial runs carefully"
            ;;
        experimental)
            echo "   • Maximum automation - USE WITH CAUTION"
            echo "   • Only for isolated development environments"
            ;;
    esac
    echo ""
    echo -e "${BLUE}Documentation:${NC}"
    echo "   • AI-WORKFLOW-QUICKSTART.md - Quick reference guide"
    echo "   • AUTOMATION-GUIDE.md - Automation setup and safety"
    echo "   • SETUP.md - Detailed setup instructions"
    echo ""
    print_success "Happy coding with AI! 🤖"
    echo ""
}

# Run main function
main
