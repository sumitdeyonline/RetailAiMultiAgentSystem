from langchain_core.tools import tool
from core.db import get_supabase_client

@tool
def get_sales_volume(timeframe: str, region: str) -> str:
    """Returns the total sales volume for a given timeframe and region. Timeframe can be 'last week', 'Q1', etc."""
    try:
        client = get_supabase_client()
        # Postgrest filtering syntax: ?region=ilike.value&timeframe=ilike.value
        params = {"region": f"ilike.{region}", "timeframe": f"ilike.{timeframe}"}
        result = client.get("sales", params)
        
        if not result:
            return f"No sales data found for {region} in {timeframe}."
            
        volume = result[0].get("volume", 0)
        return f"Sales volume for {region} in {timeframe} was ${volume:,.2f}."
    except Exception as e:
        return f"Database error: {str(e)}"

@tool
def calculate_yoy_growth(category: str) -> str:
    """Calculates year-over-year sales growth for a product category."""
    return f"YoY growth for {category} is 14%. (Mocked growth logic)"
