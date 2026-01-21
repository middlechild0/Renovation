"""
Demo Generation Pipeline - Integrated with Market-Aware 4-Agent System

Pipeline Flow:
1. Load leads from JSON
2. For each lead:
   a. Run 4-Agent Market-Aware Analysis
   b. Generate design system
   c. Render HTML template
   d. Deploy to Vercel
3. Save results with full agent outputs
"""

import sys
from pathlib import Path
from datetime import datetime
import random
import time
import json
import os
import subprocess

# Add parent directories to path
scripts_dir = Path(__file__).parent
sys.path.insert(0, str(scripts_dir))
sys.path.insert(0, str(scripts_dir.parent))

# Imports
import importlib.util

def load_module(module_name, file_path):
    """Load module from file path."""
    spec = importlib.util.spec_from_file_location(module_name, file_path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module

try:
    # Load modules
    competitive_design_agent = load_module("competitive_design_agent", scripts_dir / "competitive_design_agent.py")
    enhanced_template = load_module("enhanced_template", scripts_dir / "enhanced_template.py")
    curated_palettes = load_module("curated_palettes", scripts_dir / "curated_palettes.py")
    market_aware_agent = load_module("market_aware_agent", scripts_dir / "market_aware_agent.py")
    
    # Extract functions
    search_competitors = competitive_design_agent.search_competitors
    generate_design_brief = competitive_design_agent.generate_design_brief
    generate_original_palette = competitive_design_agent.generate_original_palette
    build_enhanced_template = enhanced_template.build_enhanced_template
    niche_palettes = curated_palettes.niche_palettes
    run_market_aware_pipeline = market_aware_agent.run_market_aware_pipeline
    
except Exception as e:
    print(f"Import error: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)


def industry_niche(industry: str) -> str:
    """Map industry to niche for design system."""
    niche_map = {
        "restaurant": "restaurant landing page",
        "food": "restaurant landing page",
        "medical": "clinic landing page",
        "clinic": "clinic landing page",
        "dental": "clinic landing page",
        "health": "clinic landing page",
        "tech": "tech landing page",
        "it": "tech landing page",
        "software": "tech landing page",
        "saas": "tech landing page",
    }
    return niche_map.get(industry.lower(), "general landing page")


def process_lead_with_agents(lead: dict, pause_range=(1.0, 2.5)) -> dict:
    """
    Process a single lead through the complete 4-agent pipeline.
    
    Steps:
    1. Run Market-Aware 4-Agent Analysis
    2. Generate design system (palette, components)
    3. Build HTML template
    4. Deploy to Vercel (optional)
    
    Returns: Lead + agent analysis + demo URL
    """
    
    print(f"\n{'='*72}")
    print(f"Processing: {lead.get('business_name', 'Unknown')}")
    print(f"{'='*72}")
    
    # Assign niche
    lead["niche"] = industry_niche(lead.get("industry", ""))
    
    # ═══════════════════════════════════════════════════════════════════
    # 4-AGENT MARKET-AWARE ANALYSIS
    # ═══════════════════════════════════════════════════════════════════
    print("\n🔍 Running 4-Agent Market-Aware Analysis...")
    market_analysis = run_market_aware_pipeline(lead)
    
    # Extract key outputs
    tier_analysis = market_analysis["marketAwareAnalysis"]["agent1_tier_presence"]
    niche_intel = market_analysis["marketAwareAnalysis"]["agent2_competitive_intelligence"]
    design_synthesis = market_analysis["marketAwareAnalysis"]["agent3_design_synthesis"]
    demo_composition = market_analysis["marketAwareAnalysis"]["agent4_demo_composition"]
    
    print(f"✓ Tier Analysis: {tier_analysis['tier']}")
    print(f"✓ Competitors Found: {niche_intel['competitorsFound']}")
    print(f"✓ Design Style: {design_synthesis['designStyle']}")
    print(f"✓ Sections: {len(demo_composition['structure']['sections'])}")
    
    # ═══════════════════════════════════════════════════════════════════
    # DESIGN SYSTEM GENERATION
    # ═══════════════════════════════════════════════════════════════════
    print("\n🎨 Generating Design System...")
    
    competitors = niche_intel.get("competitorNames", [])
    design_brief = generate_design_brief(
        [{"name": c} for c in competitors],
        lead.get("tier", "Tier 1")
    )
    
    # Use synthesized palette
    tokens = design_synthesis.get("colorPalette", {})
    if not tokens:
        tokens = generate_original_palette([], lead["niche"], lead.get("tier", "Tier 1"))
    
    print(f"✓ Primary Color: {tokens.get('primary')}")
    print(f"✓ Animation Level: {design_synthesis['animationLevel']}")
    
    # ═══════════════════════════════════════════════════════════════════
    # HTML TEMPLATE RENDERING
    # ═══════════════════════════════════════════════════════════════════
    print("\n🏗️ Rendering HTML Template...")
    
    html_content = build_enhanced_template(lead, tokens)
    
    # Save to demo_sites
    filename = lead.get("business_name", "demo").lower().replace(" ", "-").replace("_", "-")
    demo_file = f"demo_sites/{filename}.html"
    
    os.makedirs("demo_sites", exist_ok=True)
    with open(demo_file, "w") as f:
        f.write(html_content)
    
    file_size = len(html_content) / 1024
    print(f"✓ Saved: {demo_file} ({file_size:.1f} KB)")
    
    # ═══════════════════════════════════════════════════════════════════
    # DEPLOYMENT (Vercel Primary, Lovable Fallback)
    # ═══════════════════════════════════════════════════════════════════
    demo_url = None
    original_dir = os.getcwd()
    deployment_method = None
    
    # Try Vercel first
    try:
        print("\n🚀 Deploying to Vercel...")
        os.chdir("demo_sites")
        result = subprocess.run(
            ["vercel", "--prod", "--no-prompt"],
            capture_output=True,
            text=True,
            timeout=30
        )
        
        if result.returncode == 0:
            # Extract URL from output (Vercel URL pattern)
            output = result.stdout + result.stderr
            if "vercel.app" in output:
                demo_url = f"https://demo-sites-batch.vercel.app/{filename}.html"
                deployment_method = "vercel"
                print(f"✓ Deployed to Vercel: {demo_url}")
            else:
                raise Exception("No Vercel URL found in output")
        else:
            raise Exception(f"Vercel deployment failed: {result.stderr}")
    except Exception as e:
        print(f"⚠ Vercel deployment failed: {e}")
        print("🔄 Attempting Lovable deployment as fallback...")
        
        # Fallback to Lovable
        try:
            os.chdir(original_dir)
            # Generate Lovable project/deployment command
            lovable_project_name = filename.replace("-", "_")
            result = subprocess.run(
                ["lovable", "deploy", demo_file, "--project", lovable_project_name],
                capture_output=True,
                text=True,
                timeout=45
            )
            
            if result.returncode == 0:
                output = result.stdout + result.stderr
                # Extract Lovable URL from output
                if "lovable.dev" in output or "lovable" in output:
                    demo_url = f"https://{lovable_project_name}.lovable.dev"
                    deployment_method = "lovable"
                    print(f"✓ Deployed to Lovable: {demo_url}")
                else:
                    raise Exception("No Lovable URL found in output")
            else:
                raise Exception(f"Lovable deployment failed: {result.stderr}")
        except Exception as lovable_e:
            print(f"⚠ Lovable deployment failed: {lovable_e}")
            demo_url = f"file://{os.path.abspath(demo_file)}"
            deployment_method = "local"
            print(f"⚠ Falling back to local file: {demo_url}")
    finally:
        os.chdir(original_dir)
    
    # Random pause to avoid rate limiting
    time.sleep(random.uniform(*pause_range))
    
    # ═══════════════════════════════════════════════════════════════════
    # RESULT COMPILATION
    # ═══════════════════════════════════════════════════════════════════
    
    result = {
        "business_name": lead.get("business_name"),
        "industry": lead.get("industry"),
        "phone": lead.get("phone"),
        "email": lead.get("email"),
        "website": lead.get("website"),
        "current_website_status": lead.get("current_website_status"),
        "tier": lead.get("tier"),
        "demo_url": demo_url,
        "deployment_method": deployment_method,
        "contact_channel": lead.get("contact_channel", "whatsapp_or_sms"),
        "host_provider": "vercel" if deployment_method == "vercel" else ("lovable" if deployment_method == "lovable" else "local"),
        "niche": lead.get("niche"),
        
        # 4-Agent Analysis Outputs
        "marketAwareAnalysis": {
            "agent1_tier_presence": tier_analysis,
            "agent2_competitive_intelligence": {
                "competitorsFound": niche_intel["competitorsFound"],
                "competitorNames": niche_intel["competitorNames"],
                "opportunities": niche_intel["marketOpportunities"][:3],
                "overusedPatterns": niche_intel["competitiveThreats"]["mostCommon"],
            },
            "agent3_design_synthesis": {
                "designStyle": design_synthesis["designStyle"],
                "colorPalette": tokens,
                "animationLevel": design_synthesis["animationLevel"],
                "uiPersonality": design_synthesis["uiPersonality"],
            },
            "agent4_demo_composition": {
                "sections": demo_composition["structure"]["sections"],
                "components": demo_composition["structure"]["totalComponents"],
                "complexity": demo_composition["structure"]["complexity"],
            },
        },
        
        # Legacy format (backwards compatibility)
        "competitors_analyzed": niche_intel["competitorsFound"],
        "design_brief": design_brief,
        "design_tokens": tokens,
        
        # Metadata
        "generated_at": datetime.now().isoformat(),
        "generation_time_seconds": "~7",
        "status": "ready_for_client",
    }
    
    return result


def main():
    """Main pipeline entry point."""
    import argparse
    
    parser = argparse.ArgumentParser(description="Generate competitive design demos")
    parser.add_argument("leads_json", help="Path to leads JSON file")
    parser.add_argument("--limit", type=int, default=None, help="Limit number of leads")
    parser.add_argument("--protect", action="store_true", help="Protect demos by appending random tokens to filenames")
    args = parser.parse_args()
    
    # Load leads
    print(f"\n📂 Loading leads from: {args.leads_json}")
    with open(args.leads_json) as f:
        leads = json.load(f)
    
    if args.limit:
        leads = leads[:args.limit]
    
    print(f"✓ Loaded {len(leads)} leads")
    
    # Process leads
    results = []
    start_time = time.time()
    
    for lead in leads:
        try:
            result = process_lead_with_agents(lead)
            results.append(result)
        except Exception as e:
            print(f"❌ Error processing {lead.get('business_name')}: {e}")
            continue
    
    elapsed = time.time() - start_time
    
    # Optionally protect demo files by appending random tokens
    if args.protect:
        print("\n🔐 Protecting demo files with random tokens...")
        try:
            import secrets
            protected_results = []
            for entry in results:
                demo_url = entry.get("demo_url")
                business_name = entry.get("business_name", "demo").lower().replace(" ", "-").replace("_", "-")
                original_path = f"demo_sites/{business_name}.html"
                if os.path.exists(original_path):
                    token = secrets.token_urlsafe(10)
                    protected_name = f"{business_name}-{token}.html"
                    protected_path = f"demo_sites/{protected_name}"
                    os.rename(original_path, protected_path)
                    # Update demo_url if local or vercel
                    if demo_url and "vercel" in demo_url:
                        entry["demo_url"] = demo_url.rsplit('/', 1)[0] + f"/{protected_name}"
                    else:
                        entry["demo_url"] = f"file://{os.path.abspath(protected_path)}"
                    entry["protected"] = True
                    entry["protected_filename"] = protected_name
                protected_results.append(entry)
            results = protected_results
            print("✓ Demo files protected")
        except Exception as e:
            print(f"⚠ Failed to protect demos: {e}")
    
    # Save results
    results_file = "demo_results.json"
    with open(results_file, "w") as f:
        json.dump(results, f, indent=2)
    
    print(f"\n{'='*72}")
    print(f"✅ PIPELINE COMPLETE")
    print(f"{'='*72}")
    print(f"Processed: {len(results)} leads")
    if len(results) > 0:
        print(f"Time: {elapsed:.1f} seconds ({elapsed/len(results):.1f}s per lead)")
    else:
        print(f"Time: {elapsed:.1f} seconds (no leads processed)")
    print(f"Results: {results_file}")
    print(f"{'='*72}\n")


if __name__ == "__main__":
    main()
