from project.nodes.retrieval import retrieval_node

state = {
    "query": "How do I rotate API credentials?"
}

new_state = retrieval_node(state)

print(len(new_state["retrieved_documents"]))

for doc in new_state["retrieved_documents"]:
    print(doc.metadata)