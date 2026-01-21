/**
 * AI Design Assistant Service
 * 
 * Provides natural language design modifications and continuous analysis
 * of usability, accessibility, SEO, and performance.
 */

import { AIAnalysis, AIDesignModification, DesignCustomization, GuardrailViolation } from '@/types';

// ============================================================================
// AI ANALYSIS ENGINE
// ============================================================================

export class AIAnalysisEngine {
  /**
   * Analyze design for usability issues
   */
  static analyzeUsability(design: DesignCustomization, contentLength: number): {
    score: number;
    issues: string[];
    suggestions: string[];
  } {
    const issues: string[] = [];
    const suggestions: string[] = [];
    let score = 100;

    // Check contrast ratios
    const primaryBrightness = this.getBrightness(design.colors.primary);
    const backgroundBrightness = this.getBrightness(design.colors.background);
    const contrast = Math.abs(primaryBrightness - backgroundBrightness);

    if (contrast < 30) {
      issues.push('Low contrast between primary color and background');
      suggestions.push('Increase color contrast for better readability (aim for 4.5:1 ratio)');
      score -= 15;
    }

    // Check font sizes (implied from design)
    if (design.fonts.body === design.fonts.heading) {
      issues.push('Heading and body fonts are the same');
      suggestions.push('Use different fonts for headings and body text to establish hierarchy');
      score -= 10;
    }

    // Check spacing
    if (design.spacing.scale < 0.8) {
      issues.push('Spacing is too tight, may affect readability');
      suggestions.push('Increase spacing scale to at least 0.8 for better content breathing room');
      score -= 10;
    }

    if (design.spacing.scale > 1.5) {
      issues.push('Excessive spacing may make content feel disconnected');
      suggestions.push('Consider reducing spacing scale for better content cohesion');
      score -= 5;
    }

    // Check animations
    if (design.animations.enabled && design.animations.duration > 800) {
      issues.push('Animation duration is too long, may frustrate users');
      suggestions.push('Reduce animation duration to 300-500ms for snappier feel');
      score -= 10;
    }

    return { score: Math.max(0, score), issues, suggestions };
  }

  /**
   * Analyze accessibility compliance
   */
  static analyzeAccessibility(design: DesignCustomization): {
    score: number;
    issues: string[];
    suggestions: string[];
    wcagLevel: 'A' | 'AA' | 'AAA' | 'None';
  } {
    const issues: string[] = [];
    const suggestions: string[] = [];
    let score = 100;

    // Color contrast check
    const textContrast = this.calculateContrast(design.colors.text, design.colors.background);
    const primaryContrast = this.calculateContrast(design.colors.primary, design.colors.background);

    if (textContrast < 4.5) {
      issues.push('Text color contrast does not meet WCAG AA standards');
      suggestions.push('Adjust text or background color to achieve 4.5:1 contrast ratio');
      score -= 30;
    }

    if (primaryContrast < 3) {
      issues.push('Primary color contrast is too low for interactive elements');
      suggestions.push('Ensure interactive elements have at least 3:1 contrast ratio');
      score -= 20;
    }

    // Animation check
    if (design.animations.enabled && design.animations.type === 'dramatic') {
      issues.push('Dramatic animations may trigger motion sensitivity');
      suggestions.push('Add "prefers-reduced-motion" support or use subtle animations');
      score -= 15;
    }

    // Determine WCAG level
    let wcagLevel: 'A' | 'AA' | 'AAA' | 'None' = 'None';
    if (textContrast >= 7 && primaryContrast >= 4.5) {
      wcagLevel = 'AAA';
    } else if (textContrast >= 4.5 && primaryContrast >= 3) {
      wcagLevel = 'AA';
    } else if (textContrast >= 3 && primaryContrast >= 2) {
      wcagLevel = 'A';
    }

    return { score: Math.max(0, score), issues, suggestions, wcagLevel };
  }

  /**
   * Analyze SEO readiness
   */
  static analyzeSEO(hasMetaTags: boolean, imageCount: number, contentLength: number): {
    score: number;
    issues: string[];
    suggestions: string[];
  } {
    const issues: string[] = [];
    const suggestions: string[] = [];
    let score = 100;

    if (!hasMetaTags) {
      issues.push('Missing meta tags for SEO');
      suggestions.push('Add title, description, and Open Graph meta tags');
      score -= 40;
    }

    if (imageCount > 5) {
      issues.push('Many images detected - ensure all have alt text');
      suggestions.push('Add descriptive alt text to all images for SEO and accessibility');
      score -= 10;
    }

    if (contentLength < 300) {
      issues.push('Content is too short for good SEO');
      suggestions.push('Add at least 300 words of unique content to improve search rankings');
      score -= 20;
    }

    return { score: Math.max(0, score), issues, suggestions };
  }

  /**
   * Analyze performance
   */
  static analyzePerformance(
    imageCount: number,
    videoCount: number,
    animationsEnabled: boolean,
    customFonts: number
  ): {
    score: number;
    estimatedLoadTime: number;
    issues: string[];
    suggestions: string[];
  } {
    const issues: string[] = [];
    const suggestions: string[] = [];
    let score = 100;
    let estimatedLoadTime = 1000; // Base 1 second

    // Image impact
    if (imageCount > 20) {
      issues.push('High number of images may slow page load');
      suggestions.push('Consider lazy loading images and using WebP format');
      score -= 20;
      estimatedLoadTime += imageCount * 50;
    } else {
      estimatedLoadTime += imageCount * 30;
    }

    // Video impact
    if (videoCount > 0) {
      issues.push('Videos significantly impact page load time');
      suggestions.push('Use video streaming services and lazy load video content');
      score -= videoCount * 15;
      estimatedLoadTime += videoCount * 500;
    }

    // Animation impact
    if (animationsEnabled) {
      estimatedLoadTime += 200;
      if (score > 80) score -= 5;
    }

    // Custom fonts impact
    if (customFonts > 3) {
      issues.push('Multiple custom fonts increase load time');
      suggestions.push('Limit to 2-3 font families and use system fonts when possible');
      score -= 10;
      estimatedLoadTime += customFonts * 100;
    }

    return {
      score: Math.max(0, score),
      estimatedLoadTime,
      issues,
      suggestions,
    };
  }

  /**
   * Analyze mobile responsiveness
   */
  static analyzeMobile(design: DesignCustomization): {
    score: number;
    issues: string[];
    responsive: boolean;
  } {
    const issues: string[] = [];
    let score = 100;
    let responsive = true;

    // Check spacing for mobile
    if (design.spacing.scale < 0.7) {
      issues.push('Tight spacing may be problematic on mobile devices');
      score -= 15;
    }

    // Check if animations are too complex
    if (design.animations.enabled && design.animations.type === 'dramatic') {
      issues.push('Complex animations may perform poorly on mobile devices');
      score -= 10;
    }

    // Border radius check
    if (design.borderRadius.scale > 0.8) {
      issues.push('Highly rounded corners may look odd on small mobile screens');
      score -= 5;
    }

    // Overall responsive check
    if (score < 70) {
      responsive = false;
    }

    return { score: Math.max(0, score), issues, responsive };
  }

  /**
   * Comprehensive analysis
   */
  static async performFullAnalysis(
    design: DesignCustomization,
    contentLength: number = 500,
    imageCount: number = 10,
    videoCount: number = 0,
    customFonts: number = 2,
    hasMetaTags: boolean = true
  ): Promise<AIAnalysis> {
    const usability = this.analyzeUsability(design, contentLength);
    const accessibility = this.analyzeAccessibility(design);
    const seo = this.analyzeSEO(hasMetaTags, imageCount, contentLength);
    const performance = this.analyzePerformance(imageCount, videoCount, design.animations.enabled, customFonts);
    const mobile = this.analyzeMobile(design);

    return {
      usability,
      accessibility,
      seo,
      performance,
      mobile,
    };
  }

  /**
   * Parse natural language design request
   */
  static async parseDesignRequest(request: string): Promise<AIDesignModification[]> {
    // This would integrate with OpenAI in production
    // For now, we'll implement rule-based parsing
    
    const modifications: AIDesignModification[] = [];
    const lower = request.toLowerCase();

    // Color changes
    if (lower.includes('color') || lower.includes('blue') || lower.includes('red') || lower.includes('green')) {
      modifications.push({
        type: 'color',
        description: 'Update color scheme',
        changes: {
          colors: this.suggestColors(lower),
        },
        affectedSections: ['all'],
        priceImpact: 0,
      });
    }

    // Layout changes
    if (lower.includes('layout') || lower.includes('grid') || lower.includes('columns')) {
      modifications.push({
        type: 'layout',
        description: 'Modify layout structure',
        changes: {
          layout: 'modified',
        },
        affectedSections: ['content'],
        priceImpact: 25,
        warning: 'Layout changes may affect mobile responsiveness',
      });
    }

    // Content changes
    if (lower.includes('text') || lower.includes('content') || lower.includes('write')) {
      modifications.push({
        type: 'content',
        description: 'Update content',
        changes: {
          content: 'modified',
        },
        affectedSections: ['all'],
        priceImpact: 0,
      });
    }

    return modifications;
  }

  // Helper methods
  private static getBrightness(hex: string): number {
    const rgb = this.hexToRgb(hex);
    if (!rgb) return 128;
    return (rgb.r * 299 + rgb.g * 587 + rgb.b * 114) / 1000;
  }

  private static hexToRgb(hex: string): { r: number; g: number; b: number } | null {
    const result = /^#?([a-f\d]{2})([a-f\d]{2})([a-f\d]{2})$/i.exec(hex);
    return result
      ? {
          r: parseInt(result[1], 16),
          g: parseInt(result[2], 16),
          b: parseInt(result[3], 16),
        }
      : null;
  }

  private static calculateContrast(foreground: string, background: string): number {
    const l1 = this.getLuminance(foreground);
    const l2 = this.getLuminance(background);
    const lighter = Math.max(l1, l2);
    const darker = Math.min(l1, l2);
    return (lighter + 0.05) / (darker + 0.05);
  }

  private static getLuminance(hex: string): number {
    const rgb = this.hexToRgb(hex);
    if (!rgb) return 0;

    const [r, g, b] = [rgb.r, rgb.g, rgb.b].map(val => {
      val = val / 255;
      return val <= 0.03928 ? val / 12.92 : Math.pow((val + 0.055) / 1.055, 2.4);
    });

    return 0.2126 * r + 0.7152 * g + 0.0722 * b;
  }

  private static suggestColors(request: string): any {
    // Simple color suggestions based on keywords
    if (request.includes('blue')) {
      return { primary: '#0284c7', secondary: '#0369a1', accent: '#38bdf8' };
    }
    if (request.includes('red')) {
      return { primary: '#dc2626', secondary: '#991b1b', accent: '#f87171' };
    }
    if (request.includes('green')) {
      return { primary: '#059669', secondary: '#047857', accent: '#34d399' };
    }
    return {};
  }
}

// ============================================================================
// GUARDRAILS SYSTEM
// ============================================================================

export class GuardrailsSystem {
  /**
   * Check for guardrail violations
   */
  static checkViolations(
    design: DesignCustomization,
    analysis: AIAnalysis,
    imageCount: number,
    videoCount: number
  ): GuardrailViolation[] {
    const violations: GuardrailViolation[] = [];

    // SEO Guardrails (enforce)
    if (analysis.seo.score < 60) {
      violations.push({
        severity: 'error',
        category: 'seo',
        message: 'SEO score is too low',
        consequence: 'Your site may not rank well in search engines',
        suggestion: 'Add meta tags, optimize content length, and add alt text to images',
        canProceed: false, // Block deployment
      });
    }

    // Accessibility Guardrails (warn but allow)
    if (analysis.accessibility.score < 70) {
      violations.push({
        severity: 'warning',
        category: 'accessibility',
        message: 'Accessibility standards not met',
        consequence: 'Site may not be usable for people with disabilities',
        suggestion: 'Improve color contrast and add proper ARIA labels',
        canProceed: true, // Warn but allow
      });
    }

    // Mobile Guardrails (enforce)
    if (!analysis.mobile.responsive) {
      violations.push({
        severity: 'error',
        category: 'mobile',
        message: 'Site is not mobile-responsive',
        consequence: 'Over 50% of visitors may have poor experience',
        suggestion: 'Use responsive layouts and test on mobile devices',
        canProceed: false, // Block deployment
      });
    }

    // Performance Guardrails (warn)
    if (analysis.performance.estimatedLoadTime > 5000) {
      violations.push({
        severity: 'warning',
        category: 'performance',
        message: 'Estimated load time exceeds 5 seconds',
        consequence: 'Users may abandon your site before it loads',
        suggestion: 'Optimize images, reduce animations, and enable caching',
        canProceed: true, // Warn but allow
      });
    }

    // Animation Guardrails (warn)
    if (design.animations.enabled && design.animations.duration > 1000) {
      violations.push({
        severity: 'warning',
        category: 'ux',
        message: 'Animation duration is too long',
        consequence: 'Users may find animations distracting or slow',
        suggestion: 'Reduce animation duration to 300-500ms',
        canProceed: true,
      });
    }

    // Media Guardrails (warn)
    if (imageCount > 50) {
      violations.push({
        severity: 'warning',
        category: 'performance',
        message: 'Excessive number of images',
        consequence: 'Page load time will be significantly impacted',
        suggestion: 'Reduce image count or implement lazy loading',
        canProceed: true,
      });
    }

    if (videoCount > 3) {
      violations.push({
        severity: 'warning',
        category: 'performance',
        message: 'Multiple videos detected',
        consequence: 'Videos will significantly slow down page load',
        suggestion: 'Limit videos to 1-2 or use external hosting (YouTube/Vimeo)',
        canProceed: true,
      });
    }

    return violations;
  }

  /**
   * Check if deployment is allowed
   */
  static canDeploy(violations: GuardrailViolation[]): boolean {
    return !violations.some(v => v.severity === 'error' && !v.canProceed);
  }

  /**
   * Get deployment readiness report
   */
  static getDeploymentReadiness(violations: GuardrailViolation[]): {
    ready: boolean;
    blockers: GuardrailViolation[];
    warnings: GuardrailViolation[];
    info: GuardrailViolation[];
  } {
    return {
      ready: this.canDeploy(violations),
      blockers: violations.filter(v => v.severity === 'error' && !v.canProceed),
      warnings: violations.filter(v => v.severity === 'warning'),
      info: violations.filter(v => v.severity === 'info'),
    };
  }
}
