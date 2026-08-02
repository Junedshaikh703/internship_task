from project.graph.builder import graph


def test_out_of_scope_query():
    """
    Verify that an unrelated query
    is routed to the out_of_scope node.
    """

    result = graph.invoke(
        {
            "query": "Write a refund request for my Netflix subscription."
        }
    )

    assert result["classification"] == "out_of_scope"
    assert result["sources"] == []