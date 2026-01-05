from fastapi import FastAPI
from app.routes import scoring
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(
    title="AI Credit Scoring Platform",
    description="API for alternative credit scoring for micro-finance",
    version="1.0.0"
)
app.include_router(scoring.router)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # allow frontend URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
def root():
    return {"message": "AI Credit Platform backend is running 🚀"}

@app.get("/health")
def health_check():
    return {"status": "OK"}
