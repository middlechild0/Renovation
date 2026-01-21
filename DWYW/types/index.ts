/**
 * Core Type Definitions for DWYW Platform
 * 
 * These types define the structure of templates, sections, customizations,
 * and the overall design system architecture.
 */

// ============================================================================
// SECTION SYSTEM
// ============================================================================

export type SectionType =
  | 'hero'
  | 'gallery'
  | 'pricing'
  | 'checkout'
  | 'dashboard'
  | 'features'
  | 'testimonials'
  | 'contact'
  | 'footer'
  | 'navigation'
  | 'about'
  | 'blog'
  | 'team'
  | 'cta';

export interface SectionVariant {
  id: string;
  name: string;
  description: string;
  thumbnail: string;
  price: number; // Base price for this variant
  component: string; // Component reference
}

export interface SectionDefinition {
  type: SectionType;
  name: string;
  description: string;
  variants: SectionVariant[];
  customizationLimits: CustomizationLimits;
  requiredFeatures: string[]; // Features needed for this section
}

// ============================================================================
// CUSTOMIZATION SYSTEM
// ============================================================================

export interface CustomizationLimits {
  colors: {
    min: number;
    max: number;
    allowCustom: boolean;
  };
  fonts: {
    allowed: string[];
    maxFonts: number;
  };
  layout: {
    allowColumnChange: boolean;
    minColumns: number;
    maxColumns: number;
  };
  content: {
    maxTextLength: number;
    allowHTML: boolean;
  };
  animations: {
    allowed: boolean;
    maxDuration: number; // milliseconds
    safeAnimations: string[]; // Only allow certain animation types
  };
  images: {
    maxSize: number; // MB
    allowedFormats: string[];
    maxImages: number;
  };
}

export interface DesignCustomization {
  colors: {
    primary: string;
    secondary: string;
    accent: string;
    background: string;
    text: string;
    [key: string]: string;
  };
  fonts: {
    heading: string;
    body: string;
    accent?: string;
  };
  spacing: {
    scale: number; // 0.5 to 2.0
  };
  borderRadius: {
    scale: number; // 0 to 1 (0 = sharp, 1 = very rounded)
  };
  animations: {
    enabled: boolean;
    duration: number;
    type: 'subtle' | 'moderate' | 'dramatic';
  };
}

export interface ContentCustomization {
  [sectionId: string]: {
    text: {
      [key: string]: string;
    };
    images: {
      [key: string]: string; // URL
    };
    links: {
      [key: string]: string;
    };
  };
}

// ============================================================================
// TEMPLATE SYSTEM
// ============================================================================

export type BusinessCategory = 'restaurant' | 'ecommerce' | 'saas' | 'portfolio' | 'blog' | 'landing';

export interface TemplateSection {
  id: string;
  type: SectionType;
  variantId: string;
  order: number;
  customization?: Partial<DesignCustomization>;
}

export interface TemplateDefinition {
  id: string;
  name: string;
  category: BusinessCategory;
  description: string;
  thumbnail: string;
  icon?: string; // Emoji icon for display
  basePrice: number;
  sections: TemplateSection[];
  defaultCustomization: DesignCustomization;
  features: string[]; // Required features
  seoDefaults: SEOConfiguration;
}

// ============================================================================
// FEATURE & PRICING SYSTEM
// ============================================================================

export interface Feature {
  id: string;
  name: string;
  description: string;
  category: 'frontend' | 'backend' | 'integration' | 'hosting';
  price: number;
  dependencies: string[]; // Other feature IDs required
  priceExplanation: string; // Why this costs what it costs
  estimatedImplementationTime: string;
}

export interface PricingBreakdown {
  baseTemplate: number;
  sections: Array<{
    name: string;
    variant: string;
    price: number;
  }>;
  features: Array<{
    name: string;
    price: number;
    explanation: string;
  }>;
  assets: {
    images: number;
    videos: number;
    customFonts: number;
  };
  subtotal: number;
  total: number;
  breakdown: string;
}

// ============================================================================
// AI ASSISTANT SYSTEM
// ============================================================================

export interface AIAnalysis {
  usability: {
    score: number; // 0-100
    issues: string[];
    suggestions: string[];
  };
  accessibility: {
    score: number; // 0-100
    issues: string[];
    suggestions: string[];
    wcagLevel: 'A' | 'AA' | 'AAA' | 'None';
  };
  seo: {
    score: number; // 0-100
    issues: string[];
    suggestions: string[];
  };
  performance: {
    score: number; // 0-100
    estimatedLoadTime: number; // ms
    issues: string[];
    suggestions: string[];
  };
  mobile: {
    score: number; // 0-100
    issues: string[];
    responsive: boolean;
  };
}

export interface AIDesignModification {
  type: 'color' | 'layout' | 'content' | 'feature' | 'section';
  description: string;
  changes: Record<string, any>;
  affectedSections: string[];
  priceImpact: number;
  warning?: string;
}

// ============================================================================
// BUILD PIPELINE SYSTEM
// ============================================================================

export interface BuildConfiguration {
  projectName: string;
  template: TemplateDefinition;
  customization: DesignCustomization;
  content: ContentCustomization;
  features: string[]; // Selected feature IDs
  authentication: {
    enabled: boolean;
    provider: 'auth0' | 'clerk' | 'supabase' | 'custom';
  };
  payments: {
    enabled: boolean;
    provider: 'stripe' | 'paypal' | 'both';
  };
  database: {
    enabled: boolean;
    provider: 'supabase' | 'mongodb' | 'postgresql' | 'firebase';
  };
  hosting: {
    primary: 'vercel' | 'netlify' | 'custom';
    fallback: 'vercel';
  };
}

export interface GeneratedCode {
  frontend: {
    files: Record<string, string>; // filename -> content
    dependencies: string[];
    buildCommand: string;
  };
  backend: {
    files: Record<string, string>;
    dependencies: string[];
    environment: Record<string, string>;
  };
  configuration: {
    env: Record<string, string>;
    deployment: Record<string, any>;
  };
}

export interface DeploymentResult {
  success: boolean;
  primaryUrl?: string;
  fallbackUrl?: string;
  errors?: string[];
  buildTime: number; // seconds
}

// ============================================================================
// SEO & GUARDRAILS
// ============================================================================

export interface SEOConfiguration {
  title: string;
  description: string;
  keywords: string[];
  ogImage?: string;
  twitterCard?: 'summary' | 'summary_large_image';
  canonicalUrl?: string;
  robots: 'index,follow' | 'noindex,nofollow';
}

export interface GuardrailViolation {
  severity: 'error' | 'warning' | 'info';
  category: 'seo' | 'accessibility' | 'performance' | 'mobile' | 'ux';
  message: string;
  consequence: string;
  suggestion: string;
  canProceed: boolean;
}

// ============================================================================
// USER PROJECT STATE
// ============================================================================

export interface UserProject {
  id: string;
  name: string;
  template: TemplateDefinition;
  customization: DesignCustomization;
  content: ContentCustomization;
  selectedFeatures: string[];
  pricing: PricingBreakdown;
  aiAnalysis?: AIAnalysis;
  guardrails: GuardrailViolation[];
  status: 'draft' | 'building' | 'deployed' | 'failed';
  createdAt: Date;
  updatedAt: Date;
  deploymentUrl?: string;
}

// ============================================================================
// EXPORT ALL TYPES
// ============================================================================

export type * from './index';
