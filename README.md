# Business Scraper & Analysis Platform

A comprehensive Python-based scraper that finds local businesses worldwide, analyzes their websites, and identifies high-value leads for web development/redesign services.

## 🎯 What This Does

- **Multi-API Scraping**: Fetches business data from Foursquare, TomTom, Yelp, and more
- **Comprehensive Analysis**: Evaluates website quality (SSL, mobile-friendly, performance, SEO)
- **Tier Classification**: Automatically categorizes businesses into 4 tiers based on website issues
- **Lead Scoring**: Identifies businesses most likely to need your services
- **Global Coverage**: Support for 40+ major cities across Europe, USA, Canada, Australia, and Africa

## 🚀 Quick Start

### 1. Clone the Repository
```bash
git clone https://github.com/middlechild0/scraper-project.git
cd scraper-project
```

### 2. Install Dependencies
```bash
pip install -r requirements.txt
```

### 3. Configure API Keys
```bash
# Copy the example environment file
cp .env.example .env

# Edit .env and add your API keys
nano .env
```

Get your free API keys:
- **Foursquare**: https://foursquare.com/developers/ (95,000 requests/day free)
- **TomTom**: https://developer.tomtom.com/ (2,500 requests/day free)
- **Yelp**: https://www.yelp.com/developers (500 requests/day free)

### 4. Run Your First Scrape
```bash
# Scrape businesses outside Africa (Europe, USA, Canada, Australia)
python3 start_abroad_analysis.py

# Or scrape all regions including Africa
python3 start_comprehensive_analysis.py
```

### 5. Export Results
```bash
# Export all businesses to CSV
python3 generate_our_first_clients.py

# Export only abroad prospects
python3 export_abroad_prospects.py
```

## 📊 Features

### Tier Classification System

- **Tier 1** 🚨: No website (highest value - offer to build website)
- **Tier 2** 🔴: Critical issues (SSL, mobile, contact forms)
- **Tier 3** 🟡: Multiple issues (performance, SEO, outdated)
- **Tier 4** 🟢: Good websites (low priority)

### Business Categories Tracked

- Professional Services
- Legal & Accounting
- Marketing & Advertising
- IT & Consulting
- Real Estate
- Travel & Tourism
- Hotels & Restaurants
- Medical Services
- And more...

## 🗂️ Project Structure

```
├── start_abroad_analysis.py       # Main scraper (Europe/USA/Canada/Australia)
├── start_comprehensive_analysis.py # Full global scraper
├── multi_api_scraper.py           # API integration layer
├── comprehensive_analyzer.py      # Website analysis engine
├── database.py                    # SQLite database manager
├── export.py                      # CSV/Excel export utilities
├── config.py                      # Configuration management
├── api_manager.py                 # API key & rate limit management
└── requirements.txt               # Python dependencies
```

## 📈 Database Schema

All scraped data is stored in `businesses.db` (SQLite):

```sql
- Business Info: name, address, location, phone, email, website
- Analysis: tier, scores, issues, last_analyzed
- Lead Scoring: lead_score, priority, needs_redesign
- Status: is_active, is_contacted, contact_date
```

## 🔒 Security

- API keys stored in `.env` file (not tracked in Git)
- Database and exports excluded from version control
- See [SECURITY_SETUP.md](SECURITY_SETUP.md) for details

## 📝 Usage Examples

### Find Tier 1 Prospects (No Website)
```bash
sqlite3 businesses.db "SELECT name, country, phone FROM businesses WHERE tier = 1 LIMIT 10;"
```

### Export High-Priority Leads
```python
from database import BusinessDatabase
db = BusinessDatabase()
tier1_leads = db.get_businesses_by_tier(tier=1, limit=100)
```

### Custom City Search
```python
from multi_api_scraper import MultiAPIScraper
scraper = MultiAPIScraper()
results = scraper.search_all_apis("Berlin", "Professional Services", radius=5000)
```

## 🌍 Supported Cities

**Europe**: London, Paris, Berlin, Amsterdam, Barcelona, Rome, Madrid, Vienna, Prague, Dublin

**USA**: New York, Los Angeles, Chicago, Houston, Phoenix, Philadelphia, San Antonio, San Diego, Dallas, San Francisco

**Canada**: Toronto, Vancouver, Montreal, Calgary

**Australia**: Sydney, Melbourne, Brisbane, Perth, Adelaide

**Africa**: Nairobi, Lagos, Accra (and more)

## 📦 Dependencies

- `requests` - API calls
- `beautifulsoup4` - HTML parsing
- `pandas` - Data export
- `rich` - Terminal UI
- `python-dotenv` - Environment variables
- `sqlite3` - Built-in database

## 🤝 Contributing

Pull requests welcome! For major changes, please open an issue first.

## 📄 License

MIT License - feel free to use for commercial purposes

## 👤 Author

**Jimmy Mathu**
- GitHub: [@middlechild0](https://github.com/middlechild0)
- Email: jimmymathu28@gmail.com

## ⚠️ Disclaimer

Please respect API rate limits and terms of service. This tool is for legitimate lead generation purposes only.

---

**Built with ❤️ for finding business opportunities worldwide**
