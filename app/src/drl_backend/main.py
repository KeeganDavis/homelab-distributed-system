import logging

from fastapi import FastAPI

from .logging_config import configure_logging

configure_logging()
logger = logging.getLogger(__name__)

app = FastAPI(
    title="Distributed Reliability Lab Backend",
    version="0.1.0",
)


@app.get("/health")
def health() -> dict[str, str]:
    logger.debug("Health check requested")
    return {"status": "ok"}