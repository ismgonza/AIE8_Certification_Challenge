# Security Maturity Assistant - Frontend

React + Vite + Tailwind frontend for the Security Maturity Assistant.

## Setup

```bash
npm install
```

## Development

```bash
npm run dev
```

The app will run on `http://localhost:5173`

**Make sure the backend is running on `http://localhost:8000`**

## Features

### 📊 Security Assessment Mode
- 7-question company profile form
- AI-powered security scoring (0-10)
- Top 5 critical gaps with recommendations
- Personalized for your industry, size, and tech stack

### 🔧 Implementation Helper Mode
- Search any security topic
- Step-by-step guides with copy-paste commands
- Based on CIS, NIST, OWASP standards
- Real-time markdown rendering

### 🎨 UI/UX
- Clean, modern dark theme with Tailwind CSS
- Responsive design (mobile-friendly)
- Loading animations with security tips
- Copy-to-clipboard functionality

## Project Structure

```
src/
├── App.jsx                    # Landing page with mode selection
├── Assessment.jsx             # Security assessment flow
├── ImplementationHelper.jsx   # Search interface
├── StepByStepGuide.jsx        # Guide rendering with markdown
├── Dashboard.jsx              # (Legacy - not currently used)
├── main.jsx                   # App entry point
└── index.css                  # Tailwind styles
```

## Key Components

### App.jsx
Main landing page with two mode options:
- 📊 Assess My Security
- 🔧 Get Help With Something

### Assessment.jsx
Complete assessment workflow:
1. Form with 7 questions
2. Loading screen with security tips
3. Results display with score and gaps

### ImplementationHelper.jsx
Search interface with:
- Large search bar
- Example searches
- Popular topics

### StepByStepGuide.jsx
Renders implementation guides with:
- Markdown formatting
- Code syntax highlighting
- Copy buttons
- Source attribution

## API Integration

Backend endpoints used:
- `POST /assess` - Security assessment
- `POST /query` - Implementation questions

See main [README.md](../README.md) for backend setup.
