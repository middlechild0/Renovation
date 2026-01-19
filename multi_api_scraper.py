# multi_api_scraper.py
"""
Multi-API Business Scraper
Uses multiple APIs with automatic fallback for reliability
"""
import requests
import time
from typing import List, Dict, Optional
import json
from datetime import datetime
from api_manager import APIManager
from rich.console import Console

console = Console()

class MultiAPIScraper:
    """Scraper that uses multiple place APIs with automatic fallback"""
    
    def __init__(self):
        self.api_manager = APIManager()
        self.active_apis = self._get_active_apis()
        
    def _get_active_apis(self) -> List[str]:
        """Get list of active place APIs"""
        active = []
        for api_name, config in self.api_manager.configs.get("apis", {}).items():
            if config.get("api_key") and config.get("category") == "places":
                active.append(api_name)
        
        # Prioritize by reliability and coverage
        priority_order = ["tomtom", "foursquare", "yelp", "openstreetmap"]
        sorted_active = []
        for api in priority_order:
            if api in active:
                sorted_active.append(api)
        
        return sorted_active
    
    def search_all_apis(self, city_name: str, category: str, radius: int = 5000) -> List[Dict]:
        """Search using ALL available APIs to maximize results"""
        
        # Get city coordinates
        coords = self._geocode_city(city_name)
        if not coords:
            console.print(f"[yellow]⚠ Could not find coordinates for '{city_name}'[/yellow]")
            return []
        
        lat, lng = coords['lat'], coords['lng']
        console.print(f"[dim]Searching at coordinates: {lat}, {lng}[/dim]")
        
        # Collect results from ALL active APIs (not just until we get 10)
        all_results = []
        apis_tried = []
        
        for api_name in self.active_apis:
            apis_tried.append(api_name)
            console.print(f"[cyan]Trying {api_name.upper()}...[/cyan]", end=" ")
            
            try:
                if api_name == "foursquare":
                    results = self._search_foursquare(lat, lng, category, radius)
                elif api_name == "tomtom":
                    results = self._search_tomtom(lat, lng, category, radius)
                elif api_name == "yelp":
                    results = self._search_yelp(lat, lng, category, radius)
                else:
                    console.print("[dim]Not supported[/dim]")
                    continue
                
                if results:
                    console.print(f"[green]Found {len(results)} ✓[/green]")
                    all_results.extend(results)
                else:
                    console.print(f"[yellow]No results[/yellow]")
                    
            except Exception as e:
                console.print(f"[red]Failed[/red]")
                continue
        
        if not all_results:
            console.print(f"\n[red]❌ No results from any API[/red]")
            console.print(f"[yellow]APIs tried: {', '.join(apis_tried)}[/yellow]")
        
        # Remove duplicates based on name + address
        unique_results = self._deduplicate_results(all_results)
        console.print(f"[dim]Total after deduplication: {len(unique_results)} unique businesses[/dim]")
        return unique_results
    
    def search_by_city(self, city_name: str, category: str, radius: int = 5000) -> List[Dict]:
        """Search using multiple APIs with automatic fallback"""
        
        # Get city coordinates
        coords = self._geocode_city(city_name)
        if not coords:
            console.print(f"[yellow]⚠ Could not find coordinates for '{city_name}'[/yellow]")
            return []
        
        lat, lng = coords['lat'], coords['lng']
        console.print(f"[dim]Searching at coordinates: {lat}, {lng}[/dim]")
        
        # Try each active API until we get results
        all_results = []
        apis_tried = []
        
        for api_name in self.active_apis:
            apis_tried.append(api_name)
            console.print(f"[cyan]Trying {api_name.upper()} API...[/cyan]")
            
            try:
                if api_name == "foursquare":
                    results = self._search_foursquare(lat, lng, category, radius)
                elif api_name == "tomtom":
                    results = self._search_tomtom(lat, lng, category, radius)
                elif api_name == "yelp":
                    results = self._search_yelp(lat, lng, category, radius)
                else:
                    continue
                
                if results:
                    console.print(f"[green]✅ {api_name.upper()}: Found {len(results)} businesses[/green]")
                    all_results.extend(results)
                    
                    # If we have good results, we can stop
                    if len(all_results) >= 10:
                        break
                else:
                    console.print(f"[yellow]⚠ {api_name.upper()}: No results[/yellow]")
                    
            except Exception as e:
                console.print(f"[red]❌ {api_name.upper()} failed: {str(e)[:100]}[/red]")
                continue
        
        if not all_results:
            console.print(f"\n[red]❌ No results from any API[/red]")
            console.print(f"[yellow]APIs tried: {', '.join(apis_tried)}[/yellow]")
            console.print(f"[cyan]💡 Tip: Configure more APIs in quick_start.py (Option 11)[/cyan]\n")
        
        # Remove duplicates based on name + address
        unique_results = self._deduplicate_results(all_results)
        return unique_results
    
    def _search_foursquare(self, lat: float, lng: float, category: str, radius: int) -> List[Dict]:
        """Search using Foursquare API"""
        api_config = self.api_manager.configs["apis"]["foursquare"]
        api_key = api_config.get("api_key")
        
        if not api_key:
            return []
        
        # Map generic category to Foursquare category ID
        category_map = {
            "coffee": "13003",
            "restaurant": "13026",
            "doctor": "13035",
            "lawyer": "13038",
            "dentist": "13040",
            "real_estate": "13041",
            "accountant": "13044"
        }
        
        category_id = category_map.get(category, "13026")
        
        url = "https://api.foursquare.com/v3/places/search"
        headers = {
            "Accept": "application/json",
            "Authorization": api_key
        }
        params = {
            "ll": f"{lat},{lng}",
            "radius": radius,
            "categories": category_id,
            "limit": 50,
            "fields": "fsq_id,name,geocodes,location,categories,website,tel,email"
        }
        
        response = requests.get(url, headers=headers, params=params, timeout=30)
        
        if response.status_code == 401:
            raise Exception("API key invalid or expired")
        
        response.raise_for_status()
        data = response.json()
        
        results = []
        for place in data.get('results', []):
            business = self._parse_foursquare_data(place)
            if business:
                results.append(business)
        
        return results
    
    def _search_tomtom(self, lat: float, lng: float, category: str, radius: int) -> List[Dict]:
        """Search using TomTom API"""
        api_config = self.api_manager.configs["apis"]["tomtom"]
        api_key = api_config.get("api_key")
        
        if not api_key:
            return []
        
        # Map category to search query
        category_queries = {
            "coffee": "coffee shop",
            "restaurant": "restaurant",
            "doctor": "doctor",
            "lawyer": "lawyer",
            "dentist": "dentist",
            "real_estate": "real estate",
            "accountant": "accountant"
        }
        
        query = category_queries.get(category, "restaurant")
        
        url = f"https://api.tomtom.com/search/2/search/{query}.json"
        params = {
            "key": api_key,
            "lat": lat,
            "lon": lng,
            "radius": radius,
            "limit": 50
        }
        
        response = requests.get(url, params=params, timeout=30)
        
        if response.status_code == 403:
            raise Exception("API key invalid or expired")
        
        response.raise_for_status()
        data = response.json()
        
        results = []
        for place in data.get('results', []):
            business = self._parse_tomtom_data(place)
            if business:
                results.append(business)
        
        return results
    
    def _search_yelp(self, lat: float, lng: float, category: str, radius: int) -> List[Dict]:
        """Search using Yelp API"""
        api_config = self.api_manager.configs["apis"]["yelp"]
        api_key = api_config.get("api_key")
        
        if not api_key:
            return []
        
        url = "https://api.yelp.com/v3/businesses/search"
        headers = {
            "Authorization": f"Bearer {api_key}"
        }
        params = {
            "latitude": lat,
            "longitude": lng,
            "radius": min(radius, 40000),  # Yelp max is 40km
            "categories": category,
            "limit": 50
        }
        
        response = requests.get(url, headers=headers, params=params, timeout=30)
        
        if response.status_code == 401:
            raise Exception("API key invalid or expired")
        
        response.raise_for_status()
        data = response.json()
        
        results = []
        for business in data.get('businesses', []):
            parsed = self._parse_yelp_data(business)
            if parsed:
                results.append(parsed)
        
        return results
    
    def _parse_foursquare_data(self, place: Dict) -> Optional[Dict]:
        """Parse Foursquare place data"""
        try:
            location = place.get('location', {})
            geocodes = place.get('geocodes', {}).get('main', {})
            categories = place.get('categories', [])
            primary_category = categories[0] if categories else {}
            
            return {
                'source_api': 'foursquare',
                'fsq_id': place.get('fsq_id', ''),
                'name': place.get('name', '').strip(),
                'address': location.get('formatted_address', ''),
                'locality': location.get('locality', ''),
                'region': location.get('region', ''),
                'postcode': location.get('postcode', ''),
                'country': location.get('country', ''),
                'latitude': geocodes.get('latitude'),
                'longitude': geocodes.get('longitude'),
                'phone': place.get('tel', '').strip(),
                'email': place.get('email', '').strip(),
                'website': self._clean_website(place.get('website', '')),
                'category': primary_category.get('name', ''),
                'category_id': str(primary_category.get('id', ''))
            }
        except Exception as e:
            console.print(f"[dim]Parse error (Foursquare): {e}[/dim]")
            return None
    
    def _parse_tomtom_data(self, place: Dict) -> Optional[Dict]:
        """Parse TomTom place data"""
        try:
            poi = place.get('poi', {})
            address = place.get('address', {})
            position = place.get('position', {})
            
            return {
                'source_api': 'tomtom',
                'fsq_id': place.get('id', ''),
                'name': poi.get('name', '').strip(),
                'address': address.get('freeformAddress', ''),
                'locality': address.get('municipality', ''),
                'region': address.get('countrySubdivision', ''),
                'postcode': address.get('postalCode', ''),
                'country': address.get('country', ''),
                'latitude': position.get('lat'),
                'longitude': position.get('lon'),
                'phone': poi.get('phone', '').strip(),
                'email': '',
                'website': poi.get('url', '').strip(),
                'category': ', '.join(poi.get('categories', [])),
                'category_id': ''
            }
        except Exception as e:
            console.print(f"[dim]Parse error (TomTom): {e}[/dim]")
            return None
    
    def _parse_yelp_data(self, business: Dict) -> Optional[Dict]:
        """Parse Yelp business data"""
        try:
            location = business.get('location', {})
            coordinates = business.get('coordinates', {})
            
            return {
                'source_api': 'yelp',
                'fsq_id': business.get('id', ''),
                'name': business.get('name', '').strip(),
                'address': ', '.join(location.get('display_address', [])),
                'locality': location.get('city', ''),
                'region': location.get('state', ''),
                'postcode': location.get('zip_code', ''),
                'country': location.get('country', ''),
                'latitude': coordinates.get('latitude'),
                'longitude': coordinates.get('longitude'),
                'phone': business.get('phone', '').strip(),
                'email': '',
                'website': '',
                'category': ', '.join([c.get('title', '') for c in business.get('categories', [])]),
                'category_id': ''
            }
        except Exception as e:
            console.print(f"[dim]Parse error (Yelp): {e}[/dim]")
            return None
    
    def _geocode_city(self, city_name: str) -> Optional[Dict]:
        """Get coordinates for a city"""
        city_map = {
            "london": {"lat": 51.5074, "lng": -0.1278},
            "new york": {"lat": 40.7128, "lng": -74.0060},
            "tokyo": {"lat": 35.6762, "lng": 139.6503},
            "sydney": {"lat": -33.8688, "lng": 151.2093},
            "toronto": {"lat": 43.6532, "lng": -79.3832},
            "berlin": {"lat": 52.5200, "lng": 13.4050},
            "paris": {"lat": 48.8566, "lng": 2.3522},
            "amsterdam": {"lat": 52.3676, "lng": 4.9041},
            "barcelona": {"lat": 41.3851, "lng": 2.1734},
            "rome": {"lat": 41.9028, "lng": 12.4964},
            "madrid": {"lat": 40.4168, "lng": -3.7038},
            "vienna": {"lat": 48.2082, "lng": 16.3738},
            "prague": {"lat": 50.0755, "lng": 14.4378},
            "dublin": {"lat": 53.3498, "lng": -6.2603},
            "vancouver": {"lat": 49.2827, "lng": -123.1207},
            "montreal": {"lat": 45.5017, "lng": -73.5673},
            "calgary": {"lat": 51.0447, "lng": -114.0719},
            "melbourne": {"lat": -37.8136, "lng": 144.9631},
            "brisbane": {"lat": -27.4698, "lng": 153.0251},
            "perth": {"lat": -31.9505, "lng": 115.8605},
            "adelaide": {"lat": -34.9285, "lng": 138.6007},
            "singapore": {"lat": 1.3521, "lng": 103.8198},
            "dubai": {"lat": 25.2048, "lng": 55.2708},
            "mumbai": {"lat": 19.0760, "lng": 72.8777},
            "nairobi": {"lat": -1.2864, "lng": 36.8172},
            "lagos": {"lat": 6.5244, "lng": 3.3792},
            "johannesburg": {"lat": -26.2041, "lng": 28.0473},
            "cairo": {"lat": 30.0444, "lng": 31.2357},
            "cape town": {"lat": -33.9249, "lng": 18.4241},
            "accra": {"lat": 5.6037, "lng": -0.1870},
            "dar es salaam": {"lat": -6.7924, "lng": 39.2083},
            "kampala": {"lat": 0.3476, "lng": 32.5825},
            "addis ababa": {"lat": 9.0320, "lng": 38.7469},
            "casablanca": {"lat": 33.5731, "lng": -7.5898},
            "san francisco": {"lat": 37.7749, "lng": -122.4194},
            "los angeles": {"lat": 34.0522, "lng": -118.2437},
            "chicago": {"lat": 41.8781, "lng": -87.6298},
            "houston": {"lat": 29.7604, "lng": -95.3698},
            "phoenix": {"lat": 33.4484, "lng": -112.0740},
            "philadelphia": {"lat": 39.9526, "lng": -75.1652},
            "san antonio": {"lat": 29.4241, "lng": -98.4936},
            "san diego": {"lat": 32.7157, "lng": -117.1611},
            "dallas": {"lat": 32.7767, "lng": -96.7970},
            "miami": {"lat": 25.7617, "lng": -80.1918},
            "boston": {"lat": 42.3601, "lng": -71.0589},
        }
        
        city_lower = city_name.lower()
        for city, coords in city_map.items():
            if city in city_lower:
                return coords
        
        console.print(f"\n[yellow]⚠ City '{city_name}' not in database.[/yellow]")
        console.print("[dim]Available cities: London, New York, Tokyo, Sydney, Toronto, Berlin, Paris,[/dim]")
        console.print("[dim]Singapore, Dubai, Mumbai, Nairobi, Lagos, Johannesburg, Cairo, and more...[/dim]\n")
        return None
    
    def _clean_website(self, url: str) -> str:
        """Clean and standardize website URL"""
        if not url:
            return ''
        url = url.strip()
        if not url.startswith(('http://', 'https://')):
            url = 'https://' + url
        return url
    
    def _deduplicate_results(self, results: List[Dict]) -> List[Dict]:
        """Remove duplicate businesses based on name and address"""
        seen = set()
        unique = []
        
        for business in results:
            # Create identifier from name + address
            identifier = f"{business.get('name', '').lower()}_{business.get('address', '').lower()}"
            
            if identifier not in seen:
                seen.add(identifier)
                unique.append(business)
        
        if len(results) > len(unique):
            console.print(f"[dim]Removed {len(results) - len(unique)} duplicate(s)[/dim]")
        
        return unique
