# Adding New Standards to the System

This guide shows you how to add support for new ISO standards (like ISO 31000, ISO 19011, ISO 9001, etc.)

## Quick Overview

The system is designed to support multiple standards with minimal code changes. Each standard needs:
1. A control definitions file
2. PDF documents uploaded to vector database
3. One line changed in `utils/standards.py`

---

## Step-by-Step: Adding ISO 31000 (Risk Management)

### Step 1: Create Control Definitions File

Create `backend/standards/iso_31000_controls.py`:

```python
"""
ISO 31000:2018 Risk Management Controls
"""

ISO_31000_CONTROLS = {
    # Principles
    "principles": [
        {
            "id": "P1",
            "title": "Integrated",
            "priority": "high",
            "estimated_hours": 8,
            "owner": "Risk Manager / CISO",
            "deliverables": [
                "Risk_Management_Framework.docx",
                "Integration_Plan.docx"
            ],
            "description": "Risk management is an integral part of all organizational activities"
        },
        {
            "id": "P2",
            "title": "Structured and Comprehensive",
            "priority": "high",
            "estimated_hours": 6,
            "owner": "Risk Manager",
            "deliverables": [
                "Risk_Management_Policy.docx",
                "Risk_Assessment_Procedure.docx"
            ],
            "description": "A structured and comprehensive approach contributes to consistent results"
        },
        {
            "id": "P3",
            "title": "Customized",
            "priority": "medium",
            "estimated_hours": 4,
            "owner": "Risk Manager",
            "deliverables": [
                "Context_Analysis.docx",
                "Risk_Criteria.xlsx"
            ],
            "description": "Risk management framework and process are customized and proportionate"
        }
    ],
    
    # Framework
    "framework": [
        {
            "id": "F1",
            "title": "Leadership and Commitment",
            "priority": "high",
            "estimated_hours": 4,
            "owner": "Senior Management",
            "deliverables": [
                "Risk_Management_Charter.docx",
                "Management_Commitment_Statement.pdf"
            ],
            "description": "Ensure leadership and commitment to risk management"
        },
        {
            "id": "F2",
            "title": "Integration into Organizational Processes",
            "priority": "high",
            "estimated_hours": 10,
            "owner": "Risk Manager / Process Owners",
            "deliverables": [
                "Process_Integration_Plan.docx",
                "Risk_Workflow_Diagrams.pdf"
            ],
            "description": "Integrate risk management into all organizational processes"
        }
    ],
    
    # Process
    "process": [
        {
            "id": "PR1",
            "title": "Risk Identification",
            "priority": "high",
            "estimated_hours": 12,
            "owner": "Risk Manager",
            "deliverables": [
                "Risk_Identification_Procedure.docx",
                "Risk_Register.xlsx",
                "Risk_Identification_Workshop_Template.pptx"
            ],
            "description": "Systematically identify sources of risk and potential consequences"
        },
        {
            "id": "PR2",
            "title": "Risk Analysis",
            "priority": "high",
            "estimated_hours": 10,
            "owner": "Risk Manager / Analysts",
            "deliverables": [
                "Risk_Analysis_Methodology.docx",
                "Risk_Heat_Map.xlsx",
                "Analysis_Report_Template.docx"
            ],
            "description": "Comprehend the nature of risk and determine level of risk"
        },
        {
            "id": "PR3",
            "title": "Risk Evaluation",
            "priority": "high",
            "estimated_hours": 8,
            "owner": "Risk Manager",
            "deliverables": [
                "Risk_Evaluation_Criteria.docx",
                "Risk_Acceptance_Matrix.xlsx"
            ],
            "description": "Compare risk analysis results with risk criteria"
        },
        {
            "id": "PR4",
            "title": "Risk Treatment",
            "priority": "high",
            "estimated_hours": 15,
            "owner": "Risk Manager / Risk Owners",
            "deliverables": [
                "Risk_Treatment_Plan.docx",
                "Risk_Treatment_Options_Analysis.xlsx",
                "Implementation_Roadmap.pdf"
            ],
            "description": "Select and implement options for addressing risk"
        }
    ]
}


def get_all_controls():
    """Get all controls as a flat list."""
    all_controls = []
    for theme, controls in ISO_31000_CONTROLS.items():
        for control in controls:
            control["theme"] = theme
            all_controls.append(control)
    return sorted(all_controls, key=lambda x: x["id"])


def get_high_priority_controls():
    """Get only high-priority controls."""
    all_controls = get_all_controls()
    return [c for c in all_controls if c.get("priority") == "high"]


def get_control_by_id(control_id: str):
    """Get a specific control by ID."""
    all_controls = get_all_controls()
    for control in all_controls:
        if control["id"] == control_id:
            return control
    return None
```

**Key Points:**
- Use the exact same structure as `iso_27001_controls.py`
- Include the 3 helper functions at the bottom
- Customize control IDs, themes, and content for your standard

---

### Step 2: Upload Standard PDFs

Upload ISO 31000 PDF documents to the vector database:

```bash
# Using the upload endpoint:
curl -X POST "http://localhost:8000/upload?clear_existing=false" \
  -F "files=@iso_31000_2018.pdf"
```

Or use the frontend upload feature (uncheck "replace existing").

**Important:** Set `clear_existing=false` to add to existing documents, not replace them!

---

### Step 3: Activate the Standard

Update `backend/utils/standards.py`:

**Change this:**
```python
"ISO_31000": {
    ...
    "status": "coming_soon"  # ← BEFORE
}
```

**To this:**
```python
"ISO_31000": {
    ...
    "status": "active"  # ← AFTER (or just remove this line)
}
```

**And uncomment the import:**
```python
# In get_controls_for_standard() function:
elif standard_id == "ISO_31000":
    from standards.iso_31000_controls import get_all_controls
    return get_all_controls()
```

---

### Step 4: Test It!

Restart the backend:
```bash
cd backend
uv run uvicorn main:app --reload
```

Test the API:
```bash
# Get ISO 31000 controls
curl http://localhost:8000/controls?standard=ISO_31000

# Generate implementation guide
curl -X POST http://localhost:8000/controls/PR1/implement \
  -H "Content-Type: application/json" \
  -d '{
    "company_size": "50-100",
    "industry": "Software/SaaS",
    "tech_stack": ["AWS"],
    "deadline_months": 6
  }'
```

---

## Adding Other Standards

### ISO 19011 (Auditing Management Systems)

1. Create `backend/standards/iso_19011_controls.py`
2. Structure controls around audit principles, managing audit programs, and conducting audits
3. Upload ISO 19011 PDFs
4. Activate in `standards.py`

### ISO 9001 (Quality Management)

1. Create `backend/standards/iso_9001_controls.py`
2. Structure controls around QMS requirements (context, leadership, planning, support, operation, performance evaluation, improvement)
3. Upload ISO 9001 PDFs
4. Activate in `standards.py`

---

## Frontend Integration (Future)

To add standard selector to the frontend:

```jsx
// In Dashboard.jsx, add:
const [selectedStandard, setSelectedStandard] = useState('ISO_27001')

// Fetch standards on load:
useEffect(() => {
  fetch(`${API_URL}/standards`)
    .then(res => res.json())
    .then(data => setStandards(data.standards))
}, [])

// Add dropdown:
<select onChange={(e) => setSelectedStandard(e.target.value)}>
  {standards.map(s => (
    <option key={s.id} value={s.id} disabled={!s.is_available}>
      {s.name} {!s.is_available && '(Coming Soon)'}
    </option>
  ))}
</select>

// Update controls fetch:
fetchControls(selectedStandard)
```

---

## File Structure

```
backend/
├── standards/
│   ├── __init__.py
│   ├── iso_27001_controls.py  ✅ (Active)
│   ├── iso_31000_controls.py  🟡 (Add this)
│   ├── iso_19011_controls.py  🟡 (Add this)
│   └── iso_9001_controls.py   🟡 (Add this)
├── utils/
│   ├── standards.py           ← Registry of all standards
│   ├── agents.py              ← Agentic RAG (works for all standards)
│   └── ...
└── data/
    ├── isoiec_27001_2022.pdf
    ├── isoiec_27002_2022.pdf
    ├── iso_31000_2018.pdf     🟡 (Upload this)
    └── iso_19011_2018.pdf     🟡 (Upload this)
```

---

## Control Structure Template

Every control needs these fields:

```python
{
    "id": str,              # e.g., "5.1", "P1", "A1"
    "title": str,           # Short descriptive name
    "priority": str,        # "high", "medium", or "low"
    "estimated_hours": int, # Time to implement
    "owner": str,           # Who implements it
    "deliverables": [str],  # List of files to create
    "description": str,     # What the control does
    "theme": str           # Auto-added (organizational, process, etc.)
}
```

---

## That's It!

Adding a new standard requires:
1. ✍️ ~200 lines of Python (control definitions)
2. 📄 Upload PDFs
3. 🔧 Change 1 status flag

The agentic RAG system automatically works with any standard - no changes needed! 🚀

---

## Questions?

- **Q: Can I mix multiple standards in one project?**
  A: Yes! The system tracks controls per standard. Upload all PDFs, and the RAG will use context from all of them.

- **Q: Do I need to modify the prompts for new standards?**
  A: No! The prompts are generic and work with any ISO standard.

- **Q: What if my standard doesn't have "controls" but has different structure?**
  A: Just adapt the structure in your controls file. The "control" is just a unit of work - it can be a principle, requirement, clause, or whatever makes sense.

- **Q: Can I add non-ISO standards?**
  A: Absolutely! NIST, CIS Controls, PCI-DSS, etc. all work the same way.

