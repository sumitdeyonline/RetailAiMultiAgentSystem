from langchain_core.tools import tool
from core.db import get_supabase_client

@tool
def find_delayed_orders(days_delayed: int) -> str:
    """Returns a list of orders delayed by more than the specified number of days."""
    try:
        client = get_supabase_client()
        # Postgrest filtering syntax: ?days_delayed=gt.value
        params = {"days_delayed": f"gt.{days_delayed}"}
        result = client.get("orders", params)
        
        count = len(result)
        return f"Found {count} orders delayed by more than {days_delayed} days."
    except Exception as e:
        return f"Database error: {str(e)}"

@tool
def get_order_status(order_id: str) -> str:
    """Returns the current fulfillment status of an order."""
    try:
        client = get_supabase_client()
        params = {"order_id": f"eq.{order_id}"}
        result = client.get("orders", params)
        
        if not result:
            return f"Order {order_id} not found."
            
        status = result[0].get("status", "UNKNOWN")
        return f"Order {order_id} is currently {status}."
    except Exception as e:
        return f"Database error: {str(e)}"
