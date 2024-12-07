"""
File: propertygraph.py
Description: An implementation of a PropertyGraph consisting of
Node and Relationship objects.  Nodes and Relationships carry
properties.  Property graphs are used to represent connected knowledge.

"""


class Node:

    def __init__(self, name, category, props=None):
        """ Class constructor """
        pass

    def __getitem__(self, key):
        """ Fetch a property from the node using []
         return None if property doesn't exist """
        pass

    def __setitem__(self, key, value):
        """ Set a node property with a specified value using [] """
        pass

    def __eq__(self, other):
        """ Two nodes are equal if they have the same
        name and category irrespective of their properties """
        pass

    def __hash__(self):
        """ By making Nodes hashable we can now
        store them as keys in a dictionary! """
        pass

    def __repr__(self):
        """ Output the node as a string in the following format:
        name:category<tab>properties.
        Note: __repr__ is more versatile than __str__ """
        pass


class Relationship:

    def __init__(self, category, props=None):
        """ Class constructor """
        pass

    def __getitem__(self, key):
        """ Fetch a property from the node using []
         return None if property doesn't exist """
        pass

    def __setitem__(self, key, value):
        """ Set a node property with a specified value using [] """
        pass

    def __repr__(self):
        """ Output the relationship as a string in the following format:
        :category<space>properties.
        Note: __repr__ is more versatile than __str__ """
        pass


class PropertyGraph:

    def __init__(self):
        """ Construct an empty property graph """
        pass

    def add_node(self, node):
        """ Add a node to the property graph """
        pass

    def add_relationship(self, src, targ, rel):
        """ Connect src and targ nodes via the specified directed relationship.
        If either src or targ nodes are not in the graph, add them.
        Note that there can be many relationships between two nodes! """
        pass

    def get_nodes(self, name=None, category=None, key=None, value=None):
        """ Return the SET of nodes matching all the specified criteria.
        If the criterion is None it means that the particular criterion is ignored. """
        pass

    def adjacent(self, node, node_category=None, rel_category=None):
        """ Return a set of all nodes that are adjacent to node.
        If specified include only adjacent nodes with the specified node_category.
        If specified include only adjacent nodes connected via relationships with
        the specified rel_category """
        pass

    def subgraph(self, nodes):
        """ Return the subgraph as a PropertyGraph consisting of the specified
        set of nodes and all interconnecting relationships """
        pass

    def __repr__(self):
        """ A string representation of the property graph
        Properties are not displaced.

        Node
            Relationship Node
            Relationship Node
            .
            .
            etc.
        Node
            Relationship Node
            Relationship Node
            .
            .
            etc.
        .
        .
        etc.
        """

        pass

