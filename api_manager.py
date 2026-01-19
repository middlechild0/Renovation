# api_manager.py
import json
import os
from datetime import datetime
from typing import Dict, List, Optional
import requests
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich import box
from dotenv import load_dotenv

load_dotenv()

console = Console()

class APIManager:
    """Comprehensive API management system"""
    
    def __init__(self, config_file="api_configs.json"):
        self.config_file = config_file
        self.configs = self.load_configs()
        self.test_results = {}
        
    def load_configs(self):
        """Load API configurations from file"""
        if os.path.exists(self.config_file):
            try:
                with open(self.config_file, 'r') as f:
                    return json.load(f)
            except:
                pass
        
        # Default configurations
        default_configs = {
            "apis": {
                "foursquare": {
                    "name": "Foursquare",
                    "api_key": os.getenv("FOURSQUARE_API_KEY", ""),
                    "base_url": "https://api.foursquare.com/v3/",
                    "status": "active",
                    "rate_limit": 95000,
                    "used_today": 0,
                    "last_used": None,
                    "category": "places",
                    "description": "Global place database with 105M+ businesses"
                },
                "yelp": {
                    "name": "Yelp Fusion",
                    "api_key": "",
                    "base_url": "https://api.yelp.com/v3/",
                    "status": "inactive",
                    "rate_limit": 500,
                    "used_today": 0,
                    "last_used": None,
                    "category": "places",
                    "description": "Business reviews and information (strong in US)"
                },
                "tomtom": {
                    "name": "TomTom Places",
                    "api_key": "",
                    "base_url": "https://api.tomtom.com/search/2/",
                    "status": "inactive",
                    "rate_limit": 2500,
                    "used_today": 0,
                    "last_used": None,
                    "category": "places",
                    "description": "Global points of interest with free tier"
                },
                "openstreetmap": {
                    "name": "OpenStreetMap",
                    "api_key": "",
                    "base_url": "https://nominatim.openstreetmap.org/",
                    "status": "inactive",
                    "rate_limit": 1,  # Very strict limit
                    "used_today": 0,
                    "last_used": None,
                    "category": "places",
                    "description": "Open source mapping data"
                }
            },
            "enrichment_apis": {
                "hunter": {
                    "name": "Hunter.io",
                    "api_key": "",
                    "base_url": "https://api.hunter.io/v2/",
                    "status": "inactive",
                    "purpose": "Email finding",
                    "description": "Find business email addresses"
                },
                "clearbit": {
                    "name": "Clearbit",
                    "api_key": "",
                    "base_url": "https://person.clearbit.com/v2/",
                    "status": "inactive",
                    "purpose": "Company data",
                    "description": "Company information and enrichment"
                }
            },
            "analysis_apis": {
                "builtwith": {
                    "name": "BuiltWith",
                    "api_key": "",
                    "base_url": "https://api.builtwith.com/",
                    "status": "inactive",
                    "purpose": "Tech stack",
                    "description": "Detect website technologies"
                },
                "wappalyzer": {
                    "name": "Wappalyzer",
                    "api_key": "",
                    "base_url": "https://api.wappalyzer.com/v2/",
                    "status": "inactive",
                    "purpose": "Tech detection",
                    "description": "Identify web technologies"
                }
            },
            "active_services": ["foursquare"],
            "api_usage": {},
            "last_updated": datetime.now().isoformat()
        }
        
        self.save_configs(default_configs)
        return default_configs
    
    def save_configs(self, configs=None):
        """Save configurations to file"""
        if configs is None:
            configs = self.configs
        
        configs['last_updated'] = datetime.now().isoformat()
        
        with open(self.config_file, 'w') as f:
            json.dump(configs, f, indent=2, default=str)
        
        self.configs = configs
        return True
    
    def add_api(self, api_type, api_name, api_config):
        """Add a new API configuration"""
        if api_type not in self.configs:
            self.configs[api_type] = {}
        
        self.configs[api_type][api_name] = api_config
        self.save_configs()
        return True
    
    def update_api_key(self, api_name, api_key, api_type="apis"):
        """Update API key for a service"""
        # Search through all API types
        for api_category in ["apis", "enrichment_apis", "analysis_apis"]:
            if api_name in self.configs.get(api_category, {}):
                self.configs[api_category][api_name]["api_key"] = api_key
                self.configs[api_category][api_name]["status"] = "active"
                
                if api_name not in self.configs["active_services"]:
                    self.configs["active_services"].append(api_name)
                
                self.save_configs()
                return True
        
        # If not found, add to main apis
        if api_name not in self.configs["apis"]:
            self.configs["apis"][api_name] = {
                "name": api_name.title(),
                "api_key": api_key,
                "status": "active",
                "rate_limit": 1000,
                "used_today": 0,
                "last_used": None,
                "description": "Custom API added by user"
            }
            if api_name not in self.configs["active_services"]:
                self.configs["active_services"].append(api_name)
            self.save_configs()
        
        return False
    
    def test_api_connection(self, api_name):
        """Test if an API connection works"""
        console.print(f"\n[cyan]Testing {api_name} API...[/cyan]")
        
        # Find the API in configurations
        api_config = None
        api_category = None
        
        for category in ["apis", "enrichment_apis", "analysis_apis"]:
            if api_name in self.configs.get(category, {}):
                api_config = self.configs[category][api_name]
                api_category = category
                break
        
        if not api_config:
            console.print(f"[red]API '{api_name}' not found in configurations[/red]")
            return False
        
        api_key = api_config.get("api_key", "")
        
        if not api_key:
            console.print(f"[yellow]No API key configured for {api_name}[/yellow]")
            return False
        
        # Test based on API type
        test_result = False
        test_message = ""
        
        try:
            if api_name == "foursquare":
                test_result, test_message = self.test_foursquare(api_key)
            elif api_name == "yelp":
                test_result, test_message = self.test_yelp(api_key)
            elif api_name == "tomtom":
                test_result, test_message = self.test_tomtom(api_key)
            elif api_name == "hunter":
                test_result, test_message = self.test_hunter(api_key)
            elif api_name == "clearbit":
                test_result, test_message = self.test_clearbit(api_key)
            elif api_name == "builtwith":
                test_result, test_message = self.test_builtwith(api_key)
            else:
                # Generic test for unknown APIs
                test_result, test_message = self.generic_api_test(api_config)
        
        except Exception as e:
            test_result = False
            test_message = f"Test error: {str(e)}"
        
        # Update test results
        self.test_results[api_name] = {
            "success": test_result,
            "message": test_message,
            "tested_at": datetime.now().isoformat()
        }
        
        if test_result:
            console.print(f"[green]✅ {api_name} API: {test_message}[/green]")
        else:
            console.print(f"[red]❌ {api_name} API: {test_message}[/red]")
        
        return test_result
    
    def test_foursquare(self, api_key):
        """Test Foursquare API"""
        url = "https://api.foursquare.com/v3/places/search"
        headers = {
            "Accept": "application/json",
            "Authorization": api_key
        }
        params = {
            "query": "coffee",
            "near": "London",
            "limit": 1
        }
        
        try:
            response = requests.get(url, headers=headers, params=params, timeout=10)
            
            if response.status_code == 200:
                data = response.json()
                count = len(data.get('results', []))
                return True, f"Connected! Found {count} results"
            elif response.status_code == 401:
                return False, "Invalid API key"
            else:
                return False, f"HTTP {response.status_code}: {response.text[:100]}"
        
        except Exception as e:
            return False, f"Connection failed: {str(e)}"
    
    def test_yelp(self, api_key):
        """Test Yelp API"""
        if not api_key:
            return False, "No API key provided"
        
        url = "https://api.yelp.com/v3/businesses/search"
        headers = {
            "Authorization": f"Bearer {api_key}"
        }
        params = {
            "term": "coffee",
            "location": "San Francisco",
            "limit": 1
        }
        
        try:
            response = requests.get(url, headers=headers, params=params, timeout=10)
            
            if response.status_code == 200:
                return True, "Connected successfully"
            elif response.status_code == 401:
                return False, "Invalid API key"
            else:
                return False, f"HTTP {response.status_code}"
        
        except Exception as e:
            return False, f"Connection failed: {str(e)}"
    
    def test_tomtom(self, api_key):
        """Test TomTom API"""
        if not api_key:
            return False, "No API key provided"
        
        url = f"https://api.tomtom.com/search/2/search/coffee.json"
        params = {
            "key": api_key,
            "limit": 1,
            "lat": 37.7749,
            "lon": -122.4194,
            "radius": 1000
        }
        
        try:
            response = requests.get(url, params=params, timeout=10)
            
            if response.status_code == 200:
                data = response.json()
                results = data.get('results', [])
                return True, f"Connected! Found {len(results)} results"
            elif response.status_code == 403:
                return False, "Invalid or expired API key"
            else:
                return False, f"HTTP {response.status_code}"
        
        except Exception as e:
            return False, f"Connection failed: {str(e)}"
    
    def test_hunter(self, api_key):
        """Test Hunter.io API"""
        if not api_key:
            return False, "No API key provided"
        
        url = "https://api.hunter.io/v2/account"
        params = {"api_key": api_key}
        
        try:
            response = requests.get(url, params=params, timeout=10)
            
            if response.status_code == 200:
                data = response.json()
                if data.get('data', {}).get('first_name'):
                    return True, "Connected! Account verified"
                else:
                    return True, "Connected"
            elif response.status_code == 401:
                return False, "Invalid API key"
            else:
                return False, f"HTTP {response.status_code}"
        
        except Exception as e:
            return False, f"Connection failed: {str(e)}"
    
    def test_clearbit(self, api_key):
        """Test Clearbit API"""
        if not api_key:
            return False, "No API key provided"
        
        url = "https://company.clearbit.com/v2/companies/find"
        params = {"domain": "google.com"}
        headers = {"Authorization": f"Bearer {api_key}"}
        
        try:
            response = requests.get(url, headers=headers, params=params, timeout=10)
            
            if response.status_code == 200:
                return True, "Connected successfully"
            elif response.status_code == 401:
                return False, "Invalid API key"
            elif response.status_code == 404:
                return True, "Connected (test domain not found)"
            else:
                return False, f"HTTP {response.status_code}"
        
        except Exception as e:
            return False, f"Connection failed: {str(e)}"
    
    def test_builtwith(self, api_key):
        """Test BuiltWith API"""
        if not api_key:
            return False, "No API key provided"
        
        url = "https://api.builtwith.com/v20/api.json"
        params = {
            "KEY": api_key,
            "LOOKUP": "google.com"
        }
        
        try:
            response = requests.get(url, params=params, timeout=10)
            
            if response.status_code == 200:
                return True, "Connected successfully"
            else:
                return False, f"HTTP {response.status_code}"
        
        except Exception as e:
            return False, f"Connection failed: {str(e)}"
    
    def generic_api_test(self, api_config):
        """Generic API test for unknown APIs"""
        base_url = api_config.get('base_url', '')
        api_key = api_config.get('api_key', '')
        
        if not base_url or not api_key:
            return False, "Missing base_url or api_key"
        
        # Try a simple GET request to the base URL
        try:
            response = requests.get(base_url, timeout=10)
            if response.status_code < 400:
                return True, f"Connected to {base_url}"
            else:
                return False, f"HTTP {response.status_code}"
        except:
            return False, "Could not connect"
    
    def show_api_status(self):
        """Display status of all APIs"""
        console.print("\n[bold cyan]📡 API Status Dashboard[/bold cyan]")
        
        # Active APIs
        active_table = Table(title="Active APIs", box=box.ROUNDED, show_header=True)
        active_table.add_column("API", style="cyan")
        active_table.add_column("Status", style="green")
        active_table.add_column("Usage", style="yellow")
        active_table.add_column("Last Used", style="dim")
        
        # Inactive APIs
        inactive_table = Table(title="Inactive / Needs Setup", box=box.SIMPLE, show_header=True)
        inactive_table.add_column("API", style="cyan")
        inactive_table.add_column("Purpose", style="white")
        inactive_table.add_column("Action", style="yellow")
        
        for category in ["apis", "enrichment_apis", "analysis_apis"]:
            for api_name, config in self.configs.get(category, {}).items():
                name = config.get('name', api_name)
                status = config.get('status', 'inactive')
                api_key = config.get('api_key', '')
                used = config.get('used_today', 0)
                limit = config.get('rate_limit', 0)
                last_used = config.get('last_used', 'Never')
                
                if status == 'active' and api_key:
                    usage_str = f"{used}/{limit}"
                    active_table.add_row(name, "✅ Active", usage_str, str(last_used)[:10])
                else:
                    purpose = config.get('purpose', config.get('description', 'Business data'))
                    action = "Add API Key" if not api_key else "Activate"
                    inactive_table.add_row(name, purpose, action)
        
        console.print(active_table)
        console.print(inactive_table)
    
    def show_api_recommendations(self):
        """Show recommended APIs for different use cases"""
        console.print("\n[bold cyan]🌟 Recommended APIs for Your Business[/bold cyan]")
        
        recommendations = [
            {
                "use_case": "Basic Business Discovery",
                "recommended": ["Foursquare (free)", "TomTom (free tier)"],
                "budget": "Free",
                "coverage": "Global"
            },
            {
                "use_case": "Professional Lead Generation",
                "recommended": ["Foursquare + Hunter.io"],
                "budget": "$50-200/month",
                "coverage": "Global with emails"
            },
            {
                "use_case": "Tech Stack Analysis",
                "recommended": ["BuiltWith API"],
                "budget": "$295/month",
                "coverage": "1B+ websites"
            },
            {
                "use_case": "Enterprise B2B",
                "recommended": ["ZoomInfo", "Apollo.io"],
                "budget": "$1000+/month",
                "coverage": "100M+ companies"
            }
        ]
        
        for rec in recommendations:
            panel = Panel(
                f"[bold]Use Case:[/bold] {rec['use_case']}\n"
                f"[bold]Recommended:[/bold] {', '.join(rec['recommended'])}\n"
                f"[bold]Budget:[/bold] {rec['budget']}\n"
                f"[bold]Coverage:[/bold] {rec['coverage']}",
                title=f"📊 {rec['use_case']}",
                border_style="blue"
            )
            console.print(panel)
    
    def interactive_api_setup(self):
        """Interactive wizard for setting up APIs"""
        console.print("\n[bold cyan]🔧 Interactive API Setup Wizard[/bold cyan]")
        
        while True:
            console.print("\n[bold]Select API to configure:[/bold]")
            console.print("1. 🗺️  Foursquare (Already active)")
            console.print("2. 📍 Yelp Fusion (US-focused)")
            console.print("3. 🗺️  TomTom Places (Global, free tier)")
            console.print("4. 📧 Hunter.io (Email finding)")
            console.print("5. 🏢 Clearbit (Company enrichment)")
            console.print("6. 💻 BuiltWith (Tech stack analysis)")
            console.print("7. 🆕 Add custom API")
            console.print("8. ↩️  Back to main menu")
            
            choice = console.input("\nSelect (1-8): ").strip()
            
            if choice == "1":
                new_key = console.input("Enter new Foursquare API key (press Enter to keep current): ").strip()
                if new_key:
                    self.update_api_key("foursquare", new_key)
                    console.print("[green]✓ Foursquare API key updated[/green]")
                    self.test_api_connection("foursquare")
            
            elif choice == "2":
                console.print("\n[bold]Yelp Fusion API Setup[/bold]")
                console.print("[dim]Get API key from: https://www.yelp.com/developers/documentation/v3[/dim]")
                api_key = console.input("Enter Yelp API key: ").strip()
                if api_key:
                    self.update_api_key("yelp", api_key)
                    console.print("[green]✓ Yelp API configured[/green]")
                    self.test_api_connection("yelp")
            
            elif choice == "3":
                console.print("\n[bold]TomTom Places API Setup[/bold]")
                console.print("[dim]Get API key from: https://developer.tomtom.com/[/dim]")
                api_key = console.input("Enter TomTom API key: ").strip()
                if api_key:
                    self.update_api_key("tomtom", api_key)
                    console.print("[green]✓ TomTom API configured[/green]")
                    self.test_api_connection("tomtom")
            
            elif choice == "4":
                console.print("\n[bold]Hunter.io API Setup[/bold]")
                console.print("[dim]Get API key from: https://hunter.io/api[/dim]")
                console.print("[yellow]Cost: $49-$499/month[/yellow]")
                api_key = console.input("Enter Hunter.io API key: ").strip()
                if api_key:
                    self.update_api_key("hunter", api_key)
                    console.print("[green]✓ Hunter.io API configured[/green]")
                    self.test_api_connection("hunter")
            
            elif choice == "5":
                console.print("\n[bold]Clearbit API Setup[/bold]")
                console.print("[dim]Get API key from: https://clearbit.com/api[/dim]")
                console.print("[yellow]Cost: $99-$999/month[/yellow]")
                api_key = console.input("Enter Clearbit API key: ").strip()
                if api_key:
                    self.update_api_key("clearbit", api_key)
                    console.print("[green]✓ Clearbit API configured[/green]")
                    self.test_api_connection("clearbit")
            
            elif choice == "6":
                console.print("\n[bold]BuiltWith API Setup[/bold]")
                console.print("[dim]Get API key from: https://builtwith.com/api[/dim]")
                console.print("[yellow]Cost: $295-$1995/month[/yellow]")
                api_key = console.input("Enter BuiltWith API key: ").strip()
                if api_key:
                    self.update_api_key("builtwith", api_key)
                    console.print("[green]✓ BuiltWith API configured[/green]")
                    self.test_api_connection("builtwith")
            
            elif choice == "7":
                self.add_custom_api()
            
            elif choice == "8":
                break
            
            else:
                console.print("[red]Invalid choice![/red]")
    
    def add_custom_api(self):
        """Add a custom API"""
        console.print("\n[bold cyan]🆕 Add Custom API[/bold cyan]")
        
        api_name = console.input("API name (e.g., 'my_custom_api'): ").strip()
        if not api_name:
            console.print("[red]API name required![/red]")
            return
        
        display_name = console.input("Display name (e.g., 'My Custom API'): ").strip() or api_name.title()
        api_key = console.input("API key: ").strip()
        base_url = console.input("Base URL (e.g., https://api.example.com/v1/): ").strip()
        
        if not api_key:
            console.print("[yellow]Warning: No API key provided[/yellow]")
        
        api_config = {
            "name": display_name,
            "api_key": api_key,
            "base_url": base_url,
            "status": "active" if api_key else "inactive",
            "rate_limit": 1000,
            "used_today": 0,
            "last_used": None,
            "description": "Custom API added by user"
        }
        
        self.add_api("apis", api_name, api_config)
        console.print(f"[green]✓ Custom API '{display_name}' added[/green]")
        
        if api_key:
            test = console.input("Test connection now? (y/n): ").strip().lower()
            if test == 'y':
                self.test_api_connection(api_name)
