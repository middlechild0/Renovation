"""
Agent 2: Competitive Intelligence Analyzer
Analyzes niche competitors and identifies market opportunities
"""

import sys
from pathlib import Path
from typing import Dict, Any, List
from datetime import datetime

# Import base agent
sys.path.append(str(Path(__file__).parents[2]))
from agents.base_agent import BaseAgent, AgentType

# Import competitive tools
sys.path.append(str(Path(__file__).parents[3] / "scripts"))
from competitive_design_agent import search_competitors


class CompetitiveIntelligenceAgent(BaseAgent):
    """
    Agent 2: Analyzes competitors and extracts niche standards
    
    Input: Lead with niche, industry
    Output: Niche standards, overused patterns, and opportunities
    """
    
    def __init__(self):
        super().__init__(
            name="Competitive Intelligence Analyzer",
            agent_type=AgentType.ANALYSIS
        )
        
        # Niche-specific standards
        self.niche_standards_map = {
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
    
    def validate_input(self, input_data: Dict[str, Any]) -> bool:
        """Validate lead has niche or industry"""
        return "niche" in input_data or "industry" in input_data
    
    def validate_output(self, output_data: Dict[str, Any]) -> bool:
        """Validate output has competitive analysis"""
        required = ["competitorsFound", "marketOpportunities"]
        return all(key in output_data for key in required)
    
    def execute(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """Analyze niche intelligence"""
        niche = input_data.get("niche", "general")
        industry = input_data.get("industry", "General").lower()
        
        # Search for competitors
        competitors = search_competitors(niche, limit=5)
        
        # Get niche standards
        niche_key = next((k for k in self.niche_standards_map if k in niche.lower()), None)
        standards = self.niche_standards_map.get(
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


# Backward compatibility function
def analyze_niche_intelligence(lead: Dict) -> Dict:
    """
    Legacy function wrapper for backward compatibility
    """
    agent = CompetitiveIntelligenceAgent()
    result = agent.run(lead)
    return result.get("outputs", {})


__all__ = ["CompetitiveIntelligenceAgent", "analyze_niche_intelligence"]
