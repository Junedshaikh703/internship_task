from project.nodes.retrieval import retrieval_node
from project.nodes.generation import generation_node
from project.nodes.verification import verification_node

state = {
    "query": "How do I rotate API credentials?"
}

# Retrieval
state = retrieval_node(state)

# Generation
state = generation_node(state)

print("=" * 80)
print("Generated Answer:\n")
print(state["answer"])

# Verification
state = verification_node(state)

print("\n" + "=" * 80)
print("Verification Result:\n")

print(f"Verification Passed : {state['verification_passed']}")
print(f"Confidence          : {state['confidence']}")
print(f"Requires Human      : {state['requires_human']}")
print(f"Reason              : {state['reason']}")