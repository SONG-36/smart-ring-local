from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from mangum import Mangum
import uvicorn

# Import routing modules
from api.routers import data_router, chat_router

# Initialize core application
app = FastAPI(title="Smart Ring MVP", version="1.0.0")

# Configure CORS for frontend integration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], # MVP stage: allow all origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mount sub-routers
app.include_router(data_router.router)
app.include_router(chat_router.router)

@app.get("/health", tags=["0. System Probe"])
def health_check():
    """Lightweight probe for load balancers and container health checks."""
    return {"status": "System Online", "component": "FastAPI Gateway"}

# AWS Lambda adapter for Serverless deployment
handler = Mangum(app)

if __name__ == "__main__":
    # Local development server
    uvicorn.run("api.main:app", host="127.0.0.1", port=8000, reload=True)