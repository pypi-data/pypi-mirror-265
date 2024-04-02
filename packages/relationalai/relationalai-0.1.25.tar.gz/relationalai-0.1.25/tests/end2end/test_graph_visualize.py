import pytest
import relationalai as rai
from relationalai.std.graphs import Graph

DEFAULT_METADATA = {
    'arrow_color': '#999',
    'arrow_size': 4,
    'edge_border_color': '#999',
    'edge_border_size': 1,
    'edge_color': '#999',
    'edge_label_color': 'black',
    'edge_label_size': 10,
    'edge_opacity': 1,
    'edge_shape': 'circle',
    'edge_size': 2,
    'node_border_color': 'black',
    'node_border_size': 1,
    'node_color': 'black',
    'node_label_color': 'black',
    'node_label_size': 10,
    'node_opacity': 1,
    'node_shape': 'circle',
    'node_size': 10,
}


# Test that graph._visual_dict() returns a dictionary with the correct keys and values
@pytest.mark.parametrize(
    ["adj_list", "node_props", "edge_props", "undirected", "style", "expected_dict", "test_id"],
    [
        # Undirected graph with one data edge, no props, default style
        pytest.param(
            {1: [2]},
            {1: {}, 2: {}},
            {(1, 2): {}, (2, 1): {}},
            True,
            {},
            {
                'directed': False,
                'nodes': {
                    'jLWfdS5w49/Nqwx+mYthYw': {'metadata': {}},
                    'peH/vEX2TeRy3NL41/2Nag': {'metadata': {}},
                },
                'edges': [{'metadata': {}, 'source': 'jLWfdS5w49/Nqwx+mYthYw', 'target': 'peH/vEX2TeRy3NL41/2Nag'}],
                'metadata': DEFAULT_METADATA,
            },
            "undirected_no_props_default_style",
            id="undirected_no_props_default_style",
        ),
        # Directed graph with one data edge, no props, no style
        pytest.param(
            {1: [2]},
            {1: {}, 2: {}},
            {(1, 2): {}, (2, 1): {}},
            False,
            {},
            {
                'directed': True,
                'nodes': {
                    'jLWfdS5w49/Nqwx+mYthYw': {'metadata': {}},
                    'peH/vEX2TeRy3NL41/2Nag': {'metadata': {}},
                },
                'edges': [
                    {'metadata': {}, 'source': 'jLWfdS5w49/Nqwx+mYthYw', 'target': 'peH/vEX2TeRy3NL41/2Nag'},
                    {'metadata': {}, 'source': 'peH/vEX2TeRy3NL41/2Nag', 'target': 'jLWfdS5w49/Nqwx+mYthYw'}
                ],
                'metadata': DEFAULT_METADATA,
            },
            "directed_no_props_default_style",
            id="directed_no_props_default_style",
        ),
        # Undirected graph with two data edges (but one graph edge), props, custom node and edge colors.
        # Shows property merge behavior for undirected graphs with multiple data edges for a single graph edge.
        # Compare to the directed graph case below.
        pytest.param(
            {1: [2]},
            {1: {'color': 'blue'}, 2: {'color': 'red'}},
            {(1, 2): {'color': 'green'}, (2, 1): {'color': 'yellow'}},
            True,
            {'nodes': {'color': lambda n: n['color']}, 'edges': {'color': lambda e: e['color']}},
            {
                'directed': False,
                'nodes': {
                    'jLWfdS5w49/Nqwx+mYthYw': {'metadata': {'color': 'red'}},
                    'peH/vEX2TeRy3NL41/2Nag': {'metadata': {'color': 'blue'}},
                },
                'edges': [{'metadata': {'color': 'green'}, 'source': 'jLWfdS5w49/Nqwx+mYthYw', 'target': 'peH/vEX2TeRy3NL41/2Nag'}],
                'metadata': DEFAULT_METADATA,
            },
            "undirected_with_props_custom_style",
            id="undirected_with_props_custom_style",
        ),
        # Directed graph with two data edges (and two graph edges), props, custom node and edge colors.
        pytest.param(
            {1: [2]},
            {1: {'color': 'blue'}, 2: {'color': 'red'}},
            {(1, 2): {'color': 'green'}, (2, 1): {'color': 'yellow'}},
            False,
            {'nodes': {'color': lambda n: n['color']}, 'edges': {'color': lambda e: e['color']}},
            {
                'directed': True,
                'nodes': {
                    'jLWfdS5w49/Nqwx+mYthYw': {'metadata': {'color': 'red'}},
                    'peH/vEX2TeRy3NL41/2Nag': {'metadata': {'color': 'blue'}},
                },
                'edges': [
                    {'metadata': {'color': 'yellow'}, 'source': 'jLWfdS5w49/Nqwx+mYthYw', 'target': 'peH/vEX2TeRy3NL41/2Nag'},
                    {'metadata': {'color': 'green'}, 'source': 'peH/vEX2TeRy3NL41/2Nag', 'target': 'jLWfdS5w49/Nqwx+mYthYw'}
                ],
                'metadata': DEFAULT_METADATA,
            },
            "directed_with_props_custom_style",
            id="directed_with_props_custom_style",
        ),
    ],
)
def test_visual_dict(
    engine_config,
    adj_list,
    node_props,
    edge_props,
    undirected,
    style,
    expected_dict,
    test_id,
):
    model = rai.Model(f"testVisualDict_{test_id}", config=engine_config)
    Node = model.Type("Node")

    # Add objects to the model.
    with model.rule(dynamic=True):
        for (id1, adj) in adj_list.items():
            node1 = Node.add(id=id1)
            for id2 in adj:
                node2 = Node.add(id=id2)
                node1.set(adjacent_to=node2)

    # Create a graph object.
    graph = Graph(model, undirected=undirected)

    # Add nodes to the graph.
    with model.rule(dynamic=True):
        for (id, props) in node_props.items():
            node = Node(id=id)
            graph.nodes.add(node, **props)

    # Add edges to the graph.
    with model.rule(dynamic=True):
        for ((id1, id2), props) in edge_props.items():
            node1, node2 = Node(id=id1), Node(id=id2)
            graph.edges.add(node1, node2, **props)

    # Get the dictionary representation of the graph passed to the visualization backend.
    visual_dict = graph._visual_dict(style=style)

    # Check that the dictionary has the correct keys and values.
    assert visual_dict == {'graph': expected_dict}