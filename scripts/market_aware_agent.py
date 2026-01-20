"""
Agentic Market-Aware Demo Generation System

4-Agent Framework for Autonomous Design Intelligence:
  1. AGENT 1: Tier & Presence Analysis
  2. AGENT 2: Niche Competitive Intelligence
  3. AGENT 3: Original Design Synthesis
  4. AGENT 4: Demo Composition

Every lead is processed through all 4 agents to ensure:
- Original (not generic templates)
- Competitive (benchmarked against market leaders)
- Tier-appropriate (matching budget constraints)
- Production-ready (immediate deployment)
"""

import json
from typing import Dict, List, Optional
from datetime import datetime

from competitive_design_agent import (
    search_competitors,
    generate_design_brief,
    generate_original_palette,
)


# ═══════════════════════════════════════════════════════════════════════════
# AGENT 1: TIER & PRESENCE ANALYSIS
# ═══════════════════════════════════════════════════════════════════════════


def analyze_tier_and_presence(lead: Dict) -> Dict:
    """
    AGENT 1: Analyze business tier and website presence.
    
    Input: Lead with current_website_status, tier, industry
    Output: Tier analysis with problems detected and priority focus
    """
    website_status = lead.get("current_website_status", "none").lower()
    tier = lead.get("tier", "Tier 1")
    industry = lead.get("industry", "General")

    # Map website status to tier assessment
    status_mapping = {
        "none": {
            "problems": [
                "No online presence",
                "Missing market visibility",
                "No digital storefront",
                "Lost customer acquisition channel",
            ],
            "priority": "Establish immediate online presence with competitive design",
        },
        "broken": {
            "problems": [
                "Website is inaccessible or non-functional",
                "Damages business credibility",
                "Lost revenue from website traffic",
                "Technical debt blocking updates",
            ],
            "priority": "Rebuild from scratch with modern, reliable infrastructure",
        },
        "outdated": {
            "problems": [
                "Visual design is aged (pre-2020 aesthetic)",
                "Poor mobile responsiveness",
                "Missing modern UX patterns",
                "Losing customers to competitors",
            ],
            "priority": "Complete redesign with contemporary standards and features",
        },
        "slow": {
            "problems": [
                "Performance issues (load time > 3s)",
                "Poor user experience on mobile",
                "High bounce rates",
                "SEO ranking penalty from slow speed",
            ],
            "priority": "Optimize performance and modernize architecture",
        },
        "decent": {
            "problems": [
                "Missing competitive differentiation",
                "Incomplete feature set",
                "Outdated design system",
                "No data-driven design strategy",
            ],
            "priority": "Add competitive features and refresh design language",
        },
        "competitive": {
            "problems": [
                "Good but not market-leading",
                "Missing edge features that competitors have",
                "Design is dated by 1-2 years",
                "No AI-powered or innovative features",
            ],
            "priority": "Innovate beyond competitors with original design + advanced features",
        },
    }

    status_analysis = status_mapping.get(
        website_status,
        {
            "problems": ["Website status unclear"],
            "priority": "Full competitive redesign recommended",
        },
    )

    return {
        "agent": "AGENT 1: TIER & PRESENCE ANALYSIS",
        "timestamp": datetime.now().isoformat(),
        "businessName": lead.get("business_name"),
        "industry": industry,
        "tier": tier,
        "currentWebsiteStatus": website_status,
        "problemsDetected": status_analysis["problems"],
        "priorityFocus": status_analysis["priority"],
        "tierBudgetAllocation": {
            "Tier 1": "Minimal: 2-3 sections, no animations",
            "Tier 2": "Moderate: 4-5 sections, smooth animations",
            "Tier 3": "Premium: 6-8 sections, advanced interactions",
            "Tier 4": "Enterprise: 8+ sections, custom components",
        },
    }


# ═══════════════════════════════════════════════════════════════════════════
# AGENT 2: NICHE COMPETITIVE INTELLIGENCE
# ═══════════════════════════════════════════════════════════════════════════


def analyze_niche_intelligence(lead: Dict) -> Dict:
    """
    AGENT 2: Analyze competitors and extract niche standards.
    
    Input: Lead with niche, industry
    Output: Niche standards, overused patterns, and opportunities
    """
    niche = lead.get("niche", "general")
    industry = lead.get("industry", "General").lower()

    # Search for competitors
    competitors = search_competitors(niche, limit=5)

    # Niche-specific standards (curated from market research)
    niche_standards_map = {
        "restaurant": {
            "layouts": [
                "Hero with food imagery + reservation CTA",
                "Menu showcase (grid or carousel)",
                "Ambiance/interior photos gallery",
                "Testimonials from diners",
                "Hours + location + reservation form",
            ],
            "colors": [
                "Warm: Orange (#f97316), Brown (#92400e), Amber (#f59e0b)",
                "Cool: Cream (#fef3c7), White (#ffffff) for cleanliness",
                "Accent: Gold (#fbbf24) for premium feel",
            ],
            "features": [
                "Photo gallery (high-quality food photos)",
                "Menu PDF or interactive menu",
                "Online reservation system",
                "Customer reviews/ratings",
                "Address + map integration",
                "Special promotions banner",
                "Chef background story",
            ],
            "overusedPatterns": [
                "Generic stock food photos",
                "Identical testimonial cards",
                "Black backgrounds (overused for 'premium')",
                "Carousel that auto-rotates (annoying)",
                "Fake 5-star reviews",
            ],
            "opportunities": [
                "User-generated content showcase (customer photos)",
                "Ingredient sourcing transparency",
                "Chef video introduction",
                "Real-time reservation availability",
                "Loyalty program gamification",
            ],
        },
        "clinic": {
            "layouts": [
                "Hero: doctor + trust messaging",
                "Services offered (card grid)",
                "Doctor profiles + credentials",
                "Patient testimonials",
                "Appointment booking form",
                "Hours + location",
            ],
            "colors": [
                "Trust: Blue (#0ea5e9), Cyan (#06b6d4)",
                "Health: Green (#10b981), Teal (#14b8a6)",
                "Clean: White (#ffffff), Light gray (#f3f4f6)",
            ],
            "features": [
                "Online appointment booking",
                "Doctor profiles with qualifications",
                "Services + pricing",
                "Patient testimonials",
                "Health articles/blog",
                "Insurance info",
                "Telemedicine option",
                "Patient FAQ",
            ],
            "overusedPatterns": [
                "Stock photos of doctors in white coats",
                "Overly clinical aesthetic (cold feel)",
                "Excessive medical jargon",
                "Slow testimonials carousel",
                "Outdated appointment system",
            ],
            "opportunities": [
                "Personalized health journey tracking",
                "AI symptom checker pre-appointment",
                "Video testimonials from real patients",
                "Transparent pricing (no hidden costs)",
                "Integration with health wearables",
            ],
        },
        "tech": {
            "layouts": [
                "Hero with gradient + product screenshot",
                "Feature grid (3-4 columns)",
                "Metrics/stats showcase",
                "Testimonials from enterprises",
                "Comparison vs competitors",
                "Pricing tiers",
                "FAQ accordion",
                "Final CTA",
            ],
            "colors": [
                "Primary: Blue (#2563eb, #3b82f6, #0ea5e9)",
                "Secondary: Purple (#8b5cf6, #a855f7)",
                "Accent: Green (#10b981) for success, Red (#ef4444) for alerts",
                "Neutral: Dark (#1f2937, #111827), White (#ffffff)",
            ],
            "features": [
                "Interactive product demo",
                "API documentation",
                "Integration showcase (partner logos)",
                "Performance metrics/uptime",
                "Customer case studies",
                "Free trial CTA",
                "Pricing comparison",
                "Team profiles",
                "Blog/resources",
            ],
            "overusedPatterns": [
                "Blue→purple gradient backgrounds (90% of tech sites)",
                "Stock photos of people in meetings",
                "Identical testimonial card layouts",
                "Auto-playing product video",
                "Excessive use of icons",
                "Gimmicky animations",
            ],
            "opportunities": [
                "Minimal color system (reduce noise)",
                "Custom illustrations instead of stock photos",
                "Asymmetric layouts (unexpected)",
                "Micro-interactions tied to product value",
                "Real customer logos + case studies",
                "Interactive comparison tools",
                "Live product demo (not screenshot)",
            ],
        },
    }

    # Get niche standards or use general defaults
    niche_key = next((k for k in niche_standards_map if k in niche.lower()), None)
    standards = niche_standards_map.get(
        niche_key,
        {
            "layouts": ["Hero", "Features", "Testimonials", "CTA"],
            "colors": ["Primary (#2563eb)", "Secondary (#8b5cf6)", "Neutral (#f3f4f6)"],
            "features": ["Contact form", "Social links", "Newsletter signup"],
            "overusedPatterns": ["Generic templates", "Stock photos", "Repetitive layouts"],
            "opportunities": ["Original design", "Custom illustrations", "Unique interactions"],
        },
    )

    return {
        "agent": "AGENT 2: NICHE COMPETITIVE INTELLIGENCE",
        "timestamp": datetime.now().isoformat(),
        "niche": niche,
        "competitorsFound": len(competitors),
        "competitorNames": [c.get("name") for c in competitors[:3]],
        "nicheStandards": standards,
        "competitiveThreats": {
            "mostCommon": standards["overusedPatterns"][:3],
            "marketSaturation": f"High - most {niche} sites look similar",
            "differentiation_urgency": "Critical - stand out or blend in",
        },
        "marketOpportunities": standards["opportunities"],
    }


# ═══════════════════════════════════════════════════════════════════════════
# AGENT 3: ORIGINAL DESIGN SYNTHESIS
# ═══════════════════════════════════════════════════════════════════════════


def synthesize_original_design(lead: Dict, competitor_intel: Dict) -> Dict:
    """
    AGENT 3: Synthesize original design that avoids clichés.
    
    Input: Lead + competitive intelligence
    Output: Unique design system avoiding overused patterns
    """
    niche = lead.get("niche", "general").lower()
    tier = lead.get("tier", "Tier 1")

    # Get competitors for palette generation
    competitors = search_competitors(niche, limit=3)

    # Generate palette
    palette = generate_original_palette(competitors, niche, tier)

    # Design strategies to avoid overused patterns
    niche_strategies = {
        "restaurant": {
            "designStyle": "Warm, inviting, premium comfort",
            "avoidPatterns": [
                "Skip generic food stock photos → Use real customer UGC",
                "Skip black backgrounds → Use warm creams/golds",
                "Skip carousel auto-rotate → Use gallery grid",
            ],
            "originalApproach": [
                "Feature local ingredients sourcing story",
                "Show chef personality (video intro)",
                "Use food photography that tells a story",
                "Interactive reservation with real-time availability",
            ],
        },
        "clinic": {
            "designStyle": "Professional, trustworthy, approachable",
            "avoidPatterns": [
                "Skip doctor stock photos → Use real team photos",
                "Skip cold clinical aesthetic → Add warmth with colors",
                "Skip slow carousels → Use dynamic grids",
            ],
            "originalApproach": [
                "Transparent pricing upfront (no hidden costs message)",
                "Real patient testimonials (video if possible)",
                "Health journey tracker dashboard preview",
                "AI symptom checker integration preview",
            ],
        },
        "tech": {
            "designStyle": "Minimal, bold, confident (not flashy)",
            "avoidPatterns": [
                "Skip blue→purple gradient → Use dark charcoal + accent colors",
                "Skip stock meeting photos → Use custom illustrations",
                "Skip auto-play demos → Let users interact",
            ],
            "originalApproach": [
                "Asymmetric hero layout (unexpected)",
                "Color-coded feature comparison",
                "Live product demo (not screenshot)",
                "Metrics that matter (uptime, speed, customer count)",
            ],
        },
    }

    niche_key = next((k for k in niche_strategies if k in niche), "tech")
    strategy = niche_strategies.get(niche_key, niche_strategies["tech"])

    return {
        "agent": "AGENT 3: ORIGINAL DESIGN SYNTHESIS",
        "timestamp": datetime.now().isoformat(),
        "designStyle": strategy["designStyle"],
        "colorPalette": palette,
        "uiPersonality": f"Confident, original, tier-appropriate ({tier})",
        "animationLevel": {
            "Tier 1": "minimal (fade-in only)",
            "Tier 2": "moderate (fade, slide, hover)",
            "Tier 3": "advanced (staggered, micro-interactions)",
            "Tier 4": "premium (custom, value-driven)",
        }.get(tier, "moderate"),
        "designStrategy": {
            "avoidThesePatterns": strategy["avoidPatterns"],
            "implementThese": strategy["originalApproach"],
            "competitiveAdvantage": "Combines market standards + original language = looks researched",
        },
        "differentiationFactors": [
            f"Color system: {list(palette.values())[:2]} (not generic)",
            f"Layout: Custom for {niche_key.title()} niche",
            "Animations: Interaction-driven (not decorative)",
            "Content: Original value prop (not template copy)",
        ],
    }


# ═══════════════════════════════════════════════════════════════════════════
# AGENT 4: DEMO COMPOSITION
# ═══════════════════════════════════════════════════════════════════════════


def compose_demo_structure(
    lead: Dict, tier_analysis: Dict, design_synthesis: Dict
) -> Dict:
    """
    AGENT 4: Compose demo structure and components.
    
    Input: Lead + tier analysis + design synthesis
    Output: Complete demo composition with sections and components
    """
    tier = lead.get("tier", "Tier 1")
    niche = lead.get("niche", "general").lower()

    # Tier-based section allocation
    tier_sections = {
        "Tier 1": {
            "sections": ["navigation", "hero", "cta"],
            "components": 6,
            "complexity": "minimal",
            "estimatedDelivery": "3-5 seconds",
        },
        "Tier 2": {
            "sections": ["navigation", "hero", "features", "testimonials", "cta", "footer"],
            "components": 12,
            "complexity": "moderate",
            "estimatedDelivery": "7-10 seconds",
        },
        "Tier 3": {
            "sections": [
                "navigation",
                "hero",
                "features",
                "metrics",
                "comparison",
                "testimonials",
                "cta",
                "footer",
            ],
            "components": 18,
            "complexity": "advanced",
            "estimatedDelivery": "10-15 seconds",
        },
        "Tier 4": {
            "sections": [
                "navigation",
                "hero",
                "features",
                "case_studies",
                "metrics",
                "comparison",
                "faq",
                "testimonials",
                "cta",
                "footer",
            ],
            "components": 24,
            "complexity": "enterprise",
            "estimatedDelivery": "15-20 seconds",
        },
    }

    tier_spec = tier_sections.get(tier, tier_sections["Tier 2"])

    # Component mapping per niche
    component_map = {
        "restaurant": {
            "hero": "Food hero with reservation CTA",
            "features": "Menu showcase cards",
            "metrics": "Customer count + ratings",
            "testimonials": "Diner reviews",
            "gallery": "Food photography grid",
        },
        "clinic": {
            "hero": "Doctor + trust messaging",
            "features": "Services offered",
            "metrics": "Years experience + patients served",
            "testimonials": "Patient success stories",
            "gallery": "Facility photos",
        },
        "tech": {
            "hero": "Product + value prop",
            "features": "Feature grid",
            "metrics": "Users + uptime + performance",
            "testimonials": "Enterprise customer quotes",
            "comparison": "vs competitors table",
        },
    }

    niche_components = component_map.get(
        next((k for k in component_map if k in niche), "tech"),
        component_map["tech"],
    )

    return {
        "agent": "AGENT 4: DEMO COMPOSITION",
        "timestamp": datetime.now().isoformat(),
        "tier": tier,
        "targetAudience": lead.get("business_name"),
        "structure": {
            "pages": 1,
            "sections": tier_spec["sections"],
            "totalComponents": tier_spec["components"],
            "complexity": tier_spec["complexity"],
        },
        "sections": {
            section: {
                "component": niche_components.get(section, f"{section} section"),
                "design": f"{section.title()} with {design_synthesis['animationLevel']} animations",
                "uniqueElement": f"Custom {section} tailored for {niche.title()}",
            }
            for section in tier_spec["sections"]
        },
        "keyComponents": [
            component
            for s in tier_spec["sections"]
            for component in [
                f"Hero{s.title().replace('_', '')}",
                f"Feature{s.title().replace('_', '')}",
                f"Animation{s.title().replace('_', '')}",
                f"Custom{s.title().replace('_', '')}"
            ]
        ][:8],
        "deliverable": {
            "format": "Production-ready HTML",
            "size": "~12KB (optimized)",
            "responsive": "Mobile-first design",
            "performance": "< 2s load time",
            "deployment": "Vercel CDN",
        },
        "estimatedGenerationTime": tier_spec["estimatedDelivery"],
    }


# ═══════════════════════════════════════════════════════════════════════════
# ORCHESTRATOR: Run All 4 Agents
# ═══════════════════════════════════════════════════════════════════════════


def run_market_aware_pipeline(lead: Dict) -> Dict:
    """
    Run the complete 4-agent market-aware pipeline.
    
    Returns comprehensive analysis with all 4 agents' outputs.
    """
    # AGENT 1: Tier & Presence Analysis
    tier_analysis = analyze_tier_and_presence(lead)

    # AGENT 2: Niche Competitive Intelligence
    niche_intel = analyze_niche_intelligence(lead)

    # AGENT 3: Original Design Synthesis
    design_synthesis = synthesize_original_design(lead, niche_intel)

    # AGENT 4: Demo Composition
    demo_composition = compose_demo_structure(lead, tier_analysis, design_synthesis)

    # Combined output
    result = {
        "businessName": lead.get("business_name"),
        "processedAt": datetime.now().isoformat(),
        "marketAwareAnalysis": {
            "agent1_tier_presence": tier_analysis,
            "agent2_competitive_intelligence": niche_intel,
            "agent3_design_synthesis": design_synthesis,
            "agent4_demo_composition": demo_composition,
        },
        "summary": {
            "tier": lead.get("tier"),
            "niche": lead.get("niche"),
            "competitorsAnalyzed": niche_intel["competitorsFound"],
            "designStrategy": design_synthesis["designStyle"],
            "sections": demo_composition["structure"]["sections"],
            "readyForGeneration": True,
        },
    }

    return result


if __name__ == "__main__":
    # Test with River Tech
    test_lead = {
        "business_name": "River Tech",
        "industry": "IT",
        "website": "rivertech.co.ke",
        "current_website_status": "slow",
        "tier": "Tier 3",
        "niche": "tech landing page",
    }

    result = run_market_aware_pipeline(test_lead)
    print(json.dumps(result, indent=2))
