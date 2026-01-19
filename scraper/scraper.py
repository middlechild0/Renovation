# scraper.py
import requests
import time
from typing import List, Dict, Optional
import json
from datetime import datetime
import hashlib
from config import config

class FoursquareScraper:
    def __init__(self, api_key: str = config.FOURSQUARE_API_KEY):
        self.api_key = api_key
        self.headers = {
            "Accept": "application/json",
            "Authorization": self.api_key
        }
        self.base_url = "https://api.foursquare.com/v3/places"
        
    def search_places(self, lat: float, lng: float, category_id: str, 
                     radius: int = 5000, limit: int = 50) -> List[Dict]:
        """Search for places near a location"""
        url = f"{self.base_url}/search"
        
        params = {
            "ll": f"{lat},{lng}",
            "radius": radius,
            "categories": category_id,
            "limit": min(limit, 50),  # Foursquare max is 50 per request
            "fields": "fsq_id,name,geocodes,location,categories,website,tel,email"
        }
        
        try:
            response = requests.get(url, headers=self.headers, params=params, timeout=30)
            response.raise_for_status()
            data = response.json()
            
            businesses = []
            for place in data.get('results', []):
                business = self._parse_place_data(place)
                if business:
                    businesses.append(business)
            
            return businesses
            
        except requests.exceptions.HTTPError as e:
            if response.status_code == 401:
                print(f"\n❌ API Authentication Failed (401 Unauthorized)")
                print(f"Your Foursquare API key is invalid or expired.")
                print(f"\nTo fix this:")
                print(f"1. Go to https://foursquare.com/developers/")
                print(f"2. Sign up/login and create a new project")
                print(f"3. Get your API key")
                print(f"4. Update it in config.py or use option 11 (Manage APIs) in quick_start.py\n")
            else:
                print(f"Error searching places: {e}")
            return []
        except requests.exceptions.RequestException as e:
            print(f"Error searching places: {e}")
            return []
    
    def get_place_details(self, fsq_id: str) -> Optional[Dict]:
        """Get detailed information for a specific place"""
        url = f"{self.base_url}/{fsq_id}"
        
        params = {
            "fields": "fsq_id,name,geocodes,location,categories,website,tel,email,hours,rating,price,photos"
        }
        
        try:
            response = requests.get(url, headers=self.headers, params=params, timeout=30)
            response.raise_for_status()
            place = response.json()
            return self._parse_place_data(place, detailed=True)
            
        except requests.exceptions.RequestException as e:
            print(f"Error getting place details: {e}")
            return None
    
    def _parse_place_data(self, place: Dict, detailed: bool = False) -> Optional[Dict]:
        """Parse Foursquare place data into our format"""
        try:
            fsq_id = place.get('fsq_id')
            if not fsq_id:
                return None
            
            # Get location
            location = place.get('location', {})
            geocodes = place.get('geocodes', {}).get('main', {})
            
            # Get categories
            categories = place.get('categories', [])
            primary_category = categories[0] if categories else {}
            
            business_data = {
                'fsq_id': fsq_id,
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
            
            if detailed:
                # Add additional details if available
                business_data.update({
                    'hours': place.get('hours', {}),
                    'rating': place.get('rating', 0),
                    'price': place.get('price', 0),
                    'photos': len(place.get('photos', []))
                })
            
            return business_data
            
        except Exception as e:
            print(f"Error parsing place data: {e}")
            return None
    
    def _clean_website(self, website: str) -> str:
        """Clean and validate website URL"""
        if not website:
            return ""
        
        website = website.strip()
        
        # Add http:// if missing
        if not website.startswith(('http://', 'https://')):
            website = 'https://' + website
        
        # Remove tracking parameters
        website = website.split('?')[0]
        
        return website
    
    def search_by_city(self, city_name: str, category_id: str, 
                      radius: int = 10000) -> List[Dict]:
        """Search for places in a city by name"""
        # First, geocode the city name (simplified - in production use geocoding API)
        city_coords = self._geocode_city(city_name)
        
        if not city_coords:
            return []
        
        return self.search_places(
            lat=city_coords['lat'],
            lng=city_coords['lng'],
            category_id=category_id,
            radius=radius
        )
    
    def _geocode_city(self, city_name: str) -> Optional[Dict]:
        """Simple geocoding (for production, use Google Maps or Nominatim API)"""
        # This is a simplified version - you should use a proper geocoding service
        city_map = {
            "london": {"lat": 51.5074, "lng": -0.1278},
            "new york": {"lat": 40.7128, "lng": -74.0060},
            "tokyo": {"lat": 35.6762, "lng": 139.6503},
            "sydney": {"lat": -33.8688, "lng": 151.2093},
            "toronto": {"lat": 43.6532, "lng": -79.3832},
            "berlin": {"lat": 52.5200, "lng": 13.4050},
            "paris": {"lat": 48.8566, "lng": 2.3522},
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
        }
        
        city_lower = city_name.lower()
        for city, coords in city_map.items():
            if city in city_lower:
                return coords
        
        # If city not found in map, warn user
        print(f"\n⚠ City '{city_name}' not in predefined list.")
        print("Available cities: London, New York, Tokyo, Sydney, Toronto, Berlin, Paris,")
        print("Singapore, Dubai, Mumbai, Nairobi, Lagos, Johannesburg, Cairo, Cape Town,")
        print("Accra, Dar es Salaam, Kampala, Addis Ababa, Casablanca")
        print("\nPlease use one of the above cities or add coordinates manually.\n")
        return None
