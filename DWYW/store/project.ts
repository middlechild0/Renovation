/**
 * Global State Management (Zustand)
 * 
 * Manages user project state, customizations, and real-time preview
 */

import { create } from 'zustand';
import { UserProject, DesignCustomization, ContentCustomization, AIAnalysis, GuardrailViolation, SectionInstance } from '@/types';
import { calculatePricing } from '@/lib/pricing';
import { AIAnalysisEngine, GuardrailsSystem } from '@/lib/ai-assistant';

interface HistoryState {
  past: UserProject[];
  future: UserProject[];
}

interface ProjectState {
  // Current project
  currentProject: UserProject | null;
  
  // Customization state
  design: DesignCustomization | null;
  content: ContentCustomization;
  
  // Analysis state
  analysis: AIAnalysis | null;
  guardrails: GuardrailViolation[];
  
  // UI state
  previewMode: 'desktop' | 'tablet' | 'mobile';
  showingPricing: boolean;
  isAnalyzing: boolean;
  
  // History for undo/redo
  history: HistoryState;
  
  // Actions
  setProject: (project: UserProject) => void;
  updateDesign: (design: Partial<DesignCustomization>) => void;
  updateContent: (sectionId: string, content: any) => void;
  setPreviewMode: (mode: 'desktop' | 'tablet' | 'mobile') => void;
  togglePricing: () => void;
  runAnalysis: () => Promise<void>;
  refreshPricing: () => void;
  
  // Section management
  addSection: (section: SectionInstance, index?: number) => void;
  removeSection: (sectionId: string) => void;
  duplicateSection: (sectionId: string) => void;
  reorderSections: (fromIndex: number, toIndex: number) => void;
  
  // Undo/Redo
  undo: () => void;
  redo: () => void;
  canUndo: () => boolean;
  canRedo: () => boolean;
  
  // Project persistence
  saveProject: () => void;
  loadProject: (projectId: string) => void;
  getAllProjects: () => UserProject[];
  deleteProject: (projectId: string) => void;
}

export const useProjectStore = create<ProjectState>((set, get) => ({
  currentProject: null,
  design: null,
  content: {},
  analysis: null,
  guardrails: [],
  previewMode: 'desktop',
  showingPricing: false,
  isAnalyzing: false,
  history: {
    past: [],
    future: [],
  },

  setProject: (project) => {
    // Save to history before setting
    const state = get();
    if (state.currentProject) {
      set({
        history: {
          past: [...state.history.past, state.currentProject],
          future: [],
        },
      });
    }

    set({
      currentProject: project,
      design: project.customization,
      content: project.content,
      analysis: project.aiAnalysis,
      guardrails: project.guardrails,
    });
  },

  updateDesign: (designUpdate) => {
    const state = get();
    if (!state.design || !state.currentProject) return;

    // Save to history
    set({
      history: {
        past: [...state.history.past, state.currentProject],
        future: [],
      },
    });

    const newDesign = { ...state.design, ...designUpdate };
    
    set({ design: newDesign });
    
    // Update project
    const updatedProject = {
      ...state.currentProject,
      customization: newDesign,
      updatedAt: new Date(),
    };
    
    set({ currentProject: updatedProject });
    
    // Refresh pricing and analysis
    get().refreshPricing();
  },

  updateContent: (sectionId, content) => {
    const state = get();
    
    // Save to history
    if (state.currentProject) {
      set({
        history: {
          past: [...state.history.past, state.currentProject],
          future: [],
        },
      });
    }

    const newContent = {
      ...state.content,
      [sectionId]: content,
    };
    
    set({ content: newContent });
    
    if (state.currentProject) {
      const updatedProject = {
        ...state.currentProject,
        content: newContent,
        updatedAt: new Date(),
      };
      set({ currentProject: updatedProject });
    }
  },

  setPreviewMode: (mode) => {
    set({ previewMode: mode });
  },

  togglePricing: () => {
    set((state) => ({ showingPricing: !state.showingPricing }));
  },

  runAnalysis: async () => {
    const state = get();
    if (!state.design || !state.currentProject) return;

    set({ isAnalyzing: true });

    try {
      // Run AI analysis
      const analysis = await AIAnalysisEngine.performFullAnalysis(
        state.design,
        500, // Content length (would be calculated from actual content)
        10, // Image count
        0, // Video count
        2, // Custom fonts
        true // Has meta tags
      );

      // Check guardrails
      const guardrails = GuardrailsSystem.checkViolations(
        state.design,
        analysis,
        10,
        0
      );

      set({ analysis, guardrails });

      // Update project
      const updatedProject = {
        ...state.currentProject,
        aiAnalysis: analysis,
        guardrails,
        updatedAt: new Date(),
      };

      set({ currentProject: updatedProject });
    } finally {
      set({ isAnalyzing: false });
    }
  },

  refreshPricing: () => {
    const state = get();
    if (!state.currentProject) return;

    const pricing = calculatePricing(
      state.currentProject.template,
      state.currentProject.selectedFeatures,
      10, // Image count
      0, // Video count
      2 // Custom font count
    );

    const updatedProject = {
      ...state.currentProject,
      pricing,
    };

    set({ currentProject: updatedProject });
  },

  // Section management
  addSection: (section, index) => {
    const state = get();
    if (!state.currentProject) return;

    // Save to history
    set({
      history: {
        past: [...state.history.past, state.currentProject],
        future: [],
      },
    });

    const newSections = [...state.currentProject.template.sections];
    if (index !== undefined) {
      newSections.splice(index, 0, section);
    } else {
      newSections.push(section);
    }

    const updatedProject = {
      ...state.currentProject,
      template: {
        ...state.currentProject.template,
        sections: newSections,
      },
      updatedAt: new Date(),
    };

    set({ currentProject: updatedProject });
  },

  removeSection: (sectionId) => {
    const state = get();
    if (!state.currentProject) return;

    // Save to history
    set({
      history: {
        past: [...state.history.past, state.currentProject],
        future: [],
      },
    });

    const newSections = state.currentProject.template.sections.filter(
      (s) => s.id !== sectionId
    );

    const updatedProject = {
      ...state.currentProject,
      template: {
        ...state.currentProject.template,
        sections: newSections,
      },
      updatedAt: new Date(),
    };

    set({ currentProject: updatedProject });
  },

  duplicateSection: (sectionId) => {
    const state = get();
    if (!state.currentProject) return;

    // Save to history
    set({
      history: {
        past: [...state.history.past, state.currentProject],
        future: [],
      },
    });

    const sections = state.currentProject.template.sections;
    const index = sections.findIndex((s) => s.id === sectionId);
    if (index === -1) return;

    const sectionToDuplicate = sections[index];
    const duplicatedSection = {
      ...sectionToDuplicate,
      id: `${sectionToDuplicate.id}-copy-${Date.now()}`,
    };

    const newSections = [
      ...sections.slice(0, index + 1),
      duplicatedSection,
      ...sections.slice(index + 1),
    ];

    const updatedProject = {
      ...state.currentProject,
      template: {
        ...state.currentProject.template,
        sections: newSections,
      },
      updatedAt: new Date(),
    };

    set({ currentProject: updatedProject });
  },

  reorderSections: (fromIndex, toIndex) => {
    const state = get();
    if (!state.currentProject) return;

    // Save to history
    set({
      history: {
        past: [...state.history.past, state.currentProject],
        future: [],
      },
    });

    const sections = [...state.currentProject.template.sections];
    const [removed] = sections.splice(fromIndex, 1);
    sections.splice(toIndex, 0, removed);

    const updatedProject = {
      ...state.currentProject,
      template: {
        ...state.currentProject.template,
        sections,
      },
      updatedAt: new Date(),
    };

    set({ currentProject: updatedProject });
  },

  // Undo/Redo
  undo: () => {
    const state = get();
    const { past, future } = state.history;
    
    if (past.length === 0) return;

    const previous = past[past.length - 1];
    const newPast = past.slice(0, past.length - 1);

    if (state.currentProject) {
      set({
        currentProject: previous,
        design: previous.customization,
        content: previous.content,
        history: {
          past: newPast,
          future: [state.currentProject, ...future],
        },
      });
    }
  },

  redo: () => {
    const state = get();
    const { past, future } = state.history;
    
    if (future.length === 0) return;

    const next = future[0];
    const newFuture = future.slice(1);

    if (state.currentProject) {
      set({
        currentProject: next,
        design: next.customization,
        content: next.content,
        history: {
          past: [...past, state.currentProject],
          future: newFuture,
        },
      });
    }
  },

  canUndo: () => {
    const state = get();
    return state.history.past.length > 0;
  },

  canRedo: () => {
    const state = get();
    return state.history.future.length > 0;
  },

  // Project persistence
  saveProject: () => {
    const state = get();
    if (!state.currentProject) return;

    const projects = get().getAllProjects();
    const existingIndex = projects.findIndex((p) => p.id === state.currentProject!.id);

    if (existingIndex >= 0) {
      projects[existingIndex] = state.currentProject;
    } else {
      projects.push(state.currentProject);
    }

    if (typeof window !== 'undefined') {
      localStorage.setItem('dwyw-projects', JSON.stringify(projects));
    }
  },

  loadProject: (projectId) => {
    const projects = get().getAllProjects();
    const project = projects.find((p) => p.id === projectId);
    
    if (project) {
      get().setProject({
        ...project,
        createdAt: new Date(project.createdAt),
        updatedAt: new Date(project.updatedAt),
      });
    }
  },

  getAllProjects: () => {
    if (typeof window === 'undefined') return [];
    
    const saved = localStorage.getItem('dwyw-projects');
    if (!saved) return [];
    
    try {
      return JSON.parse(saved);
    } catch {
      return [];
    }
  },

  deleteProject: (projectId) => {
    const projects = get().getAllProjects();
    const filtered = projects.filter((p) => p.id !== projectId);
    
    if (typeof window !== 'undefined') {
      localStorage.setItem('dwyw-projects', JSON.stringify(filtered));
    }

    // If deleted current project, clear it
    const state = get();
    if (state.currentProject?.id === projectId) {
      set({
        currentProject: null,
        design: null,
        content: {},
      });
    }
  },
}));
