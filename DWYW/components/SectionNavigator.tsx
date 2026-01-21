'use client';

import { useProjectStore } from '@/store/project';
import { motion, AnimatePresence } from 'framer-motion';
import { Menu, ChevronUp } from 'lucide-react';
import { useState } from 'react';

export function SectionNavigator() {
  const { currentProject } = useProjectStore();
  const [isOpen, setIsOpen] = useState(false);

  if (!currentProject) return null;

  const scrollToSection = (sectionId: string) => {
    const element = document.getElementById(`section-${sectionId}`);
    if (element) {
      element.scrollIntoView({ behavior: 'smooth', block: 'center' });
      setIsOpen(false);
    }
  };

  const scrollToTop = () => {
    const container = document.getElementById('preview-container');
    if (container) {
      container.scrollTo({ top: 0, behavior: 'smooth' });
    }
  };

  const getSectionLabel = (type: string, index: number) => {
    const labels: Record<string, string> = {
      hero: 'Hero',
      features: 'Features',
      pricing: 'Pricing',
      testimonials: 'Testimonials',
      cta: 'Call to Action',
      footer: 'Footer',
      about: 'About',
      contact: 'Contact',
      team: 'Team',
      gallery: 'Gallery',
      blog: 'Blog',
      faq: 'FAQ',
      stats: 'Stats',
    };
    return `${labels[type] || type.charAt(0).toUpperCase() + type.slice(1)} ${index + 1}`;
  };

  return (
    <>
      {/* Floating Navigation Button */}
      <div className="fixed bottom-6 right-6 z-40 flex flex-col gap-2">
        {/* Scroll to Top */}
        <motion.button
          whileHover={{ scale: 1.1 }}
          whileTap={{ scale: 0.9 }}
          onClick={scrollToTop}
          className="w-12 h-12 bg-blue-600 text-white rounded-full shadow-lg hover:bg-blue-700 flex items-center justify-center"
          title="Scroll to top"
        >
          <ChevronUp className="w-5 h-5" />
        </motion.button>

        {/* Section Navigator Toggle */}
        <motion.button
          whileHover={{ scale: 1.1 }}
          whileTap={{ scale: 0.9 }}
          onClick={() => setIsOpen(!isOpen)}
          className="w-12 h-12 bg-gray-800 text-white rounded-full shadow-lg hover:bg-gray-900 flex items-center justify-center"
          title="Section navigator"
        >
          <Menu className="w-5 h-5" />
        </motion.button>
      </div>

      {/* Navigation Panel */}
      <AnimatePresence>
        {isOpen && (
          <>
            {/* Backdrop */}
            <motion.div
              initial={{ opacity: 0 }}
              animate={{ opacity: 1 }}
              exit={{ opacity: 0 }}
              onClick={() => setIsOpen(false)}
              className="fixed inset-0 bg-black/20 z-40"
            />

            {/* Panel */}
            <motion.div
              initial={{ opacity: 0, x: 300 }}
              animate={{ opacity: 1, x: 0 }}
              exit={{ opacity: 0, x: 300 }}
              transition={{ type: 'spring', damping: 25 }}
              className="fixed right-20 bottom-6 z-50 bg-white rounded-lg shadow-2xl p-4 w-64"
            >
              <h3 className="text-sm font-semibold text-gray-700 mb-3 px-2">Jump to Section</h3>
              <div className="space-y-1 max-h-96 overflow-y-auto">
                {currentProject.template.sections.map((section, index) => (
                  <button
                    key={section.id}
                    onClick={() => scrollToSection(section.id)}
                    className="w-full text-left px-3 py-2 rounded hover:bg-blue-50 transition-colors text-sm text-gray-700 hover:text-blue-600 flex items-center gap-2"
                  >
                    <div className="w-2 h-2 rounded-full bg-blue-500" />
                    {getSectionLabel(section.type, index)}
                  </button>
                ))}
              </div>
            </motion.div>
          </>
        )}
      </AnimatePresence>
    </>
  );
}
