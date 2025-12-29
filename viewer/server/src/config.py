import os

from pathlib import Path

# qdrant configuration
QDRANT_URL = os.getenv("QDRANT_URL", "http://localhost:6333")
QDRANT_COLLECTION_NAME = os.getenv("QDRANT_COLLECTION_NAME", "proteins")

# model configuration
ESM_MODEL_SIZE = int(os.getenv("ESM_MODEL_SIZE", "6"))
PROTEINCLIP_MODEL_PATH = os.getenv(
    "PROTEINCLIP_MODEL_PATH",
    str(Path(__file__).parent / f"proteinclip_esm2_{ESM_MODEL_SIZE}.onnx")
)

# embedding configuration
EMBED_LAYER = int(os.getenv("EMBED_LAYER", str(ESM_MODEL_SIZE)))
DEVICE = os.getenv("DEVICE", "cpu")

# sequence validation
MAX_SEQUENCE_LENGTH = int(os.getenv("MAX_SEQUENCE_LENGTH", "1024"))
VALID_AMINO_ACIDS = set("ACDEFGHIKLMNPQRSTVWY")  # standard 20 amino acids