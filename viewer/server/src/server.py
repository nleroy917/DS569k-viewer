from __future__ import annotations

import uvicorn

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from utils import custom_generate_unique_id
from routes import info_router, search_router

app = FastAPI(
    title="Backend",
    generate_unique_id_function=custom_generate_unique_id
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

if __name__ == "__main__":
    uvicorn.run(app, host="localhost", port=8000)
