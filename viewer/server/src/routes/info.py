from fastapi import APIRouter

from datasets import load_dataset

from models import TaxonomyInfo

router = APIRouter()

ds = load_dataset("donnyb/DS569k")['train'].to_polars()
classes = ds.select("ncbi_taxonomy_class").drop_nulls().unique().to_series().to_list()
phyla = ds.select("ncbi_taxonomy_phylum").drop_nulls().unique().to_series().to_list()

@router.get("/taxonomy-info", response_model=TaxonomyInfo)
def taxonomy_info():
    return TaxonomyInfo(phyla=phyla, classes=classes)