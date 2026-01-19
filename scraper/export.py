# export.py
import pandas as pd
import json
from datetime import datetime
from typing import List, Dict
import sqlite3
from pathlib import Path

class DataExporter:
    def __init__(self, db_path: str = "businesses.db"):
        self.db_path = db_path
    
    def export_to_excel(self, min_score: int = 50, filename: str = None) -> str:
        """Export high-priority leads to Excel"""
        if filename is None:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"leads_high_priority_{timestamp}.xlsx"
        
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        
        # Get high priority leads
        query = '''
        SELECT 
            name,
            address,
            locality,
            region,
            country,
            phone,
            email,
            website,
            category,
            website_score,
            mobile_friendly,
            has_ssl,
            load_time,
            lead_score,
            priority,
            needs_redesign,
            has_contact_form,
            last_analyzed
        FROM businesses 
        WHERE website_score >= ? 
        AND is_active = TRUE 
        AND is_contacted = FALSE
        ORDER BY lead_score DESC, website_score DESC
        '''
        
        df = pd.read_sql_query(query, conn, params=(min_score,))
        conn.close()
        
        if df.empty:
            print("No leads found matching criteria")
            return ""
        
        # Create Excel writer with multiple sheets
        with pd.ExcelWriter(filename, engine='openpyxl') as writer:
            # Main leads sheet
            df.to_excel(writer, sheet_name='High Priority Leads', index=False)
            
            # Summary statistics
            summary_data = {
                'Metric': ['Total Leads', 'Average Score', 'Needs Redesign', 'Has Contact Form'],
                'Value': [
                    len(df),
                    round(df['website_score'].mean(), 1),
                    df['needs_redesign'].sum(),
                    df['has_contact_form'].sum()
                ]
            }
            summary_df = pd.DataFrame(summary_data)
            summary_df.to_excel(writer, sheet_name='Summary', index=False)
            
            # By category
            category_stats = df.groupby('category').agg({
                'name': 'count',
                'website_score': 'mean',
                'lead_score': 'mean'
            }).round(1)
            category_stats.columns = ['Count', 'Avg Website Score', 'Avg Lead Score']
            category_stats.to_excel(writer, sheet_name='By Category')
            
            # Auto-adjust column widths
            for sheet_name in writer.sheets:
                worksheet = writer.sheets[sheet_name]
                for column in worksheet.columns:
                    max_length = 0
                    column_letter = column[0].column_letter
                    for cell in column:
                        try:
                            if len(str(cell.value)) > max_length:
                                max_length = len(str(cell.value))
                        except:
                            pass
                    adjusted_width = min(max_length + 2, 50)
                    worksheet.column_dimensions[column_letter].width = adjusted_width
        
        print(f"Exported {len(df)} leads to {filename}")
        return filename
    
    def export_to_csv(self, filename: str = None) -> str:
        """Export all data to CSV"""
        if filename is None:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"businesses_export_{timestamp}.csv"
        
        conn = sqlite3.connect(self.db_path)
        df = pd.read_sql_query("SELECT * FROM businesses", conn)
        conn.close()
        
        df.to_csv(filename, index=False, encoding='utf-8')
        print(f"Exported {len(df)} businesses to {filename}")
        return filename
    
    def generate_report(self) -> Dict:
        """Generate comprehensive report"""
        conn = sqlite3.connect(self.db_path)
        
        report = {
            'generated_at': datetime.now().isoformat(),
            'summary': {},
            'categories': {},
            'top_leads': []
        }
        
        # Summary statistics
        cursor = conn.cursor()
        
        cursor.execute('SELECT COUNT(*) FROM businesses')
        report['summary']['total_businesses'] = cursor.fetchone()[0]
        
        cursor.execute('SELECT COUNT(*) FROM businesses WHERE website IS NOT NULL')
        report['summary']['with_websites'] = cursor.fetchone()[0]
        
        cursor.execute('SELECT COUNT(*) FROM businesses WHERE last_analyzed IS NOT NULL')
        report['summary']['analyzed'] = cursor.fetchone()[0]
        
        cursor.execute('''
            SELECT COUNT(*), AVG(website_score) 
            FROM businesses 
            WHERE website_score > 0
        ''')
        count, avg_score = cursor.fetchone()
        report['summary']['average_score'] = round(avg_score, 2) if avg_score else 0
        
        # Category breakdown
        cursor.execute('''
            SELECT category, COUNT(*) as count, AVG(website_score) as avg_score
            FROM businesses 
            WHERE category IS NOT NULL 
            GROUP BY category 
            ORDER BY count DESC
        ''')
        
        for row in cursor.fetchall():
            category, count, avg_score = row
            report['categories'][category] = {
                'count': count,
                'average_score': round(avg_score, 2) if avg_score else 0
            }
        
        # Top 10 leads
        cursor.execute('''
            SELECT name, website, website_score, lead_score, priority
            FROM businesses 
            WHERE website_score >= 60 
            ORDER BY lead_score DESC 
            LIMIT 10
        ''')
        
        for row in cursor.fetchall():
            report['top_leads'].append({
                'name': row[0],
                'website': row[1],
                'website_score': row[2],
                'lead_score': row[3],
                'priority': row[4]
            })
        
        conn.close()
        
        # Save report to JSON
        report_file = f"report_{datetime.now().strftime('%Y%m%d')}.json"
        with open(report_file, 'w') as f:
            json.dump(report, f, indent=2)
        
        return report
