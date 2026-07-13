import os
import asyncio
import sys

from dotenv import load_dotenv
from langchain_mcp_adapters.client import MultiServerMCPClient

#load_dotenv()
load_dotenv(override=True)
TAVILY_API_KEY = os.getenv("TAVILY_API_KEY")
OPENWEATHER_API_KEY = os.getenv("OPENWEATHER_API_KEY")

# client = MultiServerMCPClient(
#     {
#         "tavily": {
#             "transport": "streamable_http",
#             "url": f"https://mcp.tavily.com/mcp/?tavilyApiKey={TAVILY_API_KEY}"
#         },
#         "weather": {
#             "transport": "stdio",
#             "command": r"C:\Users\Vinay Verma\Desktop\code\Multi-Agent-System-MCP\.venv\Scripts\python.exe",
#             "args": [
#                 r"C:\Users\Vinay Verma\Desktop\code\Multi-Agent-System-MCP\custom_weather_mcp_server.py"
#             ],
#             "env": {
#                 "OPENWEATHER_API_KEY": OPENWEATHER_API_KEY
#             }
#         }
#     }
# )



CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
WEATHER_SERVER_SCRIPT = os.path.join(CURRENT_DIR, "custom_weather_mcp_server.py")

# Ensure this matches the file name where you pasted your FastMCP code!

client = MultiServerMCPClient(
    {
        "tavily": {
            "transport": "streamable_http",
            "url": f"https://mcp.tavily.com/mcp/?tavilyApiKey={TAVILY_API_KEY}"
        },
        "weather": {
            "transport": "stdio",
            "command": sys.executable,
            "args": [WEATHER_SERVER_SCRIPT],
            "env": {
                "OPENWEATHER_API_KEY": OPENWEATHER_API_KEY or ""
            }
        }
    }
)


search_tool = None

async def initialize_mcp():
    global search_tool

    if search_tool is not None:
        return

    tools = await client.get_tools()

    print("\nAvailable MCP Tools:\n")

    for tool in tools:
        print(tool.name)

    search_tool = next(
        tool
        for tool in tools
        if tool.name == "tavily_search"
    )

async def tavily_mcp_search(query: str):
    await initialize_mcp()
    result = await search_tool.ainvoke(
        {
            "query": query
        }
    )
    return result





weather_tool = None
forecast_tool = None


async def initialize_weather_tools():

    global weather_tool, forecast_tool

    if weather_tool is not None:
        return

    tools = await client.get_tools()

    weather_tool = next(
        t for t in tools
        if t.name == "get_current_weather"
    )

    forecast_tool = next(
        t for t in tools
        if t.name == "get_forecast"
    )


async def weather_mcp_search(city: str):

    await initialize_weather_tools()

    return await weather_tool.ainvoke(
        {
            "city": city
        }
    )


async def forecast_mcp_search(city: str):

    await initialize_weather_tools()

    return await forecast_tool.ainvoke(
        {
            "city": city
        }
    )




from langchain_groq import ChatGroq

# LLM
llm = ChatGroq(
    model="llama-3.3-70b-versatile"
)

###################################
# Destination Extractor
###################################

def extract_destination(query: str):

    prompt = f"""
        Extract the destination city from the user's travel query.

        Rules:
        - Return ONLY the city name.
        - No explanation.
        - No punctuation.
        - No markdown.
        - No extra words.
        - If country only is mentioned, return the capital city.

        Query:
        {query}
        """

    response = llm.invoke(prompt)
    city = response.content.strip().replace(".", "").replace('"', "")

    return city