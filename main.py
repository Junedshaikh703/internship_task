from dotenv import load_dotenv

from project.graph.builder import graph

load_dotenv()

# import os

# print(os.getenv("LANGSMITH_TRACING"))
# print(os.getenv("LANGSMITH_API_KEY"))
# print(os.getenv("LANGSMITH_PROJECT"))


query = "How do I rotate API credentials?"

result = graph.invoke({"query": query})

print("=" * 80)
print(f"Query: {query}\n")

print(f"Classification       : {result['classification']}")
print(f"Answer              : {result['answer']}")
print(f"Verification Passed : {result['verification_passed']}")
print(f"Confidence          : {result['confidence']}")
print(f"Requires Human      : {result['requires_human']}")
print(f"Reason              : {result['reason']}")
print(f"Sources             : {result['sources']}")
