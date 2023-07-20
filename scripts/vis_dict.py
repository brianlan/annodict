import argparse
from pathlib import Path

import graphviz as gv
import pandas as pd
from loguru import logger


parser = argparse.ArgumentParser()
parser.add_argument("-d", "--dict", type=Path, required=True)
parser.add_argument("-o", "--output-path", type=Path, required=True)


def main(args):
    df = pd.read_excel(args.dict, engine="openpyxl")
    classnames = df['class'].values
    g = create_graph(classnames)
    visualize_graph(g, args.output_path)


def create_graph(classnames):
    g = gv.Digraph()
    for classname in classnames:
        nodes = classname.split('.')
        if 'undefined' in nodes:
            nodes = [nodes[-2], classname]
            # _idx = classname.rfind('.')
            # nodes = [classname[:_idx], classname[_idx+1:]]
        for node in nodes:
            if not exist_in_graph(node, g):
                g.node(node)
        for i in range(len(nodes) - 1):
            edge = f"{nodes[i]} -> {nodes[i+1]}"
            if not exist_in_graph(edge, g):
                g.edge(nodes[i], nodes[i+1])
    return g

def exist_in_graph(ele, g):
    for node in [ele.strip() for ele in g.body]:
        if ele in node:
            return True
    return False

def visualize_graph(g, output_path):
    g.render(str(output_path), view=True)


if __name__ == "__main__":
    main(parser.parse_args())
