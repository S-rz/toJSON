import argparse

def parameter_parser():
    parser = argparse.ArgumentParser(description="To JSON")

    parser.add_argument("--dataset",
                        nargs="?",
                        default="MUTAG",
                        help="")
    parser.add_argument("--input-folder",
                        nargs="?",
                        default="./input/",
                        help="")
    parser.add_argument("--output-folder",
                        nargs="?",
                        default="./output/",
                        help="")
    return parser.parse_args()

def node_label(args):
    dataset = args.dataset
    input_folder = args.input_folder
    folder_ending = ".txt"
    folder_name = input_folder + dataset + "_node_labels" + folder_ending
    labels = dict()
    with open(folder_name) as f:
        num = 1
        line = f.readline()
        while(line):
            labels[str(num)] = str(line).strip()
            num = num + 1
            line = f.readline()

    return labels, (num - 1)

def graph_indicator(args):
    dataset = args.dataset
    input_folder = args.input_folder
    folder_ending = ".txt"
    folder_name = input_folder + dataset + "_graph_indicator" + folder_ending
    nodes = dict()
    max_graph = 0
    with open(folder_name) as f:
        num = 1
        line = f.readline()
        while (line):
            nodes[str(num)] = line.strip()
            max_graph = max(max_graph, int(line))
            num = num + 1
            line = f.readline()

    return nodes, max_graph

def edge(args):
    dataset = args.dataset
    input_folder = args.input_folder
    folder_ending = ".txt"
    folder_name = input_folder + dataset + "_A" + folder_ending
    edges = []
    with open(folder_name) as f:
        line = f.readline()
        while(line):
            index_comma = line.find(',')
            edge_i = int(line[0 : index_comma])
            edge_v = int(line[index_comma + 1 :].strip())
            edges.append([edge_i, edge_v])
            line = f.readline()

    return edges

def graph_label(args, num_graph):
    dataset = args.dataset
    input_folder = args.input_folder
    folder_ending = ".txt"
    folder_name = input_folder + dataset + "_graph_labels" + folder_ending
    with open(folder_name) as f:
        text = f.readlines()
        label = text[num_graph].strip()
        # if label == '6':
        #     label = '0'
        # print(label)

    return label

def save_json(args, result):
    dataset = args.dataset
    output_folder = args.output_folder
    folder_ending = ".json"

    for num in result.keys():
        folder_name = output_folder + dataset + '/' + num + folder_ending
        # print(folder_name)
        with open(folder_name, "a") as f:
            f.write( (str(result[num])).replace('\'','\"') )

def deal_nodes_num(result):
    for graph in result.keys():
        node_min = 1e10
        temp_label = dict()

        for node in result[graph]["labels"].keys():
            node_min = min(node_min, int(node))

        for node in result[graph]["labels"].keys():
            temp_node = int(node) - node_min
            temp_label[str(temp_node)] = result[graph]["labels"][node]

        result[graph]["labels"].clear()
        result[graph]["labels"] = temp_label

        for edge in result[graph]["edges"]:
            edge[0] = edge[0] - node_min
            edge[1] = edge[1] - node_min

if __name__ == "__main__":
    args = parameter_parser()
    nodes_labels, nodes_num = node_label(args)
    nodes_in_graph, max_graph = graph_indicator(args)
    edges = edge(args)
    result = dict()

    for i in range(max_graph):
        str_graph = str(i)
        result[str_graph] = dict()
        graphs_labels = graph_label(args, i)
        result[str_graph]["target"] = int(graphs_labels)
        result[str_graph]["labels"] = dict()
        result[str_graph]["edges"] = []

    for nodes in nodes_in_graph.keys():
        graph = int(nodes_in_graph[nodes]) - 1
        label = nodes_labels[nodes]
        result[str(graph)]["labels"][nodes] = label

    for edge_temp in edges:
        nodes = str(edge_temp[0])
        graph = int(nodes_in_graph[nodes]) - 1
        (result[str(graph)]["edges"]).append(edge_temp)

    deal_nodes_num(result)
    # print(str(result).replace('\'','\"'))
    save_json(args, result)