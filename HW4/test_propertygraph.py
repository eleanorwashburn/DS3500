"""
Eleanor Washburn
DS3500 - HW4

File: test_propertygraph.py
Description: Tests for the PropertyGraph implementation, which includes
testing the functionality of Node and Relationship objects. These tests
ensure that the graph's structure and behaviors operate as intended.
"""
# Import needed libraries
from propertygraph import Node, Relationship, PropertyGraph

def test_node_init():
    # Test initializing a Node with a name, category, and properties
    node = Node("Alice", "Person", {"age": 25})
    # Check that the name is set correctly
    assert node.name == "Alice"
    # Check that the category is set correctly
    assert node.category == "Person"
    # Check that the properties are initialized correctly
    assert node.properties["age"] == 25

def test_node_getitem():
    # Test getting properties from a Node using item access
    node = Node("Alice", "Person", {"age": 25})
    # Check that accessing 'age' returns the correct value
    assert node["age"] == 25
    # Check that accessing a non-existent property returns None
    assert node["height"] is None

def test_node_setitem():
    # Test setting properties on a Node using item assignment
    node = Node("Alice", "Person")
    # Set the 'age' property
    node["age"] = 30
    # Check that the property is set correctly
    assert node["age"] == 30

def test_node_eq():
    # Test equality comparison between Nodes
    node1 = Node("Alice", "Person")
    # Create another Node with the same attributes
    node2 = Node("Alice", "Person")
    # Create another Node with the same attributes
    node3 = Node("Bob", "Person")
    # Check that equal Nodes are considered equal
    assert node1 == node2
    # Check that different Nodes are not considered equal
    assert node1 != node3

def test_node_hash():
    # Test hashing of Nodes to ensure they can be added to a set
    node1 = Node("Alice", "Person")
    # Create another Node with the same attributes
    node2 = Node("Alice", "Person")
    # Create a set with both Nodes
    node_set = {node1, node2}
    # Check that the set contains only one unique Node
    assert len(node_set) == 1

def test_node_repr():
    # Test the string representation of a Node
    node = Node("Alice", "Person", {"age": 25})
    # Check that the repr is formatted correctly
    assert repr(node) == "Alice:Person\t{'age': 25}"

def test_relationship_init():
    # Test initializing a Relationship with a category and properties
    rel = Relationship("Friend", {"since": 2020})
    # Check that the category is set correctly
    assert rel.category == "Friend"
    # Check that the properties are initialized correctly
    assert rel.props["since"] == 2020

def test_relationship_getitem():
    # Test getting properties from a Relationship using item access
    rel = Relationship("Friend", {"since": 2020})
    # Check that accessing 'since' returns the correct value
    assert rel["since"] == 2020
    # Check that accessing a non-existent property returns None
    assert rel["unknown"] is None

def test_relationship_setitem():
    # Test setting properties on a Relationship using item assignment
    rel = Relationship("Friend")
    # Set the 'since' property
    rel["since"] = 2021
    # Check that the property is set correctly
    assert rel["since"] == 2021

def test_relationship_repr():
    # Test the string representation of a Relationship
    rel = Relationship("Friend", {"since": 2020})
    # Check that the repr is formatted correctly
    assert repr(rel) == ":Friend {'since': 2020}"

def test_propertygraph_init():
    # Test initializing an empty PropertyGraph
    graph = PropertyGraph()
    # Check that the initial node set is empty
    assert len(graph.nodes) == 0
    # Check that nodes are stored in a set
    assert isinstance(graph.nodes, set)
    # Check that the initial relationships are empty
    assert len(graph.relationships) == 0
    # Check that relationships are stored in a dictionary
    assert isinstance(graph.relationships, dict)

def test_propertygraph_add_node():
    # Test adding a Node to a PropertyGraph
    graph = PropertyGraph()
    node = Node("Alice", "Person")
    # Add the node to the graph
    graph.add_node(node)
    # Check that the node was added
    assert node in graph.nodes

def test_propertygraph_add_relationship():
    # Test adding a Relationship between Nodes in a PropertyGraph
    graph = PropertyGraph()
    alice = Node("Alice", "Person")
    bob = Node("Bob", "Person")
    rel = Relationship("Friend")
    # Add the relationship between Alice and Bob
    graph.add_relationship(alice, bob, rel)
    # Check that Alice is in the graph
    assert alice in graph.nodes
    # Check that Bob is in the graph
    assert bob in graph.nodes
    # Check that the relationship is recorded
    assert (rel, bob) in graph.relationships[alice]

def test_propertygraph_get_nodes():
    # Test retrieving Nodes from a PropertyGraph based on specified criteria
    graph = PropertyGraph()
    alice = Node("Alice", "Person", {"age": 30})
    bob = Node("Bob", "Person", {"age": 25})
    # Add Alice to the graph
    graph.add_node(alice)
    # Add Bob to the graph
    graph.add_node(bob)
    # Check retrieval by name
    assert graph.get_nodes(name="Alice") == {alice}
    # Check retrieval by category
    assert graph.get_nodes(category="Person") == {alice, bob}
    # Check retrieval by key-value pair
    assert graph.get_nodes(key="age", value=25) == {bob}

def test_propertygraph_adjacent():
    # Test finding adjacent Nodes in a PropertyGraph
    graph = PropertyGraph()
    alice = Node("Alice", "Person")
    bob = Node("Bob", "Person")
    carol = Node("Carol", "Person")
    friend_rel = Relationship("Friend")
    colleague_rel = Relationship("Colleague")
    # Alice is friends with Bob
    graph.add_relationship(alice, bob, friend_rel)
    # Alice is a colleague of Carol
    graph.add_relationship(alice, carol, colleague_rel)
    # Check that Alice's adjacent Nodes are Bob and Carol
    assert graph.adjacent(alice) == {bob, carol}
    # Check that only the friend relationship is considered
    assert graph.adjacent(alice, rel_category="Friend") == {bob}

def test_propertygraph_subgraph():
    # Test creating a subgraph from a PropertyGraph
    graph = PropertyGraph()
    alice = Node("Alice", "Person")
    bob = Node("Bob", "Person")
    carol = Node("Carol", "Person")
    friend_rel = Relationship("Friend")
    # Add relationship between Alice and Bob
    graph.add_relationship(alice, bob, friend_rel)
    # Add relationship between Bob and Carol
    graph.add_relationship(bob, carol, friend_rel)
    # Define nodes for the subgraph
    subgraph_nodes = {alice, bob}
    # Create the subgraph
    subgraph = graph.subgraph(subgraph_nodes)
    # Check that Alice is in the subgraph
    assert alice in subgraph.nodes
    # Check that Bob is in the subgraph
    assert bob in subgraph.nodes
    # Check that the relationship is preserved in the subgraph
    assert (friend_rel, bob) in subgraph.relationships[alice]
    # Check that Carol is not in the subgraph
    assert carol not in subgraph.nodes

def test_propertygraph_repr():
    # Test the string representation of a PropertyGraph
    graph = PropertyGraph()
    alice = Node("Alice", "Person")
    bob = Node("Bob", "Person")
    # Adding a property to the relationship
    friend_rel = Relationship("Friend", {"since": 2021})

    # Add Alice to the graph
    graph.add_node(alice)
    # Add Bob to the graph
    graph.add_node(bob)
    # Add the relationship between Alice and Bob
    graph.add_relationship(alice, bob, friend_rel)

    # Update expected representation to include properties
    expected_repr = "Alice:Person\t{}\n    :Friend Bob:Person\t{since: 2021}\n"
    assert repr(graph) == expected_repr