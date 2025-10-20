import { useState, useEffect } from 'react'
import ReactMarkdown from 'react-markdown'

const API_URL = 'http://localhost:8000'

function Dashboard() {
  const [standards, setStandards] = useState([])
  const [selectedStandard, setSelectedStandard] = useState('ISO_27001')
  const [controls, setControls] = useState([])
  const [stats, setStats] = useState({ total: 0, completed: 0, in_progress: 0, pending: 0 })
  const [loading, setLoading] = useState(true)
  const [selectedControl, setSelectedControl] = useState(null)
  const [implementationGuide, setImplementationGuide] = useState(null)
  const [generatingGuide, setGeneratingGuide] = useState(false)
  const [showUpload, setShowUpload] = useState(false)
  const [uploadFiles, setUploadFiles] = useState([])
  const [uploading, setUploading] = useState(false)
  const [clearExisting, setClearExisting] = useState(false)
  const [showCompanyProfile, setShowCompanyProfile] = useState(false)
  const [companyProfile, setCompanyProfile] = useState({
    name: '',
    industry: '',
    size: '',
    tech_stack: '',
    current_tools: '',
    budget: '',
    timeline: '',
    main_challenges: ''
  })
  const [aiRecommendations, setAiRecommendations] = useState(null)
  const [loadingRecommendations, setLoadingRecommendations] = useState(false)
  const [showRecommendations, setShowRecommendations] = useState(false)
  const [filterRecommended, setFilterRecommended] = useState(false)

  useEffect(() => {
    fetchStandards()
  }, [])

  useEffect(() => {
    if (selectedStandard) {
      fetchControls(selectedStandard)
    }
  }, [selectedStandard])

  const fetchStandards = async () => {
    try {
      const response = await fetch(`${API_URL}/standards`)
      const data = await response.json()
      setStandards(data.standards)
    } catch (error) {
      console.error('Error fetching standards:', error)
    }
  }

  const fetchControls = async (standardId) => {
    setLoading(true)
    try {
      const response = await fetch(`${API_URL}/controls?standard=${standardId}`)
      const data = await response.json()
      setControls(data.controls)
      setStats({
        total: data.total,
        completed: data.completed,
        in_progress: data.in_progress,
        pending: data.pending
      })
    } catch (error) {
      console.error('Error fetching controls:', error)
    } finally {
      setLoading(false)
    }
  }

  const handleFileChange = (e) => {
    setUploadFiles(Array.from(e.target.files))
  }

  const handleUpload = async () => {
    if (uploadFiles.length === 0) {
      alert('Please select at least one PDF file')
      return
    }

    setUploading(true)
    const formData = new FormData()
    uploadFiles.forEach(file => {
      formData.append('files', file)
    })

    try {
      const response = await fetch(`${API_URL}/upload?clear_existing=${clearExisting}`, {
        method: 'POST',
        body: formData
      })
      const data = await response.json()
      
      if (response.ok) {
        alert(`✅ Success! Uploaded ${data.files_processed} files with ${data.chunks_count} chunks`)
        setUploadFiles([])
        setShowUpload(false)
        // Reset file input
        document.getElementById('file-input').value = ''
      } else {
        alert(`❌ Upload failed: ${data.detail}`)
      }
    } catch (error) {
      console.error('Error uploading files:', error)
      alert('❌ Upload failed. Check console for details.')
    } finally {
      setUploading(false)
    }
  }

  const generateImplementationGuide = async (controlId) => {
    // Check if company profile is filled
    if (!companyProfile.name || !companyProfile.industry || !companyProfile.size) {
      alert('⚠️ Please set up your Company Profile first! Click the "🏢 Company Profile" button.')
      setShowCompanyProfile(true)
      return
    }

    setGeneratingGuide(true)
    setImplementationGuide(null)
    
    try {
      const response = await fetch(`${API_URL}/controls/${controlId}/implement`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          company_name: companyProfile.name,
          company_size: companyProfile.size,
          industry: companyProfile.industry,
          tech_stack: companyProfile.tech_stack.split(',').map(t => t.trim()).filter(Boolean),
          current_tools: companyProfile.current_tools,
          budget: companyProfile.budget,
          deadline_months: parseInt(companyProfile.timeline) || 6,
          main_challenges: companyProfile.main_challenges
        })
      })
      const data = await response.json()
      setImplementationGuide(data)
    } catch (error) {
      console.error('Error generating guide:', error)
      alert('❌ Failed to generate guide. Check console for details.')
    } finally {
      setGeneratingGuide(false)
    }
  }

  const downloadMarkdown = () => {
    if (!implementationGuide) return
    const content = implementationGuide.implementation_guide || implementationGuide.answer || ''
    const blob = new Blob([content], { type: 'text/markdown' })
    const url = URL.createObjectURL(blob)
    const a = document.createElement('a')
    a.href = url
    a.download = `${selectedControl.id}_implementation_guide.md`
    a.click()
    URL.revokeObjectURL(url)
  }

  const copyToClipboard = () => {
    if (!implementationGuide) return
    const content = implementationGuide.implementation_guide || implementationGuide.answer || ''
    navigator.clipboard.writeText(content)
    alert('✅ Copied to clipboard!')
  }

  const getAiRecommendations = async () => {
    if (!companyProfile.name || !companyProfile.industry || !companyProfile.size) {
      alert('⚠️ Please fill in at least: Company Name, Industry, and Company Size')
      return
    }

    setLoadingRecommendations(true)
    try {
      const response = await fetch(`${API_URL}/controls/recommend`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          company_name: companyProfile.name,
          company_size: companyProfile.size,
          industry: companyProfile.industry,
          tech_stack: companyProfile.tech_stack.split(',').map(t => t.trim()).filter(Boolean),
          current_tools: companyProfile.current_tools,
          budget: companyProfile.budget,
          deadline_months: parseInt(companyProfile.timeline) || 6,
          main_challenges: companyProfile.main_challenges
        })
      })
      const data = await response.json()
      setAiRecommendations(data)
      setShowRecommendations(true)
      setShowCompanyProfile(false)
    } catch (error) {
      console.error('Error getting recommendations:', error)
      alert('❌ Failed to get recommendations. Check console for details.')
    } finally {
      setLoadingRecommendations(false)
    }
  }

  // Filter controls based on AI recommendations
  const getDisplayControls = () => {
    if (filterRecommended && aiRecommendations?.control_ids) {
      return controls.filter(c => aiRecommendations.control_ids.includes(c.id))
    }
    return controls
  }
  
  const displayControls = getDisplayControls()
  const highPriorityControls = displayControls.filter(c => c.priority === 'high')
  const progress = stats.total > 0 ? Math.round((stats.completed / stats.total) * 100) : 0

  const getPriorityColor = (priority) => {
    switch(priority) {
      case 'high': return 'text-red-400 bg-red-900/30'
      case 'medium': return 'text-yellow-400 bg-yellow-900/30'
      case 'low': return 'text-green-400 bg-green-900/30'
      default: return 'text-gray-400 bg-gray-900/30'
    }
  }

  if (loading) {
    return (
      <div className="min-h-screen bg-gradient-to-br from-gray-900 via-gray-800 to-gray-900 flex items-center justify-center">
        <div className="text-white">Loading...</div>
      </div>
    )
  }

  return (
    <div className="min-h-screen bg-gradient-to-br from-gray-900 via-gray-800 to-gray-900">
      {/* Header */}
      <header className="bg-gray-800/50 backdrop-blur-sm border-b border-gray-700">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-6">
          <div className="flex items-center justify-between">
            <div className="flex items-center space-x-3">
              <div className="w-10 h-10 bg-gradient-to-br from-blue-500 to-purple-600 rounded-lg flex items-center justify-center">
                <svg className="w-6 h-6 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 12l2 2 4-4m5.618-4.016A11.955 11.955 0 0112 2.944a11.955 11.955 0 01-8.618 3.04A12.02 12.02 0 003 9c0 5.591 3.824 10.29 9 11.622 5.176-1.332 9-6.03 9-11.622 0-1.042-.133-2.052-.382-3.016z" />
                </svg>
              </div>
              <div>
                <h1 className="text-2xl font-bold text-white">ISO Implementation Dashboard</h1>
                <p className="text-sm text-gray-400">Your path to certification</p>
              </div>
            </div>

            {/* Standard Selector */}
            <div className="flex items-center gap-3">
              <label className="text-sm font-medium text-gray-300">Standard:</label>
              <select
                value={selectedStandard}
                onChange={(e) => setSelectedStandard(e.target.value)}
                className="px-4 py-2 bg-gray-700 text-white border border-gray-600 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
              >
                {standards.map(std => (
                  <option 
                    key={std.id} 
                    value={std.id}
                    disabled={!std.is_available}
                  >
                    {std.icon} {std.name} {!std.is_available ? '(Coming Soon)' : ''}
                  </option>
                ))}
              </select>
            </div>
            
            {/* Action Buttons & Progress */}
            <div className="flex items-center gap-4">
              <button
                onClick={() => setShowCompanyProfile(!showCompanyProfile)}
                className={`px-4 py-2 ${companyProfile.name ? 'bg-green-600 hover:bg-green-700' : 'bg-purple-600 hover:bg-purple-700'} text-white rounded-lg transition flex items-center gap-2 text-sm font-medium`}
              >
                🏢 Company Profile {companyProfile.name && '✓'}
              </button>
              <button
                onClick={() => setShowUpload(!showUpload)}
                className="px-4 py-2 bg-blue-600 hover:bg-blue-700 text-white rounded-lg transition flex items-center gap-2 text-sm font-medium"
              >
                📤 Upload Documents
              </button>
              <div className="text-right">
                <div className="text-3xl font-bold text-white">{progress}%</div>
                <div className="text-sm text-gray-400">{stats.completed}/{stats.total} controls</div>
              </div>
            </div>
          </div>

          {/* Company Profile Section */}
          {showCompanyProfile && (
            <div className="mt-6 bg-gradient-to-br from-purple-900/30 to-blue-900/30 rounded-lg p-6 border border-purple-500/50">
              <div className="flex justify-between items-start mb-4">
                <div>
                  <h3 className="text-lg font-semibold text-white mb-1">🏢 Company Profile</h3>
                  <p className="text-sm text-gray-300">This information will be used to customize implementation guides specifically for your organization</p>
                </div>
                <button
                  onClick={() => setShowCompanyProfile(false)}
                  className="text-gray-400 hover:text-white"
                >
                  ✕
                </button>
              </div>
              
              <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                <div>
                  <label className="block text-sm font-medium text-gray-300 mb-1">Company Name *</label>
                  <input
                    type="text"
                    value={companyProfile.name}
                    onChange={(e) => setCompanyProfile({...companyProfile, name: e.target.value})}
                    placeholder="Acme Corp"
                    className="w-full px-3 py-2 bg-gray-700 text-white border border-gray-600 rounded-lg focus:ring-2 focus:ring-purple-500"
                  />
                </div>
                <div>
                  <label className="block text-sm font-medium text-gray-300 mb-1">Industry *</label>
                  <input
                    type="text"
                    value={companyProfile.industry}
                    onChange={(e) => setCompanyProfile({...companyProfile, industry: e.target.value})}
                    placeholder="Software/SaaS, Healthcare, Finance, etc."
                    className="w-full px-3 py-2 bg-gray-700 text-white border border-gray-600 rounded-lg focus:ring-2 focus:ring-purple-500"
                  />
                </div>
                <div>
                  <label className="block text-sm font-medium text-gray-300 mb-1">Company Size *</label>
                  <select
                    value={companyProfile.size}
                    onChange={(e) => setCompanyProfile({...companyProfile, size: e.target.value})}
                    className="w-full px-3 py-2 bg-gray-700 text-white border border-gray-600 rounded-lg focus:ring-2 focus:ring-purple-500"
                  >
                    <option value="">Select size</option>
                    <option value="1-10">1-10 employees</option>
                    <option value="11-50">11-50 employees</option>
                    <option value="51-200">51-200 employees</option>
                    <option value="201-500">201-500 employees</option>
                    <option value="500+">500+ employees</option>
                  </select>
                </div>
                <div>
                  <label className="block text-sm font-medium text-gray-300 mb-1">Tech Stack</label>
                  <input
                    type="text"
                    value={companyProfile.tech_stack}
                    onChange={(e) => setCompanyProfile({...companyProfile, tech_stack: e.target.value})}
                    placeholder="AWS, Microsoft 365, Salesforce (comma separated)"
                    className="w-full px-3 py-2 bg-gray-700 text-white border border-gray-600 rounded-lg focus:ring-2 focus:ring-purple-500"
                  />
                </div>
                <div>
                  <label className="block text-sm font-medium text-gray-300 mb-1">Current Security Tools</label>
                  <input
                    type="text"
                    value={companyProfile.current_tools}
                    onChange={(e) => setCompanyProfile({...companyProfile, current_tools: e.target.value})}
                    placeholder="What security tools do you already have?"
                    className="w-full px-3 py-2 bg-gray-700 text-white border border-gray-600 rounded-lg focus:ring-2 focus:ring-purple-500"
                  />
                </div>
                <div>
                  <label className="block text-sm font-medium text-gray-300 mb-1">Budget Range</label>
                  <select
                    value={companyProfile.budget}
                    onChange={(e) => setCompanyProfile({...companyProfile, budget: e.target.value})}
                    className="w-full px-3 py-2 bg-gray-700 text-white border border-gray-600 rounded-lg focus:ring-2 focus:ring-purple-500"
                  >
                    <option value="">Select budget</option>
                    <option value="< $5K">Less than $5,000</option>
                    <option value="$5K-$20K">$5,000 - $20,000</option>
                    <option value="$20K-$50K">$20,000 - $50,000</option>
                    <option value="$50K+">$50,000+</option>
                  </select>
                </div>
                <div>
                  <label className="block text-sm font-medium text-gray-300 mb-1">Timeline (months)</label>
                  <input
                    type="number"
                    value={companyProfile.timeline}
                    onChange={(e) => setCompanyProfile({...companyProfile, timeline: e.target.value})}
                    placeholder="6"
                    min="1"
                    max="24"
                    className="w-full px-3 py-2 bg-gray-700 text-white border border-gray-600 rounded-lg focus:ring-2 focus:ring-purple-500"
                  />
                </div>
                <div className="md:col-span-2">
                  <label className="block text-sm font-medium text-gray-300 mb-1">Main Challenges</label>
                  <textarea
                    value={companyProfile.main_challenges}
                    onChange={(e) => setCompanyProfile({...companyProfile, main_challenges: e.target.value})}
                    placeholder="What are your biggest security/compliance challenges?"
                    rows="3"
                    className="w-full px-3 py-2 bg-gray-700 text-white border border-gray-600 rounded-lg focus:ring-2 focus:ring-purple-500"
                  />
                </div>
              </div>

              <div className="mt-4 flex gap-3">
                <button
                  onClick={() => {
                    if (companyProfile.name && companyProfile.industry && companyProfile.size) {
                      setShowCompanyProfile(false)
                      alert('✅ Company profile saved! Now generate implementation guides or get AI recommendations.')
                    } else {
                      alert('⚠️ Please fill in at least: Company Name, Industry, and Company Size')
                    }
                  }}
                  className="px-6 py-2 bg-purple-600 hover:bg-purple-700 text-white rounded-lg transition font-medium"
                >
                  Save Profile
                </button>
                <button
                  onClick={getAiRecommendations}
                  disabled={loadingRecommendations}
                  className="px-6 py-2 bg-gradient-to-r from-blue-600 to-purple-600 hover:from-blue-700 hover:to-purple-700 disabled:from-gray-600 disabled:to-gray-600 text-white rounded-lg transition font-medium flex items-center gap-2"
                >
                  {loadingRecommendations ? '🤖 Analyzing...' : '🎯 Get AI Recommendations'}
                </button>
                <button
                  onClick={() => setShowCompanyProfile(false)}
                  className="px-6 py-2 bg-gray-600 hover:bg-gray-700 text-white rounded-lg transition"
                >
                  Cancel
                </button>
              </div>
            </div>
          )}

          {/* Upload Section */}
          {showUpload && (
            <div className="mt-6 bg-gray-700/50 rounded-lg p-6 border border-gray-600">
              <h3 className="text-lg font-semibold text-white mb-4">Upload ISO Standard PDFs</h3>
              
              <div className="space-y-4">
                <div>
                  <label className="block text-sm font-medium text-gray-300 mb-2">
                    Select PDF files (ISO 27001, ISO 31000, etc.)
                  </label>
                  <input
                    id="file-input"
                    type="file"
                    accept=".pdf"
                    multiple
                    onChange={handleFileChange}
                    className="block w-full text-sm text-gray-300
                      file:mr-4 file:py-2 file:px-4
                      file:rounded-lg file:border-0
                      file:text-sm file:font-semibold
                      file:bg-blue-600 file:text-white
                      hover:file:bg-blue-700
                      file:cursor-pointer cursor-pointer"
                  />
                  {uploadFiles.length > 0 && (
                    <p className="mt-2 text-sm text-gray-400">
                      Selected: {uploadFiles.map(f => f.name).join(', ')}
                    </p>
                  )}
                </div>

                <div className="flex items-center gap-2">
                  <input
                    type="checkbox"
                    id="clear-existing"
                    checked={clearExisting}
                    onChange={(e) => setClearExisting(e.target.checked)}
                    className="w-4 h-4 text-blue-600 bg-gray-700 border-gray-600 rounded focus:ring-blue-500"
                  />
                  <label htmlFor="clear-existing" className="text-sm text-gray-300">
                    Clear existing documents before uploading (⚠️ This will delete all current data)
                  </label>
                </div>

                <div className="flex gap-3">
                  <button
                    onClick={handleUpload}
                    disabled={uploading || uploadFiles.length === 0}
                    className="px-6 py-2 bg-green-600 hover:bg-green-700 disabled:bg-gray-600 disabled:cursor-not-allowed text-white rounded-lg transition font-medium"
                  >
                    {uploading ? 'Uploading...' : 'Upload & Process'}
                  </button>
                  <button
                    onClick={() => {
                      setShowUpload(false)
                      setUploadFiles([])
                      if (document.getElementById('file-input')) {
                        document.getElementById('file-input').value = ''
                      }
                    }}
                    className="px-6 py-2 bg-gray-600 hover:bg-gray-700 text-white rounded-lg transition"
                  >
                    Cancel
                  </button>
                </div>
              </div>
            </div>
          )}
          
          {/* Progress Bar */}
          <div className="mt-4 w-full bg-gray-700 rounded-full h-2">
            <div 
              className="bg-gradient-to-r from-blue-500 to-purple-600 h-2 rounded-full transition-all duration-500"
              style={{ width: `${progress}%` }}
            ></div>
          </div>

          {/* Current Standard Info */}
          {standards.length > 0 && selectedStandard && (
            <div className="mt-4 p-3 bg-gray-700/30 rounded-lg border border-gray-600/50">
              {(() => {
                const std = standards.find(s => s.id === selectedStandard)
                return std ? (
                  <div className="flex items-start gap-3">
                    <span className="text-2xl">{std.icon}</span>
                    <div>
                      <h3 className="text-sm font-semibold text-white">{std.title}</h3>
                      <p className="text-xs text-gray-400 mt-1">{std.description}</p>
                    </div>
                  </div>
                ) : null
              })()}
            </div>
          )}
        </div>
      </header>

      {/* Main Content */}
      <main className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        {/* AI Recommendations Section */}
        {showRecommendations && aiRecommendations && (
          <div className="mb-8 bg-gradient-to-br from-blue-900/30 to-purple-900/30 border-2 border-purple-500/50 rounded-lg p-6">
            <div className="flex justify-between items-start mb-4">
              <div>
                <h2 className="text-2xl font-bold text-white mb-2">🎯 AI-Recommended Controls for {aiRecommendations.company_context?.name}</h2>
                <p className="text-gray-300">Based on your industry ({aiRecommendations.company_context?.industry}) and challenges</p>
              </div>
              <button
                onClick={() => setShowRecommendations(false)}
                className="text-gray-400 hover:text-white text-xl"
              >
                ✕
              </button>
            </div>
            
            <div className="bg-gray-800/50 rounded-lg p-6 markdown-content">
              <ReactMarkdown
                components={{
                  h1: ({node, ...props}) => <h1 className="text-2xl font-bold text-white mt-6 mb-3" {...props} />,
                  h2: ({node, ...props}) => <h2 className="text-xl font-semibold text-white mt-5 mb-2" {...props} />,
                  h3: ({node, ...props}) => <h3 className="text-lg font-medium text-white mt-4 mb-2" {...props} />,
                  p: ({node, ...props}) => <p className="text-gray-300 mb-4 leading-relaxed" {...props} />,
                  ul: ({node, ...props}) => <ul className="list-disc ml-6 mb-4 space-y-2 text-gray-300" {...props} />,
                  strong: ({node, ...props}) => <strong className="font-bold text-white" {...props} />,
                }}
              >
                {aiRecommendations.recommendations}
              </ReactMarkdown>
            </div>

            <div className="mt-4 flex gap-3 flex-wrap">
              <button
                onClick={() => {
                  setFilterRecommended(true)
                  setShowRecommendations(false)
                  // Scroll to controls
                  setTimeout(() => {
                    window.scrollTo({ top: document.querySelector('.control-card')?.offsetTop - 100, behavior: 'smooth' })
                  }, 100)
                }}
                className="px-5 py-2.5 bg-gradient-to-r from-purple-600 to-blue-600 hover:from-purple-700 hover:to-blue-700 text-white rounded-lg transition font-semibold flex items-center gap-2"
              >
                🎯 Work on These {aiRecommendations.control_ids?.length || 5} Controls
              </button>
              <button
                onClick={() => {
                  setShowRecommendations(false)
                  // Scroll to controls
                  window.scrollTo({ top: document.querySelector('.control-card')?.offsetTop - 100, behavior: 'smooth' })
                }}
                className="px-4 py-2 bg-gray-700 hover:bg-gray-600 text-white rounded-lg transition"
              >
                👁️ View All Controls
              </button>
              <button
                onClick={() => {
                  const content = aiRecommendations.recommendations
                  navigator.clipboard.writeText(content)
                  alert('✅ Recommendations copied to clipboard!')
                }}
                className="px-4 py-2 bg-gray-700 hover:bg-gray-600 text-white rounded-lg transition"
              >
                📋 Copy
              </button>
            </div>
          </div>
        )}

        {!selectedControl ? (
          <>
            {/* Filter Badge */}
            {filterRecommended && (
              <div className="mb-6 bg-gradient-to-r from-purple-900/50 to-blue-900/50 border border-purple-500/50 rounded-lg p-4 flex justify-between items-center">
                <div>
                  <h3 className="text-lg font-semibold text-white mb-1">🎯 Showing AI-Recommended Controls</h3>
                  <p className="text-sm text-gray-300">Personalized for {aiRecommendations?.company_context?.name || 'your company'}</p>
                </div>
                <button
                  onClick={() => setFilterRecommended(false)}
                  className="px-4 py-2 bg-gray-700 hover:bg-gray-600 text-white rounded-lg transition text-sm"
                >
                  Show All Controls
                </button>
              </div>
            )}

            {/* High Priority Section */}
            <div className="mb-8 control-card">
              <h2 className="text-2xl font-bold text-white mb-4">
                {filterRecommended ? '🎯 Your Priority Controls' : '🔴 Start Here (High Priority)'}
              </h2>
              <p className="text-gray-400 mb-6">
                {filterRecommended 
                  ? `AI-recommended controls based on ${aiRecommendations?.company_context?.industry} industry and your challenges`
                  : 'These controls are critical and should be implemented first'}
              </p>
              
              <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
                {highPriorityControls.map(control => (
                  <div 
                    key={control.id}
                    onClick={() => setSelectedControl(control)}
                    className="bg-gray-800/50 border border-gray-700 rounded-lg p-5 hover:border-blue-500 cursor-pointer transition-all"
                  >
                    <div className="flex items-start justify-between mb-3">
                      <div className="flex items-center space-x-2">
                        <span className="text-blue-400 font-bold">{control.id}</span>
                        <span className={`text-xs px-2 py-0.5 rounded ${getPriorityColor(control.priority)}`}>
                          {control.priority}
                        </span>
                      </div>
                      <div className="w-6 h-6 rounded-full border-2 border-gray-600"></div>
                    </div>
                    <h3 className="text-white font-semibold mb-2">{control.title}</h3>
                    <p className="text-gray-400 text-sm mb-3">{control.description}</p>
                    <div className="flex items-center justify-between text-xs text-gray-500">
                      <span>⏱️ {control.estimated_hours}h</span>
                      <span>👤 {control.owner}</span>
                    </div>
                  </div>
                ))}
              </div>
            </div>

            {/* All Controls by Theme */}
            {!filterRecommended && (
              <div>
                <h2 className="text-2xl font-bold text-white mb-4">📋 All Controls ({stats.total})</h2>
                <div className="space-y-2">
                  {displayControls.map(control => (
                  <div 
                    key={control.id}
                    onClick={() => setSelectedControl(control)}
                    className="bg-gray-800/30 border border-gray-700/50 rounded-lg p-4 hover:bg-gray-800/50 hover:border-gray-600 cursor-pointer transition-all flex items-center justify-between"
                  >
                    <div className="flex items-center space-x-4">
                      <div className="w-8 h-8 rounded-full border-2 border-gray-600"></div>
                      <div>
                        <div className="flex items-center space-x-2">
                          <span className="text-blue-400 font-mono">{control.id}</span>
                          <span className="text-white font-medium">{control.title}</span>
                          <span className={`text-xs px-2 py-0.5 rounded ${getPriorityColor(control.priority)}`}>
                            {control.priority}
                          </span>
                        </div>
                        <p className="text-gray-500 text-sm mt-1">{control.theme}</p>
                      </div>
                    </div>
                    <div className="text-gray-500 text-sm">
                      ⏱️ {control.estimated_hours}h
                    </div>
                  </div>
                  ))}
                </div>
              </div>
            )}
          </>
        ) : (
          /* Control Detail View */
          <ControlDetail 
            control={selectedControl}
            onBack={() => {
              setSelectedControl(null)
              setImplementationGuide(null)
            }}
            implementationGuide={implementationGuide}
            generatingGuide={generatingGuide}
            onGenerateGuide={generateImplementationGuide}
            companyProfile={companyProfile}
            onCopy={copyToClipboard}
            onDownload={downloadMarkdown}
          />
        )}
      </main>
    </div>
  )
}

// Control Detail Component
function ControlDetail({ control, onBack, implementationGuide, generatingGuide, onGenerateGuide, companyProfile, onCopy, onDownload }) {
  return (
    <div>
      <button 
        onClick={onBack}
        className="text-gray-400 hover:text-white mb-6 flex items-center space-x-2"
      >
        <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M15 19l-7-7 7-7" />
        </svg>
        <span>Back to Dashboard</span>
      </button>

      <div className="bg-gray-800/50 border border-gray-700 rounded-lg p-8 mb-6">
        <div className="flex items-start justify-between mb-4">
          <div>
            <div className="flex items-center space-x-3 mb-2">
              <span className="text-3xl font-bold text-blue-400">{control.id}</span>
              <h1 className="text-3xl font-bold text-white">{control.title}</h1>
            </div>
            <p className="text-gray-400">{control.description}</p>
          </div>
        </div>

        <div className="grid grid-cols-3 gap-4 mt-6">
          <div className="bg-gray-700/30 rounded-lg p-4">
            <div className="text-gray-400 text-sm mb-1">Estimated Time</div>
            <div className="text-white text-xl font-bold">⏱️ {control.estimated_hours} hours</div>
          </div>
          <div className="bg-gray-700/30 rounded-lg p-4">
            <div className="text-gray-400 text-sm mb-1">Owner</div>
            <div className="text-white text-xl font-bold">👤 {control.owner}</div>
          </div>
          <div className="bg-gray-700/30 rounded-lg p-4">
            <div className="text-gray-400 text-sm mb-1">Priority</div>
            <div className="text-white text-xl font-bold">🎯 {control.priority.toUpperCase()}</div>
          </div>
        </div>

        <div className="mt-6">
          <h3 className="text-white font-semibold mb-3">📄 Deliverables You'll Create:</h3>
          <ul className="space-y-2">
            {control.deliverables.map((deliverable, idx) => (
              <li key={idx} className="text-gray-300 flex items-center space-x-2">
                <span className="text-green-400">✓</span>
                <span>{deliverable}</span>
              </li>
            ))}
          </ul>
        </div>

        <button
          onClick={() => onGenerateGuide(control.id)}
          disabled={generatingGuide}
          className="mt-6 w-full bg-gradient-to-r from-blue-500 to-purple-600 text-white px-6 py-3 rounded-lg hover:from-blue-600 hover:to-purple-700 disabled:from-gray-600 disabled:to-gray-600 font-semibold transition-all"
        >
          {generatingGuide ? '🔍 Generating Implementation Guide...' : '🚀 Generate Implementation Guide'}
        </button>
      </div>

      {/* Implementation Guide */}
      {generatingGuide && (
        <div className="bg-gray-800/50 border border-gray-700 rounded-lg p-12">
          <div className="flex flex-col items-center justify-center space-y-4">
            <div className="w-16 h-16 border-4 border-gray-600 border-t-blue-500 rounded-full animate-spin"></div>
            <p className="text-gray-400 text-sm">Analyzing ISO requirements and researching best practices...</p>
          </div>
        </div>
      )}

      {implementationGuide && !generatingGuide && (
        <div className="bg-gray-800/50 border border-gray-700 rounded-lg p-8">
          <div className="flex justify-between items-start mb-6">
            <h2 className="text-2xl font-bold text-white">📋 Implementation Guide</h2>
            <div className="flex gap-2">
              <button
                onClick={onCopy}
                className="px-3 py-1.5 bg-gray-700 hover:bg-gray-600 text-white rounded text-sm flex items-center gap-1.5 font-medium"
                title="Copy to clipboard"
              >
                📋 Copy
              </button>
              <button
                onClick={onDownload}
                className="px-3 py-1.5 bg-blue-600 hover:bg-blue-700 text-white rounded text-sm flex items-center gap-1.5 font-medium"
                title="Download as Markdown"
              >
                ⬇️ Download
              </button>
            </div>
          </div>

          {/* Company Context Badge */}
          {companyProfile.name && (
            <div className="mb-6 p-4 bg-gradient-to-r from-purple-900/40 to-blue-900/40 border border-purple-500/40 rounded-lg">
              <div className="text-sm">
                <span className="font-semibold text-purple-300">✨ Customized for your organization:</span>
                <div className="mt-2 grid grid-cols-2 gap-x-4 gap-y-1 text-purple-200">
                  <div><span className="text-purple-400">Company:</span> {companyProfile.name}</div>
                  <div><span className="text-purple-400">Industry:</span> {companyProfile.industry}</div>
                  <div><span className="text-purple-400">Size:</span> {companyProfile.size} employees</div>
                  {companyProfile.tech_stack && <div><span className="text-purple-400">Tech:</span> {companyProfile.tech_stack}</div>}
                  {companyProfile.budget && <div><span className="text-purple-400">Budget:</span> {companyProfile.budget}</div>}
                  {companyProfile.timeline && <div><span className="text-purple-400">Timeline:</span> {companyProfile.timeline} months</div>}
                </div>
              </div>
            </div>
          )}

          <div className="markdown-content">
            <ReactMarkdown
              components={{
                h1: ({node, ...props}) => <h1 className="text-2xl font-bold text-white mt-6 mb-3" {...props} />,
                h2: ({node, ...props}) => <h2 className="text-xl font-semibold text-white mt-5 mb-2" {...props} />,
                h3: ({node, ...props}) => <h3 className="text-lg font-medium text-white mt-4 mb-2" {...props} />,
                p: ({node, ...props}) => <p className="text-gray-300 mb-4 leading-relaxed" {...props} />,
                ul: ({node, ...props}) => <ul className="list-disc ml-6 mb-4 space-y-2 text-gray-300" {...props} />,
                ol: ({node, ...props}) => <ol className="list-decimal ml-6 mb-4 space-y-3 text-gray-300" {...props} />,
                li: ({node, ...props}) => <li className="text-gray-300 pl-2" {...props} />,
                strong: ({node, ...props}) => <strong className="font-bold text-white" {...props} />,
                em: ({node, ...props}) => <em className="italic text-gray-300" {...props} />,
                code: ({node, inline, ...props}) => 
                  inline 
                    ? <code className="bg-gray-700 px-2 py-0.5 rounded text-blue-400 text-sm" {...props} />
                    : <code className="block bg-gray-700 p-4 rounded my-3 text-blue-400 overflow-x-auto whitespace-pre-wrap" {...props} />,
                blockquote: ({node, ...props}) => <blockquote className="border-l-4 border-blue-500 pl-4 italic text-gray-400 my-4" {...props} />,
                table: ({node, ...props}) => <table className="w-full border-collapse my-4" {...props} />,
                th: ({node, ...props}) => <th className="border border-gray-600 bg-gray-700 px-4 py-2 text-left text-white" {...props} />,
                td: ({node, ...props}) => <td className="border border-gray-600 px-4 py-2 text-gray-300" {...props} />,
              }}
            >
              {implementationGuide.implementation_guide}
            </ReactMarkdown>
          </div>
        </div>
      )}
    </div>
  )
}

export default Dashboard

