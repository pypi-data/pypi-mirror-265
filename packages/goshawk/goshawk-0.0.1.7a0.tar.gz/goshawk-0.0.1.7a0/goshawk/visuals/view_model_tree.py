import urllib
import urllib.parse
import urllib.request
import webbrowser
from typing import Dict, List, Optional, Set

import goshawk.builder.file_reader as fr


def schema_dag_to_dot(schema_dag: Dict[str, Set[str]]) -> str:
    dot_graph = "digraph G {\n"
    for child_schema in schema_dag:
        dot_graph = dot_graph + f'"{child_schema}";\n'
    for child_schema in schema_dag:
        for parent_schema in schema_dag[child_schema]:
            dot_graph = dot_graph + f'"{parent_schema}" -> "{child_schema}";\n'
    dot_graph = dot_graph + "}"
    return dot_graph


def model_dag_to_dot(model_dag: Dict[str, Set[str]]) -> str:
    dot_graph = "digraph G {\n"
    for child_model in model_dag:
        dot_graph = dot_graph + f'"{child_model}";\n'
    for child_model, parent_model_list in model_dag.items():
        for parent_model in parent_model_list:
            dot_graph = dot_graph + f'"{parent_model}" -> "{child_model}";\n'
    dot_graph = dot_graph + "}"
    return dot_graph


def view_schema_tree(masks: Optional[List[str]]) -> None:
    result = fr.read_files(masks)
    # print("building dag")
    ts = fr.build_schema_dag(result)

    valid = fr.validate_schema_dag(ts)
    if not valid:
        print("Cycle error exists")
    dot = schema_dag_to_dot(ts)

    # url = f'https://graphviz.shn.hk/?src={urllib.parse.quote(dot)}&format=svg'
    # urllib.request.urlretrieve(url, "dag.svg")
    url = "https://edotor.net/?engine=dot#" + urllib.parse.quote(dot)

    # url='https://quickchart.io/graphviz?graph='+urllib.parse.quote(dot)

    print(dot)
    # body = {"graph": dot, "layout": "dot", "format": "svg"}

    # r = requests.post('https://quickchart.io/graphviz', json=body)

    # r.text is sufficient for SVG. Use `r.raw` for png images
    # svg = r.text
    # with open("dag.svg", "w") as file1:
    #    file1.write(svg)

    # webbrowser.open_new('/Users/ericb/Code/goshawk/dag.html')

    webbrowser.open_new(url)


def view_model_tree(masks: Optional[List[str]]) -> None:
    result = fr.read_files(masks)
    # print("building dag")
    dag = fr.build_dag(result)
    dot = model_dag_to_dot(dag)
    print(dot)

    url = "https://edotor.net/?engine=dot#" + urllib.parse.quote(dot)

    webbrowser.open_new(url)
