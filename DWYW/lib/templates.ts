/**
 * Template Registry
 * 
 * Defines all available templates for different business categories.
 * Each template is composed of modular sections with safe customization limits.
 */

import { TemplateDefinition, BusinessCategory } from '@/types';

// ============================================================================
// RESTAURANT TEMPLATE
// ============================================================================

export const restaurantTemplate: TemplateDefinition = {
  id: 'restaurant-classic',
  name: 'Classic Restaurant',
  category: 'restaurant',
  description: 'Perfect for cafes, restaurants, and food businesses with online ordering',
  thumbnail: '/templates/restaurant-classic.jpg',
  icon: '🍽️',
  basePrice: 99,
  sections: [
    {
      id: 'nav-1',
      type: 'navigation',
      variantId: 'sticky-transparent',
      order: 0,
    },
    {
      id: 'hero-1',
      type: 'hero',
      variantId: 'full-screen-video',
      order: 1,
    },
    {
      id: 'features-1',
      type: 'features',
      variantId: 'grid-icons',
      order: 2,
    },
    {
      id: 'gallery-1',
      type: 'gallery',
      variantId: 'masonry-grid',
      order: 3,
    },
    {
      id: 'testimonials-1',
      type: 'testimonials',
      variantId: 'carousel',
      order: 4,
    },
    {
      id: 'contact-1',
      type: 'contact',
      variantId: 'map-form',
      order: 5,
    },
    {
      id: 'footer-1',
      type: 'footer',
      variantId: 'four-column',
      order: 6,
    },
  ],
  defaultCustomization: {
    colors: {
      primary: '#c85a1f', // Burnt orange
      secondary: '#8b4513',
      accent: '#f4a460',
      background: '#ffffff',
      text: '#2d2d2d',
    },
    fonts: {
      heading: 'Playfair Display',
      body: 'Open Sans',
    },
    spacing: {
      scale: 1.0,
    },
    borderRadius: {
      scale: 0.3,
    },
    animations: {
      enabled: true,
      duration: 500,
      type: 'moderate',
    },
  },
  features: ['online-ordering', 'reservations', 'menu-management'],
  seoDefaults: {
    title: 'Welcome to Our Restaurant',
    description: 'Experience exceptional dining with fresh ingredients and warm hospitality',
    keywords: ['restaurant', 'dining', 'food', 'cuisine'],
    robots: 'index,follow',
  },
};

// ============================================================================
// E-COMMERCE TEMPLATE
// ============================================================================

export const ecommerceTemplate: TemplateDefinition = {
  id: 'ecommerce-modern',
  name: 'Modern E-commerce',
  category: 'ecommerce',
  description: 'Full-featured online store with product catalog and checkout',
  thumbnail: '/templates/ecommerce-modern.jpg',
  icon: '🛍️',
  basePrice: 199,
  sections: [
    {
      id: 'nav-1',
      type: 'navigation',
      variantId: 'mega-menu',
      order: 0,
    },
    {
      id: 'hero-1',
      type: 'hero',
      variantId: 'split-content',
      order: 1,
    },
    {
      id: 'features-1',
      type: 'features',
      variantId: 'cards-hover',
      order: 2,
    },
    {
      id: 'gallery-1',
      type: 'gallery',
      variantId: 'product-grid',
      order: 3,
    },
    {
      id: 'pricing-1',
      type: 'pricing',
      variantId: 'three-tier',
      order: 4,
    },
    {
      id: 'checkout-1',
      type: 'checkout',
      variantId: 'multi-step',
      order: 5,
    },
    {
      id: 'footer-1',
      type: 'footer',
      variantId: 'newsletter-footer',
      order: 6,
    },
  ],
  defaultCustomization: {
    colors: {
      primary: '#0284c7',
      secondary: '#0369a1',
      accent: '#38bdf8',
      background: '#f8fafc',
      text: '#1e293b',
    },
    fonts: {
      heading: 'Inter',
      body: 'Inter',
    },
    spacing: {
      scale: 1.0,
    },
    borderRadius: {
      scale: 0.5,
    },
    animations: {
      enabled: true,
      duration: 300,
      type: 'subtle',
    },
  },
  features: ['product-catalog', 'shopping-cart', 'checkout', 'inventory-management', 'order-tracking'],
  seoDefaults: {
    title: 'Shop Our Collection',
    description: 'Discover quality products with fast shipping and easy returns',
    keywords: ['shop', 'online store', 'products', 'e-commerce'],
    robots: 'index,follow',
  },
};

// ============================================================================
// SAAS TEMPLATE
// ============================================================================

export const saasTemplate: TemplateDefinition = {
  id: 'saas-professional',
  name: 'Professional SaaS',
  category: 'saas',
  description: 'Software-as-a-Service platform with dashboard and user authentication',
  thumbnail: '/templates/saas-professional.jpg',
  icon: '💼',
  basePrice: 299,
  sections: [
    {
      id: 'nav-1',
      type: 'navigation',
      variantId: 'sticky-cta',
      order: 0,
    },
    {
      id: 'hero-1',
      type: 'hero',
      variantId: 'gradient-animated',
      order: 1,
    },
    {
      id: 'features-1',
      type: 'features',
      variantId: 'alternating-blocks',
      order: 2,
    },
    {
      id: 'dashboard-1',
      type: 'dashboard',
      variantId: 'analytics-dashboard',
      order: 3,
    },
    {
      id: 'pricing-1',
      type: 'pricing',
      variantId: 'feature-comparison',
      order: 4,
    },
    {
      id: 'testimonials-1',
      type: 'testimonials',
      variantId: 'logo-wall',
      order: 5,
    },
    {
      id: 'cta-1',
      type: 'cta',
      variantId: 'centered-boxed',
      order: 6,
    },
    {
      id: 'footer-1',
      type: 'footer',
      variantId: 'minimal-links',
      order: 7,
    },
  ],
  defaultCustomization: {
    colors: {
      primary: '#6366f1',
      secondary: '#4f46e5',
      accent: '#818cf8',
      background: '#ffffff',
      text: '#111827',
    },
    fonts: {
      heading: 'Poppins',
      body: 'Inter',
    },
    spacing: {
      scale: 1.2,
    },
    borderRadius: {
      scale: 0.6,
    },
    animations: {
      enabled: true,
      duration: 400,
      type: 'moderate',
    },
  },
  features: ['user-authentication', 'dashboard', 'api-integration', 'analytics', 'team-collaboration'],
  seoDefaults: {
    title: 'Powerful SaaS Platform',
    description: 'Transform your workflow with our innovative software solution',
    keywords: ['saas', 'software', 'platform', 'business tools'],
    robots: 'index,follow',
  },
};

// ============================================================================
// PORTFOLIO TEMPLATE
// ============================================================================

export const portfolioTemplate: TemplateDefinition = {
  id: 'portfolio-creative',
  name: 'Creative Portfolio',
  category: 'portfolio',
  description: 'Showcase your work with a stunning portfolio site',
  thumbnail: '/templates/portfolio-creative.jpg',  icon: '🎨',  basePrice: 79,
  sections: [
    {
      id: 'nav-1',
      type: 'navigation',
      variantId: 'minimal-sidebar',
      order: 0,
    },
    {
      id: 'hero-1',
      type: 'hero',
      variantId: 'fullscreen-minimal',
      order: 1,
    },
    {
      id: 'about-1',
      type: 'about',
      variantId: 'split-image-text',
      order: 2,
    },
    {
      id: 'gallery-1',
      type: 'gallery',
      variantId: 'full-width-grid',
      order: 3,
    },
    {
      id: 'testimonials-1',
      type: 'testimonials',
      variantId: 'minimal-quotes',
      order: 4,
    },
    {
      id: 'contact-1',
      type: 'contact',
      variantId: 'simple-form',
      order: 5,
    },
    {
      id: 'footer-1',
      type: 'footer',
      variantId: 'social-only',
      order: 6,
    },
  ],
  defaultCustomization: {
    colors: {
      primary: '#000000',
      secondary: '#333333',
      accent: '#ff6b6b',
      background: '#ffffff',
      text: '#1a1a1a',
    },
    fonts: {
      heading: 'Montserrat',
      body: 'Lato',
    },
    spacing: {
      scale: 1.5,
    },
    borderRadius: {
      scale: 0.1,
    },
    animations: {
      enabled: true,
      duration: 600,
      type: 'dramatic',
    },
  },
  features: ['portfolio-gallery', 'project-pages', 'contact-form'],
  seoDefaults: {
    title: 'Creative Portfolio',
    description: 'View my latest work and creative projects',
    keywords: ['portfolio', 'creative', 'design', 'work'],
    robots: 'index,follow',
  },
};

// ============================================================================
// TEMPLATE REGISTRY
// ============================================================================

export const templateRegistry: Record<string, TemplateDefinition> = {
  'restaurant-classic': restaurantTemplate,
  'ecommerce-modern': ecommerceTemplate,
  'saas-professional': saasTemplate,
  'portfolio-creative': portfolioTemplate,
};

export const getTemplatesByCategory = (category: BusinessCategory): TemplateDefinition[] => {
  return Object.values(templateRegistry).filter(t => t.category === category);
};

export const getTemplateById = (id: string): TemplateDefinition | undefined => {
  return templateRegistry[id];
};

export const getAllTemplates = (): TemplateDefinition[] => {
  return Object.values(templateRegistry);
};
