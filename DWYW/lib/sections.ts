/**
 * Section Definitions Registry
 * 
 * Defines all available section types, their variants, and customization limits.
 * This is the foundation of the modular template system.
 */

import { SectionDefinition, SectionType, CustomizationLimits } from '@/types';

// ============================================================================
// CUSTOMIZATION LIMITS (Default safe bounds)
// ============================================================================

const defaultLimits: CustomizationLimits = {
  colors: {
    min: 2,
    max: 10,
    allowCustom: true,
  },
  fonts: {
    allowed: [
      'Inter', 'Roboto', 'Open Sans', 'Lato', 'Montserrat',
      'Poppins', 'Playfair Display', 'Merriweather', 'Raleway',
    ],
    maxFonts: 3,
  },
  layout: {
    allowColumnChange: true,
    minColumns: 1,
    maxColumns: 4,
  },
  content: {
    maxTextLength: 5000,
    allowHTML: false, // For security
  },
  animations: {
    allowed: true,
    maxDuration: 1000, // 1 second max
    safeAnimations: ['fade', 'slide', 'scale', 'rotate'],
  },
  images: {
    maxSize: 5, // MB
    allowedFormats: ['jpg', 'jpeg', 'png', 'webp', 'svg'],
    maxImages: 20,
  },
};

// ============================================================================
// HERO SECTION
// ============================================================================

export const heroSection: SectionDefinition = {
  type: 'hero',
  name: 'Hero Section',
  description: 'Main landing section with headline and call-to-action',
  variants: [
    {
      id: 'full-screen-video',
      name: 'Full Screen Video',
      description: 'Background video with centered content',
      thumbnail: '/sections/hero-video.jpg',
      price: 25,
      component: 'HeroVideoFullScreen',
    },
    {
      id: 'split-content',
      name: 'Split Content',
      description: 'Image on one side, content on other',
      thumbnail: '/sections/hero-split.jpg',
      price: 15,
      component: 'HeroSplitContent',
    },
    {
      id: 'gradient-animated',
      name: 'Animated Gradient',
      description: 'Animated gradient background with particles',
      thumbnail: '/sections/hero-gradient.jpg',
      price: 30,
      component: 'HeroGradientAnimated',
    },
    {
      id: 'fullscreen-minimal',
      name: 'Minimal Fullscreen',
      description: 'Clean, minimal fullscreen design',
      thumbnail: '/sections/hero-minimal.jpg',
      price: 10,
      component: 'HeroMinimal',
    },
  ],
  customizationLimits: defaultLimits,
  requiredFeatures: [],
};

// ============================================================================
// GALLERY SECTION
// ============================================================================

export const gallerySection: SectionDefinition = {
  type: 'gallery',
  name: 'Gallery Section',
  description: 'Display images, products, or portfolio items',
  variants: [
    {
      id: 'masonry-grid',
      name: 'Masonry Grid',
      description: 'Pinterest-style masonry layout',
      thumbnail: '/sections/gallery-masonry.jpg',
      price: 20,
      component: 'GalleryMasonry',
    },
    {
      id: 'product-grid',
      name: 'Product Grid',
      description: 'E-commerce style product grid with hover effects',
      thumbnail: '/sections/gallery-product.jpg',
      price: 25,
      component: 'GalleryProduct',
    },
    {
      id: 'full-width-grid',
      name: 'Full Width Grid',
      description: 'Edge-to-edge image grid',
      thumbnail: '/sections/gallery-fullwidth.jpg',
      price: 15,
      component: 'GalleryFullWidth',
    },
  ],
  customizationLimits: {
    ...defaultLimits,
    images: {
      ...defaultLimits.images,
      maxImages: 50, // Galleries can have more images
    },
  },
  requiredFeatures: [],
};

// ============================================================================
// PRICING SECTION
// ============================================================================

export const pricingSection: SectionDefinition = {
  type: 'pricing',
  name: 'Pricing Section',
  description: 'Display pricing tiers and plans',
  variants: [
    {
      id: 'three-tier',
      name: 'Three Tier',
      description: 'Classic 3-column pricing table',
      thumbnail: '/sections/pricing-three.jpg',
      price: 20,
      component: 'PricingThreeTier',
    },
    {
      id: 'feature-comparison',
      name: 'Feature Comparison',
      description: 'Detailed feature comparison table',
      thumbnail: '/sections/pricing-comparison.jpg',
      price: 30,
      component: 'PricingComparison',
    },
  ],
  customizationLimits: defaultLimits,
  requiredFeatures: [],
};

// ============================================================================
// CHECKOUT SECTION
// ============================================================================

export const checkoutSection: SectionDefinition = {
  type: 'checkout',
  name: 'Checkout Section',
  description: 'E-commerce checkout flow',
  variants: [
    {
      id: 'multi-step',
      name: 'Multi-Step Checkout',
      description: 'Wizard-style checkout process',
      thumbnail: '/sections/checkout-multi.jpg',
      price: 50,
      component: 'CheckoutMultiStep',
    },
    {
      id: 'single-page',
      name: 'Single Page',
      description: 'All-in-one checkout page',
      thumbnail: '/sections/checkout-single.jpg',
      price: 35,
      component: 'CheckoutSinglePage',
    },
  ],
  customizationLimits: defaultLimits,
  requiredFeatures: ['checkout', 'payments'],
};

// ============================================================================
// DASHBOARD SECTION
// ============================================================================

export const dashboardSection: SectionDefinition = {
  type: 'dashboard',
  name: 'Dashboard Section',
  description: 'User dashboard with analytics',
  variants: [
    {
      id: 'analytics-dashboard',
      name: 'Analytics Dashboard',
      description: 'Charts and KPIs dashboard',
      thumbnail: '/sections/dashboard-analytics.jpg',
      price: 75,
      component: 'DashboardAnalytics',
    },
    {
      id: 'admin-panel',
      name: 'Admin Panel',
      description: 'Full admin management panel',
      thumbnail: '/sections/dashboard-admin.jpg',
      price: 100,
      component: 'DashboardAdmin',
    },
  ],
  customizationLimits: defaultLimits,
  requiredFeatures: ['user-authentication', 'dashboard'],
};

// ============================================================================
// FEATURES SECTION
// ============================================================================

export const featuresSection: SectionDefinition = {
  type: 'features',
  name: 'Features Section',
  description: 'Highlight product or service features',
  variants: [
    {
      id: 'grid-icons',
      name: 'Icon Grid',
      description: '3-column grid with icons',
      thumbnail: '/sections/features-grid.jpg',
      price: 15,
      component: 'FeaturesGrid',
    },
    {
      id: 'alternating-blocks',
      name: 'Alternating Blocks',
      description: 'Left-right alternating feature blocks',
      thumbnail: '/sections/features-alternating.jpg',
      price: 20,
      component: 'FeaturesAlternating',
    },
    {
      id: 'cards-hover',
      name: 'Hover Cards',
      description: 'Cards with hover effects',
      thumbnail: '/sections/features-cards.jpg',
      price: 18,
      component: 'FeaturesCards',
    },
  ],
  customizationLimits: defaultLimits,
  requiredFeatures: [],
};

// ============================================================================
// TESTIMONIALS SECTION
// ============================================================================

export const testimonialsSection: SectionDefinition = {
  type: 'testimonials',
  name: 'Testimonials Section',
  description: 'Customer reviews and testimonials',
  variants: [
    {
      id: 'carousel',
      name: 'Carousel',
      description: 'Auto-rotating testimonial carousel',
      thumbnail: '/sections/testimonials-carousel.jpg',
      price: 20,
      component: 'TestimonialsCarousel',
    },
    {
      id: 'logo-wall',
      name: 'Logo Wall',
      description: 'Client logos with quotes',
      thumbnail: '/sections/testimonials-logos.jpg',
      price: 15,
      component: 'TestimonialsLogoWall',
    },
    {
      id: 'minimal-quotes',
      name: 'Minimal Quotes',
      description: 'Simple, elegant quote cards',
      thumbnail: '/sections/testimonials-minimal.jpg',
      price: 12,
      component: 'TestimonialsMinimal',
    },
  ],
  customizationLimits: defaultLimits,
  requiredFeatures: [],
};

// ============================================================================
// NAVIGATION SECTION
// ============================================================================

export const navigationSection: SectionDefinition = {
  type: 'navigation',
  name: 'Navigation',
  description: 'Site navigation menu',
  variants: [
    {
      id: 'sticky-transparent',
      name: 'Sticky Transparent',
      description: 'Transparent nav that sticks on scroll',
      thumbnail: '/sections/nav-sticky.jpg',
      price: 10,
      component: 'NavigationSticky',
    },
    {
      id: 'mega-menu',
      name: 'Mega Menu',
      description: 'Dropdown mega menu with categories',
      thumbnail: '/sections/nav-mega.jpg',
      price: 25,
      component: 'NavigationMega',
    },
    {
      id: 'sticky-cta',
      name: 'Sticky with CTA',
      description: 'Sticky nav with prominent CTA button',
      thumbnail: '/sections/nav-cta.jpg',
      price: 12,
      component: 'NavigationCTA',
    },
    {
      id: 'minimal-sidebar',
      name: 'Minimal Sidebar',
      description: 'Side navigation menu',
      thumbnail: '/sections/nav-sidebar.jpg',
      price: 15,
      component: 'NavigationSidebar',
    },
  ],
  customizationLimits: defaultLimits,
  requiredFeatures: [],
};

// ============================================================================
// FOOTER SECTION
// ============================================================================

export const footerSection: SectionDefinition = {
  type: 'footer',
  name: 'Footer',
  description: 'Site footer with links and info',
  variants: [
    {
      id: 'four-column',
      name: 'Four Column',
      description: 'Classic 4-column footer',
      thumbnail: '/sections/footer-four.jpg',
      price: 10,
      component: 'FooterFourColumn',
    },
    {
      id: 'newsletter-footer',
      name: 'Newsletter Footer',
      description: 'Footer with newsletter signup',
      thumbnail: '/sections/footer-newsletter.jpg',
      price: 15,
      component: 'FooterNewsletter',
    },
    {
      id: 'minimal-links',
      name: 'Minimal Links',
      description: 'Simple footer with links',
      thumbnail: '/sections/footer-minimal.jpg',
      price: 8,
      component: 'FooterMinimal',
    },
    {
      id: 'social-only',
      name: 'Social Only',
      description: 'Social media links only',
      thumbnail: '/sections/footer-social.jpg',
      price: 5,
      component: 'FooterSocial',
    },
  ],
  customizationLimits: defaultLimits,
  requiredFeatures: [],
};

// ============================================================================
// CONTACT SECTION
// ============================================================================

export const contactSection: SectionDefinition = {
  type: 'contact',
  name: 'Contact Section',
  description: 'Contact form and information',
  variants: [
    {
      id: 'map-form',
      name: 'Map with Form',
      description: 'Contact form with embedded map',
      thumbnail: '/sections/contact-map.jpg',
      price: 20,
      component: 'ContactMapForm',
    },
    {
      id: 'simple-form',
      name: 'Simple Form',
      description: 'Clean contact form',
      thumbnail: '/sections/contact-simple.jpg',
      price: 12,
      component: 'ContactSimple',
    },
  ],
  customizationLimits: defaultLimits,
  requiredFeatures: ['contact-form'],
};

// ============================================================================
// CTA SECTION
// ============================================================================

export const ctaSection: SectionDefinition = {
  type: 'cta',
  name: 'Call-to-Action',
  description: 'Call-to-action section',
  variants: [
    {
      id: 'centered-boxed',
      name: 'Centered Boxed',
      description: 'Centered CTA in a box',
      thumbnail: '/sections/cta-centered.jpg',
      price: 10,
      component: 'CTACentered',
    },
  ],
  customizationLimits: defaultLimits,
  requiredFeatures: [],
};

// ============================================================================
// SECTION REGISTRY
// ============================================================================

export const sectionRegistry: Record<SectionType, SectionDefinition> = {
  hero: heroSection,
  gallery: gallerySection,
  pricing: pricingSection,
  checkout: checkoutSection,
  dashboard: dashboardSection,
  features: featuresSection,
  testimonials: testimonialsSection,
  contact: contactSection,
  footer: footerSection,
  navigation: navigationSection,
  about: featuresSection, // Reuse features for about
  blog: gallerySection, // Reuse gallery for blog posts
  team: featuresSection, // Reuse features for team
  cta: ctaSection,
};

export const getSectionDefinition = (type: SectionType): SectionDefinition | undefined => {
  return sectionRegistry[type];
};

export const getSectionVariant = (type: SectionType, variantId: string) => {
  const section = sectionRegistry[type];
  return section?.variants.find(v => v.id === variantId);
};

export const getAllSections = (): SectionDefinition[] => {
  return Object.values(sectionRegistry);
};
