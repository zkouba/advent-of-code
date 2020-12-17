import unittest

from aoc2020.task07.task07 import load, Graph, Bag, Child


class MyTestCase(unittest.TestCase):

    def test_add_node(self):
        # setup a graph
        graph = Graph()

        # add first node with 1 child
        graph.add_node('root', [(1, 'child')])

        # verify that the node became the graph's root
        self.assertEqual(1, len(graph.root_colors))
        self.assertEqual('root', graph.root_colors[0])
        # verify both the node and it's child have been added
        self.assertEqual(2, len(graph.graph_map))
        # verify the node's children
        self.assertEqual(1, len(graph.graph_map['root'].children))
        # verify that the node's children list and the graph's overall map point to the same instance
        # (e.g. there's only a single instance representing the node's child and it's referenced from both places)
        self.assertEqual(graph.graph_map['root'].children['child'].bag, graph.graph_map['child'])
        # verify the child's parent list
        self.assertEqual(1, len(graph.graph_map['child'].parents))
        # verify that the child's parent list and the graph's overall map point to the same instance
        # (e.g. there's only a single instance representing the node - e.g. the child's parent - and it's referenced
        # from both places)
        self.assertEqual(graph.graph_map['child'].parents['root'], graph.graph_map['root'])

        # add a rule for the previous node's child, which itself has 2 children
        # and perform similar verifications as above
        graph.add_node('child', [(1, 'grandchild a'), (2, 'grandchild b')])
        self.assertEqual(1, len(graph.root_colors))
        self.assertEqual('root', graph.root_colors[0])
        self.assertEqual(4, len(graph.graph_map))
        self.assertEqual(1, len(graph.graph_map['root'].children))
        self.assertEqual(graph.graph_map['root'].children['child'].bag, graph.graph_map['child'])
        self.assertEqual(1, len(graph.graph_map['child'].parents))
        self.assertEqual(graph.graph_map['child'].parents['root'], graph.graph_map['root'])
        self.assertEqual(2, len(graph.graph_map['child'].children))
        self.assertEqual(graph.graph_map['child'].children['grandchild a'].bag, graph.graph_map['grandchild a'])
        self.assertEqual(graph.graph_map['child'].children['grandchild b'].bag, graph.graph_map['grandchild b'])
        self.assertEqual(1, len(graph.graph_map['grandchild a'].parents))
        self.assertEqual(graph.graph_map['grandchild a'].parents['child'], graph.graph_map['child'])
        self.assertEqual(1, len(graph.graph_map['grandchild b'].parents))
        self.assertEqual(graph.graph_map['grandchild b'].parents['child'], graph.graph_map['child'])

    def test_count_parents(self):
        simple_graph = load("./simple_graph.txt")
        self.assertEqual(4, len(simple_graph.count_all_parents_for('shiny gold')))

    def test_count_needed_bags(self):
        simple_graph = load("./simple_graph.txt")
        self.assertEqual(32, simple_graph.count_needed_other_bags_for('shiny gold'))


if __name__ == '__main__':
    unittest.main()
