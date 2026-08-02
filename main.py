from project.graph.builder import graph

queries = [
    "How do I rotate API credentials?",
    "My export failed.",
    "Write a refund request for my Netflix subscription.",
    "The suggested solution did not work. What information should I collect before escalating?",
]

for query in queries:
    print("=" * 80)
    print(f"Query: {query}\n")

    result = graph.invoke({"query": query})

    print(f"Classification       : {result['classification']}")
    print(f"Answer              : {result['answer']}")
    print(f"Verification Passed : {result['verification_passed']}")
    print(f"Confidence          : {result['confidence']}")
    print(f"Requires Human      : {result['requires_human']}")
    print(f"Reason              : {result['reason']}")
    print(f"Sources             : {result['sources']}")
    print()