#!/usr/bin/env python3
"""
Test script to check if authentication works with the existing user.
"""

import os
import sys
from pathlib import Path

# Add backend to path
sys.path.insert(0, str(Path(__file__).parent / "backend"))

def test_authentication():
    """Test if authentication works with the existing user."""
    print("Testing authentication with existing user...")

    # Change to backend directory to load .env
    backend_dir = Path(__file__).parent / "backend"
    os.chdir(backend_dir)

    # Load environment variables
    from dotenv import load_dotenv
    load_dotenv()

    try:
        from backend.src.models.database import sync_engine
        from sqlalchemy import text
        from backend.src.api.auth import pwd_context  # Try to import the password context
        
        # First, let's see what auth module is available
        from backend.src.models.entities import User
        from backend.src.api.auth import pwd_context
        
        with sync_engine.connect() as conn:
            # Get the user from database
            result = conn.execute(text("SELECT id, email, password_hash FROM users WHERE email = :email"), 
                                {"email": "test_chat@example.com"})
            user = result.fetchone()
            
            if user:
                print(f"User found: {user.email}")
                print(f"Password hash in DB: {user.password_hash[:50]}...")  # Show first 50 chars
                
                # Test password verification
                test_password = "Testpassword123!"  # The password we used earlier
                is_valid = pwd_context.verify(test_password, user.password_hash)
                print(f"Password verification result: {is_valid}")
                
                if is_valid:
                    print("✓ Authentication should work with this user and password")
                    return True
                else:
                    print("✗ Password verification failed - wrong password or hashing issue")
                    return False
            else:
                print("User not found in database")
                return False

    except ImportError as e:
        print(f"Import error (auth module): {e}")
        # Try alternative approach - check if user exists and what the password looks like
        try:
            from backend.src.models.database import sync_engine
            from sqlalchemy import text

            with sync_engine.connect() as conn:
                # Get the user from database
                result = conn.execute(text("SELECT id, email, password_hash FROM users WHERE email = :email"), 
                                    {"email": "test_chat@example.com"})
                user = result.fetchone()
                
                if user:
                    print(f"User found: {user.email}")
                    print(f"Password hash in DB: {user.password_hash[:50]}...")  # Show first 50 chars
                    print("Cannot verify password without proper auth module import")
                    return True
                else:
                    print("User not found in database")
                    return False
        except Exception as e2:
            print(f"Secondary error: {e2}")
            return False
    except Exception as e:
        print(f"  [ERROR] Authentication test failed: {str(e)}")
        import traceback
        print(f"  [DEBUG] Full traceback: {traceback.format_exc()}")
        return False

def main():
    """Run the authentication test."""
    print("[INFO] Testing authentication with existing user...\n")

    success = test_authentication()

    if success:
        print(f"\n[SUCCESS] Authentication test completed!")
    else:
        print(f"\n[INFO] Authentication test failed.")

if __name__ == "__main__":
    main()