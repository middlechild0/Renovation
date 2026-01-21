/**
 * Pricing Display Component
 * 
 * Shows transparent pricing breakdown with feature explanations
 */

'use client';

import { useProjectStore } from '@/store/project';
import { motion, AnimatePresence } from 'framer-motion';
import { featureRegistry } from '@/lib/pricing';

export function PricingDisplay() {
  const { currentProject, showingPricing, togglePricing } = useProjectStore();

  if (!currentProject) return null;

  const { pricing } = currentProject;

  return (
    <>
      {/* Floating Pricing Button */}
      <motion.button
        onClick={togglePricing}
        className="fixed bottom-8 right-8 px-6 py-3 bg-gradient-to-r from-blue-600 to-purple-600 text-white rounded-full shadow-lg font-semibold z-50 hover:scale-105 transition-transform"
        whileHover={{ scale: 1.05 }}
        whileTap={{ scale: 0.95 }}
      >
        💰 ${pricing.total.toFixed(2)}
      </motion.button>

      {/* Pricing Panel */}
      <AnimatePresence>
        {showingPricing && (
          <>
            {/* Backdrop */}
            <motion.div
              initial={{ opacity: 0 }}
              animate={{ opacity: 1 }}
              exit={{ opacity: 0 }}
              onClick={togglePricing}
              className="fixed inset-0 bg-black/50 z-40"
            />

            {/* Panel */}
            <motion.div
              initial={{ x: '100%' }}
              animate={{ x: 0 }}
              exit={{ x: '100%' }}
              transition={{ type: 'spring', damping: 25 }}
              className="fixed right-0 top-0 bottom-0 w-full max-w-md bg-white shadow-2xl z-50 overflow-y-auto"
            >
              <div className="p-6">
                <div className="flex items-center justify-between mb-6">
                  <h2 className="text-2xl font-bold">Pricing Breakdown</h2>
                  <button
                    onClick={togglePricing}
                    className="w-8 h-8 flex items-center justify-center rounded-full hover:bg-gray-100"
                  >
                    ✕
                  </button>
                </div>

                {/* Total */}
                <div className="bg-gradient-to-r from-blue-600 to-purple-600 text-white p-6 rounded-xl mb-6">
                  <p className="text-sm opacity-90 mb-1">Total Project Cost</p>
                  <p className="text-5xl font-bold">${pricing.total.toFixed(2)}</p>
                  <p className="text-sm opacity-75 mt-2">One-time payment • Full ownership</p>
                </div>

                {/* Template Base */}
                <div className="mb-6">
                  <h3 className="font-semibold mb-3">Template Base</h3>
                  <div className="bg-gray-50 p-4 rounded-lg">
                    <div className="flex items-center justify-between">
                      <span>{currentProject.template.name}</span>
                      <span className="font-semibold">${currentProject.template.basePrice}</span>
                    </div>
                  </div>
                </div>

                {/* Features */}
                <div className="mb-6">
                  <h3 className="font-semibold mb-3">Features & Add-ons</h3>
                  <div className="space-y-3">
                    {pricing.breakdown.map((item, index) => {
                      const feature = featureRegistry.find((f) => f.id === item.featureId);
                      if (!feature) return null;

                      return (
                        <div key={index} className="bg-gray-50 p-4 rounded-lg">
                          <div className="flex items-start justify-between mb-2">
                            <div className="flex-1">
                              <p className="font-medium">{feature.name}</p>
                              <p className="text-sm text-gray-600 mt-1">{feature.description}</p>
                            </div>
                            <span className="font-semibold ml-4">${item.price.toFixed(2)}</span>
                          </div>
                          {item.explanation && (
                            <p className="text-xs text-gray-500 mt-2">{item.explanation}</p>
                          )}
                        </div>
                      );
                    })}
                  </div>
                </div>

                {/* What's Included */}
                <div className="mb-6">
                  <h3 className="font-semibold mb-3">What's Included</h3>
                  <ul className="space-y-2 text-sm">
                    <li className="flex items-start">
                      <span className="text-green-600 mr-2">✓</span>
                      <span>Full source code (Next.js, TypeScript, Tailwind CSS)</span>
                    </li>
                    <li className="flex items-start">
                      <span className="text-green-600 mr-2">✓</span>
                      <span>Production-ready deployment configuration</span>
                    </li>
                    <li className="flex items-start">
                      <span className="text-green-600 mr-2">✓</span>
                      <span>Responsive design (mobile, tablet, desktop)</span>
                    </li>
                    <li className="flex items-start">
                      <span className="text-green-600 mr-2">✓</span>
                      <span>SEO optimization</span>
                    </li>
                    <li className="flex items-start">
                      <span className="text-green-600 mr-2">✓</span>
                      <span>Performance optimization</span>
                    </li>
                    <li className="flex items-start">
                      <span className="text-green-600 mr-2">✓</span>
                      <span>Documentation and setup guide</span>
                    </li>
                    <li className="flex items-start">
                      <span className="text-green-600 mr-2">✓</span>
                      <span>30-day support</span>
                    </li>
                  </ul>
                </div>

                {/* Checkout Button */}
                <button className="w-full py-4 bg-gradient-to-r from-blue-600 to-purple-600 text-white rounded-lg font-semibold text-lg hover:shadow-xl transition-shadow">
                  Proceed to Checkout
                </button>

                <p className="text-xs text-center text-gray-500 mt-4">
                  Secure payment powered by Stripe
                </p>
              </div>
            </motion.div>
          </>
        )}
      </AnimatePresence>
    </>
  );
}
