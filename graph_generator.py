"""
    File name: graph_generator.py
    Author: Temur Malishava
"""

import textwrap
import random


def create_table():
    """
    Creates an SQL script for a table creation of the graph

    :return: number of the created graph
    :rtype: int
    """
    sql_create_table = textwrap.dedent(f"""
                                        drop table if exists graph;
                                        CREATE TABLE graph (
                                            x text,
                                            r text,
                                            y text
                                        );
                                        """)
    print(sql_create_table)


def fill_table(nodes_num=10**3, edges_num=10**4, edges_labels=['a', 'b', 'c']):
    """
    Filling the created table with the edges of the graph

    :param nodes_num: number of nodes we want to have in a graph
    :type nodes_num: int
    :param edges_num: number of edges we want to have in a graph
    :type edges_num: int
    :param edges_labels: all possible labels of the edges we want to have in a graph
    :type edges_labels: list
    """

    # Set a limit for the number of nodes
    # if nodes_num > 100:
    #     nodes_num = 100

    # Check if the graph can exist with the given number of edges and number of nodes
    max_edge_num = nodes_num * (nodes_num - 1) * len(edges_labels)
    if edges_num > max_edge_num:
        edges_num = max_edge_num

    # Create a dictionary of all possible edges
    max_graph = {}
    for node1 in range(1, nodes_num + 1):
        max_graph[node1] = []
        for node2 in range(1, nodes_num + 1):
            if node1 != node2:
                for label in edges_labels:
                    max_graph[node1].append((node2, label))
        random.shuffle(max_graph[node1])

    # Picking out the edges from the created dictionary
    edges = []
    for i in range(edges_num):
        node1 = random.choice(list(max_graph.keys()))
        node2, label = max_graph[node1].pop()

        if len(max_graph[node1]) == 0:
            max_graph.pop(node1)

        edge = f"('{node1}', '{label}', '{node2}')"
        edges.append(edge)

    edges = ', '.join(edges)

    create_table()
    sql_fill_table = textwrap.dedent(f"""
                                      INSERT
                                      INTO
                                      graph(x, r, y)
                                      VALUES
                                      {edges};
                                      """)
    print(sql_fill_table)
    with open('graph_generator.txt', 'w') as f:
        print(sql_fill_table, file=f)


fill_table()
