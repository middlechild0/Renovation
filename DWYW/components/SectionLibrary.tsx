/**
 * Section Library Component
 * 
 * Browse and add new sections to the design
 */

'use client';

import { useState } from 'react';
import { sectionRegistry } from '@/lib/sections';
import { SectionInstance } from '@/types';
import { X, Plus } from 'lucide-react';
import { motion, AnimatePresence } from 'framer-motion';

interface SectionLibraryProps {
  isOpen: boolean;
  onClose: () => void;
  onAddSection: (section: SectionInstance) => void;
}

export function SectionLibrary({ isOpen, onClose, onAddSection }: SectionLibraryProps) {
  const [selectedCategory, setSelectedCategory] = useState<string | null>(null);

  // Convert sectionRegistry object to array
  const sectionsArray = Object.values(sectionRegistry);

  const categories = Array.from(new Set(sectionsArray.map((s) => s.category)));

  const filteredSections = selectedCategory
    ? sectionsArray.filter((s) => s.category === selectedCategory)
    : sectionsArray;

  const handleAddSection = (section: typeof sectionRegistry[0]) => {
    const instance: SectionInstance = {
      id: `${section.id}-${Date.now()}`,
      type: section.id,
      variant: section.variants[0]?.id || 'default',
      customization: {},
    };
    onAddSection(instance);
    onClose();
  };

  if (!isOpen) return null;

  return (
    <AnimatePresence>
      <div className="fixed inset-0 z-50 flex items-center justify-center">
        {/* Backdrop */}
        <motion.div
          initial={{ opacity: 0 }}
          animate={{ opacity: 1 }}
          exit={{ opacity: 0 }}
          onClick={onClose}
          className="absolute inset-0 bg-black/50"
        />

        {/* Modal */}
        <motion.div
          initial={{ opacity: 0, scale: 0.95 }}
          animate={{ opacity: 1, scale: 1 }}
          exit={{ opacity: 0, scale: 0.95 }}
          className="relative bg-white rounded-xl shadow-2xl w-full max-w-6xl max-h-[80vh] overflow-hidden flex flex-col"
        >
          {/* Header */}
          <div className="flex items-center justify-between p-6 border-b border-gray-200">
            <div>
              <h2 className="text-2xl font-bold">Section Library</h2>
              <p className="text-sm text-gray-600 mt-1">
                Choose a section to add to your design
              </p>
            </div>
            <button
              onClick={onClose}
              className="w-10 h-10 flex items-center justify-center rounded-full hover:bg-gray-100"
            >
              <X size={20} />
            </button>
          </div>

          {/* Category Filters */}
          <div className="p-6 border-b border-gray-200">
            <div className="flex flex-wrap gap-2">
              <button
                onClick={() => setSelectedCategory(null)}
                className={`px-4 py-2 rounded-lg font-medium transition-colors ${
                  selectedCategory === null
                    ? 'bg-blue-600 text-white'
                    : 'bg-gray-100 hover:bg-gray-200'
                }`}
              >
                All Sections
              </button>
              {categories.map((category) => (
                <button
                  key={category}
                  onClick={() => setSelectedCategory(category)}
                  className={`px-4 py-2 rounded-lg font-medium transition-colors capitalize ${
                    selectedCategory === category
                      ? 'bg-blue-600 text-white'
                      : 'bg-gray-100 hover:bg-gray-200'
                  }`}
                >
                  {category}
                </button>
              ))}
            </div>
          </div>

          {/* Sections Grid */}
          <div className="flex-1 overflow-y-auto p-6">
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
              {filteredSections.map((section) => (
                <motion.div
                  key={section.id}
                  layout
                  initial={{ opacity: 0, scale: 0.9 }}
                  animate={{ opacity: 1, scale: 1 }}
                  exit={{ opacity: 0, scale: 0.9 }}
                  className="border border-gray-200 rounded-lg overflow-hidden hover:shadow-lg transition-shadow"
                >
                  {/* Preview */}
                  <div className="aspect-video bg-gradient-to-br from-gray-100 to-gray-200 p-4 flex items-center justify-center">
                    <div className="text-center">
                      <div className="text-4xl mb-2">{section.icon}</div>
                      <p className="text-sm text-gray-600 capitalize">{section.category}</p>
                    </div>
                  </div>

                  {/* Info */}
                  <div className="p-4">
                    <h3 className="font-bold text-lg mb-2">{section.name}</h3>
                    <p className="text-sm text-gray-600 mb-4">{section.description}</p>

                    <div className="flex items-center justify-between">
                      <div className="text-xs text-gray-500">
                        {section.variants.length} variant{section.variants.length !== 1 ? 's' : ''}
                      </div>
                      <button
                        onClick={() => handleAddSection(section)}
                        className="flex items-center space-x-2 px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition-colors"
                      >
                        <Plus size={16} />
                        <span>Add</span>
                      </button>
                    </div>
                  </div>
                </motion.div>
              ))}
            </div>
          </div>
        </motion.div>
      </div>
    </AnimatePresence>
  );
}
