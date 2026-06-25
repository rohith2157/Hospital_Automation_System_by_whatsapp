#!/usr/bin/env python
"""
Database Migration: Add password_salt column to users table
Run this to add SHA256 salt storage to your PostgreSQL database
"""

import sys
import os

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app.init import create_app, db
from sqlalchemy import text

app = create_app()

def add_password_salt_column():
    """Add password_salt column to users table"""
    
    print("🔄 Migrating database: Adding password_salt column...\n")
    
    with app.app_context():
        try:
            # Check if column already exists
            inspector = db.inspect(db.engine)
            columns = [col['name'] for col in inspector.get_columns('users')]
            
            if 'password_salt' in columns:
                print("✅ Column 'password_salt' already exists!")
                return True
            
            # Add the column
            print("Adding password_salt column to users table...")
            with db.engine.connect() as connection:
                connection.execute(text(
                    'ALTER TABLE users ADD COLUMN password_salt VARCHAR(255) NULL'
                ))
                connection.commit()
            
            print("✅ Column 'password_salt' added successfully!")
            print("\nDatabase schema updated:")
            print("  ✓ password_hash: VARCHAR(255) - Already existed")
            print("  ✓ password_salt: VARCHAR(255) - Just added")
            
            return True
            
        except Exception as e:
            print(f"❌ Error during migration: {e}")
            print("\nNote: If this is SQLite, you may need to run manually:")
            print("  ALTER TABLE users ADD COLUMN password_salt VARCHAR(255);")
            return False

def verify_migration():
    """Verify the migration was successful"""
    
    print("\n🔍 Verifying migration...\n")
    
    with app.app_context():
        try:
            inspector = db.inspect(db.engine)
            columns = {col['name']: col['type'] for col in inspector.get_columns('users')}
            
            required_columns = {
                'password_hash': 'VARCHAR',
                'password_salt': 'VARCHAR'
            }
            
            all_good = True
            for col_name, col_type in required_columns.items():
                if col_name in columns:
                    print(f"✅ {col_name}: {columns[col_name]}")
                else:
                    print(f"❌ {col_name}: MISSING")
                    all_good = False
            
            return all_good
            
        except Exception as e:
            print(f"⚠️  Could not verify: {e}")
            return False

if __name__ == '__main__':
    try:
        success = add_password_salt_column()
        if success:
            verify_migration()
            print("\n✅ Migration complete!")
            sys.exit(0)
        else:
            print("\n❌ Migration failed!")
            sys.exit(1)
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
