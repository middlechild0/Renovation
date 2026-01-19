# config.py
import os
from dataclasses import dataclass
from typing import List, Dict
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

@dataclass
class Config:
    # Foursquare API
    FOURSQUARE_API_KEY = os.getenv("FOURSQUARE_API_KEY", "")
    FOURSQUARE_API_URL = "https://api.foursquare.com/v3/places/search"
    
    # Database
    DATABASE_PATH = "businesses.db"
    
    # Categories to search (global)
    CATEGORIES = [
        "13003",  # Coffee Shop
        "13026",  # Restaurant
        "13035",  # Doctor
        "13038",  # Lawyer
        "13040",  # Dentist
        "13041",  # Real Estate Agent
        "13044",  # Accountant
        "10027",  # Spa
        "10032",  # Gym
        "17014",  # Auto Repair
        "17043",  # Plumber
        "17069",  # Electrician
    ]
    
    # Popular global cities for initial setup
    CITIES = [
        {"name": "London, UK", "lat": 51.5074, "lng": -0.1278},
        {"name": "New York, USA", "lat": 40.7128, "lng": -74.0060},
        {"name": "Tokyo, Japan", "lat": 35.6762, "lng": 139.6503},
        {"name": "Sydney, Australia", "lat": -33.8688, "lng": 151.2093},
        {"name": "Toronto, Canada", "lat": 43.6532, "lng": -79.3832},
        {"name": "Berlin, Germany", "lat": 52.5200, "lng": 13.4050},
        {"name": "Paris, France", "lat": 48.8566, "lng": 2.3522},
        {"name": "Singapore", "lat": 1.3521, "lng": 103.8198},
        {"name": "Dubai, UAE", "lat": 25.2048, "lng": 55.2708},
        {"name": "Mumbai, India", "lat": 19.0760, "lng": 72.8777},
    ]
    
    # Website analysis settings
    ANALYSIS_SETTINGS = {
        "timeout": 10,
        "user_agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
        "check_ssl": True,
        "check_mobile": True,
        "check_performance": True,
    }
    
    # Email finder (using Hunter.io - you'll need to sign up)
    HUNTER_API_KEY = os.getenv("HUNTER_API_KEY", "")  # Get from hunter.io
    CLEARBIT_API_KEY = os.getenv("CLEARBIT_API_KEY", "")  # Optional: for company enrichment
    
    # Export settings
    EXPORT_FORMATS = ["csv", "xlsx", "json"]
    BATCH_SIZE = 100

# Add this to your existing config.py, or create a new section

# API Configuration Management
class APIManager:
    """Manage multiple API configurations"""
    
    def __init__(self):
        self.api_configs = {
            "foursquare": {
                "name": "Foursquare",
                "api_key": os.getenv("FOURSQUARE_API_KEY", ""),
                "base_url": "https://api.foursquare.com/v3/",
                "status": "active",  # active, inactive, testing
                "rate_limit": 95000,  # daily limit
                "used_today": 0,
                "last_used": None,
                "categories": {
                    "13003": "Coffee Shop",
                    "13026": "Restaurant",
                    "13035": "Doctor",
                    "13038": "Lawyer",
                    "13040": "Dentist",
                    "13041": "Real Estate",
                    "13044": "Accountant"
                }
            },
            "yelp": {
                "name": "Yelp Fusion",
                "api_key": "",
                "base_url": "https://api.yelp.com/v3/",
                "status": "inactive",
                "rate_limit": 500,
                "used_today": 0,
                "last_used": None
            },
            "google_places": {
                "name": "Google Places",
                "api_key": "",
                "base_url": "https://maps.googleapis.com/maps/api/place/",
                "status": "inactive",
                "rate_limit": 1000,
                "used_today": 0,
                "last_used": None
            },
            "tomtom": {
                "name": "TomTom Places",
                "api_key": "",
                "base_url": "https://api.tomtom.com/search/2/",
                "status": "inactive",
                "rate_limit": 2500,
                "used_today": 0,
                "last_used": None
            }
        }
        
        self.active_apis = ["foursquare"]  # Which APIs are currently active
        
        # Alternative APIs for business data
        self.alternative_apis = {
            "hunter": {
                "name": "Hunter.io",
                "purpose": "Email finding",
                "url": "https://hunter.io",
                "cost": "$49-$499/month",
                "coverage": "200M+ emails"
            },
            "clearbit": {
                "name": "Clearbit",
                "purpose": "Company enrichment",
                "url": "https://clearbit.com",
                "cost": "$99-$999/month",
                "coverage": "50M+ companies"
            },
            "builtwith": {
                "name": "BuiltWith",
                "purpose": "Tech stack analysis",
                "url": "https://builtwith.com",
                "cost": "$295-$1995/month",
                "coverage": "1B+ websites"
            },
            "apollo": {
                "name": "Apollo.io",
                "purpose": "B2B database",
                "url": "https://apollo.io",
                "cost": "$99-$1500/month",
                "coverage": "265M+ contacts"
            },
            "zoominfo": {
                "name": "ZoomInfo",
                "purpose": "Enterprise B2B",
                "url": "https://zoominfo.com",
                "cost": "$15,000+/year",
                "coverage": "100M+ companies"
            }
        }
    
    def get_active_api(self, service="foursquare"):
        """Get API configuration for a service"""
        return self.api_configs.get(service)
    
    def update_api_key(self, service, api_key):
        """Update API key for a service"""
        if service in self.api_configs:
            self.api_configs[service]["api_key"] = api_key
            self.api_configs[service]["status"] = "active"
            if service not in self.active_apis:
                self.active_apis.append(service)
            return True
        return False
    
    def test_api(self, service):
        """Test if API is working"""
        api_config = self.get_active_api(service)
        if not api_config:
            return False, "API not configured"
        
        # This would be implemented in the actual test
        return True, "Test not implemented for this API"

# Add this to your config class or create a new instance
api_manager = APIManager()

config = Config()
