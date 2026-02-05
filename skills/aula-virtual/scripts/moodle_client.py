#!/usr/bin/env python3
"""
Moodle Client for UAndina
=========================
Wrapper class to test the connection once we have the token.

Usage:
    from moodle_client import MoodleClient
    
    client = MoodleClient(token="your_token")
    info = client.get_site_info()
    print(info)
"""

import os
import requests
from pathlib import Path
from typing import Dict, Any

# Try to load from .env file
try:
    from dotenv import load_dotenv
    skill_dir = Path(__file__).parent.parent
    env_path = skill_dir / ".env"
    if env_path.exists():
        load_dotenv(env_path)
except ImportError:
    pass


class MoodleClient:
    """
    Simple Moodle client wrapper to test the connection.
    
    Attributes:
        token: The Moodle web service token
        url: Base URL of the Moodle instance
    """
    
    def __init__(
        self, 
        token: str = None, 
        url: str = None
    ):
        """
        Initialize MoodleClient.
        
        Args:
            token: Moodle web service token (or from MOODLE_TOKEN env)
            url: Moodle base URL (or from MOODLE_URL env)
        """
        self.token = token or os.getenv('MOODLE_TOKEN')
        self.url = url or os.getenv('MOODLE_URL', 'https://campus.uandina.edu.pe')
        
        if not self.token:
            raise ValueError(
                "No token provided. Run get_uandina_token.py first "
                "or pass token parameter."
            )
    
    def get_site_info(self) -> Dict[str, Any]:
        """
        Get site information to test the connection.
        
        Calls endpoint: {url}/webservice/rest/server.php
        Function: core_webservice_get_site_info
        
        Returns:
            JSON response with userid, fullname, etc.
        """
        endpoint = f"{self.url}/webservice/rest/server.php"
        
        params = {
            'wstoken': self.token,
            'wsfunction': 'core_webservice_get_site_info',
            'moodlewsrestformat': 'json'
        }
        
        try:
            response = requests.post(endpoint, data=params, timeout=30)
            response.raise_for_status()
            return response.json()
            
        except requests.exceptions.RequestException as e:
            return {'error': str(e), 'errorcode': 'request_failed'}


def main():
    """Test the MoodleClient connection."""
    print("=" * 50)
    print("🎓 UAndina Moodle Client Test")
    print("=" * 50)
    
    try:
        client = MoodleClient()
        
        print("\n📡 Testing connection...")
        info = client.get_site_info()
        
        if 'error' in info:
            print(f"\n❌ Error: {info.get('error')}")
            print(f"   Code: {info.get('errorcode', 'unknown')}")
        else:
            print("\n✅ Connection successful!")
            print(f"\n📌 Site Info:")
            print(f"   Site Name: {info.get('sitename', 'N/A')}")
            print(f"   User ID: {info.get('userid', 'N/A')}")
            print(f"   Full Name: {info.get('fullname', 'N/A')}")
            print(f"   Username: {info.get('username', 'N/A')}")
            print(f"\n🎉 Ready to use the Moodle API!")
            
    except ValueError as e:
        print(f"\n❌ Configuration Error: {e}")
        print("   Run get_uandina_token.py first!")


if __name__ == "__main__":
    main()
