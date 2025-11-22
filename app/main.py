from fastapi import FastAPI
from app.api.review_routes import router as review_router

app = FastAPI(
    title="Automated PR Review Agent",
    version="1.0.0"
)

# Register API routes
app.include_router(review_router, prefix="/review")

@app.get("/")
def root():
    return {"message": "PR Review Agent Backend Running"}
