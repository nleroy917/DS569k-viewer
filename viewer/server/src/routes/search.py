
from fastapi import APIRouter

from models import ProteinData, SimilarityQuery
from embed_proteinclip import embed_proteinclip_6

    
router = APIRouter()

@router.post("/search", response_model=ProteinData)
def compute_similarity(body: SimilarityQuery):
    # we will replace all that was here with call to
    # qdrant
    return "Not implemented yet"