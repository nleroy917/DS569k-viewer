import os

from tqdm import tqdm
from qdrant_client import QdrantClient, models
from datasets import load_dataset

BATCH_SIZE = 128

client = QdrantClient(
    url=os.getenv("QDRANT_URL", "http://localhost:6333"),
    api_key=os.getenv("QDRANT_API_KEY")
)

# create collection if not exists
if not client.collection_exists("proteins"):
    client.create_collection(
        collection_name="proteins",
        vectors_config={
            "pclip": models.VectorParams(
                size=128,
                distance=models.Distance.COSINE
            )
        }, # size and distance are model dependent
    )

client.create_payload_index(
    collection_name="proteins",
    field_name="ncbi_taxonomy_class",
    field_schema="keyword",
)

client.create_payload_index(
    collection_name="proteins",
    field_name="ncbi_taxonomy_phylum",
    field_schema="keyword",
)


df = load_dataset("donnyb/DS569k")['train'].to_polars()

def generate_points_in_batches(
    batch_size: int = BATCH_SIZE,
):
    for i in range(0, len(df), batch_size):
        batch = df[i:i + batch_size]
        points = [
            models.PointStruct(
                id=idx,
                vector={
                    "pclip": row.get("embedding"),
                },
                payload={
                    "accession": row.get("accession"),
                    "protein_name": row.get("protein_name"),
                    "organism_name": row.get("organism_name"),
                    "ncbi_taxonomy_class": row.get("ncbi_taxonomy_class"),
                    "ncbi_taxonomy_phylum": row.get("ncbi_taxonomy_phylum"),
                    "gene_name": row.get("gene_name"),
                    "sequence_length": row.get("sequence_length"),
                    "protein_existence": row.get("protein_existence"),
                    "sequence_version": row.get("sequence_version"),
                    "ncbi_taxonomy_id": row.get("ncbi_taxonomy_id"),
                    "organism_identifier": row.get("organism_identifier"),
                    "function": row.get("function"),
                    "sequence": row.get("sequence"),
                }
            )
            for idx, row in enumerate(batch.iter_rows(named=True), start=i)
        ]
        yield points

for batch in tqdm(generate_points_in_batches(), total=(len(df) // BATCH_SIZE) + 1):
    client.upload_points(
        collection_name="proteins",
        points=batch
    )

# get collection info
collection_info = client.get_collection("proteins")
print("Collection info:")
print(collection_info)
