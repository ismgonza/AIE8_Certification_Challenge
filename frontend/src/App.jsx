import { useState } from 'react'
import Assessment from './Assessment'
import ImplementationHelper from './ImplementationHelper'

function App() {
  const [mode, setMode] = useState('landing') // 'landing', 'assessment', 'implementation'

  if (mode === 'landing') {
    return (
      <div className="min-h-screen bg-gradient-to-br from-gray-900 via-gray-800 to-gray-900 flex items-center justify-center p-6">
        <div className="max-w-5xl w-full">
          <div className="text-center mb-12">
            <div className="inline-block p-4 bg-blue-500/20 rounded-full mb-6">
              <svg className="w-16 h-16 text-blue-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 12l2 2 4-4m5.618-4.016A11.955 11.955 0 0112 2.944a11.955 11.955 0 01-8.618 3.04A12.02 12.02 0 003 9c0 5.591 3.824 10.29 9 11.622 5.176-1.332 9-6.03 9-11.622 0-1.042-.133-2.052-.382-3.016z" />
              </svg>
            </div>
            <h1 className="text-5xl font-bold text-white mb-4">
              🛡️ Shieldy - The AI Security Assistant
            </h1>
            <p className="text-xl text-gray-300">
              AI-powered security guidance for small-medium businesses
            </p>
          </div>

          <div className="grid md:grid-cols-2 gap-8">
            {/* Assessment Path */}
            <div 
              onClick={() => setMode('assessment')}
              className="bg-gray-800/50 border border-gray-700 rounded-lg p-8 hover:border-blue-500 transition-all cursor-pointer group hover:scale-105 transform"
            >
              <div className="text-center">
                <div className="text-5xl mb-4">📊</div>
                <h2 className="text-2xl font-bold text-white mb-3 group-hover:text-blue-400 transition">
                  Assess My Security
                </h2>
                <p className="text-gray-400 mb-6">
                  "I'm new to this - where do I start?"
                </p>
                <ul className="text-left text-gray-300 space-y-2 mb-6">
                  <li className="flex items-start gap-2">
                    <span className="text-green-400 mt-1">✓</span>
                    <span>Get your security score (0-10)</span>
                  </li>
                  <li className="flex items-start gap-2">
                    <span className="text-green-400 mt-1">✓</span>
                    <span>Identify top 5 critical gaps</span>
                  </li>
                  <li className="flex items-start gap-2">
                    <span className="text-green-400 mt-1">✓</span>
                    <span>Prioritized action plan</span>
                  </li>
                </ul>
                <div className="text-sm text-gray-500">
                  ⏱️ 5 minutes • 7 questions
                </div>
              </div>
            </div>

            {/* Implementation Helper Path */}
            <div 
              onClick={() => setMode('implementation')}
              className="bg-gray-800/50 border border-gray-700 rounded-lg p-8 hover:border-purple-500 transition-all cursor-pointer group hover:scale-105 transform"
            >
              <div className="text-center">
                <div className="text-5xl mb-4">🔧</div>
                <h2 className="text-2xl font-bold text-white mb-3 group-hover:text-purple-400 transition">
                  Get Help With Something
                </h2>
                <p className="text-gray-400 mb-6">
                  "I know what I need - show me how"
                </p>
                <ul className="text-left text-gray-300 space-y-2 mb-6">
                  <li className="flex items-start gap-2">
                    <span className="text-green-400 mt-1">✓</span>
                    <span>Step-by-step implementation guides</span>
                  </li>
                  <li className="flex items-start gap-2">
                    <span className="text-green-400 mt-1">✓</span>
                    <span>Copy-paste commands & scripts</span>
                  </li>
                  <li className="flex items-start gap-2">
                    <span className="text-green-400 mt-1">✓</span>
                    <span>Based on CIS, NIST, OWASP standards</span>
                  </li>
                </ul>
                <div className="text-sm text-gray-500">
                  ⏱️ Instant • Ask anything
                </div>
              </div>
            </div>
          </div>

          <div className="text-center mt-8">
            <p className="text-gray-500 text-sm">
              Powered by AI • Based on industry best practices • No installation required
            </p>
          </div>
        </div>
      </div>
    )
  }

  if (mode === 'assessment') {
    return <Assessment onBack={() => setMode('landing')} />
  }

  if (mode === 'implementation') {
    return <ImplementationHelper onBack={() => setMode('landing')} />
  }

  return null
}

export default App
