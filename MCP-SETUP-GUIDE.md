# MCP Server Setup Guide

> **Complete guide to installing and configuring Model Context Protocol servers with Claude Desktop**

## Table of Contents

- [What is MCP?](#what-is-mcp)
- [Quick Start](#quick-start)
- [Discovery Tool](#discovery-tool)
- [Manual Installation](#manual-installation)
- [Server Catalog](#server-catalog)
- [Configuration](#configuration)
- [Troubleshooting](#troubleshooting)
- [Security](#security)

---

## What is MCP?

**Model Context Protocol (MCP)** is an open standard by Anthropic that connects AI assistants like Claude to external data sources and tools.

### Benefits

- 🔗 **Connect Claude to your tools**: Databases, APIs, file systems, cloud services
- 🤖 **Enhanced capabilities**: Claude can read/write files, query databases, manage Git repos
- 🔌 **Plug and play**: Thousands of community MCP servers available
- 🔒 **Secure**: You control what Claude can access

### How It Works

```
Claude Desktop <--MCP--> MCP Server <---> Your Data/Tools
```

1. **MCP Server** runs locally on your machine
2. **Claude Desktop** connects to it
3. **Your data** stays on your machine (servers can't phone home)

---

## Quick Start

### Step 1: Discover Relevant Servers

Run the MCP scanner to find servers for your project:

```bash
# In Claude Code
/mcp-scan
```

This will analyze your codebase and recommend relevant MCP servers.

### Step 2: Install Recommended Servers

Based on recommendations, install servers:

```bash
# Core servers (recommended for everyone)
npm install -g @modelcontextprotocol/server-filesystem
npm install -g @modelcontextprotocol/server-git

# Project-specific (install as needed)
npm install -g @modelcontextprotocol/server-github
npm install -g @modelcontextprotocol/server-postgres
```

### Step 3: Configure Claude Desktop

Edit your Claude Desktop config:

**Location**:
- Mac: `~/Library/Application Support/Claude/claude_desktop_config.json`
- Windows: `%APPDATA%\Claude\claude_desktop_config.json`
- Linux: `~/.config/Claude/claude_desktop_config.json`

**Add servers**:
```json
{
  "mcpServers": {
    "filesystem": {
      "command": "npx",
      "args": [
        "-y",
        "@modelcontextprotocol/server-filesystem",
        "/path/to/your/project"
      ]
    },
    "git": {
      "command": "npx",
      "args": [
        "-y",
        "@modelcontextprotocol/server-git",
        "--repository",
        "/path/to/your/project"
      ]
    }
  }
}
```

### Step 4: Restart Claude Desktop

Close and reopen Claude Desktop. You should see MCP servers listed at the bottom of the interface.

---

## Discovery Tool

### `/mcp-scan` Command

The template includes an MCP scanner that automatically detects what servers you need:

```bash
# Analyze your project
/mcp-scan

# Example output:
🔍 MCP Server Recommendations

Based on your project:
✓ Node.js with TypeScript
✓ PostgreSQL database
✓ GitHub repository

Recommended:
1. filesystem - File operations (ESSENTIAL)
2. git - Version control (ESSENTIAL)
3. github - GitHub integration
4. postgres - Database access

Install? (y/n)
```

### What It Detects

- **Databases**: PostgreSQL, MySQL, MongoDB, SQLite, Redis
- **APIs**: GitHub, AWS, Google Cloud, Slack, Stripe, OpenAI
- **Tools**: Docker, Kubernetes, Puppeteer
- **Languages**: Node.js, Python, Go, Rust, Ruby, PHP
- **Frameworks**: React, Vue, Next.js, Django, Rails

---

## Manual Installation

### Prerequisites

- Node.js 18+ installed
- Claude Desktop app installed
- Terminal access

### Installing MCP Servers

#### Option A: Global Install (Recommended)

```bash
npm install -g @modelcontextprotocol/server-[name]
```

#### Option B: npx (No installation)

Use `npx` directly in config (downloads on-demand):

```json
{
  "command": "npx",
  "args": ["-y", "@modelcontextprotocol/server-[name]"]
}
```

#### Option C: Local Install (Advanced)

```bash
# Create MCP directory
mkdir -p ~/.local/share/mcp-servers
cd ~/.local/share/mcp-servers

# Install server
npm install @modelcontextprotocol/server-[name]
```

Then reference in config:
```json
{
  "command": "node",
  "args": ["~/.local/share/mcp-servers/node_modules/@modelcontextprotocol/server-[name]/dist/index.js"]
}
```

---

## Server Catalog

### Official Servers (Anthropic)

#### 🗂️ Filesystem
```bash
npm install -g @modelcontextprotocol/server-filesystem
```
**Provides**: Read/write files, search, directory operations
**Config**:
```json
{
  "filesystem": {
    "command": "npx",
    "args": ["-y", "@modelcontextprotocol/server-filesystem", "/path/to/project"]
  }
}
```

#### 🔀 Git
```bash
npm install -g @modelcontextprotocol/server-git
```
**Provides**: Git operations, history, diff, branch management
**Config**:
```json
{
  "git": {
    "command": "npx",
    "args": ["-y", "@modelcontextprotocol/server-git", "--repository", "/path/to/repo"]
  }
}
```

#### 🐙 GitHub
```bash
npm install -g @modelcontextprotocol/server-github
```
**Provides**: Issues, PRs, releases, repository management
**Requires**: `GITHUB_TOKEN` environment variable
**Config**:
```json
{
  "github": {
    "command": "npx",
    "args": ["-y", "@modelcontextprotocol/server-github"],
    "env": {
      "GITHUB_TOKEN": "ghp_your_token_here"
    }
  }
}
```

#### 🐘 PostgreSQL
```bash
npm install -g @modelcontextprotocol/server-postgres
```
**Provides**: Query execution, schema inspection
**Requires**: Database connection string
**Config**:
```json
{
  "postgres": {
    "command": "npx",
    "args": ["-y", "@modelcontextprotocol/server-postgres"],
    "env": {
      "DATABASE_URL": "postgresql://user:pass@localhost:5432/dbname"
    }
  }
}
```

#### 💾 SQLite
```bash
npm install -g @modelcontextprotocol/server-sqlite
```
**Provides**: Query execution for SQLite databases
**Config**:
```json
{
  "sqlite": {
    "command": "npx",
    "args": ["-y", "@modelcontextprotocol/server-sqlite", "--db-path", "/path/to/db.sqlite"]
  }
}
```

#### 🌐 Puppeteer
```bash
npm install -g @modelcontextprotocol/server-puppeteer
```
**Provides**: Browser automation, screenshots, web scraping
**Config**:
```json
{
  "puppeteer": {
    "command": "npx",
    "args": ["-y", "@modelcontextprotocol/server-puppeteer"]
  }
}
```

### Community Servers

#### 🧠 Memory (Persistent Context)
```bash
npm install -g mcp-server-memory
```
**Provides**: Persistent memory across Claude sessions
**Use case**: Long-running development workflows
**Config**:
```json
{
  "memory": {
    "command": "npx",
    "args": ["-y", "mcp-server-memory"]
  }
}
```

#### 🐳 Docker
```bash
npm install -g mcp-server-docker
```
**Provides**: Container management, image operations
**Config**:
```json
{
  "docker": {
    "command": "npx",
    "args": ["-y", "mcp-server-docker"]
  }
}
```

#### ☸️ Kubernetes
```bash
npm install -g mcp-server-kubernetes
```
**Provides**: Cluster management, pod operations
**Requires**: kubectl configured
**Config**:
```json
{
  "kubernetes": {
    "command": "npx",
    "args": ["-y", "mcp-server-kubernetes"]
  }
}
```

#### ☁️ AWS
```bash
npm install -g mcp-server-aws
```
**Provides**: S3, Lambda, EC2 operations
**Requires**: AWS credentials configured
**Config**:
```json
{
  "aws": {
    "command": "npx",
    "args": ["-y", "mcp-server-aws"],
    "env": {
      "AWS_ACCESS_KEY_ID": "your_key",
      "AWS_SECRET_ACCESS_KEY": "your_secret",
      "AWS_REGION": "us-east-1"
    }
  }
}
```

#### 💬 Slack
```bash
npm install -g mcp-server-slack
```
**Provides**: Message sending, channel management
**Requires**: Slack app token
**Config**:
```json
{
  "slack": {
    "command": "npx",
    "args": ["-y", "mcp-server-slack"],
    "env": {
      "SLACK_BOT_TOKEN": "xoxb-your-token"
    }
  }
}
```

---

## Configuration

### Full Config Example

```json
{
  "mcpServers": {
    "filesystem": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-filesystem", "/Users/you/projects/my-app"]
    },
    "git": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-git", "--repository", "/Users/you/projects/my-app"]
    },
    "github": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-github"],
      "env": {
        "GITHUB_TOKEN": "ghp_xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"
      }
    },
    "postgres": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-postgres"],
      "env": {
        "DATABASE_URL": "postgresql://localhost:5432/mydb"
      }
    },
    "memory": {
      "command": "npx",
      "args": ["-y", "mcp-server-memory"]
    }
  }
}
```

### Environment Variables

**Option 1: Inline in config** (shown above)

**Option 2: System environment variables**
```bash
# Add to ~/.bashrc or ~/.zshrc
export GITHUB_TOKEN="ghp_your_token"
export DATABASE_URL="postgresql://localhost:5432/mydb"
```

**Option 3: .env file** (project-specific)
```bash
# In your project
echo "GITHUB_TOKEN=ghp_your_token" >> .env
echo "DATABASE_URL=postgresql://localhost:5432/mydb" >> .env

# MCP servers can read from .env
```

### Custom MCP Directory

Set a custom location for MCP servers:

```bash
export LOCAL_MCP_DIR="$HOME/my-mcp-servers"
```

---

## Troubleshooting

### MCP Servers Not Appearing

**Issue**: Servers don't show in Claude Desktop after config

**Solutions**:
1. Check config file location is correct
2. Validate JSON syntax (use `jq` or online validator)
3. Restart Claude Desktop completely (not just close window)
4. Check Claude Desktop logs:
   - Mac: `~/Library/Logs/Claude/`
   - Windows: `%APPDATA%\Claude\logs\`
   - Linux: `~/.config/Claude/logs/`

### "Command not found" Errors

**Issue**: `npx: command not found` or similar

**Solutions**:
1. Ensure Node.js is installed: `node --version`
2. Ensure npm/npx is in PATH: `which npx`
3. Use full path in config:
   ```json
   {
     "command": "/usr/local/bin/npx",
     "args": [...]
   }
   ```

### Permission Errors

**Issue**: MCP server can't access files/databases

**Solutions**:
1. Check file permissions: `ls -la /path/to/project`
2. Ensure database user has correct permissions
3. Verify API tokens are valid and not expired

### Server Crashes

**Issue**: MCP server starts then immediately crashes

**Solutions**:
1. Check logs in Claude Desktop log directory
2. Test server manually:
   ```bash
   npx -y @modelcontextprotocol/server-filesystem /path/to/project
   ```
3. Ensure all required environment variables are set
4. Check for port conflicts if server uses networking

### GitHub Token Issues

**Issue**: GitHub MCP server not working

**Solutions**:
1. Generate new token: https://github.com/settings/tokens
2. Required scopes: `repo`, `read:org`, `read:user`
3. Use Personal Access Token (classic), not fine-grained
4. Ensure token is in config correctly (no extra quotes)

---

## Security

### Best Practices

1. **Least Privilege**: Only install servers you actually need
2. **Scope Limits**: Limit filesystem server to specific directories
3. **Token Security**: Never commit tokens to Git
4. **Read-Only When Possible**: Use read-only database users
5. **Review Access**: Periodically audit what Claude can access

### Token Management

**DO**:
- ✅ Store tokens in environment variables
- ✅ Use `.env` files (gitignored)
- ✅ Use system keychain/credential manager
- ✅ Rotate tokens regularly

**DON'T**:
- ❌ Commit tokens to Git
- ❌ Share tokens in screenshots
- ❌ Use tokens with broader access than needed
- ❌ Store in plain text config files (use env vars)

### Scoped Access

**Filesystem Server**:
```json
{
  "filesystem": {
    "command": "npx",
    "args": [
      "-y",
      "@modelcontextprotocol/server-filesystem",
      "/Users/you/projects/safe-project"  // Only this directory
    ]
  }
}
```

**Database Server** (read-only user):
```sql
-- PostgreSQL: Create read-only user
CREATE USER mcp_readonly WITH PASSWORD 'secure_password';
GRANT CONNECT ON DATABASE mydb TO mcp_readonly;
GRANT USAGE ON SCHEMA public TO mcp_readonly;
GRANT SELECT ON ALL TABLES IN SCHEMA public TO mcp_readonly;
```

---

## Advanced Topics

### Multiple Projects

**Problem**: Different projects need different MCP configurations

**Solution**: Create project-specific config files:

```bash
# Create configs
~/.config/Claude/project1_config.json
~/.config/Claude/project2_config.json

# Symlink the one you want
ln -sf ~/.config/Claude/project1_config.json ~/.config/Claude/claude_desktop_config.json

# Restart Claude
```

**Or** use a config switcher script:

```bash
#!/bin/bash
# switch-mcp-config.sh

PROJECT=$1
cp ~/.config/Claude/configs/${PROJECT}.json ~/.config/Claude/claude_desktop_config.json
echo "Switched to ${PROJECT} MCP config. Restart Claude Desktop."
```

### Custom MCP Servers

**Creating your own MCP server**:

1. Use the MCP SDK:
   ```bash
   npm install @modelcontextprotocol/sdk
   ```

2. Implement server interface:
   ```typescript
   import { Server } from '@modelcontextprotocol/sdk/server/index.js';

   const server = new Server({
     name: 'my-custom-server',
     version: '1.0.0',
   }, {
     capabilities: {
       resources: {},
       tools: {},
     },
   });
   ```

3. Add to config like any other server

**Resources**:
- SDK Docs: https://github.com/modelcontextprotocol/typescript-sdk
- Example servers: https://github.com/modelcontextprotocol/servers

### Performance Optimization

**Tips for faster MCP**:

1. **Use local installs** instead of npx (faster startup)
2. **Limit filesystem scope** (fewer directories = faster)
3. **Cache database schemas** (use persistent connections)
4. **Batch operations** when possible

---

## Resources

- **Official MCP Docs**: https://modelcontextprotocol.io
- **Server Registry**: https://github.com/modelcontextprotocol/servers
- **Claude Desktop Setup**: https://docs.claude.com/en/docs/mcp
- **Community Servers**: https://github.com/topics/mcp-server
- **SDK Documentation**: https://github.com/modelcontextprotocol/typescript-sdk

---

## Getting Help

1. **Check logs**: Claude Desktop logs are the first place to look
2. **Test manually**: Run MCP servers from terminal to see errors
3. **Community**: Ask in Claude Discord or GitHub discussions
4. **This template**: Run `/mcp-scan` for automatic diagnosis

---

**Happy MCP-ing!** 🚀

If you found this guide helpful, consider starring the template repository.
