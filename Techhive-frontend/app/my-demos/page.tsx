'use client'

import { useState, useEffect } from 'react'
import Header from '@/components/Header'
import axios from 'axios'

interface Demo {
  demo_id: string
  business_name: string
  demo_url: string
  price_paid: number
  purchased_at: string
  payment_status: string
}

export default function MyDemos() {
  const [email, setEmail] = useState('')
  const [demos, setDemos] = useState<Demo[]>([])
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState<string | null>(null)

  const fetchDemos = async () => {
    if (!email.trim()) {
      setError('Please enter your email address')
      return
    }

    setLoading(true)
    setError(null)

    try {
      const response = await axios.post('/api/client/demos', {
        client_email: email,
      })
      setDemos(response.data)
      
      if (response.data.length === 0) {
        setError('No demos found for this email address')
      }
    } catch (err) {
      setError('Failed to fetch demos. Please try again.')
      console.error('Fetch error:', err)
    } finally {
      setLoading(false)
    }
  }

  return (
    <main className="min-h-screen bg-gradient-to-b from-gray-50 to-gray-100">
      <Header />
      <div className="container mx-auto px-4 py-12">
        <div className="max-w-4xl mx-auto">
          <h1 className="text-4xl font-bold text-gray-900 mb-4">My Demos</h1>
          <p className="text-lg text-gray-600 mb-8">
            Access all your purchased demos in one place
          </p>

          {/* Email Input */}
          <div className="bg-white rounded-2xl shadow-lg p-6 mb-8">
            <label htmlFor="email" className="block text-sm font-medium text-gray-700 mb-2">
              Enter your email to view your demos
            </label>
            <div className="flex gap-4">
              <input
                type="email"
                id="email"
                value={email}
                onChange={(e) => setEmail(e.target.value)}
                onKeyPress={(e) => e.key === 'Enter' && fetchDemos()}
                placeholder="your@email.com"
                className="flex-1 px-4 py-3 border-2 border-gray-200 rounded-xl focus:border-primary-500 focus:outline-none"
              />
              <button
                onClick={fetchDemos}
                disabled={loading}
                className="px-8 py-3 bg-primary-600 text-white rounded-xl hover:bg-primary-700 transition-colors font-semibold disabled:bg-gray-400"
              >
                {loading ? 'Loading...' : 'View Demos'}
              </button>
            </div>

            {error && (
              <div className="mt-4 p-4 bg-red-50 border-l-4 border-red-500 text-red-700 rounded">
                <p>{error}</p>
              </div>
            )}
          </div>

          {/* Demos List */}
          {demos.length > 0 && (
            <div className="space-y-4">
              <h2 className="text-2xl font-bold text-gray-900 mb-4">
                Your Demos ({demos.length})
              </h2>
              
              {demos.map((demo) => (
                <div
                  key={demo.demo_id}
                  className="bg-white rounded-xl shadow-md p-6 hover:shadow-lg transition-shadow"
                >
                  <div className="flex items-start justify-between">
                    <div className="flex-1">
                      <h3 className="text-xl font-bold text-gray-900 mb-2">
                        {demo.business_name}
                      </h3>
                      
                      <div className="space-y-2 mb-4">
                        <div className="flex items-center gap-2 text-sm text-gray-600">
                          <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M8 7V3m8 4V3m-9 8h10M5 21h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v12a2 2 0 002 2z" />
                          </svg>
                          Purchased: {new Date(demo.purchased_at).toLocaleDateString()}
                        </div>
                        
                        <div className="flex items-center gap-2 text-sm text-gray-600">
                          <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 8c-1.657 0-3 .895-3 2s1.343 2 3 2 3 .895 3 2-1.343 2-3 2m0-8c1.11 0 2.08.402 2.599 1M12 8V7m0 1v8m0 0v1m0-1c-1.11 0-2.08-.402-2.599-1M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
                          </svg>
                          Paid: ${demo.price_paid.toFixed(2)}
                        </div>
                      </div>

                      <div className="bg-gray-50 rounded-lg p-3 mb-4">
                        <p className="text-xs text-gray-500 mb-1">Demo URL:</p>
                        <a
                          href={demo.demo_url}
                          target="_blank"
                          rel="noopener noreferrer"
                          className="text-sm text-primary-600 hover:text-primary-700 break-all"
                        >
                          {demo.demo_url}
                        </a>
                      </div>
                    </div>

                    <a
                      href={demo.demo_url}
                      target="_blank"
                      rel="noopener noreferrer"
                      className="ml-4 px-6 py-3 bg-primary-600 text-white rounded-lg hover:bg-primary-700 transition-colors font-semibold whitespace-nowrap"
                    >
                      View Demo →
                    </a>
                  </div>
                </div>
              ))}
            </div>
          )}
        </div>
      </div>
    </main>
  )
}
