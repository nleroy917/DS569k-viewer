To runthe server, use:
```
uvicorn src.server:app --host --reload
```     


```python
class SimilarityQuery(CamelModel):
    sequence: str
    top_k: int
    class_filters: list[str] | None = None
    phylum_filters: list[str] | None = None
```

An example curl request to the search endpoint:

```bash
curl -X 'POST' \
  'http://localhost:8000/search' \
  -H 'accept: application/json' \
  -H 'Content-Type: application/json' \
  -d '{
  "sequence": "MKTAYIAKQRQISFVKSHFSRQDILDLWIYHTQGYFPDWQNYTPGPGIRYPLKFEDLAYVYQKAGVLKSGTPEAQRLKQLATKAA",
  "top_k": 20,
  "class_filters": ["Mammalia"],
  "phylum_filters": ["Chordata"]
}' | jq
```