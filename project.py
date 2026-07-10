
# LangGraph Multi-Agent Travel Booking System with Long-Term Memory
import os
import json
from typing import TypedDict, Annotated
import operator
import asyncio
import psycopg
from langgraph.graph import StateGraph, START, END
from langgraph.checkpoint.postgres import PostgresSaver
from langchain_core.messages import (
    AnyMessage,
    HumanMessage,
    AIMessage,
    SystemMessage,
)

from langchain_groq import ChatGroq

# from tools.tavily_tool import tavily_search

#from mcp_client import tavily_mcp_search

from mcp_client import (
    tavily_mcp_search,
    get_airports,
    get_airlines,
    aviation_mcp_call,extract_destination,forecast_mcp_search,weather_mcp_search
)


#from tools.flight_tool import search_flights


from dotenv import load_dotenv
#load_dotenv()
load_dotenv(override=True)
DATABASE_URL = os.getenv("DATABASE_URL")

# LLM
llm = ChatGroq(
    model="llama-3.3-70b-versatile"
)

# State
class TravelState(TypedDict):
    messages: Annotated[list[AnyMessage], operator.add]
    user_query: str
    flight_results: str
    hotel_results: str
    itinerary: str
    llm_calls: int
    weather_results: str

# Flight Tool Router Prompt
FLIGHT_AGENT_PROMPT = """
You are a travel flight expert.

User Query:
{query}

Airport Information:
{airport_data}

Airline Information:
{airline_data}

Generate:

1. Likely departure airport
2. Likely arrival airport
3. Airlines serving this route
4. Typical flight duration
5. Estimated airfare range
6. Peak season pricing warning
7. Booking advice

Return concise travel guidance.
"""

# Flight Agent
def flight_agent(state: TravelState):
    print("\nINSIDE FLIGHT AGENT\n")

    query = state["user_query"]

    try:

        airports = asyncio.run(
            aviation_mcp_call(
                "list_airports"
            )
        )

        airlines = asyncio.run(
            aviation_mcp_call(
                "list_airlines"
            )
        )

        prompt = FLIGHT_AGENT_PROMPT.format(
            query=query,
            airport_data=str(airports)[:3000],
            airline_data=str(airlines)[:3000]
        )

        response = llm.invoke([
            SystemMessage(
                content="You are an expert travel flight planner."
            ),
            HumanMessage(content=prompt)
        ])

        flight_data = response.content

    except Exception as e:

        flight_data = f"Flight information unavailable: {str(e)}"

    return {
        "flight_results": flight_data,
        "messages": [
            AIMessage(
                content="Flight recommendations generated"
            )
        ],
        "llm_calls": state.get("llm_calls", 0) + 1
    }




# # Hotel Agent
# def hotel_agent(state: TravelState):
#     query = f"Best hotels for {state['user_query']}" 

#     hotel_results = asyncio.run(
#         tavily_mcp_search(query)
#     )

#     return {
#         "hotel_results": hotel_results,
#         "messages": [
#             AIMessage(content="Hotel information fetched")
#         ],
#         "llm_calls": state.get("llm_calls", 0) + 1
#     }

def hotel_agent(state: TravelState):
    query = f"Best hotels for {state['user_query']}"

    hotel_results = asyncio.run(
        tavily_mcp_search(query)
    )

    formatted_hotels = ""

    if hotel_results:
        data = json.loads(hotel_results[0]["text"])

        for i, result in enumerate(data.get("results", []), start=1):
            formatted_hotels += (
                f"{i}. {result['title']}\n"
                f"   {result['content']}\n\n"
            )

    return {
        "hotel_results": formatted_hotels.strip(),
        "messages": [
            AIMessage(content="Hotel information fetched")
        ],
        "llm_calls": state.get("llm_calls", 0) + 1
    }

def weather_agent(state: TravelState):

    city = extract_destination(state["user_query"])
    print(city)

    weather_data = asyncio.run(
        weather_mcp_search(city)
    )
    print(weather_data)

    forecast_data = asyncio.run(
        forecast_mcp_search(city)
    )
    print(forecast_data)

    # Parse weather data - handle both dict and list formats
    weather_dict = None
    if isinstance(weather_data, list) and len(weather_data) > 0:
        # Extract JSON from message format
        if isinstance(weather_data[0], dict) and 'text' in weather_data[0]:
            weather_dict = json.loads(weather_data[0]['text'])
        else:
            weather_dict = weather_data[0] if isinstance(weather_data[0], dict) else weather_data
    elif isinstance(weather_data, dict):
        weather_dict = weather_data

    # Parse forecast data - handle both dict and list formats
    forecast_dict = None
    if isinstance(forecast_data, list) and len(forecast_data) > 0:
        # Extract JSON from message format
        if isinstance(forecast_data[0], dict) and 'text' in forecast_data[0]:
            forecast_dict = json.loads(forecast_data[0]['text'])
        else:
            forecast_dict = forecast_data[0] if isinstance(forecast_data[0], dict) else forecast_data
    elif isinstance(forecast_data, dict):
        forecast_dict = forecast_data

    # Format weather data for readability
    formatted_weather = ""
    if weather_dict:
        formatted_weather = f"""
📍 Location: {weather_dict.get('city', 'N/A')}
🌡️ Temperature: {weather_dict.get('temperature_c', 'N/A')}°C
🤔 Feels Like: {weather_dict.get('feels_like_c', 'N/A')}°C
💧 Humidity: {weather_dict.get('humidity', 'N/A')}%
☁️ Condition: {weather_dict.get('condition', 'N/A').title()}
💨 Wind Speed: {weather_dict.get('wind_speed', 'N/A')} m/s
"""
    else:
        formatted_weather = "Weather data unavailable"

    # Format forecast data for readability
    formatted_forecast = ""
    if forecast_dict:
        forecast_list = forecast_dict.get('forecast', [])
        if forecast_list:
            formatted_forecast = "📅 5-Day Forecast:\n"
            for i, item in enumerate(forecast_list, 1):
                datetime_str = item.get('datetime', 'N/A')
                temp = item.get('temperature', 'N/A')
                weather = item.get('weather', 'N/A').title()
                formatted_forecast += f"\n   {i}. {datetime_str}\n      🌡️ {temp}°C | ☁️ {weather}"
        else:
            formatted_forecast = "No forecast data available"
    else:
        formatted_forecast = "Forecast data unavailable"

    return {
        "weather_results": f"""🌤️ Current Weather in {city}:
{formatted_weather}
{formatted_forecast}
""",
        "messages": [
            AIMessage(
                content="Weather information fetched"
            )
        ]
    }



# Itinerary Agent
def itinerary_agent(state: TravelState):

    prompt = f"""
    Create a travel itinerary.
    User Query:
    {state['user_query']}

    Flight Results:
    {state['flight_results']}

    Hotel Results:
    {state['hotel_results']}

    Weather Information:
    {state['weather_results']}
    """

    response = llm.invoke([
        SystemMessage(
            content="You are an expert travel planner"
        ),
        HumanMessage(content=prompt)
    ])

    return {
        "itinerary": response.content,
        "messages": [response],
        "llm_calls": state.get("llm_calls", 0) + 1
    }







graph = StateGraph(TravelState)

graph.add_node("flight_agent", flight_agent)
graph.add_node("hotel_agent", hotel_agent)
graph.add_node("weather_agent", weather_agent)
graph.add_node("itinerary_agent", itinerary_agent)


graph.add_edge(START, "flight_agent")
graph.add_edge("flight_agent", "hotel_agent")
graph.add_edge("hotel_agent", "weather_agent")
graph.add_edge("weather_agent", "itinerary_agent")
graph.add_edge("itinerary_agent", END)


# Persistent connection so both CLI and Streamlit can share the compiled app
_conn = psycopg.connect(DATABASE_URL)
checkpointer = PostgresSaver(_conn)
checkpointer.setup()

app = graph.compile(checkpointer=checkpointer)


if __name__ == "__main__": 

    import uuid
    config = {
        "configurable": {
            "thread_id": str(uuid.uuid4())
        }
    }


    user_input = input("Enter travel request: ")

    result = app.invoke(
        {
            "messages": [
                HumanMessage(content=user_input)
            ],
            "user_query": user_input,
            "flight_results": "",
            "hotel_results": "",
            "weather_results": "",
            "itinerary": "",
            "llm_calls": 0
        },
        config=config
    )

    print("\nFINAL RESPONSE:\n")

    for msg in result["messages"]:
        print(msg.content)