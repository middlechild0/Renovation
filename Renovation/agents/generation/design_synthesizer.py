"""
Agent 3: Design Synthesizer
Synthesizes original design system avoiding niche clichés
"""

import sys
from pathlib import Path
from typing import Dict, Any
from datetime import datetime

# Import base agent
sys.path.append(str(Path(__file__).parents[2]))
from agents.base_agent import BaseAgent, AgentType

# Import design tools
sys.path.append(str(Path(__file__).parents[3] / "scripts"))
from competitive_design_agent import search_competitors, generate_original_palette


class DesignSynthesizer(BaseAgent):
    """
    Agent 3: Synthesizes original design that avoids clichés
    
    Input: Lead + competitive intelligence
    Output: Unique design system avoiding overused patterns
    """
    
    def __init__(self):
        super().__init__(
            name="Design Synthesizer",
            agent_type=AgentType.GENERATION
        )
        
        # Design strategies per niche
        self.niche_strategies = {
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
    
    def validate_input(self, input_data: Dict[str, Any]) -> bool:
        """Validate lead has niche and tier"""
        return "niche" in input_data and "tier" in input_data
    
    def validate_output(self, output_data: Dict[str, Any]) -> bool:
        """Validate output has design system"""
        required = ["designStyle", "colorPalette", "animationLevel"]
        return all(key in output_data for key in required)
    
    def execute(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """Synthesize original design"""
        niche = input_data.get("niche", "general").lower()
        tier = input_data.get("tier", "Tier 1")
        
        # Get competitors for palette
        competitors = search_competitors(niche, limit=3)
        
        # Generate palette
        palette = generate_original_palette(competitors, niche, tier)
        
        # Get strategy
        niche_key = next((k for k in self.niche_strategies if k in niche), "tech")
        strategy = self.niche_strategies.get(niche_key, self.niche_strategies["tech"])
        
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


# Backward compatibility function
def synthesize_original_design(lead: Dict, competitor_intel: Dict) -> Dict:
    """
    Legacy function wrapper for backward compatibility
    """
    agent = DesignSynthesizer()
    result = agent.run(lead)
    return result.get("outputs", {})


__all__ = ["DesignSynthesizer", "synthesize_original_design"]
