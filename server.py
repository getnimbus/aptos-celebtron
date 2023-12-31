from dotenv import load_dotenv

# load environment variables from .env file
load_dotenv()

from fastapi import FastAPI, HTTPException
from fastapi.openapi.utils import get_openapi
from fastapi.middleware.cors import CORSMiddleware
from starlette.requests import Request
from starlette.responses import Response
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address
from slowapi.middleware import SlowAPIMiddleware
from slowapi.errors import RateLimitExceeded
from datetime import datetime
from core.aptos import get_tx_by_version, get_tx_by_hash, ask_question
import logging.config


def initialize_logging(level=logging.INFO):
    handler = logging.StreamHandler()
    handler.setFormatter(
        logging.Formatter(
            "%(asctime)s - %(levelname)s - %(name)s - module=%(module)s - %(message)s"
        )
    )
    logging.getLogger().addHandler(handler)
    logging.getLogger().setLevel(level)


app = FastAPI()

# allow CORS
origins = ["*"]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# rate limit
limiter = Limiter(key_func=get_remote_address, default_limits=["20/minute"])
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)
app.add_middleware(SlowAPIMiddleware)


async def catch_exceptions_middleware(request: Request, call_next):
    try:
        return await call_next(request)
    except Exception as e:
        logging.error(e)
        return Response("Internal server error", status_code=500)


app.middleware("http")(catch_exceptions_middleware)


@app.get("/", status_code=200)
@limiter.exempt
async def get_healthcheck():
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    return {"message": "ok", "data": f"Hello world from server, current server time is {current_time}"}


@app.get("/api/v1/tx_explain/by_version/{version_id}", status_code=200)
async def get_tx_explain(version_id: str):
    tx = get_tx_by_version(version_id)
    if tx is None:
        raise HTTPException(status_code=404, detail="Transaction not found")
    input_query = f"Explain this transaction: {tx}"
    answer = ask_question(input_query)
    return {"message": "ok", "data": answer}


@app.get("/api/v1/tx_explain/by_hash/{tx_hash}", status_code=200)
async def get_tx_hash(tx_hash: str):
    tx = get_tx_by_hash(tx_hash)
    if tx is None:
        raise HTTPException(status_code=404, detail="Transaction not found")
    input_query = f"Explain this transaction: {tx}"
    answer = ask_question(input_query)
    return {"message": "ok", "data": answer}


def custom_openapi():
    if app.openapi_schema:
        return app.openapi_schema
    openapi_schema = get_openapi(
        title="TikiGPT",
        version="1.0.0",
        description="TikiGPT Document API",
        routes=app.routes,
    )
    app.openapi_schema = openapi_schema
    return app.openapi_schema


app.openapi = custom_openapi

if __name__ == "__main__":
    import uvicorn

    initialize_logging()
    logging.info("Server running at port :5000")
    uvicorn.run(app, host="0.0.0.0", port=5000)
