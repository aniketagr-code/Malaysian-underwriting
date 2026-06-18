from fastapi import FastAPI, Request, status
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
import uvicorn

from .schemas import QuoteRequest
from .engine import generate_quote
from .database import init_db, log_quote

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    await init_db()
    yield
    # Shutdown

app = FastAPI(title="Malaysia Motor Insurance Underwriting Model", version="1.0.0", lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    # Extract the first error and format it
    errors = exc.errors()
    if errors:
        first_error = errors[0]
        field = ".".join([str(x) for x in first_error.get("loc", [])])
        msg = first_error.get("msg", "")
        return JSONResponse(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            content={
                "error_code": "VALIDATION_ERROR",
                "message": msg,
                "field": field
            }
        )
    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content={"error_code": "VALIDATION_ERROR", "message": "Invalid request payload", "field": "unknown"}
    )

import traceback
@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    traceback.print_exc()
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={
            "error_code": "SYSTEM_ERROR",
            "message": str(exc),
            "field": ""
        }
    )

@app.get("/health")
async def health_check():
    return {"status": "ok", "model_version": app.version}

@app.get("/version")
async def get_version():
    return {"model_version": app.version}

@app.post("/quote")
async def create_quote(req: QuoteRequest):
    result = generate_quote(req)
    print("DEBUG RAW RESULT:", result)
    await log_quote(req.model_dump(), result)
    return result

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)

# Trigger reload
