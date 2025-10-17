# 🚀 Quick Start Guide

## What We Just Built

✅ **ISO 31000 Risk Management Standard** - Fully integrated with 22 controls  
✅ **Upload Interface** - Now accessible from dashboard header  
✅ **Multi-Standard Architecture** - Ready to add ISO 19011, ISO 9001, etc.  
✅ **Organized Code Structure** - Standards in dedicated folder

---

## 🎯 Current System Status

### Available Standards
| Standard | Status | Controls | Focus Area |
|----------|--------|----------|------------|
| **ISO 27001:2022** | ✅ Active | 25 | Information Security |
| **ISO 31000:2018** | ✅ Active | 22 | Risk Management |
| **ISO 19011:2018** | 🟡 Coming Soon | - | Audit Guidelines |
| **ISO 9001:2015** | 🟡 Coming Soon | - | Quality Management |

### File Structure
```
backend/
├── standards/                  ← NEW!
│   ├── __init__.py
│   ├── iso_27001_controls.py  ✅ (25 controls)
│   └── iso_31000_controls.py  ✅ (22 controls)
├── utils/
│   ├── standards.py           ← Multi-standard registry
│   ├── agents.py              ← Agentic RAG (LangGraph)
│   ├── prompts.py             ← LLM prompts
│   ├── tools.py               ← External tools (Tavily)
│   ├── rag.py                 ← RAG pipeline
│   ├── vector_store.py        ← Qdrant integration
│   └── document_processor.py  ← PDF processing
└── data/
    ├── isoiec_27001_2022.pdf
    ├── isoiec_27002_2022.pdf
    └── iso_31000.pdf          ✅ Ready to upload

frontend/
└── src/
    ├── Dashboard.jsx          ✅ With upload interface
    └── App.jsx
```

---

## 🏃 How to Run

### 1. Start Backend
```bash
cd backend
uv run uvicorn main:app --reload
```
Backend will run on: `http://localhost:8000`

### 2. Upload ISO 31000 PDF
```bash
# Option A: Using curl
curl -X POST "http://localhost:8000/upload?clear_existing=false" \
  -F "files=@data/iso_31000.pdf"

# Option B: Using the frontend (recommended)
# 1. Click "📤 Upload Documents" button in dashboard header
# 2. Select iso_31000.pdf
# 3. Leave "Clear existing" unchecked
# 4. Click "Upload & Process"
```

### 3. Start Frontend
```bash
cd frontend
npm run dev
```
Frontend will run on: `http://localhost:5173`

---

## 🎨 Using the Upload Interface

### Location
- **Top-right of dashboard header**
- Click "📤 Upload Documents" button

### Features
- ✅ Multiple file upload (select multiple PDFs at once)
- ✅ Progress indicator during upload
- ✅ Option to clear existing data (use with caution!)
- ✅ Shows selected files before upload
- ✅ Success/error notifications

### Tips
- **Keep existing data**: Leave "Clear existing documents" unchecked
- **Fresh start**: Check "Clear existing documents" to remove all current data
- **Multiple standards**: Upload ISO 27001 + ISO 31000 together for cross-standard insights

---

## 🧪 Testing ISO 31000

### Test Controls Endpoint
```bash
# Get all ISO 31000 controls
curl http://localhost:8000/controls?standard=ISO_31000

# Get control details
curl http://localhost:8000/controls/6.4.1
```

### Test Implementation Guide
```bash
curl -X POST http://localhost:8000/controls/6.4.1/implement \
  -H "Content-Type: application/json" \
  -d '{
    "company_size": "50-100",
    "industry": "Manufacturing",
    "tech_stack": ["SAP", "Microsoft 365"],
    "deadline_months": 6
  }'
```

### Example Controls
- **4.1** - Integrated Risk Management (high priority, 8 hours)
- **6.4.1** - Risk Identification (high priority, 12 hours)
- **6.5** - Risk Treatment (high priority, 15 hours)
- **5.4.2** - Framework Design (high priority, 12 hours)

---

## 📊 API Endpoints

### Standards
- `GET /standards` - List all available standards
- `GET /controls?standard=ISO_31000` - Get controls for specific standard

### Controls
- `GET /controls` - Get all ISO 27001 controls (default)
- `GET /controls/priority/high` - Get high-priority controls
- `GET /controls/{control_id}` - Get specific control details
- `POST /controls/{control_id}/implement` - Generate implementation guide

### Documents
- `POST /upload?clear_existing=false` - Upload PDFs
- `GET /documents?limit=10&offset=0` - Browse vector database

### RAG
- `POST /query` - Ask questions about standards

---

## 🔮 Adding More Standards (ISO 19011, ISO 9001, etc.)

See detailed guide: `backend/ADDING_NEW_STANDARDS.md`

**Quick steps:**
1. Create `backend/standards/iso_19011_controls.py`
2. Upload ISO 19011 PDF via frontend
3. Update `backend/utils/standards.py` (2 line changes)
4. Restart backend

---

## 🎯 Next Steps

### Immediate:
1. ✅ **Test Upload Interface** - Upload ISO 31000 PDF
2. ✅ **Test ISO 31000 Controls** - Generate implementation guide for control 6.4.1
3. ✅ **Test Multi-Standard Queries** - Ask questions about both ISO 27001 and ISO 31000

### Future Enhancements:
- [ ] Add standard selector dropdown in frontend
- [ ] Company profile management (save company info)
- [ ] Progress tracking (mark controls as completed)
- [ ] Export implementation guides as PDF
- [ ] Add ISO 19011 and ISO 9001 standards
- [ ] Multi-language support

---

## 🐛 Troubleshooting

### Upload not working?
- Check backend is running on port 8000
- Verify CORS is enabled (already configured)
- Check browser console for errors

### ISO 31000 controls not showing?
- Ensure you've uploaded the PDF first
- Check `/documents` endpoint to verify upload
- Restart backend after adding new standards

### Frontend issues?
- Clear browser cache
- Check `npm run dev` output for errors
- Verify API_URL in Dashboard.jsx (`http://localhost:8000`)

---

## 📚 Documentation

- **Adding Standards**: `backend/ADDING_NEW_STANDARDS.md`
- **Backend README**: `backend/README.md`
- **Main README**: `README.md`

---

## 💡 Pro Tips

1. **Upload all PDFs at once**: Select multiple files in the upload dialog
2. **Use the agentic RAG**: It automatically researches best practices via Tavily
3. **Check high-priority controls first**: Focus on controls that give the most compliance value
4. **Copy-paste ready**: Implementation guides include actual policy text with placeholders
5. **Cross-standard queries**: Ask about relationships between ISO 27001 and ISO 31000

---

Need help? Check the documentation or review `backend/ADDING_NEW_STANDARDS.md` for detailed examples! 🚀

