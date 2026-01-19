# api_test.py
#!/usr/bin/env python3
"""
Simple API Testing Script
Test individual APIs without the full interface
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from api_manager import APIManager
from rich.console import Console

console = Console()

def main():
    """Test APIs from command line"""
    if len(sys.argv) > 1:
        # Test specific API
        api_name = sys.argv[1]
        manager = APIManager()
        success = manager.test_api_connection(api_name)
        sys.exit(0 if success else 1)
    else:
        # Show help
        console.print("[bold cyan]API Testing Tool[/bold cyan]")
        console.print("\nUsage:")
        console.print("  python api_test.py [api_name]")
        console.print("\nAvailable APIs: foursquare, yelp, tomtom, hunter, clearbit, builtwith")
        console.print("\nExamples:")
        console.print("  python api_test.py foursquare")
        console.print("  python api_test.py hunter")

if __name__ == "__main__":
    main()
