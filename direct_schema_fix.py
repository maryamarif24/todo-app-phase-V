#!/usr/bin/env python3
"""
Direct script to fix the database schema by adding missing columns to the todo table.
"""

import os
import sys
from pathlib import Path

# Add backend to path
sys.path.insert(0, str(Path(__file__).parent / "backend"))

def fix_database_schema():
    """Add missing columns to the todo table."""
    print("[INFO] Fixing Database Schema by adding missing columns...")

    # Change to backend directory to load .env
    backend_dir = Path(__file__).parent / "backend"
    os.chdir(backend_dir)

    # Load environment variables
    from dotenv import load_dotenv
    load_dotenv()

    try:
        from backend.src.models.database import sync_engine
        from sqlalchemy import inspect, text

        # Get table information
        inspector = inspect(sync_engine)
        tables = inspector.get_table_names()

        print(f"  [INFO] Current tables: {tables}")

        with sync_engine.connect() as conn:
            trans = conn.begin()

            # Check if the todo table exists
            if 'todo' not in tables:
                print("  [ERROR] 'todo' table does not exist!")
                return False

            # Check current columns in the todo table
            columns = inspector.get_columns('todo')
            column_names = [col['name'] for col in columns]
            
            print(f"  [INFO] Current columns in 'todo' table: {column_names}")

            # Define the missing columns that should exist based on the model
            required_columns = ['priority', 'due_date', 'reminder_enabled', 'reminder_time']

            # Add missing columns
            for col in required_columns:
                if col not in column_names:
                    print(f"  [INFO] Adding missing column: {col}")
                    
                    if col == 'priority':
                        alter_sql = "ALTER TABLE todo ADD COLUMN priority VARCHAR(20) DEFAULT 'MEDIUM';"
                    elif col == 'due_date':
                        alter_sql = "ALTER TABLE todo ADD COLUMN due_date TIMESTAMP NULL;"
                    elif col == 'reminder_enabled':
                        alter_sql = "ALTER TABLE todo ADD COLUMN reminder_enabled BOOLEAN DEFAULT FALSE;"
                    elif col == 'reminder_time':
                        alter_sql = "ALTER TABLE todo ADD COLUMN reminder_time VARCHAR(20) NULL;"
                    
                    conn.execute(text(alter_sql))
                else:
                    print(f"  [INFO] Column {col} already exists")

            # Also update the title column length to match the model (255 instead of 200)
            title_col = next((col for col in columns if col['name'] == 'title'), None)
            if title_col and str(title_col['type']).lower().startswith('varchar'):
                # Extract the length from the type string
                import re
                match = re.search(r'VARCHAR\((\d+)\)', str(title_col['type']))
                if match:
                    current_length = int(match.group(1))
                    if current_length != 255:
                        print(f"  [INFO] Updating title column length from {current_length} to 255")
                        conn.execute(text("ALTER TABLE todo ALTER COLUMN title TYPE VARCHAR(255);"))

            trans.commit()
            print("  [SUCCESS] Database schema fixed successfully")

            # Verify the new structure
            new_columns = inspector.get_columns('todo')
            new_column_names = [col['name'] for col in new_columns]
            print(f"  [INFO] Updated columns in 'todo' table: {new_column_names}")

            # Check if all required columns are now present
            missing_cols = [col for col in required_columns if col not in new_column_names]
            if missing_cols:
                print(f"  [ERROR] Still missing columns: {missing_cols}")
                return False
            else:
                print("  [SUCCESS] All required columns are now present")
                
            return True

    except Exception as e:
        print(f"  [ERROR] Schema fix failed: {str(e)}")
        import traceback
        print(f"  [DEBUG] Full traceback: {traceback.format_exc()}")

        # Try to rollback if connection is still open
        try:
            trans.rollback()
        except:
            pass

        return False

def main():
    """Run schema fix."""
    print("[INFO] Starting Database Schema Fix...\n")

    success = fix_database_schema()

    if success:
        print(f"\n[SUCCESS] Database schema has been fixed!")
        print("The todo table now has all the required columns.")
        print("Todo creation should now work properly.")
    else:
        print(f"\n[ERROR] Database schema fix failed!")

if __name__ == "__main__":
    main()