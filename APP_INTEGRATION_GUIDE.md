# app.py Integration Guide

## Quick Integration (3 Steps)

### Step 1: Add Import
```python
from comprehensive_analyzer import ComprehensiveAnalyzer
```

### Step 2: Add Function
Copy `analyze_websites_comprehensive()` from comprehensive_integration.py

### Step 3: Update Menu
Add tier-based analysis to your interactive menu

## Usage

```python
# Analyze businesses
results = analyze_websites_comprehensive(businesses)

# Query by tier
tier_1 = db.get_businesses_by_tier(tier=1)  # No websites
tier_2 = db.get_businesses_by_tier(tier=2)  # Critical issues
```

## Complete Setup: ~30 minutes
1. Read this file (5 min)
2. Copy functions (10 min)
3. Test (5 min)
4. Deploy (10 min)

See APP_INTEGRATION_GUIDE.md in code for full functions.
