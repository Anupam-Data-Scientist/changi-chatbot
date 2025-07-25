from pinecone import Pinecone, ServerlessSpec

pc = Pinecone(api_key="pcsk_5Se5CJ_C6ADC7o4VHRHriPca7ZFRwVetLFtnUN2dMb6AcZsozfaiAQqdrAp9HRFamLpc6C")

index_name = "changi-chatbot-index"

# Delete old index if exists
if index_name in pc.list_indexes().names():
    pc.delete_index(index_name)

# Create new index with correct dimension
pc.create_index(
    name=index_name,
    dimension=384,  # <-- match with embedding size
    metric="cosine",
    spec=ServerlessSpec(
        cloud="aws",
        region="us-east-1"  # or your region
    )
)
