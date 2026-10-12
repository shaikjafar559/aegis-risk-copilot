import os
from fastapi import FastAPI, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse, JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from app.models import GenerateRequest, InterruptRequest, BranchSelectionRequest
from app.engine.pipeline import MultiAgentBroadcastEngine
from app.engine.gcp_vertex_adapter import gcp_adapter

app = FastAPI(
    title="OmniStory Studio",
    description="Living Interactive Media & Adaptive Broadcast Engine (Google Cloud Platform & Vertex AI Compatible)",
    version="2.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Static files directory
STATIC_DIR = os.path.join(os.path.dirname(__file__), "static")
if not os.path.exists(STATIC_DIR):
    os.makedirs(STATIC_DIR, exist_ok=True)

app.mount("/static", StaticFiles(directory=STATIC_DIR), name="static")

@app.get("/")
def get_index():
    index_path = os.path.join(STATIC_DIR, "index.html")
    if os.path.exists(index_path):
        return FileResponse(index_path)
    return {"message": "OmniStory Studio API is running. UI index.html not yet built."}

@app.get("/api/health")
def health_check():
    return {
        "status": "healthy",
        "service": "OmniStory Studio",
        "version": "2.0.0",
        "cloud_platform": "Google Cloud Run / Vertex AI Compatible",
        "gcp_telemetry": gcp_adapter.get_service_telemetry(),
        "social_impact_ready": True,
        "active_broadcasts_count": len(MultiAgentBroadcastEngine.list_broadcasts())
    }

@app.get("/api/broadcasts")
def list_broadcasts():
    return MultiAgentBroadcastEngine.list_broadcasts()

@app.get("/api/broadcasts/{broadcast_id}")
def get_broadcast(broadcast_id: str):
    b = MultiAgentBroadcastEngine.get_broadcast(broadcast_id)
    if not b:
        raise HTTPException(status_code=404, detail="Broadcast not found")
    return b

@app.post("/api/generate")
def generate_broadcast(req: GenerateRequest):
    if not req.topic.strip():
        raise HTTPException(status_code=400, detail="Topic cannot be empty")
    manifest = MultiAgentBroadcastEngine.generate_custom_broadcast(req)
    return manifest

@app.post("/api/interrupt")
def interrupt_broadcast(req: InterruptRequest):
    if not req.user_question.strip():
        raise HTTPException(status_code=400, detail="Question cannot be empty")
    result = MultiAgentBroadcastEngine.handle_interrupt(req)
    return result

@app.post("/api/branch")
def choose_branch(req: BranchSelectionRequest):
    new_lines = MultiAgentBroadcastEngine.expand_branch(req.broadcast_id, req.branch_id)
    return {
        "status": "branch_activated",
        "broadcast_id": req.broadcast_id,
        "branch_id": req.branch_id,
        "new_lines": [line.dict() for line in new_lines]
    }

@app.get("/api/export/{broadcast_id}")
def export_broadcast(broadcast_id: str):
    b = MultiAgentBroadcastEngine.get_broadcast(broadcast_id)
    if not b:
        raise HTTPException(status_code=404, detail="Broadcast not found")

    # Generate an executive markdown export
    md_content = f"""# {b.title}
*{b.subtitle}*

**Format:** {b.persona_style.value.upper()} | **Estimated Runtime:** {b.duration_est}  
**Source Topic:** {b.source_topic}

---

## Executive Summary
{b.summary}

## Key Strategic Takeaways
{chr(10).join(f"- {t}" for t in b.key_takeaways)}

## Perspective Matrix
| Dimension | Score | Assessment |
|---|---|---|
{chr(10).join(f"| {p.dimension} | {p.score}/100 | {p.summary} |" for p in b.perspectives)}

---

## Complete Multi-Agent Broadcast Script
{chr(10).join(f"**[{line.speaker_name}]** ({line.emotion.value.upper()}): {line.text}\\n" for line in b.lines)}

---
## Omnichannel Social Distribution Package
- **Headline:** {b.social_assets.get('viral_headline', '')}
- **Short Video Hook:** {b.social_assets.get('short_script_hook', '')}
- **X/Twitter Thread Opener:** {b.social_assets.get('thread_post', '')}
- **LinkedIn Brief:** {b.social_assets.get('linkedin_take', '')}
"""

    return {
        "broadcast_id": b.id,
        "manifest": b.dict(),
        "markdown_export": md_content,
        "social_assets": b.social_assets
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app.main:app", host="127.0.0.1", port=8000, reload=True)
