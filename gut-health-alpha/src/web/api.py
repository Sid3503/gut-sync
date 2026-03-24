import asyncio
import base64
import time
import uuid
import logging
import tempfile
import os
from typing import Literal, Optional
from contextlib import asynccontextmanager
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

from fastapi import FastAPI, HTTPException, Request, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field

# --- Import Agent Graph ---
from src.agent.gutsync_agent.graph.graph import create_gutsync_graph
from src.agent.gutsync_agent.graph.state.gut_state import GutSyncState

# --- Logging Setup (Lightweight) ---
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S"
)
logger = logging.getLogger("GutSyncAPI")

# --- Pydantic Models ---

class ImageContentB64(BaseModel):
    filename: str
    content: str  # base64-encoded

class IncomingWebhook(BaseModel):
    user_id: str = Field(..., description="Unique identifier for the user session")
    message: str = Field(..., min_length=1, description="The user's symptom description")
    source: Literal["web", "whatsapp", "mobile"] = Field(default="web", description="Origin of the request")
    # Legacy path-based fields (local dev only — containers share filesystem)
    pdf_file_path: Optional[str] = Field(default=None, description="Path to uploaded PDF (local dev only)")
    image_file_paths: Optional[list] = Field(default=None, description="Paths to uploaded images (local dev only)")
    # Cross-container base64 fields (production)
    pdf_content_b64: Optional[str] = Field(default=None, description="Base64-encoded PDF content")
    pdf_filename: Optional[str] = Field(default=None, description="Original PDF filename")
    image_contents_b64: Optional[list[ImageContentB64]] = Field(default=None, description="Base64-encoded images")

class WebhookResponse(BaseModel):
    user_id: str
    report: str
    processing_time_ms: int

# --- Global State & Lifespan ---
app_state = {}

@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("Initializing Agent Graph...")
    try:
        app_state["graph"] = create_gutsync_graph()
        logger.info("Agent Graph Initialized Successfully.")
    except Exception as e:
        logger.critical(f"Failed to initialize Agent Graph: {e}")
        raise e
    yield
    logger.info("Shutting down GutSync API...")
    app_state.clear()

# --- FastAPI App Definition ---
app = FastAPI(
    title="GutSync API",
    version="1.0.0",
    description="Scalable Async Webhook API for Gut Health Analysis",
    lifespan=lifespan
)

# --- Middleware ---
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

def _decode_b64_to_tempfile(content_b64: str, filename: str) -> str:
    """Decode a base64-encoded file and write it to a temp file. Returns the path."""
    file_bytes = base64.b64decode(content_b64)
    suffix = os.path.splitext(filename)[1] or ".bin"
    with tempfile.NamedTemporaryFile(delete=False, suffix=suffix, prefix=f"gutsync_{filename}_") as tmp:
        tmp.write(file_bytes)
        return tmp.name

def run_graph_sync(
    user_input: str,
    pdf_file_path: Optional[str] = None,
    image_file_paths: Optional[list] = None
) -> dict:
    """
    Synchronous wrapper to run the LangGraph compiled graph.
    Accepts resolved local file paths — decoding from base64 happens before this.
    """
    graph = app_state.get("graph")
    if not graph:
        raise RuntimeError("Graph not initialized")

    initial_state: GutSyncState = {
        "user_input": user_input,
        "symptoms": [],
        "timing": None,
        "diet_changes": None,
        "medications": [],
        "symptom_patterns": [],
        "possible_root_causes": [],
        "severity": None,
        "relief_strategies": [],
        "red_flags": [],
        "report": None,
        "pdf_uploaded": bool(pdf_file_path),
        "pdf_file_path": pdf_file_path,
        "pdf_extracted_text": None,
        "pdf_medical_summary": None,
        "pdf_key_findings": None,
        "images_uploaded": bool(image_file_paths),
        "image_file_paths": image_file_paths,
        "image_count": len(image_file_paths) if image_file_paths else 0,
        "image_descriptions": [],
        "image_visual_summary": None,
        "image_key_observations": [],
        "image_clinical_relevance": None
    }

    final_state = graph.invoke(initial_state)
    return final_state

# --- Endpoints ---

@app.get("/health")
async def health_check():
    if not app_state.get("graph"):
        raise HTTPException(status_code=503, detail="Graph not initialized")
    return {"status": "healthy", "service": "GutSync"}

@app.post("/webhook/incoming", response_model=WebhookResponse)
async def incoming_webhook(payload: IncomingWebhook):
    start_time = time.perf_counter()
    logger.info(f"Received request from user_id={payload.user_id} source={payload.source}")

    if not payload.message.strip():
        raise HTTPException(status_code=400, detail="Empty message received")

    temp_files: list[str] = []
    try:
        # Resolve PDF path — prefer base64 content (cross-container), fallback to path (local dev)
        pdf_path: Optional[str] = None
        if payload.pdf_content_b64 and payload.pdf_filename:
            pdf_path = _decode_b64_to_tempfile(payload.pdf_content_b64, payload.pdf_filename)
            temp_files.append(pdf_path)
            logger.info(f"Decoded PDF from base64 → {pdf_path}")
        elif payload.pdf_file_path:
            pdf_path = payload.pdf_file_path
            logger.info(f"Using provided PDF path: {pdf_path}")

        # Resolve image paths
        image_paths: Optional[list[str]] = None
        if payload.image_contents_b64:
            image_paths = []
            for img in payload.image_contents_b64:
                path = _decode_b64_to_tempfile(img.content, img.filename)
                image_paths.append(path)
                temp_files.append(path)
            logger.info(f"Decoded {len(image_paths)} images from base64")
        elif payload.image_file_paths:
            image_paths = payload.image_file_paths

        final_state = await asyncio.to_thread(run_graph_sync, payload.message, pdf_path, image_paths)

        report_content = final_state.get("report")
        if not report_content:
            logger.error(f"Graph completed but 'report' is missing. User: {payload.user_id}")
            raise HTTPException(status_code=500, detail="Analysis completed but no report generated.")

        processing_time = int((time.perf_counter() - start_time) * 1000)
        logger.info(f"Request processed successfully in {processing_time}ms")

        return WebhookResponse(
            user_id=payload.user_id,
            report=report_content,
            processing_time_ms=processing_time
        )

    except asyncio.TimeoutError:
        logger.error(f"Timeout processing request for user {payload.user_id}")
        raise HTTPException(status_code=504, detail="Request timed out")

    except Exception as e:
        logger.error(f"Internal Error processing request: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal processing error")

    finally:
        # Clean up temp files written by this request
        for path in temp_files:
            try:
                os.unlink(path)
            except OSError:
                pass

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)