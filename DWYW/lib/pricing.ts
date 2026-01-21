/**
 * Feature Registry & Pricing System
 * 
 * Defines all available features with transparent pricing and explanations.
 * Each feature has a clear price justification and dependency tracking.
 */

import { Feature, PricingBreakdown, TemplateDefinition } from '@/types';
import { getSectionVariant } from './sections';

// ============================================================================
// FEATURE DEFINITIONS
// ============================================================================

export const featureRegistry: Record<string, Feature> = {
  // Frontend Features
  'online-ordering': {
    id: 'online-ordering',
    name: 'Online Ordering System',
    description: 'Complete online food ordering with cart and checkout',
    category: 'frontend',
    price: 150,
    dependencies: ['shopping-cart', 'checkout', 'payments'],
    priceExplanation: 'Includes custom cart logic, order management UI, and integration with payment processing',
    estimatedImplementationTime: '8-10 hours',
  },
  'shopping-cart': {
    id: 'shopping-cart',
    name: 'Shopping Cart',
    description: 'Add to cart, quantity management, cart persistence',
    category: 'frontend',
    price: 50,
    dependencies: [],
    priceExplanation: 'Custom cart state management, local storage persistence, and cart UI components',
    estimatedImplementationTime: '3-4 hours',
  },
  'checkout': {
    id: 'checkout',
    name: 'Checkout Flow',
    description: 'Multi-step checkout with validation',
    category: 'frontend',
    price: 75,
    dependencies: [],
    priceExplanation: 'Form validation, shipping calculation, order summary, and confirmation screens',
    estimatedImplementationTime: '4-5 hours',
  },
  'product-catalog': {
    id: 'product-catalog',
    name: 'Product Catalog',
    description: 'Product listings with search, filter, and sort',
    category: 'frontend',
    price: 100,
    dependencies: [],
    priceExplanation: 'Dynamic product grid, search functionality, filtering by category/price, and sorting options',
    estimatedImplementationTime: '6-7 hours',
  },
  'portfolio-gallery': {
    id: 'portfolio-gallery',
    name: 'Portfolio Gallery',
    description: 'Image gallery with lightbox and categories',
    category: 'frontend',
    price: 60,
    dependencies: [],
    priceExplanation: 'Optimized image loading, lightbox modal, category filtering, and responsive grid',
    estimatedImplementationTime: '4 hours',
  },
  'contact-form': {
    id: 'contact-form',
    name: 'Contact Form',
    description: 'Contact form with email notifications',
    category: 'frontend',
    price: 30,
    dependencies: [],
    priceExplanation: 'Form validation, spam protection, and email delivery setup',
    estimatedImplementationTime: '2 hours',
  },

  // Backend Features
  'user-authentication': {
    id: 'user-authentication',
    name: 'User Authentication',
    description: 'Sign up, login, password reset, and session management',
    category: 'backend',
    price: 200,
    dependencies: [],
    priceExplanation: 'Secure authentication implementation, session management, password hashing, and email verification',
    estimatedImplementationTime: '10-12 hours',
  },
  'payments': {
    id: 'payments',
    name: 'Payment Processing',
    description: 'Stripe payment integration with webhooks',
    category: 'backend',
    price: 150,
    dependencies: [],
    priceExplanation: 'Stripe API integration, webhook handling, payment confirmation, and refund support',
    estimatedImplementationTime: '8 hours',
  },
  'database': {
    id: 'database',
    name: 'Database Setup',
    description: 'PostgreSQL or MongoDB database with ORM',
    category: 'backend',
    price: 100,
    dependencies: [],
    priceExplanation: 'Database schema design, ORM configuration, migrations, and backup setup',
    estimatedImplementationTime: '5-6 hours',
  },
  'api-integration': {
    id: 'api-integration',
    name: 'RESTful API',
    description: 'Complete REST API with documentation',
    category: 'backend',
    price: 175,
    dependencies: [],
    priceExplanation: 'API endpoint creation, request validation, error handling, and Swagger documentation',
    estimatedImplementationTime: '9 hours',
  },
  'dashboard': {
    id: 'dashboard',
    name: 'User Dashboard',
    description: 'User dashboard with analytics and settings',
    category: 'backend',
    price: 125,
    dependencies: ['user-authentication', 'database'],
    priceExplanation: 'Dashboard data aggregation, analytics calculations, and user settings management',
    estimatedImplementationTime: '7 hours',
  },
  'inventory-management': {
    id: 'inventory-management',
    name: 'Inventory Management',
    description: 'Product inventory tracking and alerts',
    category: 'backend',
    price: 90,
    dependencies: ['database'],
    priceExplanation: 'Stock level tracking, low inventory alerts, and inventory history',
    estimatedImplementationTime: '5 hours',
  },
  'order-tracking': {
    id: 'order-tracking',
    name: 'Order Tracking',
    description: 'Order status updates and tracking',
    category: 'backend',
    price: 80,
    dependencies: ['database'],
    priceExplanation: 'Order status workflow, email notifications, and tracking page implementation',
    estimatedImplementationTime: '4-5 hours',
  },
  'analytics': {
    id: 'analytics',
    name: 'Analytics Dashboard',
    description: 'Traffic and conversion analytics',
    category: 'backend',
    price: 110,
    dependencies: ['database'],
    priceExplanation: 'Event tracking, data aggregation, chart generation, and report exports',
    estimatedImplementationTime: '6 hours',
  },

  // Integration Features
  'email-marketing': {
    id: 'email-marketing',
    name: 'Email Marketing',
    description: 'Newsletter and email campaign integration',
    category: 'integration',
    price: 70,
    dependencies: [],
    priceExplanation: 'Mailchimp/SendGrid integration, list management, and campaign tracking',
    estimatedImplementationTime: '4 hours',
  },
  'seo-optimization': {
    id: 'seo-optimization',
    name: 'SEO Optimization',
    description: 'Meta tags, sitemap, structured data',
    category: 'integration',
    price: 50,
    dependencies: [],
    priceExplanation: 'Meta tag generation, XML sitemap, schema.org markup, and robots.txt',
    estimatedImplementationTime: '3 hours',
  },
  'analytics-tracking': {
    id: 'analytics-tracking',
    name: 'Analytics Tracking',
    description: 'Google Analytics 4 integration',
    category: 'integration',
    price: 30,
    dependencies: [],
    priceExplanation: 'GA4 setup, event tracking, and conversion tracking',
    estimatedImplementationTime: '2 hours',
  },
  'social-integration': {
    id: 'social-integration',
    name: 'Social Media Integration',
    description: 'Social sharing and feeds',
    category: 'integration',
    price: 40,
    dependencies: [],
    priceExplanation: 'Social media sharing buttons, Open Graph tags, and feed widgets',
    estimatedImplementationTime: '2-3 hours',
  },

  // Hosting Features
  'ssl-certificate': {
    id: 'ssl-certificate',
    name: 'SSL Certificate',
    description: 'HTTPS with automatic renewal',
    category: 'hosting',
    price: 20,
    dependencies: [],
    priceExplanation: 'Let\'s Encrypt SSL setup with auto-renewal',
    estimatedImplementationTime: '1 hour',
  },
  'cdn-delivery': {
    id: 'cdn-delivery',
    name: 'CDN Delivery',
    description: 'Global content delivery network',
    category: 'hosting',
    price: 25,
    dependencies: [],
    priceExplanation: 'Cloudflare CDN configuration for faster global access',
    estimatedImplementationTime: '1 hour',
  },
  'backup-system': {
    id: 'backup-system',
    name: 'Automated Backups',
    description: 'Daily automated backups',
    category: 'hosting',
    price: 30,
    dependencies: ['database'],
    priceExplanation: 'Daily database and file backups with 30-day retention',
    estimatedImplementationTime: '2 hours',
  },
  'custom-domain': {
    id: 'custom-domain',
    name: 'Custom Domain',
    description: 'Connect your own domain',
    category: 'hosting',
    price: 15,
    dependencies: [],
    priceExplanation: 'DNS configuration and domain connection',
    estimatedImplementationTime: '30 minutes',
  },

  // Additional Features
  'reservations': {
    id: 'reservations',
    name: 'Table Reservations',
    description: 'Online table booking system',
    category: 'frontend',
    price: 120,
    dependencies: ['database'],
    priceExplanation: 'Booking calendar, availability checking, confirmation emails, and admin management',
    estimatedImplementationTime: '7 hours',
  },
  'menu-management': {
    id: 'menu-management',
    name: 'Menu Management',
    description: 'Dynamic menu with categories',
    category: 'backend',
    price: 80,
    dependencies: ['database'],
    priceExplanation: 'Menu CRUD operations, category management, and pricing updates',
    estimatedImplementationTime: '4-5 hours',
  },
  'team-collaboration': {
    id: 'team-collaboration',
    name: 'Team Collaboration',
    description: 'Multi-user access with roles',
    category: 'backend',
    price: 140,
    dependencies: ['user-authentication', 'database'],
    priceExplanation: 'Role-based access control, team invitations, and permission management',
    estimatedImplementationTime: '8 hours',
  },
  'project-pages': {
    id: 'project-pages',
    name: 'Project Pages',
    description: 'Individual project detail pages',
    category: 'frontend',
    price: 70,
    dependencies: [],
    priceExplanation: 'Dynamic project pages with image galleries and case study content',
    estimatedImplementationTime: '4 hours',
  },
};

// ============================================================================
// PRICING CALCULATOR
// ============================================================================

export function calculatePricing(
  template: TemplateDefinition,
  selectedFeatures: string[],
  imageCount: number = 10,
  videoCount: number = 0,
  customFontCount: number = 0
): PricingBreakdown {
  // Calculate section costs
  const sectionCosts = template.sections.map(section => {
    const variant = getSectionVariant(section.type, section.variantId);
    return {
      name: section.type,
      variant: variant?.name || 'Default',
      price: variant?.price || 0,
    };
  });

  const sectionsTotal = sectionCosts.reduce((sum, s) => sum + s.price, 0);

  // Calculate feature costs with dependencies
  const featureSet = new Set(selectedFeatures);
  const allRequiredFeatures = [...selectedFeatures];

  // Add dependencies
  selectedFeatures.forEach(featureId => {
    const feature = featureRegistry[featureId];
    if (feature) {
      feature.dependencies.forEach(dep => {
        if (!featureSet.has(dep)) {
          featureSet.add(dep);
          allRequiredFeatures.push(dep);
        }
      });
    }
  });

  const featureCosts = allRequiredFeatures.map(featureId => {
    const feature = featureRegistry[featureId];
    return {
      name: feature.name,
      price: feature.price,
      explanation: feature.priceExplanation,
    };
  });

  const featuresTotal = featureCosts.reduce((sum, f) => sum + f.price, 0);

  // Calculate asset costs
  const imageCost = Math.max(0, imageCount - 10) * 2; // First 10 free, $2 per additional
  const videoCost = videoCount * 25; // $25 per video
  const fontCost = Math.max(0, customFontCount - 2) * 10; // First 2 free, $10 per additional

  const assetCosts = {
    images: imageCost,
    videos: videoCost,
    customFonts: fontCost,
  };

  const assetsTotal = imageCost + videoCost + fontCost;

  // Calculate totals
  const subtotal = template.basePrice + sectionsTotal + featuresTotal + assetsTotal;
  const total = subtotal;

  // Generate breakdown explanation
  const breakdown = `
Base Template (${template.name}): $${template.basePrice}
Sections: $${sectionsTotal}
Features: $${featuresTotal}
${imageCount > 10 ? `Additional Images (${imageCount - 10}): $${imageCost}` : ''}
${videoCount > 0 ? `Videos (${videoCount}): $${videoCost}` : ''}
${customFontCount > 2 ? `Custom Fonts (${customFontCount - 2}): $${fontCost}` : ''}
---
Total: $${total}
  `.trim();

  return {
    baseTemplate: template.basePrice,
    sections: sectionCosts,
    features: featureCosts,
    assets: assetCosts,
    subtotal,
    total,
    breakdown,
  };
}

// ============================================================================
// HELPER FUNCTIONS
// ============================================================================

export function getFeatureById(id: string): Feature | undefined {
  return featureRegistry[id];
}

export function getFeaturesByCategory(category: Feature['category']): Feature[] {
  return Object.values(featureRegistry).filter(f => f.category === category);
}

export function getAllFeatures(): Feature[] {
  return Object.values(featureRegistry);
}

export function validateFeatureDependencies(selectedFeatures: string[]): {
  valid: boolean;
  missing: string[];
} {
  const selected = new Set(selectedFeatures);
  const missing: string[] = [];

  selectedFeatures.forEach(featureId => {
    const feature = featureRegistry[featureId];
    if (feature) {
      feature.dependencies.forEach(dep => {
        if (!selected.has(dep)) {
          missing.push(dep);
        }
      });
    }
  });

  return {
    valid: missing.length === 0,
    missing,
  };
}
