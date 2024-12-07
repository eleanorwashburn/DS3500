"""
Eleanor Washburn
DS3500 - HW4

File: propertygraph.py
Description: An implementation of a PropertyGraph consisting of
Node and Relationship objects.  Nodes and Relationships carry
properties.  Property graphs are used to represent connected knowledge.
"""

class Node:
    def __init__(self, name, category, props=None):
        """ Node constructor with optional properties. """
        # Set the name of the node
        self.name = name
        # Set the category of the node
        self.category = category
        # Initialize properties and use an empty dictionary if there are no properties
        self.properties = props if props is not None else {}

    def __getitem__(self, key):
        """ Fetch a property from the node using []
         return None if property doesn't exist """
        # Return the property value or None if it doesn't exist
        return self.properties.get(key, None)

    def __setitem__(self, key, value):
        """ Set a node property with a specified value using [] """
        # Set the property value in the dictionary
        self.properties[key] = value

    def __eq__(self, other):
        """ Two nodes are equal if they have the same
        name and category irrespective of their properties. """
        # Return False if the other object is not a Node
        if not isinstance(other, Node):
            return False
        # Compare name and category
        return self.name == other.name and self.category == other.category

    def __hash__(self):
        """ By making Nodes hashable, we can now
        store them as keys in a dictionary! """
        # Create a hash based on name and category
        return hash((self.name, self.category))

    def __repr__(self):
        """ Output the node as a string in the following format:
        name:category<tab>properties.
        Note: __repr__ is more versatile than __str__ """
        # Format the output string
        return f"{self.name}:{self.category}\t{self.properties}"


class Relationship:
    def __init__(self, category, props=None):
        """ Class constructor """
        # Set the category of the relationship
        self.category = category
        # Initialize properties and use an empty dictionary if there are no properties
        self.props = props if props is not None else {}

    def __getitem__(self, key):
        """ Fetch a property from the relationship using []
        Returns None if property doesn't exist. """
        # Return the property value or None if it doesn't exist
        return self.props.get(key, None)

    def __setitem__(self, key, value):
        """ Set a node property with a specified value using [] """
        # Set the property value in the dictionary
        self.props[key] = value

    def __repr__(self):
        """ Output the relationship as a string in the following format:
        :category<space>properties.
        Note: __repr__ is more versatile than __str__ """
        # Format the output string
        return f":{self.category} {self.props}"


class PropertyGraph:
    def __init__(self):
        """ Construct an empty property graph. """
        # Set to store unique nodes in the graph
        self.nodes = set()
        # Initialize dictionary to store relationships for each node
        self.relationships = {}

    def add_node(self, node):
        """ Add a node to the property graph. """
        # Add the node to the set of nodes
        self.nodes.add(node)
        # Initialize an empty list for relationships of the node
        self.relationships[node] = []

    def add_relationship(self, src, targ, rel):
        """ Connect src and targ nodes via the specified directed relationship.
        If either src or targ nodes are not in the graph, add them.
        Note that there can be many relationships between two nodes! """
        # Add src node if it is not already in the graph
        if src not in self.nodes:
            self.add_node(src)

        # Add targ node if it is not already in the graph
        if targ not in self.nodes:
            self.add_node(targ)

        # Add the relationship to the list of relationships for the src node
        if src in self.relationships:
            self.relationships[src].append((rel, targ))
        # Initialize with the relationship and target node
        else:
            self.relationships[src] = [(rel, targ)]

    def get_nodes(self, name=None, category=None, key=None, value=None):
        """ Return the SET of nodes matching all the specified criteria.
        If the criterion is None it means that the particular criterion is ignored. """
        # Initialize a set to collect matching nodes
        matching_nodes = set()

        # Iterate over all nodes in the graph
        for node in self.nodes:
            # Check each criterion against the current node
            if (name is None or node.name == name) and \
                    (category is None or node.category == category) and \
                    (key is None or node[key] == value):
                # Add the node to the set of matching nodes
                matching_nodes.add(node)

        return matching_nodes

    def adjacent(self, node, node_category=None, rel_category=None):
        """ Return a set of all nodes that are adjacent to the node.
        If specified, include only adjacent nodes with the specified node_category.
        If specified, include only adjacent nodes connected via relationships with
        the specified rel_category. """
        # Set to hold adjacent nodes
        adjacent_nodes = set()

        # Iterate through relationships of the specified node
        for rel, targ in self.relationships.get(node, []):
            # Check if the target node matches specified criteria
            if (node_category is None or targ.category == node_category) and \
               (rel_category is None or rel.category == rel_category):
                # Add target node to the adjacent nodes set
                adjacent_nodes.add(targ)

        return adjacent_nodes

    def subgraph(self, nodes):
        """ Return the subgraph as a PropertyGraph consisting of the specified
        set of nodes and all interconnecting relationships. """
        # Create a new PropertyGraph for the subgraph
        subgraph = PropertyGraph()

        # Iterate over nodes
        for node in nodes:
            # Add each node to the subgraph
            subgraph.add_node(node)

            # Iterate through relationships for the current node
            for rel, targ in self.relationships.get(node, []):
                # Check if the target node is part of the specified nodes
                if targ in nodes:
                    # Add the relationship to the subgraph
                    subgraph.add_relationship(node, targ, rel)
        return subgraph

    def __repr__(self):
        """ A string representation of the property graph.
        Properties are not displayed. """
        # Initialize an empty list for results
        result = []

        # Iterate over all nodes in the graph
        for node in self.nodes:
            # Collect relationships for the current node
            relationships = []
            for rel, targ in self.relationships.get(node, []):
                # Format the properties correctly
                props = ", ".join(f"{key}: {value}" for key, value in rel.props.items())
                rel_repr = f"    :{rel.category} {targ.name}:{targ.category}\t{{{props}}}"
                # Add the formatted relationship to the list
                relationships.append(rel_repr)

            # Only include the node in the representation if it has relationships
            if relationships:
                node_repr = f"{node.name}:{node.category}\t{{}}"
                # Add the node representation
                result.append(node_repr)
                # Add the relationships for the node
                result.extend(relationships)

        return "\n".join(result) + "\n"