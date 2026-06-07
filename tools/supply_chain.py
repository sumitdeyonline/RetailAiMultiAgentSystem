from langchain_core.tools import tool

@tool
def get_vendor_lead_times(vendor_id: str) -> str:
    """Returns average lead times for a vendor."""
    return f"Vendor {vendor_id} has an average lead time of 18 days."

@tool
def generate_replenishment_order(sku: str, quantity: int) -> str:
    """Creates a replenishment order for a SKU."""
    return f"Successfully generated replenishment order for {quantity} units of {sku}."
