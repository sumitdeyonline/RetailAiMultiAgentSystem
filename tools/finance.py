from langchain_core.tools import tool
from core.db import get_supabase_client

@tool
def generate_pnl_summary(quarter: str) -> str:
    """Generates a Profit and Loss summary for a specific financial quarter."""
    return f"P&L Summary for {quarter}: Revenue $10M, Costs $6M, Net Profit $4M. (Mocked P&L logic)"

@tool
def calculate_product_margin(sku: str) -> str:
    """Calculates the profit margin for a specific SKU."""
    try:
        client = get_supabase_client()
        params = {"sku": f"eq.{sku}"}
        result = client.get("products", params)
        
        if not result:
            return f"No product margin data found for {sku}."
            
        margin = result[0].get("margin_percentage", 0)
        return f"Profit margin for {sku} is {margin}%."
    except Exception as e:
        return f"Database error: {str(e)}"
