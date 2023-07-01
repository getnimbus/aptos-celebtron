from dotenv import load_dotenv

# load environment variables from .env file
load_dotenv()

from fastapi import FastAPI
from fastapi.openapi.utils import get_openapi
from fastapi.middleware.cors import CORSMiddleware
from datetime import datetime
from core.aptos import get_tx_by_version, ask_question
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


@app.get("/", status_code=200)
async def get_healthcheck():
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    return {"message": "ok", "data": f"Hello world from server, current server time is {current_time}"}


@app.get("/api/v1/tx_explain/{version_id}", status_code=200)
async def get_tx_explain(version_id: str):
    tx = get_tx_by_version(version_id)
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
