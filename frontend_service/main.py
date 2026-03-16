from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse

app = FastAPI(title="Crypto Oracle Frontend")

app.mount("/static", StaticFiles(directory="static"), name="static")

@app.get("/")
def dashboard():
    return FileResponse("templates/dashboard.html")

@app.get("/market")
def market():
    return FileResponse("templates/market.html")

@app.get("/system")
def system():
    return FileResponse("templates/system.html")

@app.get("/health")
def health():
    return {"status": "ok"}