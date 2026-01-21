/**
 * Customization Panel Component
 * 
 * Provides controls for customizing design (colors, fonts, spacing, etc.)
 */

'use client';

import { useState } from 'react';
import { HexColorPicker } from 'react-colorful';
import { DesignCustomization } from '@/types';
import { useProjectStore } from '@/store/project';
import { motion, AnimatePresence } from 'framer-motion';

export function CustomizationPanel() {
  const { design, updateDesign } = useProjectStore();
  const [activeTab, setActiveTab] = useState<'colors' | 'typography' | 'spacing' | 'animations'>('colors');
  const [activeColorPicker, setActiveColorPicker] = useState<string | null>(null);

  if (!design) return null;

  const fontOptions = [
    'Inter',
    'Roboto',
    'Open Sans',
    'Montserrat',
    'Poppins',
    'Lato',
    'Raleway',
    'Ubuntu',
    'Playfair Display',
    'Merriweather',
  ];

  const animationOptions: Array<'none' | 'fade' | 'slide' | 'bounce'> = ['none', 'fade', 'slide', 'bounce'];

  return (
    <div className="h-full bg-white border-l border-gray-200 overflow-y-auto">
      <div className="p-6">
        <h2 className="text-2xl font-bold mb-6">Customize Design</h2>

        {/* Tabs */}
        <div className="flex space-x-2 mb-6 border-b border-gray-200">
          {['colors', 'typography', 'spacing', 'animations'].map((tab) => (
            <button
              key={tab}
              onClick={() => setActiveTab(tab as any)}
              className={`pb-3 px-4 font-medium capitalize transition-colors ${
                activeTab === tab
                  ? 'border-b-2 border-blue-600 text-blue-600'
                  : 'text-gray-600 hover:text-gray-900'
              }`}
            >
              {tab}
            </button>
          ))}
        </div>

        <AnimatePresence mode="wait">
          {/* Colors Tab */}
          {activeTab === 'colors' && (
            <motion.div
              key="colors"
              initial={{ opacity: 0, x: 20 }}
              animate={{ opacity: 1, x: 0 }}
              exit={{ opacity: 0, x: -20 }}
              className="space-y-6"
            >
              {Object.entries(design.colors).map(([key, value]) => (
                <div key={key}>
                  <label className="block text-sm font-medium mb-2 capitalize">
                    {key.replace(/([A-Z])/g, ' $1').trim()}
                  </label>
                  <div className="flex items-center space-x-3">
                    <button
                      onClick={() => setActiveColorPicker(activeColorPicker === key ? null : key)}
                      className="w-12 h-12 rounded-lg border-2 border-gray-300 shadow-sm cursor-pointer hover:scale-110 transition-transform"
                      style={{ backgroundColor: value }}
                    />
                    <input
                      type="text"
                      value={value}
                      onChange={(e) => updateDesign({
                        colors: { ...design.colors, [key]: e.target.value }
                      })}
                      className="flex-1 px-3 py-2 border border-gray-300 rounded-lg font-mono text-sm"
                    />
                  </div>
                  {activeColorPicker === key && (
                    <div className="mt-3">
                      <HexColorPicker
                        color={value}
                        onChange={(color) => updateDesign({
                          colors: { ...design.colors, [key]: color }
                        })}
                      />
                    </div>
                  )}
                </div>
              ))}
            </motion.div>
          )}

          {/* Typography Tab */}
          {activeTab === 'typography' && (
            <motion.div
              key="typography"
              initial={{ opacity: 0, x: 20 }}
              animate={{ opacity: 1, x: 0 }}
              exit={{ opacity: 0, x: -20 }}
              className="space-y-6"
            >
              <div>
                <label className="block text-sm font-medium mb-2">Primary Font</label>
                <select
                  value={design.fonts.primary}
                  onChange={(e) => updateDesign({
                    fonts: { ...design.fonts, primary: e.target.value }
                  })}
                  className="w-full px-3 py-2 border border-gray-300 rounded-lg"
                >
                  {fontOptions.map((font) => (
                    <option key={font} value={font} style={{ fontFamily: font }}>
                      {font}
                    </option>
                  ))}
                </select>
              </div>

              <div>
                <label className="block text-sm font-medium mb-2">Secondary Font</label>
                <select
                  value={design.fonts.secondary}
                  onChange={(e) => updateDesign({
                    fonts: { ...design.fonts, secondary: e.target.value }
                  })}
                  className="w-full px-3 py-2 border border-gray-300 rounded-lg"
                >
                  {fontOptions.map((font) => (
                    <option key={font} value={font} style={{ fontFamily: font }}>
                      {font}
                    </option>
                  ))}
                </select>
              </div>

              <div>
                <label className="block text-sm font-medium mb-2">Heading Font</label>
                <select
                  value={design.fonts.heading}
                  onChange={(e) => updateDesign({
                    fonts: { ...design.fonts, heading: e.target.value }
                  })}
                  className="w-full px-3 py-2 border border-gray-300 rounded-lg"
                >
                  {fontOptions.map((font) => (
                    <option key={font} value={font} style={{ fontFamily: font }}>
                      {font}
                    </option>
                  ))}
                </select>
              </div>
            </motion.div>
          )}

          {/* Spacing Tab */}
          {activeTab === 'spacing' && (
            <motion.div
              key="spacing"
              initial={{ opacity: 0, x: 20 }}
              animate={{ opacity: 1, x: 0 }}
              exit={{ opacity: 0, x: -20 }}
              className="space-y-6"
            >
              <div>
                <label className="block text-sm font-medium mb-2">
                  Border Radius: {design.borderRadius}px
                </label>
                <input
                  type="range"
                  min="0"
                  max="32"
                  step="1"
                  value={design.borderRadius}
                  onChange={(e) => updateDesign({ borderRadius: parseInt(e.target.value) })}
                  className="w-full"
                />
                <div className="flex justify-between text-xs text-gray-500 mt-1">
                  <span>Sharp (0px)</span>
                  <span>Rounded (32px)</span>
                </div>
              </div>

              <div>
                <label className="block text-sm font-medium mb-2">
                  Spacing Scale: {design.spacing}
                </label>
                <input
                  type="range"
                  min="0.5"
                  max="2"
                  step="0.1"
                  value={design.spacing}
                  onChange={(e) => updateDesign({ spacing: parseFloat(e.target.value) })}
                  className="w-full"
                />
                <div className="flex justify-between text-xs text-gray-500 mt-1">
                  <span>Compact (0.5x)</span>
                  <span>Spacious (2x)</span>
                </div>
              </div>
            </motion.div>
          )}

          {/* Animations Tab */}
          {activeTab === 'animations' && (
            <motion.div
              key="animations"
              initial={{ opacity: 0, x: 20 }}
              animate={{ opacity: 1, x: 0 }}
              exit={{ opacity: 0, x: -20 }}
              className="space-y-6"
            >
              <div>
                <label className="block text-sm font-medium mb-2">Animation Style</label>
                <div className="grid grid-cols-2 gap-3">
                  {animationOptions.map((animation) => (
                    <button
                      key={animation}
                      onClick={() => updateDesign({
                        animations: { ...design.animations, enabled: animation !== 'none', style: animation }
                      })}
                      className={`px-4 py-3 rounded-lg border-2 capitalize font-medium transition-all ${
                        design.animations.style === animation
                          ? 'border-blue-600 bg-blue-50 text-blue-600'
                          : 'border-gray-300 hover:border-gray-400'
                      }`}
                    >
                      {animation}
                    </button>
                  ))}
                </div>
              </div>

              <div>
                <label className="flex items-center space-x-2">
                  <input
                    type="checkbox"
                    checked={design.animations.parallax}
                    onChange={(e) => updateDesign({
                      animations: { ...design.animations, parallax: e.target.checked }
                    })}
                    className="w-4 h-4 text-blue-600 rounded"
                  />
                  <span className="text-sm font-medium">Enable Parallax Effects</span>
                </label>
              </div>

              <div>
                <label className="flex items-center space-x-2">
                  <input
                    type="checkbox"
                    checked={design.animations.hover}
                    onChange={(e) => updateDesign({
                      animations: { ...design.animations, hover: e.target.checked }
                    })}
                    className="w-4 h-4 text-blue-600 rounded"
                  />
                  <span className="text-sm font-medium">Enable Hover Effects</span>
                </label>
              </div>
            </motion.div>
          )}
        </AnimatePresence>

        {/* Action Buttons */}
        <div className="mt-8 pt-6 border-t border-gray-200 space-y-3">
          <button
            onClick={() => {
              // Reset to defaults
              const defaultDesign: DesignCustomization = {
                colors: {
                  primary: '#3B82F6',
                  secondary: '#10B981',
                  accent: '#F59E0B',
                  background: '#FFFFFF',
                  text: '#1F2937',
                  textSecondary: '#6B7280',
                },
                fonts: {
                  primary: 'Inter',
                  secondary: 'Roboto',
                  heading: 'Poppins',
                },
                spacing: 1,
                borderRadius: 8,
                animations: {
                  enabled: true,
                  style: 'fade',
                  parallax: false,
                  hover: true,
                },
              };
              updateDesign(defaultDesign);
            }}
            className="w-full px-4 py-2 border border-gray-300 rounded-lg hover:bg-gray-50 font-medium"
          >
            Reset to Defaults
          </button>
        </div>
      </div>
    </div>
  );
}
