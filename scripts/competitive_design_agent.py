"""
Simplified Integration for 4-Agent Pipeline
Wraps existing functionality into unified interface
"""

# Stub functions for compatibility
def search_competitors(niche, limit=5):
    """Search for competitors in niche."""
    return [
        {"name": f"Market Leader {i+1}", "category": niche}
        for i in range(min(limit, 3))
    ]

def generate_design_brief(competitors, tier="Tier 1"):
    """Generate design brief based on tier."""
    return {
        "tier": tier,
        "layout": "hero + features + testimonials + cta",
        "animation": "moderate",
        "features": 4 if "2" in tier else (6 if "3" in tier else 2),
    }

def generate_original_palette(competitors, niche, tier="Tier 1"):
    """Generate color palette for niche."""
    palettes = {
        "restaurant": {
            "primary": "#c85a1f",
            "secondary": "#f4a460",
            "accent": "#8b4513",
            "success": "#10b981",
            "neutral": "#f5f5f5",
        },
        "clinic": {
            "primary": "#0891b2",
            "secondary": "#06b6d4",
            "accent": "#10b981",
            "success": "#10b981",
            "neutral": "#f5f5f5",
        },
        "tech": {
            "primary": "#2563eb",
            "secondary": "#3b82f6",
            "accent": "#10b981",
            "success": "#10b981",
            "neutral": "#f5f5f5",
        },
    }
    
    # Find matching palette
    for key in palettes:
        if key in niche.lower():
            return palettes[key]
    
    return palettes["tech"]

__all__ = [
    "search_competitors",
    "generate_design_brief",
    "generate_original_palette",
]
