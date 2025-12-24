from fastapi import FastAPI
from app.routes import scoring

app = FastAPI(
    title="AI Credit Scoring Platform",
    description="API for alternative credit scoring for micro-finance",
    version="1.0.0"
)
app.include_router(scoring.router)


@app.get("/")
def root():
    return {"message": "AI Credit Platform backend is running 🚀"}

@app.get("/health")
def health_check():
    return {"status": "OK"}
