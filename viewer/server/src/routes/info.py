from fastapi import APIRouter, Request

from models import TaxonomyInfo

router = APIRouter()


@router.get("/taxonomy-info", response_model=TaxonomyInfo)
def taxonomy_info(request: Request):
    """Get available taxonomy classes and phyla for filtering."""
    return TaxonomyInfo(
        phyla=request.app.state.taxonomy_phyla,
        classes=request.app.state.taxonomy_classes
    )