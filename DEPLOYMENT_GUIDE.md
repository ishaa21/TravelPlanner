# 🌍 Voyage — AI Travel Planner
## Complete Deployment Guide (Beginner-Friendly)
### Track 2: Connect AI Agents to Real-World Data using MCP

---

## 📁 Project Structure

```
travel_planner_agent/
├── agent.py              ← ADK LlmAgent + Google Maps MCPToolset
├── main.py               ← FastAPI server (REST API + serves HTML)
├── static/
│   └── index.html        ← Beautiful frontend UI
├── requirements.txt      ← Python packages
├── Dockerfile            ← For Cloud Run deployment
├── .env.example          ← Template for environment variables
└── __init__.py           ← Makes it a Python package
```

---

## STEP 1 — Upload files to Cloud Shell

In Cloud Shell, run:
```bash
mkdir -p ~/travel_planner_agent/static
```

Then upload all files from this folder into `~/travel_planner_agent/`
and `static/index.html` into `~/travel_planner_agent/static/`.

---

## STEP 2 — Create your .env file

```bash
cat << 'EOF' > ~/travel_planner_agent/.env
GOOGLE_GENAI_USE_VERTEXAI=TRUE
GOOGLE_CLOUD_PROJECT=qwiklabs-gcp-00-c06207955c1b
GOOGLE_CLOUD_LOCATION=global
GOOGLE_MAPS_API_KEY=AIzaSyCQu688C2JzUumUMtqbcsn7beL7zA_Qyyc
MODEL=gemini-2.5-flash
EOF
```

Replace `PASTE_YOUR_MAPS_API_KEY_HERE` with your actual key from the lab.

---

## STEP 3 — Install dependencies locally

```bash
cd ~/travel_planner_agent
pip install -r requirements.txt
```

---

## STEP 4 — Test locally (optional but recommended)

```bash
cd ~/travel_planner_agent
python3 main.py
```

Click the URL shown in the terminal to preview it.
Try a query like: "Plan a 2-day trip from Delhi to Jaipur"

Press Ctrl+C when done testing.

---

## STEP 5 — Deploy to Cloud Run

Run these commands one by one in Cloud Shell:

```bash
# Set your project ID
export PROJECT_ID=$(gcloud config get-value project)
export REGION=us-central1
export SERVICE=travel-planner-agent

# Go to project folder
cd ~/travel_planner_agent

# Build the container image
gcloud builds submit --tag gcr.io/$PROJECT_ID/$SERVICE .

# Deploy to Cloud Run
gcloud run deploy $SERVICE \
  --image gcr.io/$PROJECT_ID/$SERVICE \
  --platform managed \
  --region $REGION \
  --allow-unauthenticated \
  --memory 1Gi \
  --timeout 120 \
  --set-env-vars GOOGLE_GENAI_USE_VERTEXAI=TRUE \
  --set-env-vars GOOGLE_CLOUD_PROJECT=$PROJECT_ID \
  --set-env-vars GOOGLE_CLOUD_LOCATION=global \
  --set-env-vars MODEL=gemini-2.5-flash \
  --set-env-vars GOOGLE_MAPS_API_KEY="PASTE_YOUR_KEY_HERE"
```

---

## STEP 6 — Get your public URL

After deployment finishes, you will see:
```
Service URL: https://travel-planner-agent-xxxxxxx-uc.a.run.app
```

✅ That is your submission URL — it is publicly accessible!

---

## Troubleshooting

**Build fails?**
```bash
gcloud services enable cloudbuild.googleapis.com run.googleapis.com
```

**Agent returns empty response?**
- Check your Maps API key is correct
- Make sure Routes API and Directions API are enabled in your project

**View logs:**
```bash
gcloud run logs read --service travel-planner-agent --region us-central1
```

---

## What to Submit

1. **Cloud Run URL** — the `Service URL` from Step 6
2. **PPT** — 2–3 slide presentation (provided separately)
