import code
import logging
import logging.config
import asgi_correlation_id
from fastapi import FastAPI, HTTPException, Request
from asgi_correlation_id import CorrelationIdMiddleware
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from pydantic import BaseModel

from core.logger import CorrelationIdFilter
from core.middleware.application import ApplicationMiddleware


def configure_logging():
    console_handler = logging.StreamHandler()
    console_handler.addFilter(CorrelationIdFilter())
    logging.basicConfig(
        handlers=[console_handler],
        level="INFO",
        format="%(levelname)s:     [%(correlation_id)s] %(message)s",
    )


# disable uvicorn logs
uvicorn_access = logging.getLogger("uvicorn.access")
uvicorn_access.setLevel(level=logging.FATAL)

app = FastAPI(on_startup=[configure_logging])
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["X-Api-Request-ID"],
    # expose_headers=["X-Api-Request-ID"],
)
# app.add_middleware(CorrelationIdMiddleware, header_name="X-Api-Request-ID")
app.add_middleware(ApplicationMiddleware)


# @app.exception_handler(Exception)
# async def custom_exception_handler(request: Request, exc: Exception):
#     return JSONResponse(
#         status_code=500,
#         content={"message": f"Exception Occurred! Reason -> {str(exc)}"},
#     )
logger = logging.getLogger(__name__)


@app.get("/health")
async def health():
    logger.info("Health check")
    logger.debug("Debugging health check")
    raise Exception("xxx")
    # You can consider ping other services here
    return {"status": "ok"}


class Item(BaseModel):
    name: str


@app.post("/items")
async def create_item(item: Item):
    return item
