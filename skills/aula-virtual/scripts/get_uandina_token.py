#!/usr/bin/env python3
"""
UAndina Moodle Token Retrieval Script
======================================
Retrieves a web service token from Universidad Andina del Cusco's 
Moodle platform (campus.uandina.edu.pe).

This token is required for all subsequent API calls.

Usage:
    python get_uandina_token.py
    
The token will be printed and can be added to your .env file.
"""

import os
import sys
import requests
from pathlib import Path

# Try to load from .env file
try:
    from dotenv import load_dotenv
    
    # Load .env from skill directory
    skill_dir = Path(__file__).parent.parent
    env_path = skill_dir / ".env"
    
    if env_path.exists():
        load_dotenv(env_path)
        print(f"✅ Loaded environment from: {env_path}")
    else:
        print(f"⚠️  No .env file found at: {env_path}")
        print("   Create one from .env.example")
except ImportError:
    print("⚠️  python-dotenv not installed. Using system environment variables.")


def get_moodle_token(
    username: str,
    password: str,
    moodle_url: str = "https://campus.uandina.edu.pe"
) -> dict:
    """
    Authenticate with UAndina Moodle and retrieve web service token.
    
    Args:
        username: Student code or username
        password: Account password
        moodle_url: Base URL of the Moodle instance
        
    Returns:
        dict with 'token' on success, or 'error' and 'errorcode' on failure
    """
    
    # Moodle token endpoint
    token_endpoint = f"{moodle_url}/login/token.php"
    
    # Payload for Moodle Mobile Web Service
    # CRITICAL: 'moodle_mobile_app' is the required service ID for UAndina
    payload = {
        'username': username,
        'password': password,
        'service': 'moodle_mobile_app'  # Strictly required for UAndina
    }
    
    print(f"\n🔐 Authenticating with {moodle_url}...")
    print(f"   Username: {username}")
    print(f"   Service: moodle_mobile_app")
    
    try:
        # Make the authentication request
        response = requests.post(
            token_endpoint,
            data=payload,
            timeout=30,
            headers={
                'User-Agent': 'MoodleMobile',
                'Content-Type': 'application/x-www-form-urlencoded'
            }
        )
        
        # Check HTTP status
        response.raise_for_status()
        
        # Parse JSON response
        result = response.json()
        
        return result
        
    except requests.exceptions.Timeout:
        return {
            'error': 'Connection timed out. Check your internet connection.',
            'errorcode': 'timeout'
        }
    except requests.exceptions.ConnectionError:
        return {
            'error': 'Could not connect to Moodle server. Check the URL.',
            'errorcode': 'connection_error'
        }
    except requests.exceptions.RequestException as e:
        return {
            'error': f'Request failed: {str(e)}',
            'errorcode': 'request_error'
        }
    except ValueError:
        return {
            'error': 'Invalid response from server (not JSON)',
            'errorcode': 'invalid_response'
        }


def update_env_file(token: str, env_path: Path) -> bool:
    """
    Update the .env file with the retrieved token.
    
    Args:
        token: The Moodle token to save
        env_path: Path to the .env file
        
    Returns:
        True if successful, False otherwise
    """
    try:
        if env_path.exists():
            # Read existing content
            content = env_path.read_text(encoding='utf-8')
            
            # Replace or add token
            if 'MOODLE_TOKEN=' in content:
                import re
                content = re.sub(
                    r'MOODLE_TOKEN=.*',
                    f'MOODLE_TOKEN={token}',
                    content
                )
            else:
                content += f'\nMOODLE_TOKEN={token}\n'
            
            env_path.write_text(content, encoding='utf-8')
            return True
        else:
            # Create new .env file
            content = f"""# UAndina Moodle Configuration
MOODLE_URL=https://campus.uandina.edu.pe
MOODLE_TOKEN={token}
"""
            env_path.write_text(content, encoding='utf-8')
            return True
            
    except Exception as e:
        print(f"❌ Error updating .env: {e}")
        return False


def main():
    """Main entry point for token retrieval."""
    
    print("=" * 50)
    print("🎓 UAndina Moodle Token Retrieval")
    print("   Universidad Andina del Cusco")
    print("=" * 50)
    
    # Get credentials from environment
    username = os.getenv('MOODLE_USERNAME')
    password = os.getenv('MOODLE_PASSWORD')
    moodle_url = os.getenv('MOODLE_URL', 'https://campus.uandina.edu.pe')
    
    # Check for missing credentials
    if not username or not password:
        print("\n❌ Error: Missing credentials!")
        print("\nPlease set the following environment variables:")
        print("  - MOODLE_USERNAME: Your student code")
        print("  - MOODLE_PASSWORD: Your password")
        print("\nYou can:")
        print("  1. Copy .env.example to .env and fill in your credentials")
        print("  2. Set them as system environment variables")
        sys.exit(1)
    
    # Get the token
    result = get_moodle_token(username, password, moodle_url)
    
    # Handle the result
    if 'token' in result:
        token = result['token']
        print("\n" + "=" * 50)
        print("✅ SUCCESS! Token retrieved successfully!")
        print("=" * 50)
        print(f"\n🔑 Your token: {token}")
        
        # Try to update .env file
        skill_dir = Path(__file__).parent.parent
        env_path = skill_dir / ".env"
        
        if update_env_file(token, env_path):
            print(f"\n📝 Token saved to: {env_path}")
        else:
            print(f"\n⚠️  Could not auto-save. Add this to your .env file:")
            print(f"   MOODLE_TOKEN={token}")
        
        print("\n🎉 You can now use the Moodle API!")
        print("   Try running: python scripts/moodle_api.py")
        
        return token
        
    elif 'error' in result:
        print("\n" + "=" * 50)
        print("❌ AUTHENTICATION FAILED")
        print("=" * 50)
        print(f"\nError: {result.get('error', 'Unknown error')}")
        
        error_code = result.get('errorcode', '')
        
        if error_code == 'invalidlogin':
            print("\n💡 Possible causes:")
            print("   - Incorrect username or password")
            print("   - Account locked or disabled")
            print("   - First login requires password change on web")
        elif error_code == 'sitemaintenance':
            print("\n💡 The Moodle site is under maintenance.")
            print("   Try again later.")
        elif error_code == 'servicerequireslogin':
            print("\n💡 The mobile service may be disabled for your account.")
            print("   Contact your administrator.")
        
        sys.exit(1)
    else:
        print("\n❌ Unexpected response from server")
        print(f"   Response: {result}")
        sys.exit(1)


if __name__ == "__main__":
    main()
