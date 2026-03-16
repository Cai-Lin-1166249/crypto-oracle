from fastapi import FastAPI

from feature_src.scheduler.feature_scheduler import FeatureScheduler

app = FastAPI()

scheduler = FeatureScheduler()

@app.on_event("startup")
async def startup():
    """
    Starts the feature generation scheduler.
    """
    scheduler.start()

@app.get("/health")
def health():
    """
    health check endpoint
    """
    return {"status": "ok"}
