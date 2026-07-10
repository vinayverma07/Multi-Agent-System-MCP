<div align="center">

# ✈️ Multi-Agent AI Travel Booking System

### **AI-Powered Multi-Agent Travel Planner using LangGraph & Model Context Protocol (MCP)**

<p>
  <img src="https://img.shields.io/badge/Python-3.11-blue" />
  <img src="https://img.shields.io/badge/LangGraph-Multi--Agent-success" />
  <img src="https://img.shields.io/badge/LangChain-LLM-green" />
  <img src="https://img.shields.io/badge/MCP-Model_Context_Protocol-orange" />
  <img src="https://img.shields.io/badge/Groq-Llama_3.3_70B-red" />
  <img src="https://img.shields.io/badge/PostgreSQL-Database-blueviolet" />
</p>

</div>

---

# Overview

This project is an **AI-powered Multi-Agent Travel Booking System** that leverages **LangGraph** and the **Model Context Protocol (MCP)** to coordinate multiple intelligent agents for personalized travel planning.

The application combines **LLM reasoning**, **tool calling**, and **real-time APIs** to provide users with flight recommendations, hotel suggestions, weather forecasts, and complete travel itineraries through a seamless conversational interface.

---

# Problem Statement

Planning a trip often requires switching between multiple platforms for flights, hotels, weather updates, and itinerary planning.

**Objectives:**

- Build a collaborative **Multi-Agent AI System**
- Integrate real-time travel services using **MCP**
- Generate personalized travel itineraries
- Maintain long-term conversation memory
- Deliver an interactive travel planning experience

---

# System Architecture

```text
                   User Query
                        │
                        ▼
              LangGraph Orchestrator
                        │
        ┌───────────────┼───────────────┐
        ▼               ▼               ▼
  Flight Agent    Hotel Agent    Weather Agent
        │               │               │
        └───────────────┼───────────────┘
                        ▼
               Itinerary Agent
                        │
                        ▼
             Personalized Travel Plan
```

---

# Key Features

- 🤖 Multi-Agent AI workflow using **LangGraph**
- ✈️ Flight recommendations via Aviation MCP
- 🏨 Hotel recommendations using Tavily Search
- 🌤️ Live weather and forecast integration
- 🗺️ AI-generated personalized itineraries
- 🧠 Long-term conversational memory with PostgreSQL
- 🔐 Secure Login & Signup with PBKDF2 password hashing
- 📄 Download travel plans in **PDF** and **Markdown**
- 🎨 Interactive Streamlit dashboard

---

# Technologies Used

| Category | Technologies |
|----------|--------------|
| Programming Language | Python |
| AI Framework | LangGraph, LangChain |
| LLM | Groq Llama 3.3 70B |
| Protocol | Model Context Protocol (MCP) |
| Frontend | Streamlit |
| Backend | FastAPI |
| Database | PostgreSQL |
| Authentication | PBKDF2 Password Hashing |
| APIs | Tavily Search, AviationStack, OpenWeather |
| Others | AsyncIO, dotenv |

---

# Project Workflow

### Step 1
User enters a travel request.

⬇️

### Step 2
LangGraph routes the request to multiple specialized AI agents.

⬇️

### Step 3

Each agent performs its dedicated task:

- Flight Agent
- Hotel Agent
- Weather Agent

⬇️

### Step 4

The Itinerary Agent combines all results into a personalized travel plan.

⬇️

### Step 5

The final itinerary is displayed and can be downloaded.

---

# Project Structure

```text
Multi-Agent-System-MCP/
│
├── frontend.py
├── project.py
├── auth.py
├── mcp_client.py
├── custom_weather_mcp_server.py
├── travel_plans/
├── tools/
├── pyproject.toml
├── uv.lock
└── README.md
```

---
# Skills Demonstrated

- Multi-Agent AI Systems
- LangGraph Workflow Design
- Model Context Protocol (MCP)
- LLM Tool Calling
- Prompt Engineering
- AI Agent Orchestration
- Long-Term Memory
- Authentication & Authorization
- REST API Integration
- PostgreSQL Database Management
- Streamlit Application Development

---

# Future Enhancements

- Voice-enabled travel assistant
- Real-time flight booking integration
- Currency conversion
- Interactive travel maps
- Multi-language support
- Docker deployment
- Cloud deployment (AWS/Azure)

---

# Screenshots

> Add screenshots of the login page, dashboard, and generated itinerary here.

---

# Author

### **Vinay Verma**

**AI • GenAI • Machine Learning • Software Development**

---

# ⭐ Support

If you found this project helpful, consider giving it a **Star ⭐** on GitHub!
