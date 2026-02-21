# dashboard.py
from flask import Flask, render_template, jsonify, send_file, request
import json
from datetime import datetime
import sqlite3
from pathlib import Path

app = Flask(__name__)

def get_db_connection():
    conn = sqlite3.connect('businesses.db')
    conn.row_factory = sqlite3.Row
    return conn

@app.route('/')
def index():
    return render_template('dashboard.html')

@app.route('/api/stats')
def get_stats():
    conn = get_db_connection()
    
    stats = {}
    
    # Basic counts
    cursor = conn.cursor()
    cursor.execute('SELECT COUNT(*) FROM businesses')
    stats['total'] = cursor.fetchone()[0]
    
    cursor.execute('SELECT COUNT(*) FROM businesses WHERE website IS NOT NULL')
    stats['with_websites'] = cursor.fetchone()[0]
    
    cursor.execute('SELECT COUNT(*) FROM businesses WHERE last_analyzed IS NOT NULL')
    stats['analyzed'] = cursor.fetchone()[0]
    
    # Score distribution (for quality metric)
    cursor.execute('''
        SELECT 
            SUM(CASE WHEN website_score >= 70 THEN 1 ELSE 0 END) as high,
            SUM(CASE WHEN website_score BETWEEN 40 AND 69 THEN 1 ELSE 0 END) as medium,
            SUM(CASE WHEN website_score < 40 THEN 1 ELSE 0 END) as low
        FROM businesses 
        WHERE website_score > 0
    ''')
    high, medium, low = cursor.fetchone()
    stats['score_distribution'] = {'high': high or 0, 'medium': medium or 0, 'low': low or 0}
    
    # Lead priority distribution (based on lead_score)
    cursor.execute('''
        SELECT 
            SUM(CASE WHEN lead_score >= 70 THEN 1 ELSE 0 END) as high_priority,
            SUM(CASE WHEN lead_score BETWEEN 40 AND 69 THEN 1 ELSE 0 END) as medium_priority,
            SUM(CASE WHEN lead_score < 40 AND lead_score > 0 THEN 1 ELSE 0 END) as low_priority
        FROM businesses 
        WHERE lead_score > 0
    ''')
    high_priority, medium_priority, low_priority = cursor.fetchone()
    stats['lead_distribution'] = {
        'high': high_priority or 0,
        'medium': medium_priority or 0, 
        'low': low_priority or 0
    }
    
    # Category breakdown with lead scores
    cursor.execute('''
        SELECT category, COUNT(*) as count, AVG(lead_score) as avg_lead_score
        FROM businesses 
        WHERE category IS NOT NULL AND lead_score > 0
        GROUP BY category 
        ORDER BY count DESC 
        LIMIT 15
    ''')
    
    categories = []
    for row in cursor.fetchall():
        categories.append({
            'name': row['category'],
            'count': row['count'],
            'avg_lead_score': round(row['avg_lead_score'] or 0, 1)
        })
    stats['categories'] = categories
    
    # Niche opportunities (categories with fewer competitors but high lead scores)
    cursor.execute('''
        SELECT category, COUNT(*) as count, AVG(lead_score) as avg_lead_score
        FROM businesses 
        WHERE category IS NOT NULL AND lead_score >= 60
        GROUP BY category
        HAVING COUNT(*) BETWEEN 1 AND 10
        ORDER BY avg_lead_score DESC
        LIMIT 10
    ''')
    
    niches = []
    for row in cursor.fetchall():
        niches.append({
            'name': row['category'],
            'count': row['count'],
            'avg_lead_score': round(row['avg_lead_score'] or 0, 1)
        })
    stats['niche_opportunities'] = niches
    
    conn.close()
    
    return jsonify(stats)

@app.route('/api/leads')
def get_leads():
    lead_type = request.args.get('type', 'high', type=str)  # high, medium, low, niche
    limit = request.args.get('limit', 50, type=int)
    
    conn = get_db_connection()
    cursor = conn.cursor()
    
    if lead_type == 'high':
        # High priority leads (lead_score >= 70)
        cursor.execute('''
            SELECT name, website, website_score, lead_score, priority, 
                   category, mobile_friendly, has_ssl, needs_redesign,
                   has_contact_form, phone, email, locality
            FROM businesses 
            WHERE lead_score >= 70
            AND is_active = TRUE
            ORDER BY lead_score DESC, website_score DESC
            LIMIT ?
        ''', (limit,))
    
    elif lead_type == 'medium':
        # Medium priority leads
        cursor.execute('''
            SELECT name, website, website_score, lead_score, priority,
                   category, mobile_friendly, has_ssl, needs_redesign,
                   has_contact_form, phone, email, locality
            FROM businesses 
            WHERE lead_score BETWEEN 40 AND 69
            AND is_active = TRUE
            ORDER BY lead_score DESC, website_score DESC
            LIMIT ?
        ''', (limit,))
    
    elif lead_type == 'niche':
        # Niche opportunities: high-quality leads in underserved categories
        cursor.execute('''
            SELECT b.name, b.website, b.website_score, b.lead_score, b.priority,
                   b.category, b.mobile_friendly, b.has_ssl, b.needs_redesign,
                   b.has_contact_form, b.phone, b.email, b.locality,
                   COUNT(*) OVER (PARTITION BY b.category) as category_count
            FROM businesses b
            WHERE b.lead_score >= 60
            AND b.is_active = TRUE
            AND b.category IN (
                SELECT category FROM businesses 
                WHERE category IS NOT NULL AND lead_score >= 60
                GROUP BY category 
                HAVING COUNT(*) BETWEEN 1 AND 10
            )
            ORDER BY b.lead_score DESC, b.website_score DESC
            LIMIT ?
        ''', (limit,))
    
    else:
        # All leads
        cursor.execute('''
            SELECT name, website, website_score, lead_score, priority,
                   category, mobile_friendly, has_ssl, needs_redesign,
                   has_contact_form, phone, email, locality
            FROM businesses 
            WHERE is_active = TRUE
            ORDER BY lead_score DESC, website_score DESC
            LIMIT ?
        ''', (limit,))
    
    leads = []
    for row in cursor.fetchall():
        lead_dict = dict(row)
        # Add status badge
        if lead_dict['lead_score'] >= 70:
            lead_dict['priority_badge'] = '🔴 HIGH'
        elif lead_dict['lead_score'] >= 40:
            lead_dict['priority_badge'] = '🟡 MEDIUM'
        else:
            lead_dict['priority_badge'] = '🟢 LOW'
        
        # Add quality indicators
        lead_dict['quality_score'] = (
            (lead_dict['has_ssl'] * 20) +
            (lead_dict['mobile_friendly'] * 20) +
            (lead_dict['has_contact_form'] * 15) +
            (not lead_dict['needs_redesign'] * 45)
        )
        
        leads.append(lead_dict)
    
    conn.close()
    
    return jsonify(leads)

@app.route('/api/export')
def export_data():
    # Generate export file
    import export
    exporter = export.DataExporter()
    filename = exporter.export_to_excel()
    
    return send_file(filename, as_attachment=True)

if __name__ == '__main__':
    app.run(debug=True, port=5000)
