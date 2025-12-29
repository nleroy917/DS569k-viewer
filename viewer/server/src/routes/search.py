from fastapi import APIRouter, Request, HTTPException
from qdrant_client.http.models import Filter, FieldCondition, MatchAny

from models import SimilarityQuery
from embed_proteinclip import embed_proteinclip
from utils import validate_protein_sequence
from config import QDRANT_COLLECTION_NAME

router = APIRouter()


@router.post("/search")
def compute_similarity(body: SimilarityQuery, request: Request):
    # validate the protein sequence
    is_valid, error_msg = validate_protein_sequence(body.sequence)
    if not is_valid:
        raise HTTPException(status_code=400, detail=error_msg)

    classes = body.class_filters
    phyla = body.phylum_filters

    # build filters if provided
    if any([filt is not None and len(filt) > 0 for filt in [classes, phyla]]):
        conditions = []
        if classes is not None and len(classes) > 0:
            conditions.append(
                FieldCondition(
                    key="ncbi_taxonomy_class",
                    match=MatchAny(any=classes)
                )
            )
        if phyla is not None and len(phyla) > 0:
            conditions.append(
                FieldCondition(
                    key="ncbi_taxonomy_phylum",
                    match=MatchAny(any=phyla)
                )
            )
        query_filter = Filter(must=conditions)
    else:
        query_filter = None

    # generate embedding using pre-loaded models from app state
    try:
        query_vector = embed_proteinclip(
            seq=body.sequence,
            esm2=request.app.state.esm2,
            alphabet=request.app.state.alphabet,
            pclip=request.app.state.pclip,
            layer=request.app.state.embed_layer,
            device=request.app.state.device,
        )
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Failed to generate embedding: {str(e)}"
        )

    # query qdrant for similar proteins
    try:
        results = request.app.state.qclient.query_points(
            collection_name=QDRANT_COLLECTION_NAME,
            query=query_vector,
            limit=body.top_k,
            query_filter=query_filter,
            with_payload=True,
            using="pclip",
        )
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Failed to query vector database: {str(e)}"
        )
    
    hits = [{
        "score": point.score,
        "accession": point.payload.get("accession"),
        "protein_name": point.payload.get("protein_name"),
        "organism_name": point.payload.get("organism_name"),
        "sequence_length": point.payload.get("sequence_length"),
        "ncbi_taxonomy_class": point.payload.get("ncbi_taxonomy_class"),
        "ncbi_taxonomy_phylum": point.payload.get("ncbi_taxonomy_phylum"),
        "function": point.payload.get("function"),
    } for point in results.points]

    return {
        "hits": hits,
        "total": len(hits),
    }