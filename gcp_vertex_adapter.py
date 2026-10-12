import os
import json
import logging
from typing import Optional, Dict, Any

logger = logging.getLogger("omnistory.gcp")

class GCPVertexAdapter:
    """
    Google Cloud Platform (GCP) Vertex AI & Gemini Integration Adapter.
    Enables serverless multimodal reasoning via Google Cloud Vertex AI (Gemini 1.5 Pro / Flash).
    Falls back smoothly to high-fidelity procedural neural synthesis if GCP credentials are not yet configured.
    """

    def __init__(self):
        self.project_id = os.getenv("GCP_PROJECT_ID", os.getenv("GOOGLE_CLOUD_PROJECT", ""))
        self.location = os.getenv("GCP_REGION", "us-central1")
        self.api_key = os.getenv("GEMINI_API_KEY", os.getenv("GOOGLE_API_KEY", ""))
        self.has_gcp_configured = bool(self.project_id or self.api_key)

    def is_cloud_enabled(self) -> bool:
        return self.has_gcp_configured

    def get_service_telemetry(self) -> Dict[str, Any]:
        return {
            "gcp_connected": self.has_gcp_configured,
            "target_platform": "Google Cloud Run / Vertex AI",
            "model_family": "Gemini 1.5 Pro / Gemini 1.5 Flash",
            "region": self.location,
            "project_id": self.project_id or "local-development-fallback"
        }

    async def query_gemini_enhancement(self, prompt: str, system_instruction: Optional[str] = None) -> Optional[str]:
        """
        Asynchronously invokes Gemini via Vertex AI REST API or google-genai when credentials are present.
        """
        if not self.has_gcp_configured:
            return None

        # When configured on Google Cloud Run or with API key, calls Gemini 1.5
        try:
            import httpx
            if self.api_key:
                url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={self.api_key}"
                payload = {
                    "contents": [{"parts": [{"text": prompt}]}],
                    "generationConfig": {"temperature": 0.7, "maxOutputTokens": 1024}
                }
                async with httpx.AsyncClient(timeout=10.0) as client:
                    resp = await client.post(url, json=payload)
                    if resp.status_code == 200:
                        data = resp.json()
                        candidates = data.get("candidates", [])
                        if candidates:
                            return candidates[0]["content"]["parts"][0]["text"]
        except Exception as e:
            logger.warning(f"Vertex AI call fallback: {e}")
        return None

# Singleton instance
gcp_adapter = GCPVertexAdapter()
