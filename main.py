from project.rag.retriever import retrieve_documents

query = "How can I reset my API credentials?"

documents = retrieve_documents(query)

print(f"Retrieved {len(documents)} documents\n")

for i, doc in enumerate(documents, start=1):
    print(f"Document {i}")
    print(doc.metadata)
    print("-" * 60)