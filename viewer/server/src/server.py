from platform import python_version
from contextlib import asynccontextmanager

import uvicorn

from fastapi import FastAPI, __version__ as fastapi_version
from fastapi.middleware.cors import CORSMiddleware
from qdrant_client import QdrantClient

from utils import custom_generate_unique_id
from routes import info_router, search_router
from embed_proteinclip import get_model, load_proteinclip
from config import (
    QDRANT_URL,
    ESM_MODEL_SIZE,
    PROTEINCLIP_MODEL_PATH,
    EMBED_LAYER,
    DEVICE,
)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Load models and clients at startup, cleanup at shutdown.
    """

    # load ESM2 model and alphabet
    print(f"Loading ESM2 model (size={ESM_MODEL_SIZE})...")
    app.state.esm2, app.state.alphabet = get_model(ESM_MODEL_SIZE)

    # load protein clip model
    print(f"Loading ProteinCLIP model from {PROTEINCLIP_MODEL_PATH}...")
    app.state.pclip = load_proteinclip(PROTEINCLIP_MODEL_PATH)

    # initialize qdrant client
    print(f"Connecting to Qdrant at {QDRANT_URL}...")
    app.state.qclient = QdrantClient(url=QDRANT_URL)

    # store configuration
    app.state.embed_layer = EMBED_LAYER
    app.state.device = DEVICE

    # load taxonomy info once at startup
    print("Loading taxonomy information...")
    from datasets import load_dataset
    ds = load_dataset("donnyb/DS569k")['train'].to_polars()
    app.state.taxonomy_classes = (
        ds.select("ncbi_taxonomy_class")
        .drop_nulls()
        .unique()
        .to_series()
        .to_list()
    )
    app.state.taxonomy_phyla = (
        ds.select("ncbi_taxonomy_phylum")
        .drop_nulls()
        .unique()
        .to_series()
        .to_list()
    )
    print(f"✓ Loaded {len(app.state.taxonomy_classes)} classes and {len(app.state.taxonomy_phyla)} phyla")

    print("✓ All models and clients loaded successfully")

    yield

    # cleanup (if needed later)
    print("Shutting down...")


app = FastAPI(
    title="Backend",
    generate_unique_id_function=custom_generate_unique_id,
    lifespan=lifespan
)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(info_router)
app.include_router(search_router)

@app.get("/")
def read_root():
    return {
        "message": "protein viewer backend.",
        "python_version": python_version(),
        "fastapi_version": fastapi_version,
    }

if __name__ == "__main__":
    uvicorn.run(app, host="localhost", port=8000)
