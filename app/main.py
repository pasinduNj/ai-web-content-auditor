from fastapi import FastAPI, BackgroundTasks
from app.models import URLRequest
from app.tasks import process_website
from app.cache import init_db, get_cached_result
from fastapi import Request, status
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse

app = FastAPI(title="Website Content Analyzer")

# Create database on startup
init_db()

@app.get("/")
def home():
    return {"message": "System is active. Use /docs to test POST /analyze"}

@app.post("/analyze")
async def analyze(request: URLRequest, background_tasks: BackgroundTasks):
    # 1. Check Caching Layer first
    cached_data = get_cached_result(request.url)
    if cached_data:
        return {"status": "Cached", "url": request.url, "data": cached_data}

    # 2. Add to Background Tasks
    background_tasks.add_task(process_website, request.url)
    
    return { 
        "message": "Analysis started in background.",
        "url": request.url,
        "check_back_at": "/results"
    }

@app.get("/results")
def results(url: str):
    data = get_cached_result(url)
    if not data:
        return {"status": "Pending", "message": "Analysis still in progress or not started."}
    return {"status": "Success", "data": data}


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    # Search the errors for our custom message from models.py
    for error in exc.errors():
        # 'msg' usually contains the text from your 'raise ValueError(...)'
        if "please provide URL format" in error.get("msg", "").lower():
            return JSONResponse(
                status_code=status.HTTP_400_BAD_REQUEST,
                content={"detail": "please provide URL format"}
            )
    
    # If it's a different validation error (like a missing field), return a generic 422
    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content={"detail": "Invalid request data. Please provide a valid URL ()."}
    )