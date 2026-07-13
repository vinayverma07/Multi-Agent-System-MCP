# from tavily import TavilyClient
# import os
# from dotenv import load_dotenv

# load_dotenv()

# client = TavilyClient(
#     api_key=os.getenv("TAVILY_API_KEY")
# )

# # test it
# #################################
# # response = client.search(
#     # query="Best hotels in Dubai"
# # )

# # print(response)

# ####################################



# def tavily_search(query):
#     response = client.search(
#         query=query,
#         max_results=5
#     )

#     results = []

#     for i, r in enumerate(response["results"], 1):
#         title   = r.get("title", "Unknown")
#         url     = r.get("url", "")
#         snippet = r.get("content", "").strip()
#         # Keep only the first 300 characters to avoid wall-of-text
#         if len(snippet) > 300:
#             snippet = snippet[:300].rsplit(" ", 1)[0] + "..."

#         results.append(f"{i}. **{title}**\n   {url}\n   {snippet}")

#     return "\n\n".join(results)
    
    
    
import os
from dotenv import load_dotenv
from mcp.server.fastmcp import FastMCP
from tavily import TavilyClient

load_dotenv()

# Initialize FastMCP server
mcp = FastMCP("Tavily Search Server")

# Initialize Tavily Client
client = TavilyClient(api_key=os.getenv("TAVILY_API_KEY"))

@mcp.tool()
def tavily_search(query: str) -> str:
    """Search the web using Tavily to get high-quality, up-to-date results."""
    response = client.search(
        query=query,
        max_results=5
    )

    results = []
    for i, r in enumerate(response.get("results", []), 1):
        title   = r.get("title", "Unknown")
        url     = r.get("url", "")
        snippet = r.get("content", "").strip()
        
        if len(snippet) > 300:
            snippet = snippet[:300].rsplit(" ", 1)[0] + "..."

        results.append(f"{i}. **{title}**\n   {url}\n   {snippet}")

    return "\n\n".join(results)

if __name__ == "__main__":
    # Run the server via stdio
    mcp.run(transport="stdio")