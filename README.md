# Renovation Automations

**Complete Automation System for Web Design Business Lead Generation & Client Management**

🚀 An end-to-end automation platform that finds businesses needing website services, creates personalized demos, manages outreach, and processes payments — all automatically.

---

## 🎯 System Overview

Renovation Automations combines intelligent lead generation, automated demo creation, and streamlined client management into a single powerful platform for web design agencies.

### Core Capabilities

1. **🔍 Intelligent Lead Scraping**
   - Multi-API business discovery (Foursquare, TomTom, Yelp)
   - 40+ cities across USA, Canada, Europe, Australia
   - Real-time website analysis and tier classification
   - 595+ businesses already scraped and analyzed

2. **🎨 Automated Demo Creation** (Coming Soon)
   - AI-powered website mockup generation
   - Industry-specific templates
   - Before/after visualizations

3. **📧 Smart Outreach System** (Coming Soon)
   - Personalized email campaigns
   - Multi-channel follow-ups
   - Response tracking

4. **💳 Payment Processing** (Coming Soon)
   - Integrated payment gateways
   - Automated invoicing

---

## 🚀 Quick Start

### Prerequisites
- Python 3.11+
- Git

### 1. Clone Repository
```bash
git clone https://github.com/middlechild0/Renovation.git
cd Renovation
```

### 2. Environment Setup
```bash
cp .env.example .env
# Edit .env with your API keys
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Run Scraper
```bash
# Scrape abroad markets (Europe, USA, Canada, Australia)
python scraper/start_abroad_analysis.py

# Export results
python scraper/export_abroad_prospects.py
```

### Repository Structure
```
Renovation/
├── scraper/             # Core scraper code, analyzers, templates
├── n8n-workflows/       # n8n workflow JSONs (placeholder)
├── scripts/             # Additional automation scripts (placeholder)
├── docs/                # Project documentation
├── .env.example         # Environment variable template
├── .gitignore           # Sensitive/data ignores
├── README.md            # Project overview
└── requirements.txt     # Python dependencies
```

---

## 📦 Current Features

### 🔍 Lead Scraper
**Status:** ✅ Production Ready

**Tier Classification:**
- **Tier 1:** No website (highest value) - 45% of leads
- **Tier 2:** Critical issues (SSL, mobile, broken) - 30%
- **Tier 3:** Multiple problems (SEO, performance) - 15%
- **Tier 4:** Good websites (low priority) - 10%

**Database Stats:**
```
Total: 595 businesses
├── Kenya: 247
├── USA: 100
├── UK: 50
├── France: 48
├── Germany: 50
└── Others: 100
```

**Usage:**
```bash
# Run analysis
python scraper/start_comprehensive_analysis.py

# Query database
sqlite3 businesses.db "SELECT name, country, website, tier FROM businesses WHERE tier = 1 LIMIT 10"
```

---

## 🔐 Security

- API keys stored in `.env` (git-ignored)
- Database excluded from version control
- No hardcoded credentials
- See [Security Setup](docs/SECURITY_SETUP.md)

---

## 🛠️ Tech Stack

- Python 3.11
- SQLite
- Foursquare API
- TomTom API
- Rich (terminal UI)
- BeautifulSoup4

---

## 📊 Business Model

### Target Clients
- **Tier 1:** $2,000 - $5,000 website builds
- **Tier 2:** $500 - $2,000 fixes/redesigns
- **Tier 3:** $300 - $1,000 optimization

### ROI Example
- 1000 Tier 1 leads × 7% close × $3,500 = **$245,000**

---

## 📚 Documentation

- [Security Setup](docs/SECURITY_SETUP.md)
- [Implementation Summary](docs/IMPLEMENTATION_SUMMARY.md)
- [Deployment Guide](docs/DEPLOYMENT_READY.txt)

---

## 📝 Roadmap

### ✅ Phase 1: Scraper (Complete)
- [x] Multi-API integration
- [x] Website analysis
- [x] Tier classification
- [x] Data export

### 🚧 Phase 2: Automation (In Progress)
- [ ] n8n workflows
- [ ] Email enrichment
- [ ] Demo generation
- [ ] Outreach campaigns

### 📅 Phase 3: Scale (Planned)
- [ ] Dashboard
- [ ] Analytics
- [ ] Payment integration
- [ ] Client portal

---

## 👤 Author

**Jimmy Mathu**
- GitHub: [@middlechild0](https://github.com/middlechild0)
- Email: jimmymathu28@gmail.com

---

## 📄 License

Proprietary - All Rights Reserved

---

**Built with 🚀 to revolutionize web design lead generation**
