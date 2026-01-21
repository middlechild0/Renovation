"""
Agent 1: Tier & Presence Analyzer
Analyzes business tier and website presence to identify problems and priorities
"""

import sys
from pathlib import Path
from typing import Dict, Any
from datetime import datetime

# Import base agent
sys.path.append(str(Path(__file__).parents[2]))
from agents.base_agent import BaseAgent, AgentType


class TierPresenceAnalyzer(BaseAgent):
    """
    Agent 1: Analyzes business tier and current website status
    
    Input: Lead with current_website_status, tier, industry
    Output: Tier analysis with problems detected and priority focus
    """
    
    def __init__(self):
        super().__init__(
            name="Tier & Presence Analyzer",
            agent_type=AgentType.ANALYSIS
        )
        
        # Status to problem mapping
        self.status_mapping = {
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
    
    def validate_input(self, input_data: Dict[str, Any]) -> bool:
        """Validate lead has required fields"""
        required = ["business_name", "tier"]
        return all(key in input_data for key in required)
    
    def validate_output(self, output_data: Dict[str, Any]) -> bool:
        """Validate output has required analysis fields"""
        required = ["tier", "problemsDetected", "priorityFocus"]
        return all(key in output_data for key in required)
    
    def execute(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """Analyze tier and website presence"""
        website_status = input_data.get("current_website_status", "none").lower()
        tier = input_data.get("tier", "Tier 1")
        industry = input_data.get("industry", "General")
        
        # Get status analysis
        status_analysis = self.status_mapping.get(
            website_status,
            {
                "problems": ["Website status unclear"],
                "priority": "Full competitive redesign recommended",
            },
        )
        
        return {
            "agent": "AGENT 1: TIER & PRESENCE ANALYSIS",
            "timestamp": datetime.now().isoformat(),
            "businessName": input_data.get("business_name"),
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


# Backward compatibility function
def analyze_tier_and_presence(lead: Dict) -> Dict:
    """
    Legacy function wrapper for backward compatibility
    """
    analyzer = TierPresenceAnalyzer()
    result = analyzer.run(lead)
    return result.get("outputs", {})


__all__ = ["TierPresenceAnalyzer", "analyze_tier_and_presence"]
