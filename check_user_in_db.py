#!/usr/bin/env python3
"""
Test script to check if a user exists in the Neon database.
"""

import os
import sys
from pathlib import Path

# Add backend to path
sys.path.insert(0, str(Path(__file__).parent / "backend"))

def check_user_in_neon_db():
    """Check if a user exists in the Neon database."""
    print("Checking user in Neon database...")

    # Change to backend directory to load .env
    backend_dir = Path(__file__).parent / "backend"
    os.chdir(backend_dir)

    # Load environment variables
    from dotenv import load_dotenv
    load_dotenv()

    try:
        from backend.src.models.database import sync_engine
        from sqlalchemy import text

        with sync_engine.connect() as conn:
            # Check if the test user exists
            result = conn.execute(text("SELECT id, email FROM users WHERE email = :email"), 
                                {"email": "test_chat@example.com"})
            user = result.fetchone()
            
            if user:
                print(f"[SUCCESS] User found in database: {user.email} (ID: {user.id})")
                return True
            else:
                print("[NOT FOUND] User not found in database")
                
                # Check how many users exist
                count_result = conn.execute(text("SELECT COUNT(*) FROM users")).fetchone()
                total_users = count_result[0]
                print(f"Total users in database: {total_users}")
                
                # Show some sample users if any exist
                if total_users > 0:
                    sample_users = conn.execute(text("SELECT id, email FROM users LIMIT 5")).fetchall()
                    print("Sample users in database:")
                    for u in sample_users:
                        print(f"  - {u.email} (ID: {u.id})")
                
                return False

    except Exception as e:
        print(f"  [ERROR] Database check failed: {str(e)}")
        import traceback
        print(f"  [DEBUG] Full traceback: {traceback.format_exc()}")
        return False

def main():
    """Run the user check."""
    print("[INFO] Checking user in Neon database...\n")

    success = check_user_in_neon_db()

    if success:
        print(f"\n[SUCCESS] User exists in Neon database!")
    else:
        print(f"\n[INFO] User does not exist in Neon database.")

if __name__ == "__main__":
    main()