from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import Session
from typing import List, Optional
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Create FastAPI app
app = FastAPI(
    title="HungryJack API",
    description="API for HungryJack AI Meal Planner",
    version="0.1.0",
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, replace with specific origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Import API router
try:
    from api.router import router as api_router
    app.include_router(api_router, prefix="/api")
except ImportError:
    # If the router module is not available, create a simple endpoint
    @app.get("/")
    async def root():
        return {"message": "Welcome to HungryJack API"}
    
    @app.get("/api/health")
    async def health_check():
        return {"status": "ok", "message": "API is running"}

# Add error handlers
@app.exception_handler(HTTPException)
async def http_exception_handler(request, exc):
    return {"detail": exc.detail, "status_code": exc.status_code}

@app.exception_handler(Exception)
async def general_exception_handler(request, exc):
    return {"detail": str(exc), "status_code": status.HTTP_500_INTERNAL_SERVER_ERROR}

# Startup and shutdown events
@app.on_event("startup")
async def startup_event():
    print("Starting up HungryJack API...")
    # Check if required environment variables are set
    required_env_vars = [
        "SUPABASE_URL",
        "SUPABASE_SERVICE_KEY",
        "SUPABASE_ANON_KEY",
    ]
    
    missing_vars = [var for var in required_env_vars if not os.getenv(var)]
    if missing_vars:
        print(f"Warning: Missing environment variables: {', '.join(missing_vars)}")
        print("Some functionality may not work correctly.")

@app.on_event("shutdown")
async def shutdown_event():
    print("Shutting down HungryJack API...")

# Run the application
if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app:app", host="0.0.0.0", port=8000, reload=True)
