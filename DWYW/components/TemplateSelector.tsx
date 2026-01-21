/**
 * Template Selector Component
 * 
 * Displays available templates with live previews
 */

'use client';

import { useState } from 'react';
import { templateRegistry } from '@/lib/templates';
import { TemplateDefinition } from '@/types';
import { motion } from 'framer-motion';

interface TemplateSelectorProps {
  onSelect: (template: TemplateDefinition) => void;
}

export function TemplateSelector({ onSelect }: TemplateSelectorProps) {
  const [selectedId, setSelectedId] = useState<string | null>(null);

  const handleSelect = (template: TemplateDefinition) => {
    setSelectedId(template.id);
    onSelect(template);
  };

  return (
    <div className="p-8">
      <div className="max-w-7xl mx-auto">
        <div className="text-center mb-12">
          <h1 className="text-4xl font-bold mb-4">Choose Your Template</h1>
          <p className="text-xl text-gray-600">
            Start with a professionally designed template, then customize everything
          </p>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-8">
          {Object.values(templateRegistry).map((template) => (
            <motion.div
              key={template.id}
              whileHover={{ scale: 1.05 }}
              whileTap={{ scale: 0.95 }}
              className={`cursor-pointer rounded-xl overflow-hidden shadow-lg transition-all ${
                selectedId === template.id
                  ? 'ring-4 ring-blue-500'
                  : 'hover:shadow-xl'
              }`}
              onClick={() => handleSelect(template)}
            >
              <div className="aspect-video bg-gradient-to-br from-gray-100 to-gray-200 relative overflow-hidden">
                {/* Template preview thumbnail */}
                <div className="absolute inset-0 flex items-center justify-center">
                  <div className="text-6xl">{template.icon}</div>
                </div>
                
                {/* Category badge */}
                <div className="absolute top-3 right-3">
                  <span className="px-3 py-1 bg-white/90 rounded-full text-sm font-medium">
                    {template.category}
                  </span>
                </div>
              </div>

              <div className="p-6 bg-white">
                <h3 className="text-xl font-bold mb-2">{template.name}</h3>
                <p className="text-gray-600 text-sm mb-4">
                  {template.description}
                </p>

                <div className="space-y-2">
                  <div className="flex items-center justify-between text-sm">
                    <span className="text-gray-500">Base Price</span>
                    <span className="font-semibold">${template.basePrice}</span>
                  </div>
                  <div className="flex items-center justify-between text-sm">
                    <span className="text-gray-500">Sections</span>
                    <span className="font-semibold">{template.sections.length}</span>
                  </div>
                </div>

                <button
                  className={`w-full mt-4 py-2 rounded-lg font-medium transition-colors ${
                    selectedId === template.id
                      ? 'bg-blue-600 text-white'
                      : 'bg-gray-100 text-gray-900 hover:bg-gray-200'
                  }`}
                >
                  {selectedId === template.id ? 'Selected' : 'Select Template'}
                </button>
              </div>
            </motion.div>
          ))}
        </div>
      </div>
    </div>
  );
}
