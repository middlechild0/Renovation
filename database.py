# database.py
import sqlite3
from datetime import datetime, timedelta
import json
from typing import List, Dict, Optional
import hashlib

class BusinessDatabase:
    def __init__(self, db_path: str = "businesses.db"):
        self.db_path = db_path
        self.init_database()
    
    def init_database(self):
        """Initialize database with all required tables"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Businesses table
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS businesses (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            fsq_id TEXT UNIQUE,
            name TEXT NOT NULL,
            address TEXT,
            locality TEXT,
            region TEXT,
            postcode TEXT,
            country TEXT,
            latitude REAL,
            longitude REAL,
            phone TEXT,
            email TEXT,
            website TEXT,
            category TEXT,
            category_id TEXT,
            
            -- Website Analysis Fields (Legacy)
            website_score INTEGER DEFAULT 0,
            mobile_friendly BOOLEAN DEFAULT FALSE,
            has_ssl BOOLEAN DEFAULT FALSE,
            load_time REAL DEFAULT 0,
            tech_stack TEXT DEFAULT '[]',
            issues TEXT DEFAULT '[]',
            last_analyzed TIMESTAMP,
            
            -- Comprehensive Analysis Fields (New)
            comprehensive_analysis TEXT DEFAULT '{}',
            has_website BOOLEAN,
            website_status TEXT,
            tier INTEGER DEFAULT 4,
            tier_assignment TEXT,
            critical_failures_count INTEGER DEFAULT 0,
            critical_issues_count INTEGER DEFAULT 0,
            high_priority_issues_count INTEGER DEFAULT 0,
            medium_priority_issues_count INTEGER DEFAULT 0,
            low_priority_issues_count INTEGER DEFAULT 0,
            comprehensive_score INTEGER DEFAULT 0,
            
            -- Lead Scoring
            lead_score INTEGER DEFAULT 0,
            priority TEXT DEFAULT 'low',
            needs_redesign BOOLEAN DEFAULT FALSE,
            has_contact_form BOOLEAN DEFAULT FALSE,
            
            -- Status Tracking
            is_active BOOLEAN DEFAULT TRUE,
            is_contacted BOOLEAN DEFAULT FALSE,
            contact_date TIMESTAMP,
            
            -- Metadata
            source TEXT DEFAULT 'foursquare',
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            last_checked TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
        ''')
        
        # Categories table
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS categories (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            fsq_category_id TEXT UNIQUE,
            name TEXT NOT NULL,
            parent_category TEXT,
            icon_prefix TEXT,
            icon_suffix TEXT
        )
        ''')
        
        # Locations table (for tracking scraped areas)
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS locations (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            location_hash TEXT UNIQUE,
            city TEXT NOT NULL,
            country TEXT,
            latitude REAL,
            longitude REAL,
            radius INTEGER DEFAULT 5000,
            total_businesses INTEGER DEFAULT 0,
            last_scraped TIMESTAMP,
            next_scrape TIMESTAMP,
            is_completed BOOLEAN DEFAULT FALSE
        )
        ''')
        
        # Scraping jobs table
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS scraping_jobs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            location_hash TEXT,
            category_id TEXT,
            status TEXT DEFAULT 'pending',
            businesses_found INTEGER DEFAULT 0,
            started_at TIMESTAMP,
            completed_at TIMESTAMP,
            error_message TEXT
        )
        ''')
        
        # Create indices
        cursor.execute('CREATE INDEX IF NOT EXISTS idx_businesses_fsq_id ON businesses(fsq_id)')
        cursor.execute('CREATE INDEX IF NOT EXISTS idx_businesses_website_score ON businesses(website_score)')
        cursor.execute('CREATE INDEX IF NOT EXISTS idx_businesses_tier ON businesses(tier)')
        cursor.execute('CREATE INDEX IF NOT EXISTS idx_businesses_category ON businesses(category)')
        cursor.execute('CREATE INDEX IF NOT EXISTS idx_businesses_location ON businesses(latitude, longitude)')
        cursor.execute('CREATE INDEX IF NOT EXISTS idx_locations_hash ON locations(location_hash)')
        
        conn.commit()
        conn.close()
    
    def add_business(self, business_data: Dict) -> bool:
        """Add or update a business in the database"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            # Check if business already exists
            cursor.execute('SELECT id FROM businesses WHERE fsq_id = ?', (business_data.get('fsq_id'),))
            existing = cursor.fetchone()
            
            if existing:
                # Update existing business
                query = '''
                UPDATE businesses SET 
                    name = ?, address = ?, locality = ?, region = ?, 
                    postcode = ?, country = ?, latitude = ?, longitude = ?,
                    phone = ?, email = ?, website = ?, category = ?,
                    category_id = ?, updated_at = CURRENT_TIMESTAMP,
                    last_checked = CURRENT_TIMESTAMP
                WHERE fsq_id = ?
                '''
                params = (
                    business_data.get('name'),
                    business_data.get('address'),
                    business_data.get('locality'),
                    business_data.get('region'),
                    business_data.get('postcode'),
                    business_data.get('country'),
                    business_data.get('latitude'),
                    business_data.get('longitude'),
                    business_data.get('phone'),
                    business_data.get('email'),
                    business_data.get('website'),
                    business_data.get('category'),
                    business_data.get('category_id'),
                    business_data.get('fsq_id')
                )
                cursor.execute(query, params)
            else:
                # Insert new business
                query = '''
                INSERT INTO businesses (
                    fsq_id, name, address, locality, region, postcode,
                    country, latitude, longitude, phone, email, website,
                    category, category_id
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                '''
                params = (
                    business_data.get('fsq_id'),
                    business_data.get('name'),
                    business_data.get('address'),
                    business_data.get('locality'),
                    business_data.get('region'),
                    business_data.get('postcode'),
                    business_data.get('country'),
                    business_data.get('latitude'),
                    business_data.get('longitude'),
                    business_data.get('phone'),
                    business_data.get('email'),
                    business_data.get('website'),
                    business_data.get('category'),
                    business_data.get('category_id')
                )
                cursor.execute(query, params)
            
            conn.commit()
            conn.close()
            return True
            
        except Exception as e:
            print(f"Error adding business: {e}")
            return False
    
    def update_comprehensive_analysis(self, fsq_id: str, analysis: Dict):
        """Update business with comprehensive website analysis results"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            # Calculate lead score from comprehensive analysis
            lead_score = self._calculate_lead_score_from_comprehensive(analysis)
            
            # Extract tier from analysis
            tier = self._tier_to_number(analysis.get('tier', 'TIER_4'))
            
            query = '''
            UPDATE businesses SET
                comprehensive_analysis = ?,
                has_website = ?,
                website_status = ?,
                tier = ?,
                tier_assignment = ?,
                critical_failures_count = ?,
                critical_issues_count = ?,
                high_priority_issues_count = ?,
                medium_priority_issues_count = ?,
                low_priority_issues_count = ?,
                comprehensive_score = ?,
                lead_score = ?,
                priority = ?,
                last_analyzed = CURRENT_TIMESTAMP,
                updated_at = CURRENT_TIMESTAMP
            WHERE fsq_id = ?
            '''
            
            params = (
                json.dumps(analysis),
                analysis.get('has_website', False),
                analysis.get('website_status', 'unknown'),
                tier,
                analysis.get('tier', 'TIER_4'),
                len(analysis.get('critical_failures', [])),
                len(analysis.get('critical_issues', [])),
                len(analysis.get('high_priority_issues', [])),
                len(analysis.get('medium_priority_issues', [])),
                len(analysis.get('low_priority_issues', [])),
                analysis.get('total_score', 0),
                lead_score,
                self._tier_to_priority(tier),
                fsq_id
            )
            
            cursor.execute(query, params)
            conn.commit()
            conn.close()
            
        except Exception as e:
            print(f"Error updating comprehensive analysis: {e}")
    
    def update_website_analysis(self, fsq_id: str, analysis: Dict):
        """Update business with website analysis results (legacy)"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            # Calculate lead score based on analysis
            lead_score = self._calculate_lead_score(analysis)
            
            query = '''
            UPDATE businesses SET
                website_score = ?,
                mobile_friendly = ?,
                has_ssl = ?,
                load_time = ?,
                tech_stack = ?,
                issues = ?,
                lead_score = ?,
                priority = ?,
                needs_redesign = ?,
                has_contact_form = ?,
                last_analyzed = CURRENT_TIMESTAMP,
                updated_at = CURRENT_TIMESTAMP
            WHERE fsq_id = ?
            '''
            
            params = (
                analysis.get('score', 0),
                analysis.get('mobile_friendly', False),
                analysis.get('has_ssl', False),
                analysis.get('load_time', 0),
                json.dumps(analysis.get('tech_stack', [])),
                json.dumps(analysis.get('issues', [])),
                lead_score,
                'high' if lead_score > 70 else 'medium' if lead_score > 40 else 'low',
                analysis.get('needs_redesign', False),
                analysis.get('has_contact_form', False),
                fsq_id
            )
            
            cursor.execute(query, params)
            conn.commit()
            conn.close()
            
        except Exception as e:
            print(f"Error updating analysis: {e}")
    
    def _tier_to_number(self, tier_str: str) -> int:
        """Convert tier string to number"""
        tier_map = {
            'TIER_1': 1,
            'TIER_2': 2,
            'TIER_3': 3,
            'TIER_4': 4,
            'UNKNOWN': 0
        }
        return tier_map.get(tier_str, 4)
    
    def _tier_to_priority(self, tier_num: int) -> str:
        """Convert tier number to priority"""
        tier_map = {
            1: 'high',
            2: 'high',
            3: 'medium',
            4: 'low',
            0: 'low'
        }
        return tier_map.get(tier_num, 'low')
    
    def _calculate_lead_score_from_comprehensive(self, analysis: Dict) -> int:
        """Calculate lead score from comprehensive analysis"""
        score = 100
        
        # Reduce score based on issues
        score -= len(analysis.get('critical_failures', [])) * 50
        score -= len(analysis.get('critical_issues', [])) * 10
        score -= len(analysis.get('high_priority_issues', [])) * 5
        score -= len(analysis.get('medium_priority_issues', [])) * 3
        score -= len(analysis.get('low_priority_issues', [])) * 1
        
        return max(0, min(score, 100))
    
    def _calculate_lead_score(self, analysis: Dict) -> int:
        """Calculate lead score based on website issues"""
        score = 0
        
        # High priority issues (add more points)
        if not analysis.get('has_ssl', False):
            score += 30
        if not analysis.get('mobile_friendly', False):
            score += 25
        if analysis.get('load_time', 0) > 5:  # > 5 seconds
            score += 20
        if analysis.get('needs_redesign', False):
            score += 15
        if not analysis.get('has_contact_form', False):
            score += 10
            
        # Tech stack issues
        outdated_tech = analysis.get('outdated_tech', [])
        score += min(len(outdated_tech) * 5, 20)
        
        return min(score, 100)
    
    def get_businesses_by_tier(self, tier: int = 1, limit: int = 100) -> List[Dict]:
        """Get businesses by tier"""
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        
        cursor.execute('''
        SELECT * FROM businesses 
        WHERE tier = ? 
        AND is_active = TRUE 
        AND is_contacted = FALSE
        ORDER BY lead_score DESC 
        LIMIT ?
        ''', (tier, limit))
        
        results = [dict(row) for row in cursor.fetchall()]
        conn.close()
        return results
    
    def get_businesses_by_score(self, min_score: int = 50, limit: int = 100) -> List[Dict]:
        """Get businesses with website score above threshold"""
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        
        cursor.execute('''
        SELECT * FROM businesses 
        WHERE website_score >= ? 
        AND is_active = TRUE 
        AND is_contacted = FALSE
        ORDER BY website_score DESC 
        LIMIT ?
        ''', (min_score, limit))
        
        results = [dict(row) for row in cursor.fetchall()]
        conn.close()
        return results
    
    def get_statistics(self) -> Dict:
        """Get database statistics"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        stats = {}
        
        # Total businesses
        cursor.execute('SELECT COUNT(*) FROM businesses')
        stats['total_businesses'] = cursor.fetchone()[0]
        
        # Businesses with websites
        cursor.execute('SELECT COUNT(*) FROM businesses WHERE website IS NOT NULL AND website != ""')
        stats['with_websites'] = cursor.fetchone()[0]
        
        # Analyzed websites
        cursor.execute('SELECT COUNT(*) FROM businesses WHERE last_analyzed IS NOT NULL')
        stats['analyzed'] = cursor.fetchone()[0]
        
        # Comprehensive analysis done
        cursor.execute('SELECT COUNT(*) FROM businesses WHERE comprehensive_analysis != \'{}\'')
        stats['comprehensively_analyzed'] = cursor.fetchone()[0]
        
        # Tier distribution
        cursor.execute('SELECT COUNT(*) FROM businesses WHERE tier = 1')
        stats['tier_1_count'] = cursor.fetchone()[0]
        
        cursor.execute('SELECT COUNT(*) FROM businesses WHERE tier = 2')
        stats['tier_2_count'] = cursor.fetchone()[0]
        
        cursor.execute('SELECT COUNT(*) FROM businesses WHERE tier = 3')
        stats['tier_3_count'] = cursor.fetchone()[0]
        
        cursor.execute('SELECT COUNT(*) FROM businesses WHERE tier = 4')
        stats['tier_4_count'] = cursor.fetchone()[0]
        
        # Lead distribution
        cursor.execute('SELECT COUNT(*) FROM businesses WHERE lead_score >= 70')
        stats['high_priority'] = cursor.fetchone()[0]
        
        cursor.execute('SELECT COUNT(*) FROM businesses WHERE lead_score BETWEEN 40 AND 69')
        stats['medium_priority'] = cursor.fetchone()[0]
        
        cursor.execute('SELECT COUNT(*) FROM businesses WHERE lead_score < 40')
        stats['low_priority'] = cursor.fetchone()[0]
        
        conn.close()
        return stats
