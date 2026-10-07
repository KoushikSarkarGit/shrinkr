from fastapi import FastAPI

app = FastAPI(
    title="Shrinkr",
    description="Production-oriented URL Shortener and Analytics API",
    version="0.1.0",
)

@app.get("/healthz")
async def get_health():
    return {'status': 'Ok'}