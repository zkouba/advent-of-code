import re
from typing import List, Dict, Tuple, Set

# We're gonna traverse some graphs this time!!!! :-)

LEAF = "no other bags"

GRP_NAME_SUBJECT = "subject"
GRP_SUBJECT = "(?P<" + GRP_NAME_SUBJECT + ">[a-z][a-z\\s]*)"

GRP_NAME_CHILDREN = "children"
GRP_CHILD = "\\d+\\s*[a-z][a-z\\s]*\\s+bags?"

PATTERN_BAG_RULE = re.compile(
    "^" + GRP_SUBJECT +  "bags contain (?P<" + GRP_NAME_CHILDREN + ">" + GRP_CHILD + "(\\s*,\\s*" + GRP_CHILD + ")*)\\.$"
)

GRP_NAME_CHILD_OCCURRENCES = "occurrences"
GRP_NAME_CHILD_COLOR = "color"
PATTERN_CHILD = re.compile(
    "(?P<" + GRP_NAME_CHILD_OCCURRENCES + ">\\d+)\\s*(?P<" + GRP_NAME_CHILD_COLOR + ">[a-z][a-z\\s]*)\\s+bags?"
)


class Bag:

    # ID_BASE = 0

    def __init__(self, color: str):
        # self.id = Bag.ID_BASE
        # Bag.ID_BASE += 1
        self.color: str = color
        self.children: Dict[str, Child] = {}
        self.parents: Dict[str, Bag] = {}

    # def __eq__(self, other):
    #     if type(other) is not Bag:
    #         return False
    #     return self.id == other.id


class Child:
    def __init__(self, occurrences: int, bag: Bag):
        self.occurrences = occurrences
        self.bag = bag


class Graph:
    def __init__(self):
        self.root_colors: List[str] = []
        self.graph_map: Dict[str, Bag] = dict()

    def add_node(self, node_color: str, children=None) -> None:
        if children is None:
            # for some reason, PEP likes it more like this
            children = []

        # Check whether we've already came across this bag color, or whether it's a new one
        node: Bag
        if node_color in self.graph_map.keys():
            node = self.graph_map[node_color]
        else:
            node = Bag(color=node_color)
            self.graph_map[node_color] = node

        # Setup the children nodes of the new node
        for child_tuple in children:
            child_occurrences = child_tuple[0]
            child_color = child_tuple[1]
            # Check whether the child color is a new one, or whether we already have an object for it
            child_bag: Bag
            if child_color in self.graph_map.keys():
                child_bag = self.graph_map[child_color]
            else:
                child_bag = Bag(color=child_color)
                self.graph_map[child_color] = child_bag
            # Link the child object with it's new parent
            child_bag.parents[node_color] = node
            node.children[child_color] = Child(occurrences=child_occurrences, bag=child_bag)

        # Update this graph's roots
        # (since some of the current root nodes might have become children of the newly added node)
        new_roots: List[str] = []
        for root_candidate in self.root_colors:
            r = self.graph_map[root_candidate]
            if len(r.parents) == 0:
                new_roots.append(root_candidate)
        if len(node.parents) == 0:
            new_roots.append(node.color)
        self.root_colors = new_roots

    def count_all_parents_for(self, node_color: str, visited_nodes: List[str] = None) -> Set[str]:
        ret_val = set()
        if node_color in self.root_colors:
            return ret_val

        if visited_nodes is None:
            visited_nodes = []
        elif node_color in visited_nodes:
            raise ValueError("You lead me into a loop, you bastard!!!")
        visited_nodes.append(node_color)

        node = self.graph_map[node_color]
        for parent_color in node.parents.keys():
            ret_val.add(parent_color)
            grandparents = self.count_all_parents_for(parent_color, visited_nodes[:])
            ret_val.update(grandparents)
        return ret_val

    def count_needed_other_bags_for(self, node_color: str) -> int:
        return self.count_needed_bags_for(node_color) - 1

    def count_needed_bags_for(self, node_color: str, visited_nodes: List[str] = None) -> int:
        total = 1
        node = self.graph_map[node_color]
        if len(node.children) == 0:
            return total
        if visited_nodes is None:
            visited_nodes = []
        elif node_color in visited_nodes:
            raise ValueError("You lead me into a loop, you bastard!!!")

        for child_color in node.children.keys():
            child = node.children[child_color]
            childs_total = self.count_needed_bags_for(child_color, visited_nodes[:])
            total += (child.occurrences * childs_total)

        return total


def load(input_path: str) -> Graph or None:
    graph = Graph()
    with open(input_path, 'r') as input_file:
        for raw_line in input_file:
            line = raw_line.strip().lower()
            m_rule = PATTERN_BAG_RULE.match(line)
            if m_rule:
                bag_color = m_rule.group(GRP_NAME_SUBJECT).strip()
                children_str = m_rule.group(GRP_NAME_CHILDREN).strip()
                children: List[Tuple[int, str]] = []
                if not children_str == LEAF:
                    child_tuples = PATTERN_CHILD.findall(children_str)
                    for child_tuple in child_tuples:
                        occurrences = int(child_tuple[0].strip())
                        child_color = child_tuple[1].strip()
                        children.append((occurrences, child_color))
                graph.add_node(bag_color, children)
    return graph


def main() -> None:
    graph = load("./input.txt")
    my_bag = "shiny gold"
    n = graph.count_all_parents_for(my_bag)
    print("%s bag can be contained by %d bags" % (my_bag, len(n)))

    n = graph.count_needed_other_bags_for(my_bag)
    print("You need %d other bags if you start with a single %s bag" % (n, my_bag))


if __name__ == "__main__":
    main()
