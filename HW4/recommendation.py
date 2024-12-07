"""
Eleanor Washburn
DS3500 - HW4

File: recommendation.py
Description: This file implements a recommendation engine
utilizing a PropertyGraph to suggest books to users based
on their social connections and purchasing behaviors.
It identifies books bought by individuals known to the user,
filtering out any titles the user has already purchased.

Output for PropertyGraphs and Recommendations:

Pick between Spencer, Emily, Trevor, Brendan, or Paxtyn: Spencer
Original Property Graph:
Emily:Person	{}
    :Knows Spencer:Person	{}
    :Bought Database Design:Book	{price: $195.00}
Brendan:Person	{}
    :Bought Database Design:Book	{price: $195.00}
    :Bought DNA & You:Book	{price: $11.50}
Paxtyn:Person	{}
    :Bought Database Design:Book	{price: $195.00}
    :Bought The Life of Cronkite:Book	{price: $29.95}
Trevor:Person	{}
    :Bought Database Design:Book	{price: $195.00}
    :Bought Cosmos:Book	{price: $17.00}
Spencer:Person	{}
    :Knows Emily:Person	{}
    :Knows Brendan:Person	{}
    :Bought Database Design:Book	{price: $195.00}
    :Bought Cosmos:Book	{price: $17.00}


Recommendation Subgraph (Spencer and Recommended Books):
Spencer:Person	{}
    :Recommend DNA & You:Book	{price: $11.50}


Final Graph (Original + Recommendations):
Emily:Person	{}
    :Knows Spencer:Person	{}
    :Bought Database Design:Book	{price: $195.00}
Brendan:Person	{}
    :Bought Database Design:Book	{price: $195.00}
    :Bought DNA & You:Book	{price: $11.50}
Paxtyn:Person	{}
    :Bought Database Design:Book	{price: $195.00}
    :Bought The Life of Cronkite:Book	{price: $29.95}
Trevor:Person	{}
    :Bought Database Design:Book	{price: $195.00}
    :Bought Cosmos:Book	{price: $17.00}
Spencer:Person	{}
    :Knows Emily:Person	{}
    :Knows Brendan:Person	{}
    :Bought Database Design:Book	{price: $195.00}
    :Bought Cosmos:Book	{price: $17.00}
    :Recommend DNA & You:Book	{price: $11.50}
"""
# Import needed libraries
from propertygraph import Node, Relationship, PropertyGraph


def create_nodes(people_names, books):
    """Create nodes for people and books in a property graph."""
    # Create people nodes
    people_nodes = {}
    for name in people_names:
        people_nodes[name] = Node(name, "Person")

    # Create book nodes
    book_nodes = {}
    for title, price in books:
        book_nodes[title] = Node(title, "Book", {"price": price})

    return people_nodes, book_nodes

def create_relationships(graph, relationships, people_nodes, book_nodes):
    """Create relationships between people and books in a property graph."""
    # Iterate over each pair of people in the "Knows" relationships
    for src, targ in relationships.get("Knows", []):
        # Create a relationship indicating that src knows targ
        graph.add_relationship(people_nodes[src], people_nodes[targ], Relationship("Knows"))

    # Iterate over each pair of people and books in the "Bought" relationships
    for src, targ in relationships.get("Bought", []):
        # Retrieve the price of the book associated with the target
        price = book_nodes[targ]["price"]
        # Create a relationship indicating that src bought the book targ
        graph.add_relationship(people_nodes[src], book_nodes[targ], Relationship("Bought", {"price": price}))

def recommend_books(graph, person_node, book_nodes):
    """Generate book recommendations for a given person node."""
    # Find all people known by the given person node
    known_people = graph.adjacent(person_node, node_category="Person", rel_category="Knows")

    # Collect all books bought by the known people
    books_bought_by_known_people = []
    for person in known_people:
        for book in graph.adjacent(person, node_category="Book", rel_category="Bought"):
            books_bought_by_known_people.append(book.name)

    # Collect all books bought by the given person node
    books_spencer_bought = []
    for book in graph.adjacent(person_node, node_category="Book", rel_category="Bought"):
        books_spencer_bought.append(book.name)

    # Determine recommended books by excluding those already bought by the person
    recommended_books = []
    for book in books_bought_by_known_people:
        if book not in books_spencer_bought:
            recommended_books.append(book)

    # Create a new property graph for the recommendations
    recommendation_subgraph = PropertyGraph()
    # Add the person node to the graph
    recommendation_subgraph.add_node(person_node)

    # Add recommended books to the recommendation subgraph
    for book_title in recommended_books:
        # Get the corresponding book node
        book_node = book_nodes[book_title]
        # Add the book node to the recommendation graph
        recommendation_subgraph.add_node(book_node)
        # Retrieve the price of the book
        price = book_node["price"]
        # Create a relationship indicating the recommendation along with the price
        rel = Relationship("Recommend", {"price": price})
        # Link the person node to the book node
        recommendation_subgraph.add_relationship(person_node, book_node, rel)

    return recommended_books, recommendation_subgraph

def create_recommendation_graph(person_node, recommended_books, book_nodes):
    """Create a new property graph linking a person to their recommended books."""
    # Create a new property graph for the recommendations
    recommendation_graph = PropertyGraph()
    # Add the person node to the graph
    recommendation_graph.add_node(person_node)

    # Iterate over each recommended book
    for book_title in recommended_books:
        # Get the corresponding book node
        book_node = book_nodes[book_title]
        # Add the book node to the recommendation graph
        recommendation_graph.add_node(book_node)
        # Retrieve the price of the book
        price = book_node["price"]
        # Create a relationship indicating the recommendation along with the price
        rel = Relationship("Recommend", {"price": price, "category": "Recommendation"})
        # Link the person node to the book node
        recommendation_graph.add_relationship(person_node, book_node, rel)

    return recommendation_graph

def create_final_graph(original_graph, recommendation_graph):
    """Create the final property graph with recommended books."""
    # Initialize a new property graph for the final output
    final_graph = PropertyGraph()

    # Add nodes and relationships from the original graph
    for node in original_graph.nodes:
        # Add each node from the original graph to the final graph
        final_graph.add_node(node)

    for src in original_graph.relationships:
        for rel, targ in original_graph.relationships[src]:
            # Add relationships from the original graph to the final graph
            final_graph.add_relationship(src, targ, rel)

    # Add nodes and relationships from the recommendation graph
    for node in recommendation_graph.nodes:
        # Check if node is already added
        if node not in final_graph.nodes:
            final_graph.add_node(node)

    for src in recommendation_graph.relationships:
        for rel, targ in recommendation_graph.relationships[src]:
            # Add the node if it is not already present
            final_graph.add_relationship(src, targ, rel)

    return final_graph

def main():
    # Define names and books
    people_names = ["Emily", "Spencer", "Brendan", "Trevor", "Paxtyn"]
    books = [
        ("Cosmos", "$17.00"),
        ("Database Design", "$195.00"),
        ("The Life of Cronkite", "$29.95"),
        ("DNA & You", "$11.50")]

    # Create the property graph instance
    graph = PropertyGraph()

    # Create nodes for people and books
    people_nodes, book_nodes = create_nodes(people_names, books)

    # Add nodes to the graph
    for node in people_nodes.values():
        graph.add_node(node)
    for node in book_nodes.values():
        graph.add_node(node)

        # Define relationships from the provided diagram with recommendations
    relationships = {
        "Knows": [("Spencer", "Emily"), ("Spencer", "Brendan"), ("Emily", "Spencer")],
        "Bought": [
            ("Emily", "Database Design"),
            ("Spencer", "Database Design"),
            ("Spencer", "Cosmos"),
            ("Brendan", "Database Design"),
            ("Brendan", "DNA & You"),
            ("Trevor", "Database Design"),
            ("Trevor", "Cosmos"),
            ("Paxtyn", "Database Design"),
            ("Paxtyn", "The Life of Cronkite")],}

    # Create relationships in the graph
    create_relationships(graph, relationships, people_nodes, book_nodes)

    # Prompt user to pick a person
    user_value = str(input("Pick between Spencer, Emily, Trevor, Brendan, or Paxtyn: "))
    selected_node = people_nodes[user_value]

    # Output the original graph
    print("Original Property Graph:")
    print(graph)

    # Generate the recommendation subgraph and the list of recommended books
    recommended_books, recommendation_subgraph = recommend_books(graph, selected_node, book_nodes)

    print(f"\nRecommendation Subgraph ({user_value} and Recommended Books):")
    print(recommendation_subgraph)

    # Generate the final graph after the recommendation graph is created
    final_graph = create_final_graph(graph, recommendation_subgraph)

    # Output the final graph
    print("\nFinal Graph (Original + Recommendations):")
    print(final_graph)

if __name__ == '__main__':
    main()