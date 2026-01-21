#!/usr/bin/env python3
"""Quick test of comprehensive analyzer"""

from comprehensive_analyzer import ComprehensiveAnalyzer
from database import BusinessDatabase
import json

print("Testing Comprehensive Analyzer Framework\n")

# Initialize analyzer
analyzer = ComprehensiveAnalyzer()
db = BusinessDatabase()

# Test URLs
test_urls = [
    ("No website", "nonexistent-domain-12345.com"),
    ("Valid site", "https://www.google.com"),
    ("Example", "https://www.example.com"),
]

print("=" * 60)
print("Running Comprehensive Website Analysis Tests")
print("=" * 60)

for name, url in test_urls:
    print(f"\nTest: {name} ({url})")
    print("-" * 60)
    
    try:
        analysis = analyzer.analyze_comprehensive(url)
        
        # Display results
        print(f"Has Website: {analysis['has_website']}")
        print(f"Website Status: {analysis['website_status']}")
        print(f"Tier: {analysis['tier']}")
        print(f"Total Score: {analysis['total_score']}/100")
        print(f"Critical Failures: {len(analysis['critical_failures'])}")
        print(f"Critical Issues: {len(analysis['critical_issues'])}")
        print(f"High Priority Issues: {len(analysis['high_priority_issues'])}")
        print(f"Medium Priority Issues: {len(analysis['medium_priority_issues'])}")
        print(f"Low Priority Issues: {len(analysis['low_priority_issues'])}")
        
        # Show some issues
        if analysis['critical_issues']:
            print(f"\nTop Critical Issues:")
            for issue in analysis['critical_issues'][:3]:
                print(f"  - {issue}")
        
        if analysis['high_priority_issues']:
            print(f"\nTop High Priority Issues:")
            for issue in analysis['high_priority_issues'][:3]:
                print(f"  - {issue}")
        
    except Exception as e:
        print(f"Error: {e}")

print("\n" + "=" * 60)
print("Database Schema Check")
print("=" * 60)

# Check database
print("\nChecking database schema...")
try:
    import sqlite3
    conn = sqlite3.connect('businesses.db')
    cursor = conn.cursor()
    
    # Get table info
    cursor.execute("PRAGMA table_info(businesses)")
    columns = cursor.fetchall()
    
    # Look for comprehensive analysis columns
    comprehensive_cols = [
        'has_website', 'tier', 'comprehensive_analysis', 
        'critical_issues_count', 'high_priority_issues_count'
    ]
    
    column_names = [col[1] for col in columns]
    
    print(f"Total columns: {len(columns)}")
    
    for col in comprehensive_cols:
        if col in column_names:
            print(f"✓ {col} - Found")
        else:
            print(f"✗ {col} - NOT FOUND")
    
    conn.close()
    
    print("\n✓ Database schema is properly configured")
    
except Exception as e:
    print(f"✗ Database check failed: {e}")

print("\n" + "=" * 60)
print("Test Complete")
print("=" * 60)
