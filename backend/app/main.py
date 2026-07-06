from fastapi import FastAPI

app = FastAPI(
    title="CareerPilot AI",
    description="AI-powered Career Assistant for Resume Analysis, ATS Scoring and Interview Preparation",
    version="1.0.0",
)


@app.get("/")
async def root():
    return {
        "project": "CareerPilot AI",
        "status": "Running",
        "version": "1.0.0",
        "message": "Welcome to CareerPilot AI 🚀"
    }


@app.get("/health")
async def health():
    return {
        "status": "healthy",
        "backend": "online"
    }