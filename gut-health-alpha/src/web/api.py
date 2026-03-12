import asyncio
import time
import uuid
import logging
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

class IncomingWebhook(BaseModel):
    user_id: str = Field(..., description="Unique identifier for the user session")
    message: str = Field(..., min_length=1, description="The user's symptom description")
    source: Literal["web", "whatsapp", "mobile"] = Field(default="web", description="Origin of the request")
    pdf_file_path: Optional[str] = Field(default=None, description="Path to the uploaded PDF file for analysis")
    image_file_paths: Optional[list] = Field(default=None, description="Paths to uploaded image files for analysis")

class WebhookResponse(BaseModel):
    user_id: str
    report: str
    processing_time_ms: int

# --- Global State & Lifespan ---
# We initialize the graph once at startup to avoid overhead per request
app_state = {}

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    logger.info("Initializing Agent Graph...")
    try:
        app_state["graph"] = create_gutsync_graph()
        logger.info("Agent Graph Initialized Successfully.")
    except Exception as e:
        logger.critical(f"Failed to initialize Agent Graph: {e}")
        raise e
    
    yield
    
    # Shutdown
    logger.info("Shutting down Gut Health API...")
    app_state.clear()

# --- FastAPI App Definition ---
app = FastAPI(
    title="Gut Symptom Detective API",
    version="1.0.0",
    description="Scalable Async Webhook API for Gut Health Analysis",
    lifespan=lifespan
)

# --- Middleware ---
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Open for development; restrict in prod
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# --- Async Graph Wrapper ---
def run_graph_sync(user_input: str, pdf_file_path: Optional[str] = None, image_file_paths: Optional[list] = None) -> dict:
    """
    Synchronous wrapper to run the LangGraph compiled graph.
    This function is NOT async, so it must be run in a thread pool.
    """
    try:
        graph = app_state.get("graph")
        if not graph:
            raise RuntimeError("Graph not initialized")

        # Initialize State
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
            # PDF State Initialization
            "pdf_uploaded": bool(pdf_file_path),
            "pdf_file_path": pdf_file_path,
            "pdf_extracted_text": None,
            "pdf_medical_summary": None,
            "pdf_key_findings": None,
            # Image State Initialization (mirrors PDF exactly)
            "images_uploaded": bool(image_file_paths),
            "image_file_paths": image_file_paths,
            "image_count": len(image_file_paths) if image_file_paths else 0,
            "image_descriptions": [],
            "image_visual_summary": None,
            "image_key_observations": [],
            "image_clinical_relevance": None
        }

        # Execute Graph
        # We use .invoke() for full execution. 
        # .stream() could be used for SSE, but webhook requires full response.
        final_state = graph.invoke(initial_state)
        return final_state

    except Exception as e:
        logger.error(f"Graph Execution Failed: {e}")
        raise e

# --- Endpoints ---

@app.get("/health")
async def health_check():
    """
    Health check endpoint for load balancers.
    """
    if not app_state.get("graph"):
        raise HTTPException(status_code=503, detail="Graph not initialized")
    return {"status": "healthy", "service": "Gut Symptom Detective"}

@app.post("/webhook/incoming", response_model=WebhookResponse)
async def incoming_webhook(payload: IncomingWebhook):
    """
    Main entry point for user analysis.
    Executes the agent graph asynchronously to avoid blocking the event loop.
    """
    start_time = time.perf_counter()
    logger.info(f"Received request from user_id={payload.user_id} source={payload.source}")

    if not payload.message.strip():
        raise HTTPException(status_code=400, detail="Empty message received")

    try:
        # Offload synchronous graph execution to a thread
        # This is CRITICAL for FastAPI scalability
        final_state = await asyncio.to_thread(run_graph_sync, payload.message, payload.pdf_file_path, payload.image_file_paths)

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
        # In production, be careful not to leak stack traces to users
        raise HTTPException(status_code=500, detail="Internal processing error")

if __name__ == "__main__":
    import uvicorn
    # In production, run with: uvicorn src.web.api:app --host 0.0.0.0 --port 8000 --workers 4
    uvicorn.run(app, host="0.0.0.0", port=8000)
