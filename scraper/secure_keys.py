# SECURITY WARNING - API Keys Found
# Replace these in api_configs.json before pushing to GitHub

import json
import os

def secure_api_configs():
    """Remove API keys from api_configs.json"""
    config_file = "api_configs.json"
    
    if not os.path.exists(config_file):
        print(f"{config_file} not found")
        return
    
    with open(config_file, 'r') as f:
        config = json.load(f)
    
    # Clear all API keys
    for category in ['apis', 'enrichment_apis', 'analysis_apis']:
        if category in config:
            for api_name, api_data in config[category].items():
                if 'api_key' in api_data:
                    api_data['api_key'] = ""
    
    with open(config_file, 'w') as f:
        json.dump(config, f, indent=2)
    
    print(f"✓ Cleared all API keys from {config_file}")
    print("⚠ Remember to set keys in .env file!")

if __name__ == "__main__":
    secure_api_configs()
