#!/usr/bin/env python
"""
Migration script to add modules column to users table
Run this to update your database schema
"""
import sys
import os

# Add the Api directory to the path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app.init import db, create_app
from sqlalchemy import text

def migrate():
    app = create_app()
    with app.app_context():
        try:
            # Add modules column to users table using raw SQL
            db.session.execute(text('''
                ALTER TABLE users 
                ADD COLUMN modules JSON DEFAULT '["dashboard"]'
            '''))
            db.session.commit()
            print("✅ Successfully added 'modules' column to users table!")
            return True
        except Exception as e:
            db.session.rollback()
            error_str = str(e)
            if "Duplicate column" in error_str or "already exists" in error_str:
                print("✅ Column 'modules' already exists in users table")
                return True
            print(f"❌ Error: {e}")
            import traceback
            traceback.print_exc()
            return False

if __name__ == '__main__':
    success = migrate()
    sys.exit(0 if success else 1)
