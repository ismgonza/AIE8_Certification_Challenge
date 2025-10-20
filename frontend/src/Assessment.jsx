import { useState, useEffect } from 'react'
import ReactMarkdown from 'react-markdown'

const API_URL = 'http://localhost:8000'

// Security tips to show during loading
const SECURITY_TIPS = [
  "💡 60% of small businesses close within 6 months of a cyber attack",
  "🔒 Multi-Factor Authentication blocks 99.9% of automated attacks",
  "⚠️ 95% of breaches are caused by human error",
  "📊 Average cost of a data breach: $4.45 million",
  "🎯 81% of breaches involve weak or stolen passwords",
  "🚨 Ransomware attacks occur every 11 seconds",
  "💰 Small businesses lose an average of $200,000 per breach",
  "🔑 Password managers reduce breach risk by 70%",
  "⏰ It takes 280 days on average to identify a breach",
  "🛡️ Regular backups can save your business from ransomware",
  "📱 Mobile devices are involved in 40% of security incidents",
  "🌐 Phishing is responsible for 90% of data breaches",
  "✅ Companies with incident response plans save $2M on average",
  "🔄 Unpatched software causes 60% of breaches",
  "👥 Insider threats account for 34% of all breaches"
]

function LoadingScreen() {
  const [currentTip, setCurrentTip] = useState(0)

  useEffect(() => {
    const interval = setInterval(() => {
      setCurrentTip((prev) => (prev + 1) % SECURITY_TIPS.length)
    }, 3000) // Change tip every 3 seconds

    return () => clearInterval(interval)
  }, [])

  return (
    <div className="fixed inset-0 bg-gradient-to-br from-gray-900 via-gray-800 to-gray-900 flex items-center justify-center z-50">
      <div className="text-center">
        {/* Animated spinner */}
        <div className="relative w-32 h-32 mx-auto mb-8">
          <div className="absolute inset-0 border-8 border-gray-700 rounded-full"></div>
          <div className="absolute inset-0 border-8 border-blue-500 rounded-full border-t-transparent animate-spin"></div>
          <div className="absolute inset-4 border-8 border-purple-500 rounded-full border-t-transparent animate-spin" style={{animationDuration: '1.5s', animationDirection: 'reverse'}}></div>
          <div className="absolute inset-0 flex items-center justify-center">
            <svg className="w-12 h-12 text-blue-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 12l2 2 4-4m5.618-4.016A11.955 11.955 0 0112 2.944a11.955 11.955 0 01-8.618 3.04A12.02 12.02 0 003 9c0 5.591 3.824 10.29 9 11.622 5.176-1.332 9-6.03 9-11.622 0-1.042-.133-2.052-.382-3.016z" />
            </svg>
          </div>
        </div>

        <h2 className="text-2xl font-bold text-white mb-4">
          🔍 Analyzing Your Security Posture...
        </h2>
        <p className="text-gray-400 mb-8">
          Our AI is reviewing CIS Controls, NIST guidelines, and industry best practices
        </p>

        {/* Rotating security tips */}
        <div className="bg-gray-800/50 border border-gray-700 rounded-lg p-6 max-w-xl mx-auto min-h-[80px] flex items-center justify-center">
          <div className="transition-opacity duration-500">
            <p className="text-lg text-gray-300">
              {SECURITY_TIPS[currentTip]}
            </p>
          </div>
        </div>
      </div>
    </div>
  )
}

const SECURITY_MEASURES = [
  // Basic (Level 1-4)
  { id: 'antivirus', label: 'Antivirus/Anti-malware', category: 'basic' },
  { id: 'firewall', label: 'Firewall enabled', category: 'basic' },
  { id: 'mfa', label: 'Multi-Factor Authentication (MFA)', category: 'basic' },
  { id: 'backups', label: 'Regular backups', category: 'basic' },
  { id: 'password_policy', label: 'Password policy enforced', category: 'basic' },
  { id: 'encryption', label: 'Disk/data encryption', category: 'basic' },
  { id: 'updates', label: 'Regular security updates', category: 'basic' },
  
  // Intermediate (Level 4-6)
  { id: 'training', label: 'Security awareness training', category: 'intermediate' },
  { id: 'monitoring', label: 'Security monitoring/logging', category: 'intermediate' },
  { id: 'access_control', label: 'Access control/least privilege', category: 'intermediate' },
  { id: 'edr', label: 'EDR/Endpoint Detection & Response', category: 'intermediate' },
  { id: 'vulnerability_scanning', label: 'Vulnerability scanning', category: 'intermediate' },
  { id: 'incident_response', label: 'Incident response plan (documented)', category: 'intermediate' },
  { id: 'patch_management', label: 'Patch management process', category: 'intermediate' },
  { id: 'network_segmentation', label: 'Network segmentation', category: 'intermediate' },
  
  // Advanced (Level 6-8)
  { id: 'siem', label: 'SIEM (Security Information & Event Management)', category: 'advanced' },
  { id: 'tested_ir', label: 'Incident response plan (tested regularly)', category: 'advanced' },
  { id: 'security_reviews', label: 'Regular security reviews/audits', category: 'advanced' },
  { id: 'penetration_testing', label: 'Annual penetration testing', category: 'advanced' },
  { id: 'dlp', label: 'Data Loss Prevention (DLP)', category: 'advanced' },
  
  // Expert (Level 8-10)
  { id: 'dedicated_team', label: 'Dedicated security team/staff', category: 'expert' },
  { id: '24_7_monitoring', label: '24/7 security monitoring (SOC)', category: 'expert' },
  { id: 'threat_hunting', label: 'Active threat hunting capabilities', category: 'expert' },
  { id: 'red_team', label: 'Red team exercises/purple teaming', category: 'expert' },
  { id: 'zero_trust', label: 'Zero Trust architecture implementation', category: 'expert' }
]

const INDUSTRIES = [
  'Technology/Software',
  'Healthcare',
  'Finance/Banking',
  'Professional Services',
  'Manufacturing',
  'Retail/E-commerce',
  'Education',
  'Legal',
  'Real Estate',
  'Non-profit',
  'Government',
  'Other'
]

function Assessment({ onBack }) {
  const [step, setStep] = useState('form') // 'form', 'results'
  const [formData, setFormData] = useState({
    company_name: '',
    company_size: '',
    industry: '',
    tech_stack: '',
    security_measures: [],
    budget: '',
    main_concern: ''
  })
  const [results, setResults] = useState(null)
  const [loading, setLoading] = useState(false)

  const handleSubmit = async (e) => {
    e.preventDefault()
    setLoading(true)

    try {
      // Convert security measures to readable string
      const securityMeasuresText = formData.security_measures.length > 0
        ? formData.security_measures.map(id => 
            SECURITY_MEASURES.find(m => m.id === id)?.label
          ).join(', ')
        : 'None/Minimal'

      const response = await fetch(`${API_URL}/assess`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          ...formData,
          tech_stack: formData.tech_stack.split(',').map(t => t.trim()).filter(Boolean),
          security_measures: securityMeasuresText
        })
      })

      const data = await response.json()
      setResults(data)
      setStep('results')
    } catch (error) {
      console.error('Error:', error)
      alert('Failed to complete assessment. Check console for details.')
    } finally {
      setLoading(false)
    }
  }

  const handleChange = (e) => {
    setFormData({ ...formData, [e.target.name]: e.target.value })
  }

  const handleCheckboxChange = (measureId) => {
    setFormData(prev => ({
      ...prev,
      security_measures: prev.security_measures.includes(measureId)
        ? prev.security_measures.filter(id => id !== measureId)
        : [...prev.security_measures, measureId]
    }))
  }

  if (loading) {
    return <LoadingScreen />
  }

  if (step === 'form') {
    return (
      <div className="min-h-screen bg-gradient-to-br from-gray-900 via-gray-800 to-gray-900 p-6">
        <div className="max-w-3xl mx-auto">
          <button
            onClick={onBack}
            className="text-gray-400 hover:text-white mb-6 flex items-center gap-2"
          >
            ← Back to Home
          </button>

          <div className="bg-gray-800/50 border border-gray-700 rounded-lg p-8">
            <h2 className="text-3xl font-bold text-white mb-2">Tell us about your company</h2>
            <p className="text-gray-400 mb-8">We'll analyze your security based on this info</p>

            <form onSubmit={handleSubmit} className="space-y-6">
              <div>
                <label className="block text-sm font-medium text-gray-300 mb-2">
                  Company Name *
                </label>
                <input
                  type="text"
                  name="company_name"
                  value={formData.company_name}
                  onChange={handleChange}
                  required
                  className="w-full px-4 py-2 bg-gray-700 text-white border border-gray-600 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                  placeholder="Acme Corp"
                />
              </div>

              <div>
                <label className="block text-sm font-medium text-gray-300 mb-2">
                  Company Size *
                </label>
                <select
                  name="company_size"
                  value={formData.company_size}
                  onChange={handleChange}
                  required
                  className="w-full px-4 py-2 bg-gray-700 text-white border border-gray-600 rounded-lg focus:ring-2 focus:ring-blue-500"
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
                <label className="block text-sm font-medium text-gray-300 mb-2">
                  Industry *
                </label>
                <select
                  name="industry"
                  value={formData.industry}
                  onChange={handleChange}
                  required
                  className="w-full px-4 py-2 bg-gray-700 text-white border border-gray-600 rounded-lg focus:ring-2 focus:ring-blue-500"
                >
                  <option value="">Select industry</option>
                  {INDUSTRIES.map((industry) => (
                    <option key={industry} value={industry}>
                      {industry}
                    </option>
                  ))}
                </select>
              </div>

              <div>
                <label className="block text-sm font-medium text-gray-300 mb-2">
                  Tech Stack *
                </label>
                <input
                  type="text"
                  name="tech_stack"
                  value={formData.tech_stack}
                  onChange={handleChange}
                  required
                  className="w-full px-4 py-2 bg-gray-700 text-white border border-gray-600 rounded-lg focus:ring-2 focus:ring-blue-500"
                  placeholder="Windows, Microsoft 365, AWS (comma-separated)"
                />
              </div>

              <div>
                <label className="block text-sm font-medium text-gray-300 mb-3">
                  Current Security Measures
                </label>
                
                {/* Basic Measures */}
                <div className="mb-4">
                  <h4 className="text-xs font-semibold text-blue-400 uppercase tracking-wide mb-2">
                    🛡️ Basic Security
                  </h4>
                  <div className="grid grid-cols-1 md:grid-cols-2 gap-2">
                    {SECURITY_MEASURES.filter(m => m.category === 'basic').map((measure) => (
                      <label
                        key={measure.id}
                        className="flex items-center gap-3 px-4 py-2 bg-gray-700/50 hover:bg-gray-700 border border-gray-600 rounded-lg cursor-pointer transition"
                      >
                        <input
                          type="checkbox"
                          checked={formData.security_measures.includes(measure.id)}
                          onChange={() => handleCheckboxChange(measure.id)}
                          className="w-4 h-4 text-blue-600 bg-gray-600 border-gray-500 rounded focus:ring-blue-500"
                        />
                        <span className="text-gray-300 text-sm">{measure.label}</span>
                      </label>
                    ))}
                  </div>
                </div>

                {/* Intermediate Measures */}
                <div className="mb-4">
                  <h4 className="text-xs font-semibold text-green-400 uppercase tracking-wide mb-2">
                    🔒 Intermediate Security
                  </h4>
                  <div className="grid grid-cols-1 md:grid-cols-2 gap-2">
                    {SECURITY_MEASURES.filter(m => m.category === 'intermediate').map((measure) => (
                      <label
                        key={measure.id}
                        className="flex items-center gap-3 px-4 py-2 bg-gray-700/50 hover:bg-gray-700 border border-gray-600 rounded-lg cursor-pointer transition"
                      >
                        <input
                          type="checkbox"
                          checked={formData.security_measures.includes(measure.id)}
                          onChange={() => handleCheckboxChange(measure.id)}
                          className="w-4 h-4 text-green-600 bg-gray-600 border-gray-500 rounded focus:ring-green-500"
                        />
                        <span className="text-gray-300 text-sm">{measure.label}</span>
                      </label>
                    ))}
                  </div>
                </div>

                {/* Advanced Measures */}
                <div className="mb-4">
                  <h4 className="text-xs font-semibold text-orange-400 uppercase tracking-wide mb-2">
                    ⭐ Advanced Security
                  </h4>
                  <div className="grid grid-cols-1 md:grid-cols-2 gap-2">
                    {SECURITY_MEASURES.filter(m => m.category === 'advanced').map((measure) => (
                      <label
                        key={measure.id}
                        className="flex items-center gap-3 px-4 py-2 bg-gray-700/50 hover:bg-gray-700 border border-yellow-600/30 rounded-lg cursor-pointer transition"
                      >
                        <input
                          type="checkbox"
                          checked={formData.security_measures.includes(measure.id)}
                          onChange={() => handleCheckboxChange(measure.id)}
                          className="w-4 h-4 text-yellow-600 bg-gray-600 border-gray-500 rounded focus:ring-yellow-500"
                        />
                        <span className="text-gray-300 text-sm">{measure.label}</span>
                      </label>
                    ))}
                  </div>
                </div>

                {/* Expert Measures */}
                <div className="mb-4">
                  <h4 className="text-xs font-semibold text-purple-400 uppercase tracking-wide mb-2">
                    🏆 Expert Security
                  </h4>
                  <div className="grid grid-cols-1 md:grid-cols-2 gap-2">
                    {SECURITY_MEASURES.filter(m => m.category === 'expert').map((measure) => (
                      <label
                        key={measure.id}
                        className="flex items-center gap-3 px-4 py-2 bg-purple-900/20 hover:bg-purple-900/30 border border-purple-500/30 rounded-lg cursor-pointer transition"
                      >
                        <input
                          type="checkbox"
                          checked={formData.security_measures.includes(measure.id)}
                          onChange={() => handleCheckboxChange(measure.id)}
                          className="w-4 h-4 text-purple-600 bg-gray-600 border-gray-500 rounded focus:ring-purple-500"
                        />
                        <span className="text-gray-300 text-sm">{measure.label}</span>
                      </label>
                    ))}
                  </div>
                </div>

                <p className="text-gray-500 text-xs mt-2">
                  Select all that apply • {formData.security_measures.length} selected
                </p>
              </div>

              <div>
                <label className="block text-sm font-medium text-gray-300 mb-2">
                  Monthly Security Budget
                </label>
                <select
                  name="budget"
                  value={formData.budget}
                  onChange={handleChange}
                  className="w-full px-4 py-2 bg-gray-700 text-white border border-gray-600 rounded-lg focus:ring-2 focus:ring-blue-500"
                >
                  <option value="">Select budget</option>
                  <option value="< $500">Less than $500</option>
                  <option value="$500-$2K">$500 - $2,000</option>
                  <option value="$2K-$5K">$2,000 - $5,000</option>
                  <option value="$5K+">$5,000+</option>
                </select>
              </div>

              <div>
                <label className="block text-sm font-medium text-gray-300 mb-2">
                  What keeps you up at night?
                </label>
                <textarea
                  name="main_concern"
                  value={formData.main_concern}
                  onChange={handleChange}
                  className="w-full px-4 py-2 bg-gray-700 text-white border border-gray-600 rounded-lg focus:ring-2 focus:ring-blue-500"
                  rows="3"
                  placeholder="Ransomware? Data breach? Customer security questionnaires?"
                />
              </div>

              <button
                type="submit"
                className="w-full px-6 py-3 bg-gradient-to-r from-blue-500 to-purple-600 text-white font-semibold rounded-lg hover:from-blue-600 hover:to-purple-700 transition-all"
              >
                Get My Security Assessment →
              </button>
            </form>
          </div>
        </div>
      </div>
    )
  }

  if (step === 'results' && results) {
    return (
      <div className="min-h-screen bg-gradient-to-br from-gray-900 via-gray-800 to-gray-900 p-6">
        <div className="max-w-4xl mx-auto">
          <button
            onClick={() => setStep('form')}
            className="text-gray-400 hover:text-white mb-6 flex items-center gap-2"
          >
            ← Back to Form
          </button>

          <div className="bg-gray-800/50 border border-gray-700 rounded-lg p-8 mb-6">
            <div className="text-center mb-8">
              <h1 className="text-4xl font-bold text-white mb-2">
                {results.company_name}'s Security Report
              </h1>
              <div className="inline-block px-6 py-3 bg-blue-900/30 border border-blue-500/50 rounded-lg mt-4">
                <div className="text-5xl font-bold text-blue-400 mb-1">
                  {results.maturity_score}/10
                </div>
                <div className="text-gray-300">{results.maturity_level}</div>
              </div>
            </div>

            {/* Full Assessment with Markdown */}
            <div className="prose prose-invert max-w-none">
              <div className="bg-gray-700/30 rounded-lg p-6 mb-6">
                <ReactMarkdown
                  components={{
                    h1: ({node, ...props}) => <h1 className="text-3xl font-bold text-white mb-4" {...props} />,
                    h2: ({node, ...props}) => <h2 className="text-2xl font-bold text-white mb-3 mt-6" {...props} />,
                    h3: ({node, ...props}) => <h3 className="text-xl font-bold text-white mb-2 mt-4" {...props} />,
                    h4: ({node, ...props}) => <h4 className="text-lg font-bold text-blue-400 mb-2 mt-3" {...props} />,
                    p: ({node, ...props}) => <p className="text-gray-300 mb-3 leading-relaxed" {...props} />,
                    ul: ({node, ...props}) => <ul className="list-disc list-inside text-gray-300 mb-3 space-y-1" {...props} />,
                    ol: ({node, ...props}) => <ol className="list-decimal list-inside text-gray-300 mb-3 space-y-1" {...props} />,
                    li: ({node, ...props}) => <li className="text-gray-300" {...props} />,
                    strong: ({node, ...props}) => <strong className="font-bold text-white" {...props} />,
                    em: ({node, ...props}) => <em className="italic text-blue-300" {...props} />,
                    code: ({node, ...props}) => <code className="bg-gray-800 px-2 py-1 rounded text-blue-300 text-sm" {...props} />,
                    pre: ({node, ...props}) => <pre className="bg-gray-800 p-4 rounded-lg overflow-x-auto mb-4" {...props} />,
                  }}
                >
                  {results.top_gaps[0]?.description || results.risk_summary}
                </ReactMarkdown>
              </div>
            </div>
          </div>

          <div className="flex gap-4">
            <button
              onClick={() => {
                setStep('form')
                setResults(null)
                setFormData({
                  company_name: '',
                  company_size: '',
                  industry: '',
                  tech_stack: '',
                  security_measures: [],
                  budget: '',
                  main_concern: ''
                })
              }}
              className="px-6 py-3 bg-gray-700 hover:bg-gray-600 text-white rounded-lg transition"
            >
              Start New Assessment
            </button>
            <button
              onClick={onBack}
              className="px-6 py-3 bg-purple-600 hover:bg-purple-700 text-white rounded-lg transition"
            >
              Ask Implementation Questions →
            </button>
          </div>
        </div>
      </div>
    )
  }

  return null
}

export default Assessment
