from langchain_core.prompts import ChatPromptTemplate
from langgraph.prebuilt import create_react_agent
from core.llm import get_llm

# Import tools
from tools.inventory import get_stock_by_location, forecast_stock_depletion
from tools.sales import get_sales_volume, calculate_yoy_growth
from tools.order import find_delayed_orders, get_order_status
from tools.finance import generate_pnl_summary, calculate_product_margin
from tools.supply_chain import get_vendor_lead_times, generate_replenishment_order

llm = get_llm()

# Inventory Agent
inventory_tools = [get_stock_by_location, forecast_stock_depletion]
inventory_agent = create_react_agent(
    llm,
    tools=inventory_tools,
    prompt="You are the Inventory Agent. Provide accurate stock levels and forecasts. Always use the provided tools to answer queries."
)

# Sales Agent
sales_tools = [get_sales_volume, calculate_yoy_growth]
sales_agent = create_react_agent(
    llm,
    tools=sales_tools,
    prompt="You are the Sales Agent. Your role is to analyze sales data and provide revenue insights."
)

# Order Agent
order_tools = [find_delayed_orders, get_order_status]
order_agent = create_react_agent(
    llm,
    tools=order_tools,
    prompt="You are the Order Agent. Track shipments and manage fulfillment queries."
)

# Finance Agent
finance_tools = [generate_pnl_summary, calculate_product_margin]
finance_agent = create_react_agent(
    llm,
    tools=finance_tools,
    prompt="You are the Finance Agent. Answer financial questions regarding revenue, costs, and margins."
)

# Supply Chain Agent
supply_chain_tools = [get_vendor_lead_times, generate_replenishment_order]
supply_chain_agent = create_react_agent(
    llm,
    tools=supply_chain_tools,
    prompt="You are the Supply Chain Agent. Manage vendor relations and replenishment orders."
)

# Analytics Agent (No specific mock tools right now, acts as a reasoning engine)
analytics_agent = create_react_agent(
    llm,
    tools=[],
    prompt="You are the Analytics Agent. Synthesize data, run root-cause analysis, and detect trends from information provided in the conversation."
)
