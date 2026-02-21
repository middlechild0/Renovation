
# app.py
import sys
import time
import sqlite3
from datetime import datetime, timedelta
import json
from typing import List, Dict
import schedule
from rich.console import Console
from rich.table import Table
from rich.progress import Progress, SpinnerColumn, TextColumn
import threading

from config import config
from database import BusinessDatabase
from multi_api_scraper import MultiAPIScraper
from analyzer import WebsiteAnalyzer
from email_finder import EmailFinder
from export import DataExporter

console = Console()

class BusinessFinderApp:
    def __init__(self):
        self.db = BusinessDatabase()
        self.scraper = MultiAPIScraper()  # Use multi-API scraper with fallback
        self.analyzer = WebsiteAnalyzer()
        self.email_finder = EmailFinder(config.HUNTER_API_KEY)
        self.exporter = DataExporter()
        
        self.is_running = False
        
    def run_interactive(self):
        """Run interactive CLI application"""
        console.print("[bold cyan]🤖 Business Finder Pro[/bold cyan]")
        console.print("[dim]Find businesses with outdated websites worldwide[/dim]\n")
        
        while True:
            console.print("\n[bold]Main Menu:[/bold]")
            console.print("1. 📍 Search new location")
            console.print("2. 🔍 Analyze websites")
            console.print("3. 📊 View statistics")
            console.print("4. 📤 Export leads")
            console.print("5. ⚙️  Configure settings")
            console.print("6. 🔄 Start automated scanning")
            console.print("7. 🚪 Exit")
            
            choice = console.input("\nEnter your choice (1-7): ").strip()
            
            if choice == "1":
                self.search_location()
            elif choice == "2":
                self.analyze_websites()
            elif choice == "3":
                self.show_statistics()
            elif choice == "4":
                self.export_data()
            elif choice == "5":
                self.configure_settings()
            elif choice == "6":
                self.start_automated_scan()
            elif choice == "7":
                console.print("[yellow]Goodbye![/yellow]")
                break
            else:
                console.print("[red]Invalid choice![/red]")
    
    def search_location(self):
        """Search for businesses in a new location using all available APIs"""
        console.print("\n[bold]📍 Location Search[/bold]")
        
        city = console.input("Enter city name: ").strip()
        if not city:
            console.print("[red]City name required![/red]")
            return
        
        console.print("\n[bold]Available Categories:[/bold]")
        categories = {
            "1": ("Coffee Shops", "coffee"),
            "2": ("Restaurants", "restaurant"),
            "3": ("Doctors", "doctor"),
            "4": ("Lawyers", "lawyer"),
            "5": ("Dentists", "dentist"),
            "6": ("Real Estate", "real_estate"),
            "7": ("Accountants", "accountant"),
            "8": ("All Categories", "all")
        }
        
        for key, (name, _) in categories.items():
            console.print(f"{key}. {name}")
        
        cat_choice = console.input("\nSelect category (1-8): ").strip()
        if cat_choice not in categories:
            console.print("[red]Invalid choice![/red]")
            return
        
        _, category = categories[cat_choice]
        
        radius = console.input("Search radius in meters (default: 5000): ").strip()
        radius = int(radius) if radius.isdigit() else 5000
        
        console.print(f"\n[yellow]Searching using all available APIs for {category} in {city}...[/yellow]")
        console.print(f"[dim]This searches TomTom, Foursquare, and Yelp to maximize results[/dim]\n")
        
        businesses = []
        
        if category == "all":
            # Search all categories
            all_categories = ["coffee", "restaurant", "doctor", "lawyer", "dentist", "real_estate", "accountant"]
            for cat in all_categories:
                console.print(f"\n[bold cyan]Searching {cat.upper()}...[/bold cyan]")
                results = self.scraper.search_all_apis(city, cat, radius)
                businesses.extend(results)
                console.print(f"[green]✓ Found {len(results)} from all APIs[/green]")
                time.sleep(1)  # Rate limiting
        else:
            businesses = self.scraper.search_all_apis(city, category, radius)
        
        if not businesses:
            console.print("\n[red]❌ No businesses found![/red]")
            console.print("[yellow]💡 Tips:[/yellow]")
            console.print("  • Try a different city from the supported list")
            console.print("  • Configure more APIs (use option 11 in quick_start.py)")
            console.print("  • Increase the search radius")
            return
        
        # Save to database
        saved = 0
        with console.status("[cyan]Saving to database...") as status:
            for business in businesses:
                if self.db.add_business(business):
                    saved += 1
        
        console.print(f"\n[green]✓ Found {len(businesses)} total, saved {saved} unique businesses[/green]")
        
        # Ask to analyze websites
        if console.input("\nAnalyze websites now? (y/n): ").lower() == 'y':
            self.analyze_websites(businesses_list=businesses)
    
    def analyze_websites(self, businesses_list: List[Dict] = None, batch_size: int = 10):
        """Analyze websites for businesses without analysis"""
        console.print("\n[bold]🔍 Website Analysis[/bold]")
        
        if businesses_list:
            # Use provided list of businesses
            businesses_to_analyze = businesses_list
        else:
            # Query from database
            conn = self.db.conn if hasattr(self.db, 'conn') else None
            if not conn:
                conn = sqlite3.connect(config.DATABASE_PATH)
            
            cursor = conn.cursor()
            cursor.execute('''
                SELECT fsq_id, name, website 
                FROM businesses 
                WHERE website IS NOT NULL 
                AND website != '' 
                AND last_analyzed IS NULL
                LIMIT ?
            ''', (batch_size,))
            
            businesses_to_analyze = cursor.fetchall()
            conn.close()
        
        if not businesses_to_analyze:
            console.print("[yellow]No websites to analyze![/yellow]")
            return
        
        console.print(f"Analyzing {len(businesses_to_analyze)} websites...\n")
        analyzed = 0
        failed = 0
        
        with Progress() as progress:
            task = progress.add_task("Analyzing...", total=len(businesses_to_analyze))
            
            for business in businesses_to_analyze:
                # Handle both dict and tuple formats
                if isinstance(business, dict):
                    name = business.get('name', 'Unknown')
                    website = business.get('website', '')
                    fsq_id = business.get('fsq_id', '')
                else:
                    fsq_id, name, website = business
                
                if not website:
                    progress.update(task, advance=1)
                    continue
                
                progress.update(task, description=f"Analyzing {name[:30]}...")
                
                try:
                    # Analyze website
                    analysis = self.analyzer.analyze(website)
                    
                    # Find emails
                    emails = self.email_finder.find_emails(website)
                    
                    # Update analysis in database - only if we have fsq_id
                    if fsq_id:
                        self.db.update_website_analysis(fsq_id, analysis)
                    
                    # Update email if found
                    if emails and fsq_id:
                        conn = sqlite3.connect(config.DATABASE_PATH)
                        cursor = conn.cursor()
                        cursor.execute('UPDATE businesses SET email = ? WHERE fsq_id = ?', 
                                     (emails[0], fsq_id))
                        conn.commit()
                        conn.close()
                    
                    # Show result with color coding
                    if analysis['score'] < 50:
                        console.print(f"[red]✗ {name}: Score {analysis['score']}/100[/red]")
                    elif analysis['score'] < 70:
                        console.print(f"[yellow]⚠ {name}: Score {analysis['score']}/100[/yellow]")
                    else:
                        console.print(f"[green]✓ {name}: Score {analysis['score']}/100[/green]")
                    
                    analyzed += 1
                    
                except Exception as e:
                    failed += 1
                    error_msg = str(e)[:100]
                    console.print(f"[dim]✗ {name}: {error_msg}[/dim]")
                
                progress.update(task, advance=1)
                time.sleep(0.5)  # Rate limiting
        
        console.print(f"\n[bold green]✓ Analysis Complete![/bold green]")
        console.print(f"[cyan]Analyzed: {analyzed} | Failed: {failed} | Total: {len(businesses_to_analyze)}[/cyan]")
        console.print(f"[dim]Results saved to database. View in dashboard at http://localhost:5000[/dim]\n")
    
    def show_statistics(self):
        """Display database statistics"""
        stats = self.db.get_statistics()
        
        table = Table(title="📊 Database Statistics")
        table.add_column("Metric", style="cyan")
        table.add_column("Value", style="green")
        
        table.add_row("Total Businesses", str(stats['total_businesses']))
        table.add_row("With Websites", str(stats['with_websites']))
        table.add_row("Analyzed", str(stats['analyzed']))
        table.add_row("High Priority Leads", str(stats['high_priority']))
        table.add_row("Medium Priority", str(stats['medium_priority']))
        table.add_row("Low Priority", str(stats['low_priority']))
        
        console.print(table)
        
        # Show top 5 high-priority leads
        if stats['high_priority'] > 0:
            console.print("\n[bold]🎯 Top 5 High Priority Leads:[/bold]")
            
            leads = self.db.get_businesses_by_score(min_score=70, limit=5)
            
            lead_table = Table()
            lead_table.add_column("Name", style="cyan")
            lead_table.add_column("Website", style="blue")
            lead_table.add_column("Score", style="red")
            lead_table.add_column("Issues", style="yellow")
            
            for lead in leads:
                name = lead['name'][:30] + "..." if len(lead['name']) > 30 else lead['name']
                website = lead['website'][:30] + "..." if lead['website'] and len(lead['website']) > 30 else lead['website'] or "N/A"
                score = str(lead['website_score'])
                issues = str(len(json.loads(lead.get('issues', '[]'))))
                
                lead_table.add_row(name, website, score, issues)
            
            console.print(lead_table)
    
    def export_data(self):
        """Export data to various formats"""
        console.print("\n[bold]📤 Data Export[/bold]")
        
        console.print("1. Excel (High Priority Leads)")
        console.print("2. CSV (All Data)")
        console.print("3. JSON Report")
        
        choice = console.input("\nSelect format (1-3): ").strip()
        
        if choice == "1":
            min_score = console.input("Minimum website score (default: 50): ").strip()
            min_score = int(min_score) if min_score.isdigit() else 50
            
            filename = self.exporter.export_to_excel(min_score=min_score)
            if filename:
                console.print(f"[green]✓ Exported to {filename}[/green]")
        
        elif choice == "2":
            filename = self.exporter.export_to_csv()
            if filename:
                console.print(f"[green]✓ Exported to {filename}[/green]")
        
        elif choice == "3":
            report = self.exporter.generate_report()
            console.print("[green]✓ Generated comprehensive report[/green]")
            console.print(json.dumps(report, indent=2))
        
        else:
            console.print("[red]Invalid choice![/red]")
    
    def configure_settings(self):
        """Configure application settings"""
        console.print("\n[bold]⚙️  Configuration[/bold]")
        
        # This would be expanded with actual configuration options
        console.print("[yellow]Configuration menu under development...[/yellow]")
        console.print("Edit config.py directly for now.")
    
    def start_automated_scan(self):
        """Start automated scanning in background"""
        console.print("\n[bold]🔄 Automated Scanning[/bold]")
        
        if self.is_running:
            console.print("[yellow]Scanner is already running![/yellow]")
            return
        
        # Define scanning schedule
        schedule.every().day.at("02:00").do(self._daily_scan)
        schedule.every(6).hours.do(self._check_new_businesses)
        schedule.every().sunday.at("03:00").do(self._weekly_analysis)
        
        # Start in background thread
        self.is_running = True
        scanner_thread = threading.Thread(target=self._run_scheduler, daemon=True)
        scanner_thread.start()
        
        console.print("[green]✓ Automated scanner started![/green]")
        console.print("[dim]Running daily at 2 AM, checking every 6 hours[/dim]")
        console.print("Press Ctrl+C to stop")
        
        try:
            while self.is_running:
                time.sleep(1)
        except KeyboardInterrupt:
            self.is_running = False
            console.print("\n[yellow]Scanner stopped[/yellow]")
    
    def _run_scheduler(self):
        """Run the schedule in background"""
        while self.is_running:
            schedule.run_pending()
            time.sleep(60)
    
    def _daily_scan(self):
        """Daily scanning job"""
        console.print("[dim]Running daily scan...[/dim]")
        # Implement daily scanning logic
        
    def _check_new_businesses(self):
        """Check for new businesses"""
        console.print("[dim]Checking for new businesses...[/dim]")
        # Implement new business checking
        
    def _weekly_analysis(self):
        """Weekly deep analysis"""
        console.print("[dim]Running weekly analysis...[/dim]")
        # Implement weekly analysis


def main():
    """Main entry point"""
    app = BusinessFinderApp()
    
    if len(sys.argv) > 1:
        # Command line mode
        if sys.argv[1] == "scan":
            app.search_location()
        elif sys.argv[1] == "analyze":
            app.analyze_websites()
        elif sys.argv[1] == "export":
            app.export_data()
        elif sys.argv[1] == "stats":
            app.show_statistics()
        else:
            console.print("Usage: python app.py [scan|analyze|export|stats]")
    else:
        # Interactive mode
        app.run_interactive()


if __name__ == "__main__":
    main()
