import os
from logging import getLogger
import logging
from fastapi import FastAPI, Response, status
from crossencoder import CrossEncoderRanker, CrossEncoderInput
from meta import Meta
from contextlib import asynccontextmanager

# Logger setup
logger = getLogger('uvicorn')
logging.basicConfig(level=logging.INFO)

# Global variables
cross_encoder: CrossEncoderRanker
meta_config: Meta

@asynccontextmanager
async def lifespan(app: FastAPI):
    global cross_encoder
    global meta_config

    cuda_env = os.getenv("ENABLE_CUDA")
    cuda_support = False
    cuda_core = ""

    if cuda_env is not None and cuda_env == "true" or cuda_env == "1":
        cuda_support = True
        cuda_core = os.getenv("CUDA_CORE")
        if cuda_core is None or cuda_core == "":
            cuda_core = "cuda:0"
        logger.info(f"CUDA_CORE set to {cuda_core}")
    else:
        logger.info("Running on CPU")

    model_dir = './models/model'

    cross_encoder = CrossEncoderRanker(model_dir)
    meta_config = Meta(model_dir)

    # Startup logic complete
    yield

    # Shutdown logic (if needed)
    logger.info("Shutting down application...")

# Create FastAPI app with lifespan
app = FastAPI(lifespan=lifespan)

@app.get("/.well-known/live", response_class=Response)
@app.get("/.well-known/ready", response_class=Response)
def live_and_ready(response: Response):
    response.status_code = status.HTTP_204_NO_CONTENT


@app.get("/meta")
def meta():
    return meta_config.get()


@app.post("/rerank")
async def read_item(item: CrossEncoderInput, response: Response):
    try:
        return await cross_encoder.do(item)
    except Exception as e:
        logger.exception(
            f"Something went wrong while scoring the input."
        )
        response.status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
        return {"error": str(e)}