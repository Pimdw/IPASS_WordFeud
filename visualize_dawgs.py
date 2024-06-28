import graphviz

def create_node(id_counter=[0]):
    id_counter[0] += 1
    return {
        'children': {},
        'is_terminal': False,
        'id': id_counter[0]
    }

def insert(root, word):
    node = root
    for char in word:
        if char not in node['children']:
            node['children'][char] = create_node()
        node = node['children'][char]
    node['is_terminal'] = True

def minimize(node, nodes=None):
    if nodes is None:
        nodes = {}
    if not node['children']:
        node_id = (node['is_terminal'],)
    else:
        child_tuples = []
        for char, next_node in sorted(node['children'].items()):
            minimized_child_id = minimize(next_node, nodes)
            child_tuples.append((char, minimized_child_id))
        node_id = (node['is_terminal'],) + tuple(child_tuples)

    if node_id in nodes:
        existing_node = nodes[node_id]
        node['children'] = existing_node['children']
        node['is_terminal'] = existing_node['is_terminal']
        node['id'] = existing_node['id']
    else:
        nodes[node_id] = node
    return node_id

def visualize_dawg(node, graph=None, node_id=None, node_map=None):
    if graph is None:
        graph = graphviz.Digraph(format='png')
        node_id = str(node['id'])
        node_map = {}
        graph.node(node_id, label=node_id, shape='doublecircle' if node['is_terminal'] else 'circle')
        node_map[node['id']] = node_id

    for char, child in node['children'].items():
        if child['id'] in node_map:
            child_id = node_map[child['id']]
        else:
            child_id = str(child['id'])
            graph.node(child_id, label=child_id, shape='doublecircle' if child['is_terminal'] else 'circle')
            node_map[child['id']] = child_id
            visualize_dawg(child, graph, child_id, node_map)
        graph.edge(node_id, child_id, label=char)
    
    return graph

def render_dawg(name, root):
    graph = visualize_dawg(root)
    graph.render(name, view=True)

# Create the root node
root = create_node()
reversed_root = create_node()

words = ["cat", "cats", "car", "cars", "do", "dog", "dogs", "done", "ear", "ears", "eat", "eats"]

for word in words:
    word = word.upper()
    insert(root, word)
minimize(root)

for word in words:
    word = word.upper()
    word = reversed(word)
    insert(reversed_root, word)
minimize(reversed_root)

render_dawg('DAWG_visualization/dawg_visualization', root)
render_dawg('DAWG_visualization/r_dawg_visualization', reversed_root)

# 15x15 board
board = [['', '', '', '', '', '', '', '', '', '', '', '', '', '', ''], 
         ['', '', '', '', '', '', '', '', '', '', '', '', '', '', ''],
         ['', '', '', '', '', '', '', '', '', '', '', '', '', '', ''],
         ['', '', '', '', '', '', '', '', '', '', '', '', '', '', ''],
         ['', '', '', '', '', '', 'C', '', '', '', '', '', '', '', ''],
         ['', '', '', '', '', '', 'A', '', '', '', '', '', '', '', ''],
         ['', '', '', '', '', '', '', '', '', '', '', '', '', '', ''],
         ['', '', '', '', '', '', '', 'C', 'A', 'T', '', '', '', '', ''],
         ['', '', '', '', '', '', '', '', '', '', '', '', '', '', ''],
         ['', '', '', '', '', '', '', '', '', '', '', '', '', '', ''],
         ['', '', '', '', '', '', '', '', '', '', '', '', '', '', ''],
         ['', '', '', '', '', '', '', '', '', '', '', '', '', '', ''],
         ['', '', '', '', '', '', '', '', '', '', '', '', '', '', ''],
         ['', '', '', '', '', '', '', '', '', '', '', '', '', '', ''],
         ['', '', '', '', '', '', '', '', '', '', '', '', '', '', '']]


rack = ['E', 'R', 'S', 'L', 'A', 'T', 'T']