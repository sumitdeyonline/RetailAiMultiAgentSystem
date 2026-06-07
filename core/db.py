import requests
from typing import Dict, Any, List, Optional
from config.settings import settings

class SupabaseRESTClient:
    def __init__(self):
        if not settings.SUPABASE_URL or not settings.SUPABASE_KEY:
            raise ValueError("SUPABASE_URL and SUPABASE_KEY must be set in the .env file")
        
        self.base_url = f"{settings.SUPABASE_URL.rstrip('/')}/rest/v1"
        self.headers = {
            "apikey": settings.SUPABASE_KEY,
            "Authorization": f"Bearer {settings.SUPABASE_KEY}",
            "Content-Type": "application/json",
            "Prefer": "return=representation"
        }

    def get(self, table: str, params: Optional[Dict[str, Any]] = None) -> List[Dict[str, Any]]:
        """Perform a SELECT query."""
        url = f"{self.base_url}/{table}"
        
        # Ensure we always select everything if not specified
        if not params:
            params = {}
        if "select" not in params:
            params["select"] = "*"
            
        response = requests.get(url, headers=self.headers, params=params)
        response.raise_for_status()
        return response.json()

    def post(self, table: str, data: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Perform an INSERT query."""
        url = f"{self.base_url}/{table}"
        response = requests.post(url, headers=self.headers, json=data)
        response.raise_for_status()
        return response.json()

def get_supabase_client() -> SupabaseRESTClient:
    return SupabaseRESTClient()
