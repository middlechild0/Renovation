# Migration script
import sqlite3

def migrate_database(db_path="businesses.db"):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    print("Starting database migration...")
    cursor.execute("PRAGMA table_info(businesses)")
    existing_columns = [col[1] for col in cursor.fetchall()]
    
    new_columns = [
        ('comprehensive_analysis', "TEXT DEFAULT '{}'"),
        ('has_website', 'BOOLEAN'),
        ('website_status', 'TEXT'),
        ('tier', 'INTEGER DEFAULT 4'),
        ('tier_assignment', 'TEXT'),
        ('critical_failures_count', 'INTEGER DEFAULT 0'),
        ('critical_issues_count', 'INTEGER DEFAULT 0'),
        ('high_priority_issues_count', 'INTEGER DEFAULT 0'),
        ('medium_priority_issues_count', 'INTEGER DEFAULT 0'),
        ('low_priority_issues_count', 'INTEGER DEFAULT 0'),
        ('comprehensive_score', 'INTEGER DEFAULT 0'),
    ]
    
    for col_name, col_type in new_columns:
        if col_name not in existing_columns:
            try:
                cursor.execute(f"ALTER TABLE businesses ADD COLUMN {col_name} {col_type}")
                print(f"✓ Added column: {col_name}")
            except sqlite3.OperationalError as e:
                print(f"✗ Error adding {col_name}: {e}")
        else:
            print(f"✓ Column already exists: {col_name}")
    
    try:
        cursor.execute('CREATE INDEX IF NOT EXISTS idx_businesses_tier ON businesses(tier)')
        print("✓ Created index: idx_businesses_tier")
    except:
        pass
    
    conn.commit()
    conn.close()
    print("\n✓ Database migration complete!")

if __name__ == "__main__":
    migrate_database()
