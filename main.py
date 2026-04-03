"""
FastAPI server for the AI Travel Planner Agent.
Exposes REST endpoints consumed by the frontend UI.
"""

import os
import uuid
from contextlib import asynccontextmanager

from fastapi import FastAPI, HTTPException
from fastapi.responses import HTMLResponse
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import uvicorn
from dotenv import load_dotenv

load_dotenv()

# ── ADK imports ────────────────────────────────────────────────────────────────
from google.adk.runners import Runner
from google.adk.sessions import InMemorySessionService
from google.genai import types as genai_types

APP_NAME = "travel_planner"
session_service = InMemorySessionService()
runner = None

# ✅ Gemini key mapping (IMPORTANT)
os.environ["GOOGLE_API_KEY"] = os.getenv("GEMINI_API_KEY", "")


# ── Startup lifecycle (SAFE) ───────────────────────────────────────────────────
@asynccontextmanager
async def lifespan(app: FastAPI):
    global runner
    try:
        from agent import root_agent  # ✅ FIXED IMPORT

        runner = Runner(
            agent=root_agent,
            app_name=APP_NAME,
            session_service=session_service,
        )
        print("✅ Travel Planner Agent ready.")
    except Exception as e:
        print("❌ Startup error:", str(e))
        runner = None

    yield
    print("👋 Shutting down.")


app = FastAPI(title="AI Travel Planner", version="1.0.0", lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)


# ── Request / Response models ──────────────────────────────────────────────────
class PlanRequest(BaseModel):
    query: str
    session_id: str = ""


class PlanResponse(BaseModel):
    result: str
    session_id: str


# ── Health check ───────────────────────────────────────────────────────────────
@app.get("/health")
async def health():
    return {"status": "ok", "agent": "travel_planner_agent"}


# ── Main API ───────────────────────────────────────────────────────────────────
@app.post("/plan", response_model=PlanResponse)
async def plan_trip(body: PlanRequest):
    if not runner:
        raise HTTPException(status_code=503, detail="Agent not ready yet.")

    session_id = body.session_id or str(uuid.uuid4())

    # ✅ Always create session (Cloud Run safe)
    await session_service.create_session(
        app_name=APP_NAME,
        user_id="user",
        session_id=session_id
    )

    user_message = genai_types.Content(
        role="user",
        parts=[genai_types.Part(text=body.query)],
    )

    result_text = ""
    try:
        async for event in runner.run_async(
            user_id="user",
            session_id=session_id,
            new_message=user_message,
        ):
            if event.is_final_response() and event.content and event.content.parts:
                result_text = event.content.parts[0].text
                break
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

    return PlanResponse(
        result=result_text or "No response from agent.",
        session_id=session_id
    )


# ── Serve UI safely ────────────────────────────────────────────────────────────
@app.get("/", response_class=HTMLResponse)
async def serve_ui():
    html_path = os.path.join(os.path.dirname(__file__), "index.html")

    if not os.path.exists(html_path):
        return "<h1>UI not found</h1>"

    with open(html_path, encoding="utf-8") as f:
        return f.read()


# ── Entry point ────────────────────────────────────────────────────────────────
if __name__ == "__main__":
    port = int(os.getenv("PORT", 8080))
    uvicorn.run("main:app", host="0.0.0.0", port=port)