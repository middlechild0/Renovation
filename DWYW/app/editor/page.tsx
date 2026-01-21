/**
 * Main Editor Page
 * 
 * Full design workspace with all editing features
 */

'use client';

import { useState, useEffect } from 'react';
import { useProjectStore } from '@/store/project';
import { templateRegistry } from '@/lib/templates';
import { TemplateSelector } from '@/components/TemplateSelector';
import { CustomizationPanel } from '@/components/CustomizationPanel';
import { LivePreview } from '@/components/LivePreview';
import { AIAssistant } from '@/components/AIAssistant';
import { PricingDisplay } from '@/components/PricingDisplay';
import { SectionLibrary } from '@/components/SectionLibrary';
import { SectionNavigator } from '@/components/SectionNavigator';
import { UserProject, DesignCustomization, FeatureId, TemplateDefinition } from '@/types';
import { motion } from 'framer-motion';
import { Undo2, Redo2, Save, Plus } from 'lucide-react';
import toast, { Toaster } from 'react-hot-toast';

export default function EditorPage() {
  const {
    currentProject,
    setProject,
    setPreviewMode,
    previewMode,
    undo,
    redo,
    canUndo,
    canRedo,
    saveProject,
    addSection,
  } = useProjectStore();
  
  const [showTemplateSelector, setShowTemplateSelector] = useState(!currentProject);
  const [showAIAssistant, setShowAIAssistant] = useState(false);
  const [showCustomization, setShowCustomization] = useState(true);
  const [showSectionLibrary, setShowSectionLibrary] = useState(false);

  useEffect(() => {
    const handleKeyDown = (e: KeyboardEvent) => {
      // Undo/Redo
      if ((e.ctrlKey || e.metaKey) && e.key === 'z' && !e.shiftKey) {
        e.preventDefault();
        if (canUndo()) undo();
      }
      if ((e.ctrlKey || e.metaKey) && (e.shiftKey && e.key === 'z' || e.key === 'y')) {
        e.preventDefault();
        if (canRedo()) redo();
      }
      
      // Save
      if ((e.ctrlKey || e.metaKey) && e.key === 's') {
        e.preventDefault();
        handleSave();
      }

      // Scroll to top/bottom with keyboard
      if (e.key === 'Home' && (e.ctrlKey || e.metaKey)) {
        e.preventDefault();
        const container = document.getElementById('preview-container');
        if (container) {
          container.scrollTo({ top: 0, behavior: 'smooth' });
        }
      }
      if (e.key === 'End' && (e.ctrlKey || e.metaKey)) {
        e.preventDefault();
        const container = document.getElementById('preview-container');
        if (container) {
          container.scrollTo({ top: container.scrollHeight, behavior: 'smooth' });
        }
      }
    };

    window.addEventListener('keydown', handleKeyDown);
    return () => window.removeEventListener('keydown', handleKeyDown);
  }, []);

  const handleTemplateSelect = (template: TemplateDefinition) => {
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

    const project: UserProject = {
      id: Date.now().toString(),
      userId: 'demo-user',
      template,
      customization: defaultDesign,
      selectedFeatures: [] as FeatureId[],
      content: {},
      createdAt: new Date(),
      updatedAt: new Date(),
      pricing: {
        total: template.basePrice,
        breakdown: [],
      },
      aiAnalysis: null,
      guardrails: [],
    };

    setProject(project);
    setShowTemplateSelector(false);
    toast.success('Template selected!');
  };

  const handleSave = () => {
    saveProject();
    toast.success('Project saved!');
  };

  const handleAddSection = (section: any) => {
    addSection(section);
    toast.success('Section added!');
  };

  if (showTemplateSelector) {
    return <TemplateSelector onSelect={handleTemplateSelect} />;
  }

  return (
    <div className="h-screen flex flex-col bg-gray-50">
      <Toaster position="top-right" />

      {/* Top Bar */}
      <div className="h-16 bg-white border-b border-gray-200 flex items-center justify-between px-6">
        <div className="flex items-center space-x-4">
          <h1 className="text-2xl font-bold">DWYW</h1>
          {currentProject && (
            <span className="px-3 py-1 bg-blue-100 text-blue-700 rounded-full text-sm font-medium">
              {currentProject.template.name}
            </span>
          )}
        </div>

        <div className="flex items-center space-x-4">
          {/* Undo/Redo */}
          <div className="flex bg-gray-100 rounded-lg p-1">
            <button
              onClick={undo}
              disabled={!canUndo()}
              className="p-2 rounded hover:bg-gray-200 disabled:opacity-30"
              title="Undo (Ctrl+Z)"
            >
              <Undo2 size={18} />
            </button>
            <button
              onClick={redo}
              disabled={!canRedo()}
              className="p-2 rounded hover:bg-gray-200 disabled:opacity-30"
              title="Redo"
            >
              <Redo2 size={18} />
            </button>
          </div>

          {/* Preview Mode */}
          <div className="flex bg-gray-100 rounded-lg p-1">
            <button
              onClick={() => setPreviewMode('desktop')}
              className={`px-3 py-1 rounded transition-colors ${
                previewMode === 'desktop' ? 'bg-white shadow-sm' : 'hover:bg-gray-200'
              }`}
            >
              🖥️
            </button>
            <button
              onClick={() => setPreviewMode('tablet')}
              className={`px-3 py-1 rounded transition-colors ${
                previewMode === 'tablet' ? 'bg-white shadow-sm' : 'hover:bg-gray-200'
              }`}
            >
              📱
            </button>
            <button
              onClick={() => setPreviewMode('mobile')}
              className={`px-3 py-1 rounded transition-colors ${
                previewMode === 'mobile' ? 'bg-white shadow-sm' : 'hover:bg-gray-200'
              }`}
            >
              📱
            </button>
          </div>

          <button
            onClick={() => setShowSectionLibrary(true)}
            className="flex items-center space-x-2 px-4 py-2 bg-green-600 text-white rounded-lg font-medium"
          >
            <Plus size={18} />
            <span>Add Section</span>
          </button>

          <button
            onClick={() => setShowCustomization(!showCustomization)}
            className="px-4 py-2 bg-gray-100 rounded-lg font-medium"
          >
            {showCustomization ? 'Hide' : 'Show'} Panel
          </button>

          <button
            onClick={() => setShowAIAssistant(!showAIAssistant)}
            className="px-4 py-2 bg-purple-600 text-white rounded-lg font-medium"
          >
            ✨ AI
          </button>

          <button
            onClick={handleSave}
            className="flex items-center space-x-2 px-4 py-2 bg-blue-600 text-white rounded-lg font-medium"
          >
            <Save size={18} />
            <span>Save</span>
          </button>
        </div>
      </div>

      {/* Main Content */}
      <div className="flex-1 flex overflow-hidden">
        {showCustomization && (
          <motion.div
            initial={{ width: 0 }}
            animate={{ width: 320 }}
            className="flex-shrink-0 overflow-hidden"
          >
            <CustomizationPanel />
          </motion.div>
        )}

        <div className="flex-1 overflow-hidden">
          <LivePreview />
        </div>

        {showAIAssistant && (
          <motion.div
            initial={{ width: 0 }}
            animate={{ width: 380 }}
            className="flex-shrink-0 overflow-hidden"
          >
            <AIAssistant />
          </motion.div>
        )}
      </div>

      <PricingDisplay />
      
      <SectionLibrary
        isOpen={showSectionLibrary}
        onClose={() => setShowSectionLibrary(false)}
        onAddSection={handleAddSection}
      />

      {/* Section Navigator - only show when project is loaded */}
      {currentProject && <SectionNavigator />}
    </div>
  );
}
