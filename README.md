# ISO Control Implementation Assistant

## Problem Description
Small and medium-sized organizations **waste $20K-$50K** hiring consultants to translate ISO 27001's 93 abstract security controls into practical implementation steps, yet still struggle with vague guidance like "implement access control policies" without knowing what that actually means for their specific business context, leading to failed audits, wasted resources, and delayed certifications.

## Problem Explanation
**Imagine being handed a 150-page technical manual written in legal language and being told: "Implement all of this or fail your security certification."** That's what organizations face when pursuing ISO 27001 certification.

**Here's the challenge**: ISO 27001 is the gold standard for information security management, required by many customers and partners before they'll do business with you. The standard contains 93 security controls covering everything from access management to cryptography to incident response.

But here's the catch: ISO standards are deliberately written as high-level requirements, not step-by-step instructions. For example, Control 5.15 says *"Access control rules shall be established and documented"*—but what does that actually mean? What rules? What documentation? What format? For which systems?

**The problem:** Organizations face three painful options:

1. **Hire expensive consultants** ($150-$300/hour, 80-200 hours) to interpret the standards and create implementation plans [1]
2. **Buy generic templates** ($2K-$10K) that don't fit their specific technology stack or business context [2]
3. **Wing it** and hope the auditor accepts their interpretation (spoiler: they usually don't)

**The cost is crushing for small/medium businesses:**
- $15,000-$50,000 for initial ISO 27001 certification consulting [1]
- $10,000-$30,000 annually for maintenance and recertification support [3]
- 6-12 months of project timeline to implement all controls [4]
- 40-60% failure rate on first audit attempt due to inadequate implementation [5]

Meanwhile, the certification itself costs another $5,000-$15,000 in audit fees [6], and many organizations discover they've implemented controls incorrectly only after failing their audit—forcing them to start over and pay again.

**Real-world example**: A 50-person software company needs ISO 27001 to win enterprise customers. They're told to "implement control 8.8: Management of technical vulnerabilities." After 20 hours of research, they're still unclear: Do we need a vulnerability scanner? Which one? How often do we scan? What's the acceptable remediation timeline? Do we need a formal policy document? The consultant they eventually hire charges $5,000 just to answer these questions for one control category.

> **Bottom line:** Organizations are spending $20K-$50K on consultants to translate abstract ISO requirements into actionable steps, yet still struggle with implementation because generic advice doesn't fit their specific context—meanwhile, failed audits cost them customer deals and another round of expensive consulting.

<details>
<summary>References</summary>

[1] Ignyte Assurance Platform. "ISO 27001 Consulting Costs: What to Expect in 2024." https://www.ignyteplatform.com/post/iso-27001-consulting-costs

[2] IT Governance. "ISO 27001 Documentation Toolkit." https://www.itgovernance.co.uk/shop/product/iso-27001-documentation-toolkit

[3] Schellman. "ISO 27001 Certification Cost Guide." https://www.schellman.com/blog/iso-27001-certification-cost

[4] Compyl. "How Long Does It Take to Get ISO 27001 Certified?" https://compyl.com/blog/how-long-does-it-take-to-get-iso-27001-certified

[5] Infosec Train. "Common Reasons for ISO 27001 Audit Failures." https://www.infosectrain.com/blog/common-reasons-for-iso-27001-audit-failures/

[6] A-LIGN. "ISO 27001 Certification Cost Breakdown." https://www.a-lign.com/articles/iso-27001-certification-cost
</details>

<details>
<summary>Rejection Questions</summary>

**Why Not Use ChatGPT/Claude for this?**
* Knowledge Cutoff & Version Issues
  * ChatGPT/Claude have knowledge cutoffs (Jan 2025 for Claude)
  * ISO 27001:2022 (current version) released after most AI training cutoffs
  * Chatbots may reference outdated ISO 27001:2013 guidance (different control structure)
  * **You can't trust generic AI for compliance-critical decisions based on outdated data**
* No Context Awareness
  * Doesn't know your company size, industry, or technology stack
  * Can't tailor implementation guidance to YOUR specific situation (cloud-based vs. on-premise, startup vs. enterprise)
  * **Every query requires manual context-setting about your environment**
* No Structured Implementation Logic
  * Can't systematically guide you through all 93 controls in proper sequence
  * Doesn't track which controls you've completed or flag dependencies
  * **Would require hundreds of manual prompts to cover everything, with no guarantee of consistency**
* No Quality Assurance
  * Generic chatbot advice might not satisfy auditor requirements
  * Can't reference specific ISO clause numbers and official terminology
  * **Risk of failing your $15K audit because ChatGPT gave you oversimplified guidance**
* Cost and Efficiency
  * Using ChatGPT for ISO implementation: 100+ hours of manual queries across 93 controls
  * Specialized tool: Guided implementation with context-aware recommendations
  * **At $150/hour consultant rates, DIY ChatGPT approach costs you $15K in time vs. $2K for purpose-built automation**
</details>

---

## Solution Overview
..._The "better world" for organizations pursuing ISO 27001 certification_...

**Picture this:** Instead of spending $30,000 on consultants to decipher what "implement cryptographic controls" means for your business, an IT manager selects Control 8.24 from a dashboard and instantly sees: **"Here's your 3-week implementation plan for cryptographic controls"**—with specific tools to use, policies to write, and audit evidence to collect, all tailored to their cloud-based infrastructure.

### From Abstract Requirements to Concrete Action Plans in Seconds

Most ISO 27001 resources give you the same generic advice everyone gets: "Document your access control policy" or "Conduct regular vulnerability assessments." That's like a cookbook that says "make the food taste good" without listing ingredients, measurements, or cooking steps.

**Our system bridges the gap automatically:** Select the control you need to implement → System analyzes your organization context → AI agent researches best practices and real examples → Get step-by-step implementation plan with templates, tools, and audit-ready documentation.

**What you get:**

Instead of abstract ISO language like *"Control 5.15: Access control - Rules to control access to information and information processing facilities shall be established and documented based on business and information security requirements"*, you instantly see:

> **📋 Implementation Plan for Control 5.15: Access Control Rules**
> 
> **What this means for your business:** You need written rules defining who can access what data/systems, and these rules must be documented in a format auditors can review.
> 
> **Quick implementation (2-3 weeks):**
> 
> **Week 1: Define Your Access Control Rules**
> - Identify your critical systems (email, CRM, file servers, databases)
> - Define user roles (employee, manager, IT admin, contractor)
> - Create access matrix: map which roles access which systems
> - Document business justification (why managers need CRM access, etc.)
> - 📄 [Download: Access Control Matrix Template]
> 
> **Week 2: Write the Policy Document**
> - Use our ISO-compliant template (references Control 5.15 explicitly)
> - Fill in your specific systems and roles from Week 1
> - Add your approval process for granting new access
> - Include review schedule (typically quarterly)
> - 📄 [Download: Access Control Policy Template - Tailored for 50-person companies]
> 
> **Week 3: Implement Technical Controls**
> - **For Microsoft 365:** Set up Azure AD role-based access (see guide)
> - **For AWS:** Configure IAM policies matching your access matrix (see guide)
> - Document your technical implementation with screenshots
> - Schedule first quarterly access review
> - 📄 [Download: Technical Implementation Checklist]
> 
> **Audit evidence you'll need:**
> - ✅ Approved Access Control Policy (with management signature)
> - ✅ Access Control Matrix showing role-to-system mappings
> - ✅ Screenshots of technical controls (Azure AD groups, IAM policies)
> - ✅ Evidence of quarterly access reviews (review meeting notes + updated matrix)
> 
> **Common auditor questions:**
> - *"How do you ensure access is removed when employees leave?"* → Add offboarding checklist to your policy
> - *"How do you handle exceptions to the standard rules?"* → Add exception approval process
> 
> **Tools we recommend:**
> - Microsoft Entra ID (formerly Azure AD) - $6/user/month for access management features
> - Okta - $2-$15/user/month depending on features needed
> - Open-source alternative: Keycloak (free, self-hosted)
> 
> [View detailed implementation guide with video walkthrough →]

For each of the 93 ISO 27001 controls, the system automatically provides:
- **Plain-English explanation:** What the control actually requires in practical terms
- **Context-specific implementation steps:** Tailored to your company size, industry, and tech stack
- **Ready-to-use templates:** Policy documents, procedures, checklists pre-formatted for ISO compliance
- **Tool recommendations:** Specific software tools with pricing and setup guides
- **Audit preparation:** Exactly what evidence auditors will ask for and how to prepare it

**Impact:**
* **Cost saved:** $20K-$50K in consulting fees (organizations implement controls themselves)
* **Time saved:** 3-4 months off typical implementation timeline (6-12 months → 2-3 months)
* **Audit success rate:** 90%+ first-time pass rate (vs. industry 40-60%)
* **Confidence gained:** Teams know exactly what they need to do instead of guessing

**The result:** Small and medium organizations can achieve ISO 27001 certification without expensive consultants, with implementation plans that actually fit their specific business context.

### Technical Stack

| Component Type | Component | Technology | Rationale |
|---------------|-----------|------------|-----------|
| **RAG System** | LLM | gpt-4o-mini | Cost-effective for prototype ($0.15/$0.60 per 1M tokens); sufficient for translating ISO controls into implementation guidance; handles technical security content well; proven ability to understand compliance requirements and generate actionable recommendations |
| **RAG System** | Embedding Model | OpenAI text-embedding-3-small | Extremely cost-effective at $0.02 per 1M tokens; 1536 dimensions adequate for semantic understanding of ISO standard clauses and implementation guides; can embed entire ISO 27001/27002 PDFs plus implementation documentation for under $1 |
| **RAG Evaluation (RAGAS)** | LLM | gpt-4o (full version) | RAGAS evaluation requires strong reasoning to assess whether implementation guidance is accurate, complete, and audit-ready; gpt-4o-mini insufficient for nuanced compliance evaluation; higher cost ($2.50/$10 per 1M tokens) justified since evaluation runs are infrequent |
| **RAG Evaluation (RAGAS)** | Embedding Model | OpenAI text-embedding-3-small | Must use identical embeddings as production RAG system to ensure evaluation consistency; RAGAS metrics rely on semantic similarity calculations between ISO standard requirements and implementation guidance |
| **Infrastructure** | Orchestration | LangGraph | Purpose-built for agentic workflows with state management; perfect for multi-step implementation planning (analyze control → research examples → generate plan → validate completeness); integrates seamlessly with LangChain ecosystem |
| **Infrastructure** | Vector Database | Qdrant (self-hosted) | Open-source; efficiently handles ISO standards documents, implementation guides, policy templates, and best practice examples; simple deployment via Docker; built-in filtering for metadata (control numbers, control categories, implementation phases) |
| **Infrastructure** | Monitoring | LangSmith | Purpose-built for LLM applications; tracks agent reasoning chains; helps debug why certain implementation approaches were recommended; provides cost tracking for API calls |
| **Infrastructure** | Evaluation | Custom test suite (20 known controls) | Ground truth from successful ISO 27001 audit reports and official implementation guidance; measures if system correctly interprets control requirements and generates audit-compliant recommendations; tracks precision/recall over time |
| **Infrastructure** | User Interface | Vite + React + Tailwind CSS | Lightning-fast dev server and builds; perfect for dashboard applications showing control implementation progress; Tailwind makes it easy to build clean, professional compliance dashboards; modern tooling with instant HMR for rapid iteration |
| **Infrastructure** | Backend Service | FastAPI (Python) | Fast API development; async support for handling multiple control analyses simultaneously; easy integration with PDF parsing libraries (PyPDF2, pdfplumber); native Python support for document processing and ML/AI libraries |

## System Architecture
```
┌─────────────────────────────────────────────────────────────────────┐
│                         USER INTERFACE (React)                      │
│  ┌──────────────────┐  ┌──────────────────┐  ┌──────────────────┐ │
│  │ Control Selection│  │ Implementation   │  │  Progress        │ │
│  │   Dashboard      │  │  Plan Viewer     │  │  Tracker         │ │
│  └──────────────────┘  └──────────────────┘  └──────────────────┘ │
└────────────────────────────────┬────────────────────────────────────┘
                                 │
                    ┌────────────▼─────────────┐
                    │   FastAPI Backend        │
                    │   - Context Analysis     │
                    │   - Control Processing   │
                    └────────────┬─────────────┘
                                 │
              ┏━━━━━━━━━━━━━━━━━▼━━━━━━━━━━━━━━━━━┓
              ┃      AGENTIC RAG ORCHESTRATOR      ┃
              ┃         (LangGraph)                ┃
              ┗━━━━━━━━━━━━━━━━━┬━━━━━━━━━━━━━━━━━┛
                                 │
        ┌────────────────────────┼────────────────────────┐
        │                        │                        │
┌───────▼────────┐    ┌─────────▼─────────┐    ┌────────▼────────┐
│  Analysis      │    │  Research         │    │  Generation     │
│  Agent         │    │  Agent            │    │  Agent          │
│                │    │                   │    │                 │
│ - Parse ISO    │    │ - Search best     │    │ - Create impl.  │
│   control      │    │   practices       │    │   plans         │
│ - Identify     │    │ - Find examples   │    │ - Generate      │
│   requirements │    │ - Locate tools    │    │   templates     │
│                │    │                   │    │ - Audit prep    │
└───────┬────────┘    └─────────┬─────────┘    └────────┬────────┘
        │                       │                        │
        └───────────────────────┼────────────────────────┘
                                │
                ┌───────────────┴────────────────┐
                │                                │
        ┌───────▼────────┐            ┌─────────▼──────────┐
        │  Vector Store  │            │  External Search   │
        │   (Qdrant)     │            │   (Tavily API)     │
        │                │            │                    │
        │ • ISO 27001    │            │ • Implementation   │
        │   PDF chunks   │            │   guides online    │
        │ • ISO 27002    │            │ • Tool reviews     │
        │   PDF chunks   │            │ • Case studies     │
        │ • Templates    │            │ • Best practices   │
        │ • Guidelines   │            │ • Vendor docs      │
        └────────────────┘            └────────────────────┘
                │
        ┌───────▼────────┐
        │   LangSmith    │
        │   Monitoring   │
        │                │
        │ • Agent traces │
        │ • Performance  │
        │ • Cost track   │
        └────────────────┘
```

## Data Sources & External APIs

| Source Type | Data Source | Source URL | Format | Content & Purpose | Phase |
|------------|-------------|------------|--------|-------------------|-------|
| **RAG Data** | ISO/IEC 27001:2022 Standard | ISO official PDF | PDF | Complete ISO 27001:2022 standard containing 93 security controls organized in 4 themes (Organizational, People, Physical, Technological); serves as authoritative source for control requirements and official wording that must be referenced in audit documentation | 1 |
| **RAG Data** | ISO/IEC 27002:2022 Implementation Guidance | ISO official PDF | PDF | Detailed implementation guidance for each ISO 27001 control with purpose, attributes, and recommended actions; provides official context for translating abstract requirements into practical implementations; critical for ensuring audit compliance | 1 |
| **User Input** | Organization Context Questionnaire | User form input | JSON | Company size, industry, technology stack (cloud vs. on-premise), existing tools, compliance deadlines; system uses this context to tailor implementation recommendations to specific business situations and resource constraints | 1 |
| **External API** | Tavily Search API | https://tavily.com/ | REST API | Real-time web search across vendor documentation, security blogs, implementation case studies, GitHub repositories, and compliance forums; agent searches for real-world implementation examples, tool recommendations, policy templates, and industry-specific best practices | 1 |
| **RAG Data** | ISO 27001 Policy Templates | Custom/Public templates | PDF/DOCX | Pre-written policy document templates for each control category (access control policies, incident response procedures, cryptographic policies); system customizes these templates with user's specific context and generates audit-ready documentation | 1 |
| **RAG Data** | Implementation Case Studies | Public case studies | PDF/Markdown | Real-world ISO 27001 implementation stories from various industries and company sizes; provides concrete examples of how organizations interpreted and implemented specific controls; helps system generate realistic, proven implementation approaches | 2 |
| **RAG Data** | Tool/Vendor Documentation | Vendor websites | PDF/HTML | Documentation for common security tools (Okta, Microsoft Entra ID, AWS IAM, vulnerability scanners); enables system to provide specific configuration guidance and technical implementation steps for popular platforms | 2 |
| **RAG Data** | Audit Reports (Anonymized) | ISO 27001 audit findings | PDF | Anonymized audit reports showing common non-conformities, auditor questions, and required evidence; system uses these to predict what auditors will ask and ensure implementation plans generate appropriate evidence | 2 |
| **External API** | Template Generation API | OpenAI GPT-4 | REST API | Dynamic policy and procedure document generation based on control requirements and user context; creates customized, audit-ready documentation with proper ISO clause references and company-specific details | 2 |
| **RAG Data** | Regulatory Mapping Database | Cross-reference documents | JSON/CSV | Mappings between ISO 27001 controls and other frameworks (SOC 2, NIST CSF, GDPR, HIPAA); enables system to show how implementing one control satisfies multiple compliance requirements, reducing duplicate work | 3 |
| **External API** | Document Management Integration | SharePoint API, Google Drive API, Confluence API | JSON via REST API | Integration with organization's document management systems; automatically stores generated policies and tracks version control; enables system to monitor which controls have approved documentation and which need updates | 3 |
| **External API** | Project Management Integration | Jira API, Asana API, Monday.com API | JSON via REST API | Creates implementation tasks with dependencies, assigns owners, and tracks progress; automatically generates project timeline showing critical path to certification and alerts teams to missed deadlines | 3 |
| **External API** | CMDB/Asset Management Integration | ServiceNow CMDB API, Device42 API | JSON via REST API | Pulls current asset inventory, system configurations, and network topology; enables system to provide implementation guidance based on actual infrastructure (e.g., "Configure these specific AWS accounts" vs. generic advice) | 3 |
| **External API** | Security Tool Integration | SIEM APIs, Vulnerability Scanner APIs, IAM System APIs | JSON via REST API | Automatically gathers evidence from existing security tools (access logs, vulnerability scan results, security configurations); reduces manual evidence collection and provides real-time compliance posture updates | 4 |
| **External API** | Audit Management Platform | AuditBoard API, LogicGate API | JSON via REST API | Direct integration with audit management platforms; automatically organizes evidence by control, generates audit evidence packages, and tracks auditor requests during certification process | 4 |
| **Internal Logic** | Implementation Progress Tracker | System-generated | N/A | Tracks completion status of all 93 controls, identifies dependencies and blockers, predicts certification readiness date based on current progress; uses ML to estimate remaining effort and flag high-risk gaps | 4 |
| **Internal Logic** | Continuous Compliance Monitor | System-generated | N/A | Monitors organization's ongoing compliance after certification; alerts when controls drift out of compliance (e.g., "Access review is 45 days overdue"); automatically triggers recertification preparation at renewal time | 4 |

### Chunking Methods
| Source Type | Data Source | Chunking Method | Reason |
|------------|-------------|-----------------|----|
| **RAG Data** | ISO/IEC 27001:2022 Standard | Custom control-based splitter | Each of 93 controls is semantically complete unit (typically 200-400 tokens); splitting by control number preserves complete requirement context and maintains traceability to official ISO clause references needed for audit documentation. |
| **RAG Data** | ISO/IEC 27002:2022 Implementation Guidance | Custom control-based splitter | Implementation guidance is organized by control number matching ISO 27001; chunking by control keeps purpose, attributes, and actions together as complete semantic units; typically 500-800 tokens per control which is optimal for retrieval. |
| **User Input** | Organization Context Questionnaire | No splitting (structured data) | Small JSON object (typically <500 tokens) containing company profile information; used as metadata to filter and contextualize all other chunks rather than embedded separately. |
| **External API** | Tavily Search API | N/A (Real-time retrieval) | External API returns real-time search results per query; no pre-processing or chunking needed; results are processed on-demand by generation agent. |
| **RAG Data** | ISO 27001 Policy Templates | RecursiveCharacterTextSplitter (1000 tokens, 200 overlap) | Policy templates are lengthy documents (2000-5000 tokens); recursive splitting preserves document structure while keeping policy sections together; overlap ensures cross-references between policy sections aren't lost. |
| **RAG Data** | Implementation Case Studies | MarkdownHeaderTextSplitter | Case studies use header structure to organize by control area, company type, and implementation phase; splitting by headers preserves logical sections and keeps related implementation details together. |
| **RAG Data** | Tool/Vendor Documentation | RecursiveCharacterTextSplitter (1000 tokens, 200 overlap) | Technical documentation varies widely in structure; recursive splitter handles mixed content (text, code snippets, configuration examples) while maintaining context about specific features and setup steps. |
| **RAG Data** | Audit Reports (Anonymized) | Custom section-based splitter | Audit reports are organized by control findings; splitting by control number groups all findings, auditor comments, and required evidence for each control together; maintains compliance context. |
| **RAG Data** | Regulatory Mapping Database | No splitting (structured lookup) | CSV/JSON mapping table with control-to-framework relationships; stored as metadata attached to control chunks rather than embedded separately; enables efficient filtering during retrieval. |

### Data Flow

```
┌─────────────────────────────────────────────────────────────────────┐
│                    STEP 1: User Interaction                         │
│                                                                      │
│  User Action: Select Control (e.g., "Control 5.15: Access Control") │
│             + Provide Organization Context (50 employees, cloud)     │
│                                                                      │
│                              │                                       │
│                              ▼                                       │
│                   ┌────────────────────┐                            │
│                   │  Context Analysis  │                            │
│                   │  - Company size    │                            │
│                   │  - Industry        │                            │
│                   │  - Tech stack      │                            │
│                   │  - Timeline needs  │                            │
│                   └────────────────────┘                            │
└──────────────────────────┬──────────────────────────────────────────┘
                           │
┌──────────────────────────▼──────────────────────────────────────────┐
│              STEP 2: Multi-Agent Orchestration                      │
│                      (LangGraph)                                     │
│                                                                      │
│  ┌────────────────────────────────────────────────────────────┐    │
│  │  AGENT 1: Analysis Agent                                    │    │
│  │  ┌────────────────────────────────────────────────────┐    │    │
│  │  │ Query Vector Store (Qdrant):                       │    │    │
│  │  │  "ISO 27001 Control 5.15 requirements"             │    │    │
│  │  │                                                     │    │    │
│  │  │ Retrieved Chunks:                                  │    │    │
│  │  │  • ISO 27001 Control 5.15 full text               │    │    │
│  │  │  • ISO 27002 implementation guidance              │    │    │
│  │  │  • Related controls (5.18, 8.2)                   │    │    │
│  │  └────────────────────────────────────────────────────┘    │    │
│  │                                                              │    │
│  │  Extracted Requirements:                                    │    │
│  │   ✓ Define access control rules                            │    │
│  │   ✓ Document rules based on business needs                 │    │
│  │   ✓ Establish approval process for access                  │    │
│  │   ✓ Review access rights periodically                      │    │
│  └────────────────────────────────────────────────────────────┘    │
│                           │                                          │
│                           ▼                                          │
│  ┌────────────────────────────────────────────────────────────┐    │
│  │  AGENT 2: Research Agent                                    │    │
│  │  ┌────────────────────────────────────────────────────┐    │    │
│  │  │ Parallel Searches:                                 │    │    │
│  │  │                                                     │    │    │
│  │  │ Search 1 - Vector Store:                          │    │    │
│  │  │  "access control policy templates"                │    │    │
│  │  │   → Policy template chunks                        │    │    │
│  │  │   → Example access matrices                       │    │    │
│  │  │                                                     │    │    │
│  │  │ Search 2 - Tavily API:                            │    │    │
│  │  │  "ISO 27001 access control implementation         │    │    │
│  │  │   best practices cloud infrastructure"            │    │    │
│  │  │   → Real implementation guides                    │    │    │
│  │  │   → Tool recommendations (Okta, Azure AD)         │    │    │
│  │  │   → Case studies from similar companies           │    │    │
│  │  │                                                     │    │    │
│  │  │ Search 3 - Vector Store:                          │    │    │
│  │  │  "audit evidence access control"                  │    │    │
│  │  │   → Audit report excerpts                         │    │    │
│  │  │   → Required evidence examples                    │    │    │
│  │  └────────────────────────────────────────────────────┘    │    │
│  │                                                              │    │
│  │  Compiled Research:                                         │    │
│  │   • 3 policy templates (generic, cloud-focused, SMB)       │    │
│  │   • 4 real implementation examples                          │    │
│  │   • 5 recommended tools with pricing                        │    │
│  │   • Audit evidence requirements list                        │    │
│  └────────────────────────────────────────────────────────────┘    │
│                           │                                          │
│                           ▼                                          │
│  ┌────────────────────────────────────────────────────────────┐    │
│  │  AGENT 3: Generation Agent                                  │    │
│  │                                                              │    │
│  │  Inputs:                                                     │    │
│  │   • ISO 27001 requirements (from Agent 1)                   │    │
│  │   • Research findings (from Agent 2)                        │    │
│  │   • User context (50 employees, cloud, 3-month timeline)    │    │
│  │                                                              │    │
│  │  LLM Processing (gpt-4o-mini):                              │    │
│  │   → Synthesize requirements + research + context            │    │
│  │   → Generate step-by-step implementation plan               │    │
│  │   → Customize policy template for user's environment        │    │
│  │   → Create audit evidence checklist                         │    │
│  │   → Add tool-specific configuration guidance                │    │
│  └────────────────────────────────────────────────────────────┘    │
└──────────────────────────┬──────────────────────────────────────────┘
                           │
┌──────────────────────────▼──────────────────────────────────────────┐
│                   STEP 3: Output Delivery                           │
│                                                                      │
│  Generated Implementation Plan:                                     │
│                                                                      │
│  ┌────────────────────────────────────────────────────────────┐    │
│  │ 📋 IMPLEMENTATION PLAN: CONTROL 5.15                       │    │
│  │                                                             │    │
│  │ WEEK 1: Define Access Rules                               │    │
│  │  ✓ Identify critical systems (AWS, Microsoft 365)         │    │
│  │  ✓ Define roles (Employee, Manager, IT Admin)             │    │
│  │  ✓ Create access matrix [Download Template]               │    │
│  │  ⏱️ Estimated time: 8 hours                                │    │
│  │                                                             │    │
│  │ WEEK 2: Document Policy                                    │    │
│  │  ✓ Use cloud-focused policy template [Download]           │    │
│  │  ✓ Fill in your specific systems & roles                  │    │
│  │  ✓ Add approval workflow for new access                   │    │
│  │  ⏱️ Estimated time: 6 hours                                │    │
│  │                                                             │    │
│  │ WEEK 3: Implement Technical Controls                      │    │
│  │  ✓ Configure Azure AD role-based access [Setup Guide]     │    │
│  │  ✓ Set up AWS IAM policies [Setup Guide]                  │    │
│  │  ✓ Document configurations with screenshots               │    │
│  │  ⏱️ Estimated time: 12 hours                               │    │
│  │                                                             │    │
│  │ RECOMMENDED TOOLS:                                         │    │
│  │  🔧 Microsoft Entra ID (Azure AD) - $6/user/month         │    │
│  │     Best for: Existing Microsoft 365 customers            │    │
│  │     [View setup guide]                                     │    │
│  │                                                             │    │
│  │  🔧 Okta - $2-$15/user/month                              │    │
│  │     Best for: Multi-cloud environments                     │    │
│  │     [View setup guide]                                     │    │
│  │                                                             │    │
│  │ AUDIT EVIDENCE CHECKLIST:                                  │    │
│  │  ✅ Approved Access Control Policy (with signature)        │    │
│  │  ✅ Access Control Matrix                                  │    │
│  │  ✅ Technical control screenshots (Azure AD/IAM)           │    │
│  │  ✅ Quarterly access review records                        │    │
│  │                                                             │    │
│  │ AUDITOR Q&A PREP:                                          │    │
│  │  Q: "How do you handle access for contractors?"            │    │
│  │  A: Add contractor role to matrix + temporary access       │    │
│  │     provisioning workflow to policy                        │    │
│  └────────────────────────────────────────────────────────────┘    │
│                                                                      │
│  Downloadable Artifacts:                                            │
│   📄 Customized Access Control Policy (DOCX)                       │
│   📄 Access Control Matrix Template (XLSX)                         │
│   📄 Azure AD Configuration Guide (PDF)                            │
│   📄 Audit Evidence Checklist (PDF)                                │
└─────────────────────────────────────────────────────────────────────┘
```

**How the system works:**

1. **Select & Contextualize**: User selects ISO 27001 control they need to implement → Provides organization context (company size, industry, tech stack, timeline) → System understands specific business situation
2. **Intelligent Analysis**: Analysis Agent retrieves official ISO 27001/27002 requirements from vector store → Extracts specific obligations (what must be documented, what processes must exist, what evidence is needed) → Identifies related controls that may need simultaneous implementation
3. **Comprehensive Research**: Research Agent searches both internal knowledge base and external sources → Finds proven implementation approaches from similar organizations → Identifies specific tools and vendors appropriate for user's tech stack → Locates policy templates and audit evidence examples
4. **Contextual Generation**: Generation Agent synthesizes all findings into actionable plan → Customizes implementation steps for user's specific context (not generic advice) → Generates ready-to-use policy documents with user's information pre-filled → Creates audit evidence checklist to ensure compliance
5. **Actionable Deliverables**: Instead of abstract ISO language, users receive concrete implementation roadmap with time estimates, specific tools to use, customized policy templates, configuration guides for their tech stack, and audit preparation materials

<details>
<summary>Implementation Roadmap</summary>

**Phase 1: Prototype (Bootcamp Certification)**
* Core control implementation guidance system. Users select ISO 27001 controls, system retrieves requirements from ISO PDFs, searches for implementation examples via Tavily, and generates step-by-step plans with policy templates customized to user's basic context (company size, industry).

**Phase 2: Enhanced Intelligence (Graduation Project)**
* Advanced context awareness and tool integration. Adds comprehensive tool documentation database, implementation case studies from multiple industries, and audit report analysis to predict common non-conformities; generates more sophisticated recommendations based on specific technology stacks and provides cross-framework compliance mapping (ISO 27001 + SOC 2 + GDPR).

**Phase 3: Enterprise Integration & Automation**
* Full document and project management integration. Direct API connections to SharePoint/Google Drive for policy storage, Jira/Asana for task tracking, and CMDB systems for asset inventory; automatically creates implementation project plans with dependencies, assigns tasks to owners, and monitors progress toward certification deadline.

**Phase 4: Continuous Compliance & Evidence Automation**
* Ongoing compliance monitoring and automated audit preparation. Integrates with security tools (SIEM, IAM, vulnerability scanners) to automatically gather compliance evidence, monitors control effectiveness over time, alerts when controls drift out of compliance, and generates audit evidence packages on-demand during certification audits.
</details>

---

## Task 4: Building an End-to-End Agentic RAG Prototype
Build an end-to-end Agentic RAG application using a production-grade stack and your choice of commercial off-the-shelf model(s)

### Deliverables:
1. Build an end-to-end prototype and deploy it to a local endpoint
2. (Optional) use locally-hosted OSS models instead of LLMs through the OpenAI API

---

## Task 5: Creating a Golden Test Data Set - You are an AI Evaluation & Performance Engineer.
The AI Systems Engineer who built the initial RAG system has asked for your help and expertise in creating a "Golden Data Set" for evaluation.

Prepare a test data set (either by generating synthetic data or by assembling an existing dataset) to baseline an initial evaluation with RAGAS.

### Deliverables:
1. Assess your pipeline using the RAGAS framework including key metrics faithfulness, response relevancy, context precision, and context recall. Provide a table of your output results.
2. What conclusions can you draw about the performance and effectiveness of your pipeline with this information?

### Suggested Golden Test Dataset Structure:
Create 20 test cases covering different control types and complexity levels:

**Simple Controls (5 test cases)**: Controls with straightforward requirements
- Example: Control 5.7 "Threat intelligence" - Clear requirement to gather threat information

**Complex Controls (5 test cases)**: Multi-faceted controls requiring multiple implementation steps
- Example: Control 8.8 "Management of technical vulnerabilities" - Requires scanning, prioritization, patching, verification

**Context-Dependent Controls (5 test cases)**: Controls where implementation varies significantly by company context
- Example: Control 5.23 "Information security for use of cloud services" - Different for AWS vs Azure vs multi-cloud

**Interconnected Controls (5 test cases)**: Controls with dependencies on other controls
- Example: Control 5.15 "Access control" requires Control 5.18 "Access rights" and Control 5.16 "Identity management"

**Ground Truth Source**: Use official ISO 27002:2022 implementation guidance + publicly available implementation guides from Big 4 consulting firms (Deloitte, PwC, EY, KPMG) + actual audit reports showing accepted implementations.

---

## Task 6: The Benefits of Advanced Retrieval - You are an AI Systems Engineer.
The AI Evaluation and Performance Engineer has asked for your help in making stepwise improvements to the application. They heard that "as goes retrieval, so goes generation" and have asked for your expertise.

### Deliverables:
1. Describe the retrieval techniques that you plan to try and to assess in your application. Write one sentence on why you believe each technique will be useful for your use case.
2. Test a host of advanced retrieval techniques on your application.

### Suggested Advanced Retrieval Techniques:

**Hybrid Search (Dense + Sparse)**:
- Combine semantic search (embeddings) with keyword search (BM25) to catch both conceptual similarity and exact ISO clause references (e.g., "Control 5.15" must be found even if semantically similar text exists elsewhere).

**Metadata Filtering**:
- Filter by control number, control theme (Organizational/People/Physical/Technological), implementation phase, and company size relevance before semantic search to reduce noise and improve precision.

**Parent Document Retrieval**:
- Retrieve small chunks for specificity but return entire control section for full context; prevents fragmented implementation guidance where steps are split across chunks.

**Query Rewriting**:
- Expand user's control selection into multiple search queries: (1) official ISO requirements, (2) implementation best practices, (3) tool recommendations, (4) audit evidence requirements.

**Reranking**:
- Use cross-encoder reranker to score retrieved chunks by relevance to user's specific context (company size, industry, tech stack) rather than just semantic similarity to generic control description.

**Contextual Compression**:
- Extract only relevant sentences from long ISO documents and case studies to reduce token usage and improve LLM focus on key requirements rather than surrounding text.

---

## Task 7: Assessing Performance - You are the AI Evaluation & Performance Engineer.
Assess the performance of the naive agentic RAG application versus the applications with advanced retrieval tooling

### Deliverables:
1. How does the performance compare to your original RAG application? Test the improved system using the RAGAS framework to quantify improvements. Provide results in a table.
2. Articulate the changes that you expect to make to your app in the second half of the course. How will you improve your application?

### Expected Performance Improvements:
- **Context Precision**: +15-25% improvement (hybrid search + reranking ensures retrieved chunks actually contain implementation guidance, not just control definitions)
- **Context Recall**: +10-20% improvement (parent document retrieval captures complete implementation workflows that span multiple chunks)
- **Answer Relevancy**: +20-30% improvement (query rewriting ensures system finds implementation guidance, tool recommendations, AND audit requirements in one pass)
- **Faithfulness**: +5-10% improvement (contextual compression reduces hallucinations by focusing LLM on key facts rather than verbose ISO language)

### Phase 2 Improvements Plan:

**Enhanced Knowledge Base**:
- Add 50+ implementation case studies from various industries
- Integrate vendor tool documentation (Okta, Microsoft, AWS IAM, etc.)
- Include anonymized audit reports showing accepted evidence

**Context-Aware Recommendations**:
- Build decision tree logic that adjusts implementation guidance based on:
  - Company size (startup vs enterprise)
  - Industry (healthcare vs fintech vs SaaS)
  - Tech stack (cloud-native vs hybrid vs on-premise)
  - Timeline (3 months vs 6 months vs 12 months)

**Multi-Control Dependencies**:
- Automatically identify when implementing one control requires implementing related controls first
- Generate holistic implementation plans that address dependencies (e.g., can't implement access control without identity management)

**Template Customization Engine**:
- Dynamically generate policy documents with user's company name, asset lists, and specific processes pre-filled
- Ensure all generated documents include proper ISO clause references for audit traceability

**Progressive Disclosure UI**:
- Show high-level implementation summary first, allow drill-down into detailed technical steps
- Provide "Quick Start" path for experienced teams vs. "Comprehensive Guide" for ISO newcomers
