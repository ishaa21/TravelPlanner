# 🌍 Voyage - AI Travel Planner

Welcome to **Voyage - AI Travel Planner**, an intelligent multi-agent travel planning assistant powered by Google ADK, Google GenAI (Gemini), and the Model Context Protocol (MCP) server for Google Maps.

## 🚀 Live Demo
Experience the live application here:
**[Voyage AI Travel Planner](https://travel-planner-648281661119.us-central1.run.app/)**

## 📖 Overview

This project showcases how to connect AI Agents to Real-World Data using **MCP (Model Context Protocol)**. It integrates Google Maps into the reasoning pipeline of the AI agent, allowing it to:
- Formulate practical and accurate itineraries
- Retrieve precise venue details and nearby attractions
- Validate generated travel plans directly via Maps data
- Execute geospatial and directional reasoning

The project employs a Python FastAPI backend for serving both the REST endpoint for the LLM orchestration and a dynamic, beautiful frontend UI.

## 🛠️ Tech Stack
- **AI/LLM**: Google Gemini (via `google-genai` and `google.adk`)
- **Backend Framework**: Core Python with FastAPI
- **Frontend**: HTML5, CSS3, JavaScript (Vanilla)
- **Tooling/Integration**: `@modelcontextprotocol/server-google-maps`
- **Deployment**: Docker, Google Cloud Run

## 📁 Project Structure

```text
├── agent.py              # LLM Agent configuration & Google Maps MCP Toolset integration
├── main.py               # FastAPI application, serving API endpoints and the frontend UI
├── index.html            # The main frontend web interface
├── requirements.txt      # Python dependencies
├── Dockerfile            # Container configuration for deployment
├── .env.example          # Example environment variable file
└── DEPLOYMENT_GUIDE.md   # Step-by-step instructions for deploying to Cloud Run
```

## ⚙️ Getting Started (Local Development)

### Prerequisites
- Python 3.10+
- Node.js 20+ (required for the MCP tools execution natively via `npx`)
- A [Google Maps API Key](https://developers.google.com/maps)
- A [Gemini API Key](https://aistudio.google.com/) or Vertex AI Access

### Installation & Setup

1. **Clone the Repository**
   ```bash
   git clone <your-repo-url>
   cd travelPlanner
   ```

2. **Set Up Environment Variables**
   ```bash
   cp .env.example .env
   ```
   Update `.env` with your `GOOGLE_MAPS_API_KEY` and your project details.

3. **Install Dependencies**
   ```bash
   # Python requirements
   pip install -r requirements.txt

   # Pre-cache the Google Maps MCP Server (optional but recommended for speed)
   npm install -g @modelcontextprotocol/server-google-maps
   ```

4. **Run the API & Frontend**
   ```bash
   python main.py
   ```
   Open `http://localhost:8080/` in your browser.

## 🚢 Deployment
A comprehensive guide is provided in the [`DEPLOYMENT_GUIDE.md`](./DEPLOYMENT_GUIDE.md) covering deployment via Google Cloud Run.

## 🤝 Contributing
Contributions, issues, and feature requests are welcome!

## 📄 License
This project is open-source and available under the MIT License.
