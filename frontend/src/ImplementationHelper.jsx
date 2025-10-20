import { useState } from 'react'
import StepByStepGuide from './StepByStepGuide'

const API_URL = 'http://localhost:8000'

const EXAMPLE_SEARCHES = [
  "Harden Windows Server 2022",
  "Configure MFA in Active Directory",
  "Secure Ubuntu 22.04 baseline configuration",
  "Cisco router security best practices",
  "AWS S3 bucket security checklist",
  "Set up firewall rules for small business",
  "Password policy best practices",
  "Enable BitLocker encryption on Windows"
]

const RECENT_POPULAR = [
  "Windows Server hardening",
  "Linux SSH configuration",
  "Password policy setup",
  "MFA implementation",
  "Backup strategy"
]

function ImplementationHelper({ onBack }) {
  const [step, setStep] = useState('search') // 'search', 'context', 'guide'
  const [searchQuery, setSearchQuery] = useState('')
  const [context, setContext] = useState({
    version: '',
    timebudget: '',
    environment: ''
  })
  const [guide, setGuide] = useState(null)
  const [loading, setLoading] = useState(false)

  const handleSearch = (query) => {
    setSearchQuery(query)
    // For now, skip context gathering and go straight to generating guide
    // We can add context gathering in Phase 2
    generateGuide(query, {})
  }

  const generateGuide = async (query, contextData) => {
    setLoading(true)

    try {
      // Build enhanced query with context
      let enhancedQuery = query

      if (contextData.version) {
        enhancedQuery += ` for version ${contextData.version}`
      }
      if (contextData.timebudget === 'quick_wins') {
        enhancedQuery += `. Focus on quick wins that can be done in 2-4 hours.`
      } else if (contextData.timebudget === 'comprehensive') {
        enhancedQuery += `. Provide comprehensive hardening that takes 1-2 days.`
      }
      if (contextData.environment) {
        enhancedQuery += ` in ${contextData.environment} environment.`
      }

      enhancedQuery += ` Provide step-by-step implementation guide with specific commands, configuration steps, and verification procedures.`

      const response = await fetch(`${API_URL}/query`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          query: enhancedQuery,
          top_k: 5
        })
      })

      const data = await response.json()
      setGuide({
        title: query,
        content: data.answer,
        sources: data.sources || [],
        used_web_search: data.used_web_search || false
      })
      setStep('guide')
    } catch (error) {
      console.error('Error:', error)
      alert('Failed to generate guide. Check console for details.')
    } finally {
      setLoading(false)
    }
  }

  if (loading) {
    return <StepByStepGuide loading={true} />
  }

  if (step === 'guide' && guide) {
    return (
      <StepByStepGuide 
        guide={guide}
        onBack={() => setStep('search')}
        onNewSearch={() => {
          setStep('search')
          setSearchQuery('')
          setGuide(null)
        }}
        loading={false}
      />
    )
  }

  return (
    <div className="min-h-screen bg-gradient-to-br from-gray-900 via-gray-800 to-gray-900 p-6">
      <div className="max-w-4xl mx-auto">
        <button
          onClick={onBack}
          className="text-gray-400 hover:text-white mb-6 flex items-center gap-2"
        >
          ← Back to Home
        </button>

        <div className="bg-gray-800/50 border border-gray-700 rounded-lg p-8 mb-6">
          <div className="text-center mb-8">
            <h1 className="text-4xl font-bold text-white mb-3">
              🔧 What do you need help with?
            </h1>
            <p className="text-gray-400">
              Search or describe what you want to secure or configure
            </p>
          </div>

          {/* Search Bar */}
          <div className="mb-8">
            <form onSubmit={(e) => { e.preventDefault(); handleSearch(searchQuery); }}>
              <div className="relative">
                <input
                  type="text"
                  value={searchQuery}
                  onChange={(e) => setSearchQuery(e.target.value)}
                  placeholder="e.g., 'Harden Windows Server 2022' or 'Configure SSH on Linux'"
                  className="w-full px-6 py-4 bg-gray-700 text-white border border-gray-600 rounded-lg focus:ring-2 focus:ring-purple-500 focus:border-transparent text-lg pr-12"
                />
                <button
                  type="submit"
                  disabled={!searchQuery.trim() || loading}
                  className="absolute right-2 top-1/2 transform -translate-y-1/2 p-2 bg-purple-600 hover:bg-purple-700 disabled:bg-gray-600 text-white rounded-lg transition"
                >
                  <svg className="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z" />
                  </svg>
                </button>
              </div>
            </form>
          </div>

          {/* Example Searches */}
          <div className="mb-8">
            <h3 className="text-sm font-semibold text-gray-400 uppercase tracking-wide mb-3">
              Example searches:
            </h3>
            <div className="flex flex-wrap gap-2">
              {EXAMPLE_SEARCHES.map((example, idx) => (
                <button
                  key={idx}
                  onClick={() => setSearchQuery(example)}
                  className="px-3 py-1.5 bg-gray-700/50 hover:bg-gray-600 text-gray-300 text-sm rounded-lg transition border border-gray-600 hover:border-purple-500"
                >
                  {example}
                </button>
              ))}
            </div>
          </div>

          {/* Recent Popular Searches */}
          <div>
            <h3 className="text-sm font-semibold text-gray-400 uppercase tracking-wide mb-3">
              Recent popular searches:
            </h3>
            <div className="grid grid-cols-2 md:grid-cols-3 gap-3">
              {RECENT_POPULAR.map((search, idx) => (
                <button
                  key={idx}
                  onClick={() => handleSearch(search)}
                  className="flex items-center gap-2 px-4 py-3 bg-gray-700/30 hover:bg-gray-600/50 text-gray-300 rounded-lg transition border border-gray-600 hover:border-purple-500 text-left group"
                >
                  <span className="text-purple-400 group-hover:text-purple-300">🔵</span>
                  <span className="text-sm">{search}</span>
                </button>
              ))}
            </div>
          </div>
        </div>

        {/* Info Cards */}
        <div className="grid md:grid-cols-3 gap-4 text-center">
          <div className="bg-gray-800/30 border border-gray-700 rounded-lg p-4">
            <div className="text-2xl mb-2">📚</div>
            <div className="text-sm text-gray-400">Based on CIS, NIST, OWASP</div>
          </div>
          <div className="bg-gray-800/30 border border-gray-700 rounded-lg p-4">
            <div className="text-2xl mb-2">⚡</div>
            <div className="text-sm text-gray-400">AI-powered, instant results</div>
          </div>
          <div className="bg-gray-800/30 border border-gray-700 rounded-lg p-4">
            <div className="text-2xl mb-2">📋</div>
            <div className="text-sm text-gray-400">Copy-paste ready commands</div>
          </div>
        </div>
      </div>
    </div>
  )
}

export default ImplementationHelper

