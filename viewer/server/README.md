To run the server, use:

```
uvicorn src.server:app --host --reload
```

An example curl request to the search endpoint:

```bash
time curl -X 'POST' \
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