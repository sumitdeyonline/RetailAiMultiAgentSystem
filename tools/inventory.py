from langchain_core.tools import tool
from core.db import get_supabase_client

@tool
def get_stock_by_location(sku: str, location_id: str) -> str:
    """Returns the inventory level for a specific SKU at a given location."""
    try:
        client = get_supabase_client()
        # Equivalent to ?sku=eq.value&location_id=eq.value
        params = {"sku": f"eq.{sku}", "location_id": f"eq.{location_id}"}
        result = client.get("inventory", params)
        
        if not result:
            return f"No inventory record found for {sku} at {location_id}."
            
        quantity = result[0].get("quantity", 0)
        return f"Inventory for {sku} at {location_id} is {quantity} units."
    except Exception as e:
        return f"Database error: {str(e)}"

@tool
def forecast_stock_depletion(sku: str) -> str:
    """Predicts when a product will run out of stock based on current trends."""
    return f"{sku} is projected to run out of stock in 12 days. (Mocked forecast logic)"
