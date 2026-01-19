#!/usr/bin/env python3
"""
Business Finder Pro - Quick Start & API Tester
A simple interface to test your Foursquare API and start finding businesses
"""

import sys
import os
import requests
import sqlite3
import json
from datetime import datetime
from rich.console import Console
from rich.table import Table
from rich.progress import Progress
from api_manager import APIManager
import time

console = Console()

# Add current directory to path to import your modules
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

class QuickStarter:
    def __init__(self):
        self.api_key = None
        self.db_path = "businesses.db"
        self.api_manager = APIManager()
        self.load_config()
        
    def load_config(self):
        """Try to load API key from config.py"""
        try:
            from config import config
            self.api_key = config.FOURSQUARE_API_KEY
            console.print("[green]✓ Loaded API key from config.py[/green]")
        except ImportError:
            console.print("[yellow]⚠ Could not import config.py[/yellow]")
            # Try to get API key from environment
            import os
            from dotenv import load_dotenv
            load_dotenv()
            self.api_key = os.getenv("FOURSQUARE_API_KEY", "")
            if self.api_key:
                console.print("[green]✓ Loaded API key from environment[/green]")
            else:
                console.print(f"[red]⚠ No API key found in config or environment[/red]")
        except Exception as e:
            console.print(f"[red]Error loading config: {e}[/red]")
            import os
            from dotenv import load_dotenv
            load_dotenv()
            self.api_key = os.getenv("FOURSQUARE_API_KEY", "")
    
    def manage_apis(self):
        """API Management Menu"""
        console.print("\n[bold cyan]🔧 API Management Center[/bold cyan]")
        
        while True:
            console.print("\n" + "="*60)
            console.print("[bold]API Management Options:[/bold]")
            console.print("[cyan]1.[/cyan] 📡 View API Status Dashboard")
            console.print("[cyan]2.[/cyan] 🧪 Test All API Connections")
            console.print("[cyan]3.[/cyan] 🔧 Configure New API")
            console.print("[cyan]4.[/cyan] 🔑 Update API Key")
            console.print("[cyan]5.[/cyan] 🌟 API Recommendations")
            console.print("[cyan]6.[/cyan] 📊 View API Usage Statistics")
            console.print("[cyan]7.[/cyan] ↩️  Back to Main Menu")
            
            choice = console.input("\nSelect option (1-7): ").strip()
            
            if choice == "1":
                self.api_manager.show_api_status()
                
            elif choice == "2":
                self.test_all_apis()
                
            elif choice == "3":
                self.api_manager.interactive_api_setup()
                
            elif choice == "4":
                self.update_api_key_interactive()
                
            elif choice == "5":
                self.api_manager.show_api_recommendations()
                
            elif choice == "6":
                self.show_api_usage()
                
            elif choice == "7":
                break
                
            else:
                console.print("[red]Invalid choice![/red]")
    
    def test_all_apis(self):
        """Test all configured APIs"""
        console.print("\n[bold cyan]🧪 Testing All API Connections...[/bold cyan]")
        
        # Get all APIs from all categories
        all_apis = []
        for category in ["apis", "enrichment_apis", "analysis_apis"]:
            if category in self.api_manager.configs:
                all_apis.extend(list(self.api_manager.configs[category].keys()))
        
        # Remove duplicates
        all_apis = list(set(all_apis))
        
        if not all_apis:
            console.print("[yellow]No APIs configured[/yellow]")
            return
        
        results = []
        for api_name in all_apis:
            api_config = None
            for category in ["apis", "enrichment_apis", "analysis_apis"]:
                if api_name in self.api_manager.configs.get(category, {}):
                    api_config = self.api_manager.configs[category][api_name]
                    break
            
            if api_config:
                has_key = bool(api_config.get('api_key', ''))
                if has_key:
                    success = self.api_manager.test_api_connection(api_name)
                    results.append((api_name, success))
                else:
                    console.print(f"[yellow]⚠ {api_name}: No API key configured[/yellow]")
                    results.append((api_name, False))
        
        # Show summary
        console.print("\n[bold]📊 Test Summary:[/bold]")
        passed = sum(1 for _, success in results if success)
        total = len(results)
        
        console.print(f"✅ {passed}/{total} APIs working")
        
        if passed < total:
            console.print("\n[yellow]⚠ Some APIs need attention:[/yellow]")
            for api_name, success in results:
                if not success:
                    console.print(f"   • {api_name}")
    
    def update_api_key_interactive(self):
        """Update API key interactively"""
        console.print("\n[bold cyan]🔑 Update API Key[/bold cyan]")
        
        # Show current APIs
        self.api_manager.show_api_status()
        
        api_name = console.input("\nEnter API name to update (or 'cancel'): ").strip()
        if api_name.lower() == 'cancel':
            return
        
        new_key = console.input(f"Enter new API key for {api_name}: ").strip()
        if not new_key:
            console.print("[red]No key provided![/red]")
            return
        
        if self.api_manager.update_api_key(api_name, new_key):
            console.print(f"[green]✓ {api_name} API key updated[/green]")
            
            test = console.input("Test connection now? (y/n): ").strip().lower()
            if test == 'y':
                self.api_manager.test_api_connection(api_name)
        else:
            console.print(f"[red]Failed to update {api_name}[/red]")
    
    def show_api_usage(self):
        """Show API usage statistics"""
        console.print("\n[bold cyan]📊 API Usage Statistics[/bold cyan]")
        
        # Create usage table
        table = Table(title="API Usage", box=box.ROUNDED, show_header=True)
        table.add_column("API", style="cyan")
        table.add_column("Used Today", style="yellow")
        table.add_column("Daily Limit", style="white")
        table.add_column("Remaining", style="green")
        table.add_column("Status", style="white")
        
        total_used = 0
        total_limit = 0
        
        for category in ["apis", "enrichment_apis", "analysis_apis"]:
            for api_name, config in self.api_manager.configs.get(category, {}).items():
                used = config.get('used_today', 0)
                limit = config.get('rate_limit', 0)
                remaining = max(0, limit - used)
                status = config.get('status', 'inactive')
                
                if limit > 0:
                    percentage = (used / limit) * 100
                    if percentage > 90:
                        status_emoji = "🔴"
                    elif percentage > 70:
                        status_emoji = "🟡"
                    else:
                        status_emoji = "🟢"
                else:
                    status_emoji = "⚪"
                
                table.add_row(
                    config.get('name', api_name),
                    str(used),
                    str(limit),
                    str(remaining),
                    f"{status_emoji} {status}"
                )
                
                total_used += used
                total_limit += limit
        
        console.print(table)
        
        if total_limit > 0:
            console.print(f"\n[bold]Total Usage:[/bold] {total_used}/{total_limit} ({total_used/total_limit*100:.1f}%)")
            
            if total_used > total_limit * 0.8:
                console.print("[red]⚠ Warning: High API usage! Consider upgrading plans.[/red]")
    
    def test_api_connection(self):
        """Test if Foursquare API key works"""
        console.print("\n[bold cyan]🔌 Testing API Connection...[/bold cyan]")
        
        if not self.api_key:
            console.print("[red]❌ No API key found![/red]")
            console.print("Please add your Foursquare API key to config.py")
            return False
        
        url = "https://api.foursquare.com/v3/places/search"
        headers = {
            "Accept": "application/json",
            "Authorization": self.api_key
        }
        params = {
            "query": "coffee",
            "near": "London",
            "limit": 2
        }
        
        try:
            with console.status("[cyan]Connecting to Foursquare API...[/cyan]"):
                response = requests.get(url, headers=headers, params=params, timeout=10)
            
            if response.status_code == 200:
                data = response.json()
                count = len(data.get('results', []))
                console.print(f"[green]✅ API Connection Successful![/green]")
                console.print(f"[dim]Found {count} test results[/dim]")
                
                # Show sample data
                if count > 0:
                    place = data['results'][0]
                    table = Table(title="Sample Business Data", show_header=True, header_style="bold magenta")
                    table.add_column("Field", style="cyan")
                    table.add_column("Value", style="green")
                    
                    table.add_row("Name", place.get('name', 'N/A'))
                    table.add_row("Category", place.get('categories', [{}])[0].get('name', 'N/A'))
                    table.add_row("Address", place.get('location', {}).get('formatted_address', 'N/A'))
                    
                    console.print(table)
                
                return True
                
            elif response.status_code == 401:
                console.print("[red]❌ API Key Invalid![/red]")
                console.print("Your Foursquare API key is not valid or has expired.")
                console.print("Please check your key in config.py")
                return False
                
            else:
                console.print(f"[yellow]⚠ API Response: {response.status_code}[/yellow]")
                console.print(f"Response: {response.text[:200]}")
                return False
                
        except requests.exceptions.ConnectionError:
            console.print("[red]❌ Connection Failed![/red]")
            console.print("Check your internet connection")
            return False
        except Exception as e:
            console.print(f"[red]❌ Error: {e}[/red]")
            return False
    
    def test_database(self):
        """Test if database is working"""
        console.print("\n[bold cyan]🗄️  Testing Database...[/bold cyan]")
        
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            # Check if businesses table exists
            cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='businesses'")
            table_exists = cursor.fetchone()
            
            if table_exists:
                cursor.execute("SELECT COUNT(*) FROM businesses")
                count = cursor.fetchone()[0]
                console.print(f"[green]✅ Database is working[/green]")
                console.print(f"[dim]Found {count} businesses in database[/dim]")
            else:
                console.print("[yellow]⚠ Database exists but no businesses table[/yellow]")
                console.print("[dim]This is normal if you haven't run any searches yet[/dim]")
            
            conn.close()
            return True
            
        except sqlite3.Error as e:
            console.print(f"[red]❌ Database Error: {e}[/red]")
            return False
    
    def test_modules(self):
        """Test if all required modules can be imported"""
        console.print("\n[bold cyan]🧪 Testing Modules...[/bold cyan]")
        
        modules_to_test = [
            ("requests", "HTTP requests"),
            ("rich", "Terminal formatting"),
            ("sqlite3", "Database"),
            ("config", "Configuration"),
            ("scraper", "Foursquare scraper"),
            ("analyzer", "Website analyzer"),
            ("database", "Database models"),
        ]
        
        all_good = True
        
        for module_name, description in modules_to_test:
            try:
                if module_name == "config":
                    import config
                elif module_name == "scraper":
                    import scraper
                elif module_name == "analyzer":
                    import analyzer
                elif module_name == "database":
                    import database
                else:
                    __import__(module_name)
                
                console.print(f"[green]  ✓ {module_name}[/green] [dim]({description})[/dim]")
            except ImportError as e:
                console.print(f"[red]  ✗ {module_name}[/red] [dim]({description}) - {e}[/dim]")
                all_good = False
            except Exception as e:
                console.print(f"[yellow]  ⚠ {module_name}[/yellow] [dim]({description}) - {e}[/dim]")
        
        return all_good
    
    def run_sample_search(self):
        """Run a sample search to demonstrate functionality"""
        console.print("\n[bold cyan]🔍 Running Sample Search...[/bold cyan]")
        
        try:
            from scraper import FoursquareScraper
            
            scraper = FoursquareScraper(self.api_key)
            
            # Search for coffee shops in London
            with console.status("[cyan]Searching for coffee shops in London...[/cyan]"):
                businesses = scraper.search_by_city("London", "13003", radius=2000, limit=5)
            
            if not businesses:
                console.print("[yellow]⚠ No businesses found in sample search[/yellow]")
                return
            
            console.print(f"[green]✅ Found {len(businesses)} businesses[/green]")
            
            # Display results
            table = Table(title="Sample Search Results", show_header=True, header_style="bold blue")
            table.add_column("#", style="dim")
            table.add_column("Name", style="cyan")
            table.add_column("Address", style="green")
            table.add_column("Website", style="blue")
            
            for i, biz in enumerate(businesses, 1):
                name = biz.get('name', 'N/A')[:20] + "..." if len(biz.get('name', '')) > 20 else biz.get('name', 'N/A')
                address = biz.get('address', 'N/A')[:30] + "..." if len(biz.get('address', '')) > 30 else biz.get('address', 'N/A')
                website = biz.get('website', 'N/A')
                if website and len(website) > 20:
                    website = website[:20] + "..."
                
                table.add_row(str(i), name, address, website)
            
            console.print(table)
            
            # Ask if they want to save to database
            save = console.input("\n💾 Save these to database? (y/n): ").lower()
            if save == 'y':
                try:
                    from database import BusinessDatabase
                    db = BusinessDatabase()
                    saved = 0
                    for biz in businesses:
                        if db.add_business(biz):
                            saved += 1
                    console.print(f"[green]✅ Saved {saved} businesses to database[/green]")
                except Exception as e:
                    console.print(f"[red]❌ Error saving to database: {e}[/red]")
            
            return businesses
            
        except Exception as e:
            console.print(f"[red]❌ Error in sample search: {e}[/red]")
            import traceback
            console.print(f"[dim]{traceback.format_exc()}[/dim]")
            return None
    
    def analyze_sample_website(self):
        """Analyze a sample website"""
        console.print("\n[bold cyan]📊 Analyzing Sample Website...[/bold cyan]")
        
        try:
            from analyzer import WebsiteAnalyzer
            
            analyzer = WebsiteAnalyzer()
            
            # Test with a known website
            test_url = console.input("Enter website URL to analyze (or press Enter for example): ").strip()
            if not test_url:
                test_url = "http://example.com"  # Default test URL
            
            with console.status(f"[cyan]Analyzing {test_url}...[/cyan]"):
                analysis = analyzer.analyze(test_url)
            
            # Display analysis results
            table = Table(title=f"Website Analysis: {test_url}", show_header=True, header_style="bold green")
            table.add_column("Metric", style="cyan")
            table.add_column("Value", style="white")
            
            table.add_row("Website Score", f"{analysis.get('score', 0)}/100")
            table.add_row("Has SSL", "✅ Yes" if analysis.get('has_ssl') else "❌ No")
            table.add_row("Mobile Friendly", "✅ Yes" if analysis.get('mobile_friendly') else "❌ No")
            table.add_row("Load Time", f"{analysis.get('load_time', 0)} seconds")
            table.add_row("Status", "✅ Live" if analysis.get('exists') else "❌ Down")
            
            # Add issues if any
            issues = analysis.get('issues', [])
            if issues:
                table.add_row("Issues Found", str(len(issues)))
                for i, issue in enumerate(issues[:3]):  # Show first 3 issues
                    table.add_row(f"Issue {i+1}", issue[:50] + "..." if len(issue) > 50 else issue)
            
            console.print(table)
            
            # Give recommendation
            score = analysis.get('score', 0)
            if score < 50:
                console.print("[red]🚨 This website needs significant improvement![/red]")
                console.print("[dim]Perfect candidate for your services[/dim]")
            elif score < 70:
                console.print("[yellow]⚠ This website could use some optimization[/yellow]")
            else:
                console.print("[green]✅ This website is in good shape[/green]")
            
            return analysis
            
        except Exception as e:
            console.print(f"[red]❌ Error analyzing website: {e}[/red]")
            import traceback
            console.print(f"[dim]{traceback.format_exc()}[/dim]")
            return None
    
    def show_dashboard_preview(self):
        """Show a preview of the dashboard"""
        console.print("\n[bold cyan]📈 Dashboard Preview[/bold cyan]")
        
        try:
            # Check if we have data
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            # Get statistics
            cursor.execute("SELECT COUNT(*) FROM businesses")
            total = cursor.fetchone()[0]
            
            cursor.execute("SELECT COUNT(*) FROM businesses WHERE website IS NOT NULL")
            with_websites = cursor.fetchone()[0]
            
            cursor.execute("SELECT COUNT(*) FROM businesses WHERE last_analyzed IS NOT NULL")
            analyzed = cursor.fetchone()[0]
            
            conn.close()
            
            # Create statistics table
            table = Table(title="Current Database Statistics", show_header=True, header_style="bold magenta")
            table.add_column("Metric", style="cyan")
            table.add_column("Count", style="green")
            
            table.add_row("Total Businesses", str(total))
            table.add_row("With Websites", str(with_websites))
            table.add_row("Analyzed", str(analyzed))
            
            if analyzed > 0:
                # Get average score
                conn = sqlite3.connect(self.db_path)
                cursor = conn.cursor()
                cursor.execute("SELECT AVG(website_score) FROM businesses WHERE website_score > 0")
                avg_score = cursor.fetchone()[0]
                if avg_score:
                    table.add_row("Average Score", f"{avg_score:.1f}/100")
                conn.close()
            
            console.print(table)
            
            # Show how to start the dashboard
            console.print("\n[bold]🚀 To start the web dashboard:[/bold]")
            console.print("[cyan]1.[/cyan] Open a new terminal")
            console.print("[cyan]2.[/cyan] Run: [green]python dashboard.py[/green]")
            console.print("[cyan]3.[/cyan] Open browser to: [blue]http://localhost:5000[/blue]")
            
        except Exception as e:
            console.print(f"[yellow]⚠ Could not load dashboard preview: {e}[/yellow]")
    
    def run_comprehensive_test(self):
        """Run all tests"""
        console.print("\n" + "="*60)
        console.print("[bold cyan]🚀 COMPREHENSIVE SYSTEM TEST[/bold cyan]")
        console.print("="*60)
        
        tests = [
            ("API Connection", self.test_api_connection),
            ("Database", self.test_database),
            ("Modules", self.test_modules),
        ]
        
        results = []
        for test_name, test_func in tests:
            console.print(f"\n[bold]Testing: {test_name}[/bold]")
            try:
                result = test_func()
                results.append((test_name, result))
            except Exception as e:
                console.print(f"[red]Error in {test_name}: {e}[/red]")
                results.append((test_name, False))
        
        # Summary
        console.print("\n" + "="*60)
        console.print("[bold]📊 TEST SUMMARY[/bold]")
        
        passed = sum(1 for _, result in results if result)
        total = len(results)
        
        for test_name, result in results:
            status = "✅ PASS" if result else "❌ FAIL"
            color = "green" if result else "red"
            console.print(f"[{color}]{status}[/{color}] {test_name}")
        
        console.print(f"\n[bold]Overall: {passed}/{total} tests passed[/bold]")
        
        if passed == total:
            console.print("[green]🎉 All systems go! You're ready to start.[/green]")
        else:
            console.print("[yellow]⚠ Some tests failed. Check the errors above.[/yellow]")
        
        return passed == total
    
    def show_main_menu(self):
        """Show the main menu"""
        while True:
            console.print("\n" + "="*60)
            console.print("[bold cyan]🤖 BUSINESS FINDER PRO - QUICK START[/bold cyan]")
            console.print("="*60)
            
            console.print("\n[bold]📋 Main Menu:[/bold]")
            console.print("[cyan]1.[/cyan] 🔌 Run Comprehensive System Test")
            console.print("[cyan]2.[/cyan] 🔍 Test API Connection")
            console.print("[cyan]3.[/cyan] 🗄️  Test Database")
            console.print("[cyan]4.[/cyan] 🧪 Test All Modules")
            console.print("[cyan]5.[/cyan] 🔎 Run Sample Business Search")
            console.print("[cyan]6.[/cyan] 📊 Analyze Sample Website")
            console.print("[cyan]7.[/cyan] 📈 Show Dashboard Preview")
            console.print("[cyan]8.[/cyan] 🚀 Start Full Application (app.py)")
            console.print("[cyan]9.[/cyan] 🌐 Start Web Dashboard")
            console.print("[cyan]10.[/cyan] 📤 Export Data")
            console.print("[cyan]11.[/cyan] 🔧 Manage APIs") 
            console.print("[cyan]0.[/cyan] 🚪 Exit")
            
            choice = console.input("\n[bold]Enter your choice (0-10): [/bold]").strip()
            
            if choice == "1":
                self.run_comprehensive_test()
                
            elif choice == "2":
                self.test_api_connection()
                
            elif choice == "3":
                self.test_database()
                
            elif choice == "4":
                self.test_modules()
                
            elif choice == "5":
                self.run_sample_search()
                
            elif choice == "6":
                self.analyze_sample_website()
                
            elif choice == "7":
                self.show_dashboard_preview()
                
            elif choice == "8":
                self.start_full_application()
                
            elif choice == "9":
                self.start_web_dashboard()
                
            elif choice == "10":
                self.export_data()

            elif choice == "11":
            	self.manage_apis()
                
            elif choice == "0":
                console.print("[yellow]👋 Goodbye![/yellow]")
                break
                
            else:
                console.print("[red]❌ Invalid choice![/red]")
    
    def start_full_application(self):
        """Start the full interactive application"""
        console.print("\n[bold cyan]🚀 Starting Full Application...[/bold cyan]")
        console.print("[dim]Launching app.py in interactive mode...[/dim]")
        
        try:
            # Import and run the main app
            import app
            app.main()
        except ModuleNotFoundError as e:
            console.print(f"[red]❌ Missing required module: {e}[/red]")
            console.print("\n[yellow]⚠ Please install dependencies first:[/yellow]")
            console.print("[cyan]1. Activate virtual environment:[/cyan]")
            console.print("   source venv/bin/activate  [dim](or venv\\Scripts\\activate on Windows)[/dim]")
            console.print("\n[cyan]2. Install dependencies:[/cyan]")
            console.print("   pip install -r requirements.txt")
            console.print("\n[cyan]3. Run again from activated environment[/cyan]")
        except Exception as e:
            console.print(f"[red]❌ Error starting application: {e}[/red]")
            console.print("[yellow]Trying alternative method...[/yellow]")
            
            # Try running as module
            import subprocess
            try:
                subprocess.run([sys.executable, "app.py"], check=True)
            except subprocess.CalledProcessError as e:
                console.print(f"[red]❌ Failed to start: {e}[/red]")
    
    def start_web_dashboard(self):
        """Start the web dashboard"""
        console.print("\n[bold cyan]🌐 Starting Web Dashboard...[/bold cyan]")
        console.print("[dim]This will start a web server on port 5000[/dim]")
        console.print("[yellow]⚠ Keep this terminal open and open a new terminal for other tasks[/yellow]")
        
        start = console.input("\nStart dashboard now? (y/n): ").lower()
        if start != 'y':
            return
        
        try:
            import subprocess
            import threading
            
            def run_dashboard():
                try:
                    subprocess.run([sys.executable, "dashboard.py"], check=True)
                except KeyboardInterrupt:
                    console.print("\n[yellow]Dashboard stopped[/yellow]")
                except Exception as e:
                    console.print(f"[red]Dashboard error: {e}[/red]")
            
            # Run in background thread
            dashboard_thread = threading.Thread(target=run_dashboard, daemon=True)
            dashboard_thread.start()
            
            console.print("\n[green]✅ Dashboard started![/green]")
            console.print("[cyan]Open your browser to:[/cyan] [blue]http://localhost:5000[/blue]")
            console.print("\n[yellow]Press Enter to return to menu (dashboard will continue running)[/yellow]")
            input()
            
        except Exception as e:
            console.print(f"[red]❌ Error starting dashboard: {e}[/red]")
    
    def export_data(self):
        """Export data from database"""
        console.print("\n[bold cyan]📤 Exporting Data...[/bold cyan]")
        
        try:
            from export import DataExporter
            
            exporter = DataExporter()
            
            console.print("\n[bold]Export Options:[/bold]")
            console.print("[cyan]1.[/cyan] Excel (High Priority Leads)")
            console.print("[cyan]2.[/cyan] CSV (All Data)")
            console.print("[cyan]3.[/cyan] JSON Report")
            
            choice = console.input("\nSelect format (1-3): ").strip()
            
            if choice == "1":
                min_score = console.input("Minimum website score (default: 50): ").strip()
                min_score = int(min_score) if min_score.isdigit() else 50
                filename = exporter.export_to_excel(min_score=min_score)
                if filename:
                    console.print(f"[green]✅ Exported to {filename}[/green]")
                    
            elif choice == "2":
                filename = exporter.export_to_csv()
                if filename:
                    console.print(f"[green]✅ Exported to {filename}[/green]")
                    
            elif choice == "3":
                report = exporter.generate_report()
                console.print("[green]✅ Generated comprehensive report[/green]")
                # Save to file
                import json
                with open("report.json", "w") as f:
                    json.dump(report, f, indent=2)
                console.print("[dim]Saved to report.json[/dim]")
                
            else:
                console.print("[red]❌ Invalid choice![/red]")
                
        except Exception as e:
            console.print(f"[red]❌ Error exporting data: {e}[/red]")


def main():
    """Main entry point"""
    # Clear screen and show banner
    os.system('cls' if os.name == 'nt' else 'clear')
    
    console.print("""
    ╔══════════════════════════════════════════════════════════════╗
    ║                                                              ║
    ║    🤖 [bold cyan]BUSINESS FINDER PRO[/bold cyan] - QUICK START              ║
    ║    [dim]Find clients with outdated websites worldwide[/dim]       ║
    ║                                                              ║
    ╚══════════════════════════════════════════════════════════════╝
    """)
    
    # Show current directory
    console.print(f"[dim]Working directory: {os.getcwd()}[/dim]")
    console.print(f"[dim]Database: businesses.db[/dim]")
    
    # Initialize and run
    starter = QuickStarter()
    
    # Check if this is first run
    if not os.path.exists("businesses.db"):
        console.print("\n[yellow]⚠ First run detected[/yellow]")
        console.print("[dim]Initializing database...[/dim]")
        try:
            from database import BusinessDatabase
            db = BusinessDatabase()
            console.print("[green]✅ Database initialized[/green]")
        except Exception as e:
            console.print(f"[red]❌ Error initializing database: {e}[/red]")
    
    # Show menu
    starter.show_main_menu()


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        console.print("\n[yellow]👋 Interrupted by user[/yellow]")
    except Exception as e:
        console.print(f"\n[red]❌ Unexpected error: {e}[/red]")
        import traceback
        console.print(f"[dim]{traceback.format_exc()}[/dim]")
