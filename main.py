from project.graph.builder import graph

state = {
    "query": "How do I rotate API credentials?"
}

result = graph.invoke(state)

print(result["answer"])
print(result["verification_passed"])
print(result["confidence"])
print(result["requires_human"])
print(result["reason"])
print(result["sources"])