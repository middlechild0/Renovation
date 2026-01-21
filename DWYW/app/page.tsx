/**
 * DWYW Landing Page
 */

'use client';

import Link from 'next/link';
import { motion } from 'framer-motion';

export default function HomePage() {
  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-50 via-white to-purple-50">
      {/* Hero Section */}
      <div className="max-w-7xl mx-auto px-6 py-20">
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.6 }}
          className="text-center"
        >
          <h1 className="text-6xl font-bold mb-6 bg-gradient-to-r from-blue-600 to-purple-600 bg-clip-text text-transparent">
            Design What You Want
          </h1>
          <p className="text-2xl text-gray-600 mb-8 max-w-3xl mx-auto">
            Create stunning, professional websites in minutes with AI-powered design tools.
            No coding required.
          </p>
          <Link
            href="/editor"
            className="inline-block px-8 py-4 bg-gradient-to-r from-blue-600 to-purple-600 text-white text-lg font-semibold rounded-full hover:shadow-2xl transition-all transform hover:scale-105"
          >
            Start Designing Free →
          </Link>
        </motion.div>

        {/* Features Grid */}
        <motion.div
          initial={{ opacity: 0, y: 40 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.6, delay: 0.2 }}
          className="mt-24 grid grid-cols-1 md:grid-cols-3 gap-8"
        >
          <div className="bg-white p-8 rounded-2xl shadow-lg">
            <div className="text-4xl mb-4">🎨</div>
            <h3 className="text-xl font-bold mb-3">Visual Customization</h3>
            <p className="text-gray-600">
              Customize colors, fonts, spacing, and animations with an intuitive visual editor.
            </p>
          </div>

          <div className="bg-white p-8 rounded-2xl shadow-lg">
            <div className="text-4xl mb-4">✨</div>
            <h3 className="text-xl font-bold mb-3">AI Design Assistant</h3>
            <p className="text-gray-600">
              Describe what you want in plain English and let AI make the changes for you.
            </p>
          </div>

          <div className="bg-white p-8 rounded-2xl shadow-lg">
            <div className="text-4xl mb-4">👁️</div>
            <h3 className="text-xl font-bold mb-3">Live Preview</h3>
            <p className="text-gray-600">
              See your changes instantly across desktop, tablet, and mobile devices.
            </p>
          </div>

          <div className="bg-white p-8 rounded-2xl shadow-lg">
            <div className="text-4xl mb-4">🚀</div>
            <h3 className="text-xl font-bold mb-3">One-Click Deploy</h3>
            <p className="text-gray-600">
              Deploy your website to production with a single click. We handle everything.
            </p>
          </div>

          <div className="bg-white p-8 rounded-2xl shadow-lg">
            <div className="text-4xl mb-4">💰</div>
            <h3 className="text-xl font-bold mb-3">Transparent Pricing</h3>
            <p className="text-gray-600">
              Pay only for the features you use. No hidden fees or monthly subscriptions.
            </p>
          </div>

          <div className="bg-white p-8 rounded-2xl shadow-lg">
            <div className="text-4xl mb-4">🔒</div>
            <h3 className="text-xl font-bold mb-3">Full Ownership</h3>
            <p className="text-gray-600">
              Get complete source code. No vendor lock-in. Your website, your rules.
            </p>
          </div>
        </motion.div>

        {/* Templates Preview */}
        <motion.div
          initial={{ opacity: 0, y: 40 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.6, delay: 0.4 }}
          className="mt-24"
        >
          <h2 className="text-4xl font-bold text-center mb-12">
            Professional Templates
          </h2>
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
            {[
              { name: 'Restaurant', icon: '🍽️', category: 'Food & Beverage' },
              { name: 'E-Commerce', icon: '🛍️', category: 'Online Store' },
              { name: 'SaaS', icon: '💼', category: 'Software' },
              { name: 'Portfolio', icon: '🎨', category: 'Personal' },
            ].map((template) => (
              <div
                key={template.name}
                className="bg-white rounded-xl overflow-hidden shadow-lg hover:shadow-2xl transition-shadow cursor-pointer"
              >
                <div className="aspect-video bg-gradient-to-br from-gray-100 to-gray-200 flex items-center justify-center">
                  <span className="text-6xl">{template.icon}</span>
                </div>
                <div className="p-6">
                  <h3 className="font-bold text-lg mb-1">{template.name}</h3>
                  <p className="text-sm text-gray-600">{template.category}</p>
                </div>
              </div>
            ))}
          </div>
        </motion.div>

        {/* CTA */}
        <motion.div
          initial={{ opacity: 0, y: 40 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.6, delay: 0.6 }}
          className="mt-24 text-center"
        >
          <h2 className="text-4xl font-bold mb-6">Ready to build your dream website?</h2>
          <Link
            href="/editor"
            className="inline-block px-8 py-4 bg-gradient-to-r from-blue-600 to-purple-600 text-white text-lg font-semibold rounded-full hover:shadow-2xl transition-all transform hover:scale-105"
          >
            Get Started Now →
          </Link>
        </motion.div>
      </div>
    </div>
  );
}
