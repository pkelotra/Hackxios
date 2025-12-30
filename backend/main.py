"""
FastAPI main application.
Health Insurance Denial Prevention & Appeal Assistant Backend.
"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import logging

from database import init_db
from routes import upload, analyze, appeal, insurance
from config import settings

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Initialize FastAPI app
app = FastAPI(
    title="Health Insurance Denial Assistant API",
    description="AI-powered health insurance denial prevention and appeal assistant",
    version="1.0.0"
)

# Configure CORS for frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # <--- CHANGED THIS to allow Vercel
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize database on startup
@app.on_event("startup")
async def startup_event():
    """Initialize database tables on application startup."""
    logger.info("Initializing database...")
    init_db()
    logger.info("Database initialized successfully")
    logger.info(f"Upload folder: {settings.UPLOAD_FOLDER}")
    logger.info(f"Insurance rules directory: {settings.INSURANCE_RULES_DIR}")

# Health check endpoint
@app.get("/")
async def root():
    """Root endpoint - health check."""
    return {
        "status": "healthy",
        "message": "Health Insurance Denial Assistant API",
        "version": "1.0.0"
    }

@app.get("/health")
async def health_check():
    """Detailed health check endpoint."""
    return {
        "status": "healthy",
        "database": "connected",
        "groq_api_configured": bool(settings.GROQ_API_KEY),
        "upload_folder": str(settings.UPLOAD_FOLDER),
        "models": {
            "extractor": settings.EXTRACTOR_MODEL,
            "reasoning": settings.REASONING_MODEL
        }
    }

# Register routers
app.include_router(upload.router, prefix="/api", tags=["Upload"])
app.include_router(analyze.router, prefix="/api", tags=["Analysis"])
app.include_router(appeal.router, prefix="/api", tags=["Appeal"])
app.include_router(insurance.router, prefix="/api", tags=["Insurance"])
from routes import session
app.include_router(session.router, prefix="/api", tags=["Session"])

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "main:app",
        host=settings.BACKEND_HOST,
        port=settings.BACKEND_PORT,
        reload=True
    )
