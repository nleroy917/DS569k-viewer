from fastapi import APIRouter
from qdrant_client import QdrantClient
from qdrant_client.http.models import Filter, FieldCondition, MatchAny

from models import SimilarityQuery
from embed_proteinclip import embed_proteinclip_6

qclient = QdrantClient(
    url="http://localhost:6333",
)
    
router = APIRouter()

@router.post("/search")
def compute_similarity(body: SimilarityQuery):
    classes = body.class_filters
    phyla = body.phylum_filters

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
    
    query_vector = embed_proteinclip_6(body.sequence)

    results = qclient.query_points(
        collection_name="proteins",
        query=query_vector,
        limit=body.top_k,
        query_filter=query_filter,
        with_payload=True,
        using="pclip",
    )
    
    hits = [{
        "score": point.score,
        "accession": point.payload.get("accession"),
        "protein_name": point.payload.get("protein_name"),
        "organism_name": point.payload.get("organism_name"),
        "sequence_length": point.payload.get("sequence_length"),
        "ncbi_taxonomy_class": point.payload.get("ncbi_taxonomy_class"),
        "ncbi_taxonomy_phylum": point.payload.get("ncbi_taxonomy_phylum"),
        "similarity": point.score,
        "function": point.payload.get("function"),
    } for point in results.points]

    return {
        "hits": hits,
        "total": len(hits),
    }