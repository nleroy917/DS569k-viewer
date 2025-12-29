from platform import python_version

import uvicorn

from fastapi import FastAPI, __version__ as fastapi_version
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

@app.get("/")
def read_root():
    return {
        "message": "protein viewer backend.",
        "python_version": python_version(),
        "fastapi_version": fastapi_version,
    }

if __name__ == "__main__":
    uvicorn.run(app, host="localhost", port=8000)
