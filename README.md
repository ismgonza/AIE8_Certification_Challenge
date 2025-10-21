# 🛡️ Shieldy - The AI Security Assistant

## What This Does

An AI-powered security guidance tool for small-medium businesses with **two modes**:

1. **📊 Security Assessment** - Get your security score and identify critical gaps
2. **🔧 Implementation Helper** - Get step-by-step guides for specific security tasks

---

## 🚀 Quick Start

### 1. Start Backend
```bash
cd backend
uv run uvicorn main:app --reload
```

**On first startup**, the system will automatically:
- Ingest all PDFs from `backend/data/` folder into Qdrant vector database
- This takes 1-2 minutes (only happens once)
- Subsequent startups are instant (documents already loaded)

### 2. Start Frontend
```bash
cd frontend
npm run dev
```

### 3. Open Browser
Visit: `http://localhost:5173`

---

## 📊 Mode 1: Security Assessment

**Best for**: Companies new to security who don't know where to start

### How It Works
1. Click **"📊 Assess My Security"** on landing page
2. Fill out the 7-question form:
   - Company name, size, industry
   - Tech stack (Windows, AWS, Microsoft 365, etc.)
   - Current security measures (checkboxes)
   - Budget and main concerns
3. Click **"Get My Security Assessment"**
4. Get personalized results:
   - Security score (0-10)
   - Maturity level (Survival → Baseline → Professional → Advanced)
   - Top 5 critical security gaps to fix
   - Specific recommendations for YOUR situation

### Example Results
```
Acme Corp's Security Report

5.5/10 - Level 2: Baseline Security

✅ What you're doing well:
- Antivirus and firewall enabled
- Basic password policy in place

🔴 CRITICAL Gaps:
1. No Multi-Factor Authentication (MFA)
   - Risk: Credential theft, unauthorized access
   - Cost: $3-7/user/month
   - Time: 2-4 hours to implement

2. No backup strategy
   - Risk: Data loss, ransomware impact
   - Cost: $50-200/month
   - Time: 4-6 hours to set up

[... 3 more gaps ...]
```

### What Makes It Smart
The AI analyzes your answers against:
- **CIS Controls** (industry best practices)
- **NIST Cybersecurity Framework**
- **OWASP** (web application security)
- Industry-specific threats (healthcare vs finance vs SaaS)

---

## 🔧 Mode 2: Implementation Helper

**Best for**: When you know what you need but want step-by-step guidance

### How It Works
1. Click **"🔧 Get Help With Something"** on landing page
2. Search or click example topics:
   - "Harden Windows Server 2022"
   - "Configure MFA in Active Directory"
   - "Secure Ubuntu 22.04 baseline"
   - "AWS S3 bucket security checklist"
3. Get AI-generated implementation guide with:
   - Step-by-step instructions
   - Copy-paste commands (PowerShell, bash, etc.)
   - Verification steps
   - Why each step matters
   - References to CIS/NIST/OWASP standards

### Example Guide Output
```markdown
# Windows Server 2022 Hardening Guide

## Step 1: Enable Windows Defender
**Why**: Protects against malware and zero-day exploits
**Time**: 5 minutes

Run in PowerShell (Admin):
```powershell
Set-MpPreference -DisableRealtimeMonitoring $false
Update-MpSignature
```

Verify:
```powershell
Get-MpComputerStatus
```

## Step 2: Configure Firewall
[... continues with detailed steps ...]

## CIS Benchmark References
- CIS Windows Server 2022 - Control 8.1, 8.4
- NIST 800-53 - SI-3
```

### Sources Shown
The guide displays which documents were used:
- CIS Benchmarks (AWS, Windows, Ubuntu, etc.)
- OWASP Application Security Verification Standard
- NIST guidelines

---

## 🎯 Key Features

### Auto-Ingestion
- Drop any PDF into `backend/data/` folder
- Restart backend → automatically ingested
- No manual upload needed

### Smart RAG Pipeline
- Semantic search through security standards
- AI agent workflow (analyze → research → generate)
- Optional web search via Tavily API for real-world examples
- Cohere reranking for better results (configurable in `.env`)

### SMB-Focused
- Prioritizes by **CIS Implementation Group 1** (small business appropriate)
- Budget-conscious recommendations
- Realistic time estimates
- Free alternatives mentioned

---

## 📚 Knowledge Base

Currently includes (in `backend/data/`):
- CIS Amazon Web Services Foundations Benchmark v6.0.0
- OWASP Application Security Verification Standard v5.0.0

**To add more**:
1. Download PDF (e.g., CIS Windows Server 2022, NIST CSF)
2. Place in `backend/data/` folder
3. Restart backend OR call `POST /admin/reingest`

---

## 🔧 API Endpoints

### Core Endpoints
- `POST /assess` - Security maturity assessment
- `POST /query` - Ask any security question (RAG)
- `GET /health` - System health check
- `GET /documents` - Browse vector database (debugging)

### Admin Endpoints
- `POST /admin/reingest` - Manually re-ingest PDFs (if you added new ones)
- `DELETE /admin/clear` - Clear all documents (⚠️ destructive!)
- `DELETE /admin/documents/{source_name}` - Delete specific source file

### Example API Usage
```bash
# Get security assessment
curl -X POST http://localhost:8000/assess \
  -H "Content-Type: application/json" \
  -d '{
    "company_name": "Acme Corp",
    "company_size": "11-50",
    "industry": "Technology/Software",
    "tech_stack": ["Windows", "AWS"],
    "security_measures": "Antivirus, Firewall",
    "budget": "$500-$2K",
    "main_concern": "Ransomware"
  }'

# Ask specific question
curl -X POST http://localhost:8000/query \
  -H "Content-Type: application/json" \
  -d '{
    "query": "How do I configure MFA for my small business?",
    "top_k": 5
  }'
```

---

## 🛠️ Configuration

Environment variables (`.env` in `backend/`):
```bash
# Required
OPENAI_API_KEY=sk-...

# Optional (for web search)
TAVILY_API_KEY=tvly-...

# Optional (for better reranking)
COHERE_API_KEY=...
USE_RERANKING=true
RERANKER_MODEL=rerank-english-v3.0

# Database
QDRANT_URL=http://localhost:6333
QDRANT_COLLECTION=security_knowledge

# Models
LLM_MODEL=gpt-4o
EMBEDDING_MODEL=text-embedding-3-small
```

---

## 💡 Tips

### For Best Assessment Results
- Be specific about your tech stack (not just "Cloud" - say "AWS EC2, S3, RDS")
- Check ALL security measures you have (even basic ones)
- Describe real concerns in "What keeps you up at night?"

### For Best Implementation Guides
- Include version numbers ("Windows Server 2022" not just "Windows")
- Mention environment if relevant ("on-premises" vs "cloud")
- Use example searches to discover what's possible

### Adding Industry-Specific Standards
Want HIPAA, PCI-DSS, or SOC 2 guidance?
1. Download relevant PDF guides
2. Place in `backend/data/`
3. Restart backend
4. Ask questions specific to that framework

---

## 🐛 Troubleshooting

### Backend won't start
- Check if Qdrant is running: `docker-compose up -d` in `backend/docker/`
- Check `.env` file exists with `OPENAI_API_KEY`
- Check port 8000 is not in use

### "No documents found" error
- First startup takes 1-2 minutes to ingest PDFs
- Check `backend/data/` has PDF files
- Check backend logs for ingestion errors
- Try: `curl http://localhost:8000/health` to see document count

### Assessment results too generic
- The AI analyzes based on your inputs
- More specific tech stack = more specific recommendations
- Check more security measures if you have them

### Implementation guide not specific enough
- Add version numbers to your search
- Mention environment (on-prem, cloud, hybrid)
- Try different phrasing

---

## 📈 What You Get

### Traditional Approach
- Read hundreds of pages of standards (20+ hours)
- Hire consultant ($5K-$15K for assessment)
- Wait weeks for generic report
- Struggle to implement recommendations

### With This Tool
- Fill 7-question form (5 minutes)
- Get personalized assessment (30 seconds)
- Search any security topic (instant guides)
- Copy-paste ready commands
- **FREE** (just your OpenAI API costs ~$0.30/assessment)

**Time Saved**: 20+ hours  
**Cost Saved**: $5K-$15K  
**Quality**: Personalized + up-to-date standards

---

## 🎓 Example Scenarios

### Scenario 1: Healthcare Startup
**Profile**: 15 employees, using AWS, minimal security, HIPAA required

**Assessment Result**:
- Score: 2.5/10 (Survival Mode)
- Critical gaps: Encryption, access control, backups, audit logging
- HIPAA-specific recommendations
- Free/low-cost tool suggestions

**Implementation Path**:
1. Search: "HIPAA-compliant AWS setup"
2. Search: "Enable encryption for patient data"
3. Search: "Access control best practices healthcare"

### Scenario 2: SaaS Company
**Profile**: 50 employees, AWS + Google Workspace, SOC 2 audit in 6 months

**Assessment Result**:
- Score: 4.5/10 (Baseline Security)
- Critical gaps: Monitoring, vulnerability scanning, formal incident response
- SOC 2-focused recommendations
- Timeline-aware suggestions (6 months)

**Implementation Path**:
1. Search: "Set up security monitoring for AWS"
2. Search: "SOC 2 compliance checklist"
3. Search: "Incident response plan template"

---

## 🚀 Next Steps

1. **Run an assessment** - See where you stand
2. **Pick top 3 gaps** - Don't try to fix everything at once
3. **Use Implementation Helper** - Get step-by-step guides
4. **Implement systematically** - One control at a time
5. **Re-assess in 3 months** - Track your progress

**Remember**: Security is a journey, not a destination. Start small, build momentum, and improve continuously.

---

Need help? Check `/health` endpoint for system status or review backend logs for detailed error messages.

