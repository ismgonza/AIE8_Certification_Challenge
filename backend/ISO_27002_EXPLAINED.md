# 📘 ISO 27002 - What It Is and Why You Don't Need Separate Controls

## TL;DR

**You already have ISO 27002!** 🎉

ISO 27002 is **not** a separate standard with different controls. It's the **implementation guide** for ISO 27001 Annex A controls.

---

## What's the Difference?

### ISO 27001:2022
- ✅ **Certification Standard** - You get certified against this
- ✅ **Requirements** - Tells you WHAT you must do
- ✅ **Annex A** - 93 controls (organized in 4 themes)

### ISO 27002:2022
- 📖 **Code of Practice** - Implementation guidance
- 📖 **How-To Guide** - Tells you HOW to implement the controls
- 📖 **Same Controls** - The exact same 93 controls from ISO 27001 Annex A

---

## How They Work Together

```
┌─────────────────────────────────────────────────────────┐
│                    ISO 27001:2022                        │
│  (Requirements for ISMS - What you get certified for)   │
│                                                          │
│  Clause 4-10: ISMS Requirements                         │
│  Annex A: 93 Security Controls                          │
│    ├── 5.1-5.37  Organizational (37 controls)           │
│    ├── 6.1-6.8   People (8 controls)                    │
│    ├── 7.1-7.14  Physical (14 controls)                 │
│    └── 8.1-8.34  Technological (34 controls)            │
└─────────────────────────────────────────────────────────┘
                           │
                           │ Implementation details
                           ▼
┌─────────────────────────────────────────────────────────┐
│                    ISO 27002:2022                        │
│     (Code of Practice - HOW to implement controls)      │
│                                                          │
│  For each of the 93 controls, provides:                 │
│    • Purpose                                             │
│    • Implementation guidance                             │
│    • Additional information                              │
│    • Attributes (control type, security properties)      │
└─────────────────────────────────────────────────────────┘
```

---

## In This System

### Your Current Setup ✅

```
backend/
├── data/
│   ├── isoiec_27001_2022.pdf  ← Requirements + Control list
│   └── isoiec_27002_2022.pdf  ← Implementation guidance
├── standards/
│   └── iso_27001_controls.py  ← 25 sample controls
```

**The RAG system uses BOTH PDFs together:**
- When you ask about a control (e.g., 5.15 Access Control)
- It retrieves context from **both** documents
- ISO 27001 PDF: Requirement and control statement
- ISO 27002 PDF: Detailed implementation guidance

### Example: Control 5.15 (Access Control)

**ISO 27001 says:**
> "Rules to control physical and logical access to information and other associated assets shall be established and implemented based on business and information security requirements."

**ISO 27002 says:**
> Here's HOW to do it:
> - Establish access control policy
> - Define access rights
> - Implement need-to-know principle
> - Manage special access rights
> - Review access rights regularly
> - Document everything
> - [Plus 3 more pages of detailed guidance]

**Your Implementation Guide combines both!** 🎯

---

## Why Only 25 Controls in Code?

You might wonder: "ISO 27001/27002 have 93 controls, but `iso_27001_controls.py` only has 25?"

**Answer:** These are **curated starter controls** for the dashboard UI to:
1. Focus on high-priority items first
2. Cover all 4 themes (organizational, people, physical, technological)
3. Keep the dashboard manageable for small-medium businesses

**The RAG system has access to ALL 93 controls** via the uploaded PDFs!

---

## Do You Need to Add ISO 27002 Controls Separately?

**No!** Here's why:

### ❌ Wrong Approach:
```python
# DON'T DO THIS
iso_27001_controls.py  # 25 controls
iso_27002_controls.py  # Same 25 controls again (duplicate!)
```

### ✅ Correct Approach (What You Have):
```python
# This is correct:
iso_27001_controls.py  # 25 key controls for dashboard
# Both PDFs in vector DB for comprehensive RAG answers
```

---

## What About the Other 68 Controls?

You have two options:

### Option 1: Add More to Dashboard (Recommended)
If you want all 93 controls in the dashboard:

```python
# Expand iso_27001_controls.py to include all 93:
"organizational": [
    # Add 5.4, 5.5, 5.6, 5.8-5.14, 5.19-5.22, 5.24-5.29, 5.31-5.37
    ...
],
"people": [
    # Add 6.4-6.8
    ...
],
# etc.
```

### Option 2: Use RAG for Others (Current)
The RAG system can already answer questions about **any** of the 93 controls because both PDFs are uploaded:

```bash
# You can ask about ANY control, even ones not in the dashboard:
curl -X POST http://localhost:8000/query \
  -H "Content-Type: application/json" \
  -d '{
    "question": "How do I implement ISO 27001 control 5.4 Management Responsibilities?"
  }'
```

---

## Summary

| Aspect | Status | Notes |
|--------|--------|-------|
| ISO 27001 Standard | ✅ Uploaded | PDF in `/data` |
| ISO 27002 Guide | ✅ Uploaded | PDF in `/data` |
| Controls in Dashboard | ✅ 25 controls | High-priority subset |
| Controls in RAG | ✅ All 93 | Via uploaded PDFs |
| Need separate ISO 27002 module? | ❌ No | Already covered! |

---

## Quick Actions

### 1. Verify Both PDFs Are Uploaded
```bash
curl http://localhost:8000/documents?limit=10
# Should show chunks from both PDFs
```

### 2. Test a Non-Dashboard Control
```bash
# Ask about control 5.4 (not in dashboard, but in PDFs)
curl -X POST http://localhost:8000/query \
  -H "Content-Type: application/json" \
  -d '{
    "question": "How do I implement ISO 27001 control 5.4?"
  }'
```

### 3. Add More Controls to Dashboard (Optional)
Edit `backend/standards/iso_27001_controls.py` and add more controls using the same format.

---

## Further Reading

- [ISO 27001:2022 Overview](https://www.iso.org/standard/27001)
- [ISO 27002:2022 Overview](https://www.iso.org/standard/75652.html)
- [Annex A Full Control List](https://www.isms.online/iso-27001/annex-a/)

---

**Bottom Line:** You don't need to add ISO 27002 separately. It's already working behind the scenes in your RAG system! 🚀

