import { useState, useEffect } from 'react'
import ReactMarkdown from 'react-markdown'

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
  "🛡️ Regular backups can save your business from ransomware"
]

function LoadingScreen() {
  const [currentTip, setCurrentTip] = useState(0)

  useEffect(() => {
    const interval = setInterval(() => {
      setCurrentTip((prev) => (prev + 1) % SECURITY_TIPS.length)
    }, 3000)
    return () => clearInterval(interval)
  }, [])

  return (
    <div className="fixed inset-0 bg-gradient-to-br from-gray-900 via-gray-800 to-gray-900 flex items-center justify-center z-50">
      <div className="text-center">
        <div className="relative w-32 h-32 mx-auto mb-8">
          <div className="absolute inset-0 border-8 border-gray-700 rounded-full"></div>
          <div className="absolute inset-0 border-8 border-purple-500 rounded-full border-t-transparent animate-spin"></div>
          <div className="absolute inset-4 border-8 border-blue-500 rounded-full border-t-transparent animate-spin" style={{animationDuration: '1.5s', animationDirection: 'reverse'}}></div>
          <div className="absolute inset-0 flex items-center justify-center">
            <svg className="w-12 h-12 text-purple-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
            </svg>
          </div>
        </div>

        <h2 className="text-2xl font-bold text-white mb-4">
          🔧 Generating Your Implementation Guide...
        </h2>
        <p className="text-gray-400 mb-8">
          Analyzing CIS benchmarks, NIST guidelines, and best practices
        </p>

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

function StepByStepGuide({ guide, onBack, onNewSearch, loading }) {
  const [copiedText, setCopiedText] = useState('')

  const copyToClipboard = (text) => {
    navigator.clipboard.writeText(text)
    setCopiedText(text)
    setTimeout(() => setCopiedText(''), 2000)
  }

  if (loading) {
    return <LoadingScreen />
  }

  return (
    <div className="min-h-screen bg-gradient-to-br from-gray-900 via-gray-800 to-gray-900 p-6">
      <div className="max-w-4xl mx-auto">
        <div className="flex items-center justify-between mb-6">
          <button
            onClick={onBack}
            className="text-gray-400 hover:text-white flex items-center gap-2"
          >
            ← Back
          </button>
          <button
            onClick={onNewSearch}
            className="px-4 py-2 bg-purple-600 hover:bg-purple-700 text-white rounded-lg transition"
          >
            New Search
          </button>
        </div>

        <div className="bg-gray-800/50 border border-gray-700 rounded-lg p-8">
          {/* Header */}
          <div className="mb-8">
            <h1 className="text-3xl font-bold text-white mb-2">
              {guide.title}
            </h1>
            <div className="flex items-center gap-4 text-sm text-gray-400">
              <span>📚 Based on industry standards</span>
              <span>•</span>
              <span>⏱️ AI-generated guide</span>
            </div>
          </div>

          {/* Main Content */}
          <div className="prose prose-invert max-w-none">
            <ReactMarkdown
              components={{
                h1: ({node, ...props}) => <h1 className="text-3xl font-bold text-white mb-4 mt-8 border-b border-gray-700 pb-2" {...props} />,
                h2: ({node, ...props}) => <h2 className="text-2xl font-bold text-white mb-3 mt-6" {...props} />,
                h3: ({node, ...props}) => <h3 className="text-xl font-bold text-purple-400 mb-2 mt-4" {...props} />,
                h4: ({node, ...props}) => <h4 className="text-lg font-bold text-blue-400 mb-2 mt-3" {...props} />,
                p: ({node, ...props}) => <p className="text-gray-300 mb-3 leading-relaxed" {...props} />,
                ul: ({node, ...props}) => <ul className="list-disc list-inside text-gray-300 mb-4 space-y-2" {...props} />,
                ol: ({node, ...props}) => <ol className="list-decimal list-inside text-gray-300 mb-4 space-y-2" {...props} />,
                li: ({node, ...props}) => <li className="text-gray-300 ml-4" {...props} />,
                strong: ({node, ...props}) => <strong className="font-bold text-white" {...props} />,
                em: ({node, ...props}) => <em className="italic text-blue-300" {...props} />,
                code: ({node, inline, ...props}) => {
                  if (inline) {
                    return <code className="bg-gray-900 px-2 py-1 rounded text-purple-300 text-sm font-mono" {...props} />
                  }
                  const codeText = props.children ? String(props.children) : ''
                  return (
                    <div className="relative group">
                      <pre className="bg-gray-900 p-4 rounded-lg overflow-x-auto mb-4 border border-gray-700">
                        <code className="text-green-300 text-sm font-mono" {...props} />
                      </pre>
                      <button
                        onClick={() => copyToClipboard(codeText)}
                        className="absolute top-2 right-2 px-3 py-1 bg-gray-800 hover:bg-gray-700 text-gray-300 text-xs rounded border border-gray-600 opacity-0 group-hover:opacity-100 transition"
                      >
                        {copiedText === codeText ? '✓ Copied!' : '📋 Copy'}
                      </button>
                    </div>
                  )
                },
                pre: ({node, ...props}) => <div {...props} />,
                blockquote: ({node, ...props}) => (
                  <blockquote className="border-l-4 border-purple-500 pl-4 italic text-gray-400 my-4" {...props} />
                ),
              }}
            >
              {guide.content}
            </ReactMarkdown>
          </div>

          {/* Sources (if available) */}
          {guide.sources && guide.sources.length > 0 && (
            <div className="mt-8 pt-8 border-t border-gray-700">
              <h3 className="text-lg font-bold text-white mb-4">📚 Sources Referenced:</h3>
              <div className="space-y-2">
                {guide.sources.map((source, idx) => {
                  // Check if this is a web source (URL) or PDF
                  const isWebSource = source.metadata?.type === 'web_search' || 
                                     source.metadata?.source?.startsWith('http')
                  
                  // Extract filename from path (for PDFs)
                  const getFilename = (path) => {
                    if (!path) return 'Unknown source'
                    const parts = path.split('/')
                    return parts[parts.length - 1]
                  }

                  if (isWebSource) {
                    // Display web source with clickable link
                    return (
                      <div key={idx} className="bg-purple-900/20 border border-purple-500/30 rounded-lg p-3 text-sm">
                        <div className="flex items-start gap-2 mb-2">
                          <span className="text-purple-400 font-mono text-xs">🌐</span>
                          <a 
                            href={source.metadata?.source}
                            target="_blank"
                            rel="noopener noreferrer"
                            className="text-purple-300 hover:text-purple-200 font-medium text-xs underline"
                          >
                            {source.metadata?.title || 'Web Resource'}
                          </a>
                        </div>
                        <div className="text-gray-400 text-xs line-clamp-2 ml-5">
                          {source.content?.substring(0, 150)}...
                        </div>
                      </div>
                    )
                  } else {
                    // Display PDF source
                    return (
                      <div key={idx} className="bg-gray-700/30 rounded-lg p-3 text-sm">
                        <div className="flex items-start gap-2 mb-2">
                          <span className="text-blue-400 font-mono text-xs">📄</span>
                          <span className="text-blue-300 font-medium text-xs">
                            {getFilename(source.metadata?.source)}
                            {source.metadata?.page && (
                              <span className="text-gray-500 ml-1">
                                Page {source.metadata.page}
                              </span>
                            )}
                          </span>
                        </div>
                        <div className="text-gray-400 text-xs line-clamp-2 ml-5">
                          {source.content?.substring(0, 150)}...
                        </div>
                      </div>
                    )
                  }
                })}
              </div>
            </div>
          )}
        </div>
      </div>
    </div>
  )
}

export default StepByStepGuide

