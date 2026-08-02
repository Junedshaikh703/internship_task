from langchain_huggingface import HuggingFaceEmbeddings

EMBEDDING_MODEL_NAME = "BAAI/bge-small-en-v1.5"

embeddings = HuggingFaceEmbeddings(
    model_name=EMBEDDING_MODEL_NAME
)

query = "How do I reset my password?"

docs = [
    "You can reset your password from the account settings page.",
    "The weather is sunny today."
]

query_vector = embeddings.embed_query(query)
doc_vectors = embeddings.embed_documents(docs)

print(len(query_vector))
print(len(doc_vectors))
print(len(doc_vectors[0]))