from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from routes.candles import router as candles_router
from routes.features import router as feature_router
from routes.assets import router as collector_router
from routes.market import router as market_router
from routes.system import router as system_router

app = FastAPI(title="Crypto Oracle API Gateway")

# enables CORPS for frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# API prefix unification registration
app.include_router(candles_router, prefix="/api")
app.include_router(feature_router, prefix="/api")
app.include_router(collector_router, prefix="/api")
app.include_router(market_router, prefix="/api")
app.include_router(system_router, prefix="/api")

@app.get("/health")
def health():
    return {"status": "ok"}
