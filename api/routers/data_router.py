from fastapi import APIRouter
from pydantic import BaseModel

router = APIRouter(prefix="/api/data", tags=["1. Data Ingestion"])

# Strict Data Contract (Schema)
class SleepDataPayload(BaseModel):
    user_id: str
    heart_rate: int
    hrv: int        # Heart Rate Variability
    movement: int   # Movement count during sleep

@router.post("/")
async def upload_sleep_data(payload: SleepDataPayload):
    """
    High-throughput endpoint for daily batch uploads from the smart ring.
    Currently in MVP stage: logs to terminal instead of writing to DB.
    """
    # Stage 3 will integrate the scoring_domain algorithm here
    print(f"[Event Bus] Successfully received sleep data for user {payload.user_id}: {payload.model_dump()}")
    return {"status": "success", "message": "Data received and written to mock database."}