#!/usr/bin/env python3
"""
Complete Comprehensive Analysis Starter
Scrapes → Analyzes → Updates database with tier assignments
Focus: Nairobi, Europe, USA, Australia, Canada
"""

import time
from datetime import datetime
from rich.console import Console
from rich.table import Table
from rich.progress import Progress, SpinnerColumn, BarColumn, TextColumn
from rich.panel import Panel

from multi_api_scraper import MultiAPIScraper
from comprehensive_analyzer import ComprehensiveAnalyzer
from database import BusinessDatabase

console = Console()

# Target cities for analysis
TARGET_CITIES = {
    'Africa': {
        'Nairobi': {'country': 'Kenya'},
        'Lagos': {'country': 'Nigeria'},
        'Accra': {'country': 'Ghana'},
    },
    'Europe': {
        'London': {'country': 'United Kingdom'},
        'Paris': {'country': 'France'},
        'Berlin': {'country': 'Germany'},
        'Amsterdam': {'country': 'Netherlands'},
        'Barcelona': {'country': 'Spain'},
        'Rome': {'country': 'Italy'},
        'Madrid': {'country': 'Spain'},
        'Vienna': {'country': 'Austria'},
        'Prague': {'country': 'Czech Republic'},
        'Dublin': {'country': 'Ireland'},
    },
    'North America': {
        'New York': {'country': 'USA'},
        'Los Angeles': {'country': 'USA'},
        'Chicago': {'country': 'USA'},
        'Houston': {'country': 'USA'},
        'Phoenix': {'country': 'USA'},
        'Philadelphia': {'country': 'USA'},
        'San Antonio': {'country': 'USA'},
        'San Diego': {'country': 'USA'},
        'Dallas': {'country': 'USA'},
        'San Francisco': {'country': 'USA'},
        'Toronto': {'country': 'Canada'},
        'Vancouver': {'country': 'Canada'},
        'Montreal': {'country': 'Canada'},
        'Calgary': {'country': 'Canada'},
    },
    'Oceania': {
        'Sydney': {'country': 'Australia'},
        'Melbourne': {'country': 'Australia'},
        'Brisbane': {'country': 'Australia'},
        'Perth': {'country': 'Australia'},
        'Adelaide': {'country': 'Australia'},
    }
}

TARGET_CATEGORIES = [
    'Professional Services',
    'Accounting & Finance',
    'Advertising & Marketing',
    'Legal Services',
    'Consulting',
    'IT Services',
    'Real Estate',
    'Travel & Tourism',
    'Hotels & Lodging',
    'Restaurants',
    'Retail',
    'Medical Services',
]


class ComprehensiveAnalysisStarter:
    """Complete pipeline: scrape → analyze → store"""
    
    def __init__(self):
        self.scraper = MultiAPIScraper()
        self.analyzer = ComprehensiveAnalyzer()
        self.db = BusinessDatabase()
        
        self.stats = {
            'total_scraped': 0,
            'total_analyzed': 0,
            'tier_distribution': {'TIER_1': 0, 'TIER_2': 0, 'TIER_3': 0, 'TIER_4': 0},
            'regions': {},
            'errors': 0,
        }
    
    def run_complete_analysis(self):
        """Execute complete pipeline"""
        
        console.print(Panel(
            "[bold cyan]🚀 COMPREHENSIVE BUSINESS ANALYSIS STARTER[/bold cyan]\n"
            f"Focus Cities: {sum(len(v) for v in TARGET_CITIES.values())} cities\n"
            f"Categories: {len(TARGET_CATEGORIES)} business types\n"
            f"Start Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
            title="[bold]Initialization[/bold]"
        ))
        
        start_time = time.time()
        
        for region, cities in TARGET_CITIES.items():
            console.print(f"\n[bold cyan]{'=' * 70}[/bold cyan]")
            console.print(f"[bold cyan]REGION: {region}[/bold cyan]")
            console.print(f"[bold cyan]{'=' * 70}[/bold cyan]\n")
            
            self.stats['regions'][region] = {
                'cities': len(cities),
                'businesses_found': 0,
                'businesses_analyzed': 0,
                'tiers': {'TIER_1': 0, 'TIER_2': 0, 'TIER_3': 0, 'TIER_4': 0}
            }
            
            for city, city_info in cities.items():
                self._analyze_city(city, city_info, region)
                time.sleep(0.5)
        
        elapsed = time.time() - start_time
        self._print_final_summary(elapsed)
    
    def _analyze_city(self, city: str, city_info: dict, region: str):
        """Analyze all businesses in a city"""
        
        console.print(f"[cyan]📍 {city}, {city_info['country']}[/cyan]")
        # Search all APIs for businesses across all categories
        businesses = []
        with Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            transient=True
        ) as progress:
            task = progress.add_task("[cyan]Searching APIs...", total=len(TARGET_CATEGORIES))
            
            for category in TARGET_CATEGORIES:
                try:
                    results = self.scraper.search_all_apis(
                        city,
                        category,
                        radius=5000
                    )
                    businesses.extend(results)
                    progress.update(task, advance=1)
                except Exception as e:
                    console.print(f"[red]✗ Error searching {city} for {category}: {e}[/red]")
                    self.stats['errors'] += 1
                    progress.update(task, advance=1)
                    continue
        
        if not businesses:
            console.print(f"[yellow]⚠️  No businesses found in {city}[/yellow]")
            return
        
        console.print(f"[green]✓ Found {len(businesses)} businesses[/green]")
        self.stats['total_scraped'] += len(businesses)
        self.stats['regions'][region]['businesses_found'] += len(businesses)
        
        for business in businesses:
            self.db.add_business(business)
        
        self._analyze_businesses(businesses, city, region)
    
    def _analyze_businesses(self, businesses: list, city: str, region: str):
        """Run comprehensive analysis on businesses"""
        
        analyzed = 0
        
        with Progress(
            BarColumn(),
            TextColumn("[progress.percentage]{task.percentage:>3.0f}%"),
            transient=True
        ) as progress:
            task = progress.add_task(
                f"[cyan]Analyzing {len(businesses)} businesses...",
                total=len(businesses)
            )
            
            for business in businesses:
                website = business.get('website')
                fsq_id = business.get('fsq_id')
                
                if not website:
                    analysis = {
                        'url': None,
                        'has_website': False,
                        'website_status': 'no_website',
                        'tier': 'TIER_1',
                        'total_score': 0,
                        'critical_failures': ['NO_WEBSITE'],
                        'critical_issues': [],
                        'high_priority_issues': [],
                        'medium_priority_issues': [],
                        'low_priority_issues': [],
                        'findings': {'total_critical_failures': 1}
                    }
                    
                    self.db.update_comprehensive_analysis(fsq_id, analysis)
                    tier = 'TIER_1'
                    analyzed += 1
                else:
                    try:
                        if not website.startswith(('http://', 'https://')):
                            website = 'https://' + website
                        
                        analysis = self.analyzer.analyze_comprehensive(website)
                        self.db.update_comprehensive_analysis(fsq_id, analysis)
                        
                        tier = analysis.get('tier', 'UNKNOWN')
                        analyzed += 1
                    except Exception as e:
                        self.stats['errors'] += 1
                        progress.update(task, advance=1)
                        continue
                
                self.stats['tier_distribution'][tier] = self.stats['tier_distribution'].get(tier, 0) + 1
                self.stats['regions'][region]['tiers'][tier] = \
                    self.stats['regions'][region]['tiers'].get(tier, 0) + 1
                
                progress.update(task, advance=1)
        
        self.stats['total_analyzed'] += analyzed
        self.stats['regions'][region]['businesses_analyzed'] += analyzed
        self._print_city_summary(city, analyzed, region)
    
    def _print_city_summary(self, city: str, analyzed: int, region: str):
        """Show summary for a city"""
        
        tiers = self.stats['regions'][region]['tiers']
        
        tier_info = []
        if tiers['TIER_1'] > 0:
            tier_info.append(f"🚨 Tier 1: {tiers['TIER_1']}")
        if tiers['TIER_2'] > 0:
            tier_info.append(f"🔴 Tier 2: {tiers['TIER_2']}")
        if tiers['TIER_3'] > 0:
            tier_info.append(f"🟡 Tier 3: {tiers['TIER_3']}")
        if tiers['TIER_4'] > 0:
            tier_info.append(f"🟢 Tier 4: {tiers['TIER_4']}")
        
        summary = " | ".join(tier_info) if tier_info else "No results"
        console.print(f"  → {summary}\n")
    
    def _print_final_summary(self, elapsed_time: float):
        """Print comprehensive final summary"""
        
        console.print(f"\n[bold cyan]{'=' * 70}[/bold cyan]")
        console.print(f"[bold cyan]ANALYSIS COMPLETE[/bold cyan]")
        console.print(f"[bold cyan]{'=' * 70}[/bold cyan]\n")
        
        console.print("[bold]📊 OVERALL STATISTICS[/bold]")
        
        stats_table = Table(show_header=True, header_style="bold magenta")
        stats_table.add_column("Metric", style="cyan")
        stats_table.add_column("Count", justify="right", style="bold")
        
        stats_table.add_row("Total Businesses Scraped", str(self.stats['total_scraped']))
        stats_table.add_row("Total Businesses Analyzed", str(self.stats['total_analyzed']))
        stats_table.add_row("Total Errors", str(self.stats['errors']))
        stats_table.add_row("Time Elapsed", f"{elapsed_time:.1f}s")
        stats_table.add_row("Avg Time per Business", f"{elapsed_time/max(1, self.stats['total_analyzed']):.2f}s")
        
        console.print(stats_table)
        
        console.print("\n[bold]🎯 TIER DISTRIBUTION[/bold]")
        
        tier_table = Table(show_header=True, header_style="bold magenta")
        tier_table.add_column("Tier", style="cyan")
        tier_table.add_column("Count", justify="right", style="bold")
        tier_table.add_column("Percentage", justify="right")
        
        total = self.stats['total_analyzed']
        
        tier_map = {
            'TIER_1': ('🚨', 'red'),
            'TIER_2': ('🔴', 'red'),
            'TIER_3': ('🟡', 'yellow'),
            'TIER_4': ('🟢', 'green'),
        }
        
        for tier in ['TIER_1', 'TIER_2', 'TIER_3', 'TIER_4']:
            count = self.stats['tier_distribution'].get(tier, 0)
            pct = (count / total * 100) if total > 0 else 0
            emoji, color = tier_map[tier]
            tier_table.add_row(
                f"{emoji} {tier}",
                f"[{color}]{count}[/{color}]",
                f"{pct:.1f}%"
            )
        
        console.print(tier_table)
        
        console.print("\n[bold]🌍 REGIONAL BREAKDOWN[/bold]")
        
        region_table = Table(show_header=True, header_style="bold magenta")
        region_table.add_column("Region", style="cyan")
        region_table.add_column("Cities", justify="right")
        region_table.add_column("Found", justify="right")
        region_table.add_column("Analyzed", justify="right")
        region_table.add_column("Top Tier", style="yellow")
        
        for region, data in self.stats['regions'].items():
            tiers = data['tiers']
            top_tier = max(tiers, key=tiers.get) if any(tiers.values()) else 'N/A'
            top_count = tiers.get(top_tier, 0) if top_tier != 'N/A' else 0
            
            region_table.add_row(
                region,
                str(data['cities']),
                str(data['businesses_found']),
                str(data['businesses_analyzed']),
                f"{top_tier} ({top_count})"
            )
        
        console.print(region_table)
        
        console.print("\n[bold]💡 KEY INSIGHTS[/bold]")
        
        tier_1_count = self.stats['tier_distribution']['TIER_1']
        tier_1_pct = (tier_1_count / total * 100) if total > 0 else 0
        
        console.print(f"  🚨 {tier_1_count} businesses WITHOUT websites ({tier_1_pct:.1f}%)")
        console.print(f"  → These are your HIGHEST VALUE leads!")
        console.print(f"  → Focus outreach: website creation/redesign")
        
        tier_2_count = self.stats['tier_distribution']['TIER_2']
        if tier_2_count > 0:
            console.print(f"\n  🔴 {tier_2_count} businesses with CRITICAL ISSUES")
            console.print(f"  → These need immediate fixes (SSL, mobile, contact)")
        
        console.print("\n[bold]📋 NEXT ACTIONS[/bold]")
        console.print(f"  1. Review database: {self.stats['total_analyzed']} new leads added")
        console.print(f"  2. Query TIER 1 leads: db.get_businesses_by_tier(tier=1)")
        console.print(f"  3. Create outreach templates for each tier")
        console.print(f"  4. Launch tier-based campaigns")
        
        console.print(f"\n[bold green]✓ Analysis Complete[/bold green]")
        console.print(f"[dim]Completed: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}[/dim]\n")


def main():
    """Main entry point"""
    
    try:
        starter = ComprehensiveAnalysisStarter()
        starter.run_complete_analysis()
        
    except KeyboardInterrupt:
        console.print("\n[yellow]⚠️  Analysis interrupted by user[/yellow]")
    except Exception as e:
        console.print(f"[red]✗ Fatal error: {e}[/red]")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()
