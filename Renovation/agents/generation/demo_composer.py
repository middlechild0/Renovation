"""
Agent 4: Demo Composer
Composes demo structure based on tier and niche
"""

import sys
from pathlib import Path
from typing import Dict, Any
from datetime import datetime

# Import base agent
sys.path.append(str(Path(__file__).parents[2]))
from agents.base_agent import BaseAgent, AgentType


class DemoComposer(BaseAgent):
    """
    Agent 4: Composes demo structure and components
    
    Input: Lead + tier analysis + design synthesis
    Output: Complete demo composition with sections and components
    """
    
    def __init__(self):
        super().__init__(
            name="Demo Composer",
            agent_type=AgentType.GENERATION
        )
        
        # Tier-based specifications
        self.tier_sections = {
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
        
        # Component mapping per niche
        self.component_map = {
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
    
    def validate_input(self, input_data: Dict[str, Any]) -> bool:
        """Validate lead has tier and niche"""
        return "tier" in input_data and "niche" in input_data
    
    def validate_output(self, output_data: Dict[str, Any]) -> bool:
        """Validate output has structure"""
        return "structure" in output_data and "sections" in output_data["structure"]
    
    def execute(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """Compose demo structure"""
        tier = input_data.get("tier", "Tier 1")
        niche = input_data.get("niche", "general").lower()
        
        # Get tier specification
        tier_spec = self.tier_sections.get(tier, self.tier_sections["Tier 2"])
        
        # Get niche components
        niche_key = next((k for k in self.component_map if k in niche), "tech")
        niche_components = self.component_map.get(niche_key, self.component_map["tech"])
        
        # Get design synthesis if available
        design_synthesis = input_data.get("design_synthesis", {})
        animation_level = design_synthesis.get("animationLevel", "moderate")
        
        return {
            "agent": "AGENT 4: DEMO COMPOSITION",
            "timestamp": datetime.now().isoformat(),
            "tier": tier,
            "targetAudience": input_data.get("business_name"),
            "structure": {
                "pages": 1,
                "sections": tier_spec["sections"],
                "totalComponents": tier_spec["components"],
                "complexity": tier_spec["complexity"],
            },
            "sections": {
                section: {
                    "component": niche_components.get(section, f"{section} section"),
                    "design": f"{section.title()} with {animation_level} animations",
                    "uniqueElement": f"Custom {section} tailored for {niche_key.title()}",
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


# Backward compatibility function
def compose_demo_structure(lead: Dict, tier_analysis: Dict, design_synthesis: Dict) -> Dict:
    """
    Legacy function wrapper for backward compatibility
    """
    # Merge inputs
    merged_input = {**lead}
    merged_input["design_synthesis"] = design_synthesis
    
    agent = DemoComposer()
    result = agent.run(merged_input)
    return result.get("outputs", {})


__all__ = ["DemoComposer", "compose_demo_structure"]
