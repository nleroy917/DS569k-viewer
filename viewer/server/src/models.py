from pydantic import BaseModel, ConfigDict

from utils import to_camel

# https://github.com/zeno-ml/zeno-hub/blob/9d2f8b5841d99aeba9ec405b0bc6a5b1272b276f/backend/zeno_backend/classes/base.py#L20
class CamelModel(BaseModel):
    """Converting snake_case pydantic models to camelCase models."""

    model_config = ConfigDict(alias_generator=to_camel, populate_by_name=True)  # type: ignore

class TaxonomyInfo(CamelModel):
    classes: list[str]
    phyla: list[str]

class SimilarityQuery(CamelModel):
    sequence: str
    top_k: int
    class_filters: list[str] | None = None
    phylum_filters: list[str] | None = None