import pickle
from pprint import pprint
import sys
import graphviz as gv
import math

# python analyse-tree.py <pickle-jar> [<visuals-folder>] [><out-file>]

print(f"DOT version: {gv.version()}")

if len(sys.argv) == 1:
    exit

with open(sys.argv[1], "rb") as picklejar:
    synsets: dict = pickle.load(picklejar)

reverse = {
    "attribute": "attribute_of",
#    "category_domain": "category_domain_of",
#    "eng_derivative": "eng_derivative",
    "has_state": "is_state_of",
    "has_uses": "uses",
    "holo_member": "mero_member",
    "holo_part": "mero_part",
    "holo_portion": "mero_portion",
    "hypernym": "hyponym",
    "instance_hypernym": "instance_hyponym",
#    "near_antonym": "near_antonym",
#    "region_domain": "region_domain_of",
#    "usage_domain": "usage_domain_of",
    "has_characteristic": "characteristic_of",
    "has_form": "form_of",
    "has_function": "function_of",
    "manifestation_of": "has_manifestation",
    "has_origin": "origin_of",
    "has_purpose": "purpose_of",
}

for ili in synsets:
    for rel_ili in synsets[ili]["relations"]:
        if rel_ili not in synsets:
            continue
        rel_type = synsets[ili]["relations"][rel_ili]
        modifier = ""
        if rel_type[0] in ["+", "-", "~"]:
            modifier = rel_type[0]
            rel_type = rel_type[1:]
        if ili not in synsets[rel_ili]["relations"] and rel_type in reverse:
            synsets[rel_ili]["relations"][ili] = modifier + reverse[rel_type]

def dot_label(synset:dict):
    return "< <FONT face=\"Arial\">" + synset["id"] + "<BR/>" + "; ".join([ f"<I>{lit[0]}</I>:{lit[1]}" for lit in synset["set"] ]) + "</FONT> >"

used_main = set()
used_side = set()
total_ssn = 1421
current_n = 1

def print_status():
    print(f"\r SS {current_n}/{total_ssn} - {round(current_n / total_ssn * 100)}%", end=" ")

def dot_build_up(gr: gv.Digraph, synset, in_main_tree = True, lvl = 0):
    if synset["id"] in used_main or (not in_main_tree and synset["id"] in used_side):
        return
    used_side.add(synset["id"])
    if in_main_tree:
        used_main.add(synset["id"])
    
    # print(synset["id"], dot_label(synset), lvl)
    # print(synset["relations"])
    if in_main_tree and synset["print"]:
        gr.node(synset["id"], dot_label(synset), style=("filled,bold" if lvl == 0 else "filled"), shape="box")
    else:
        gr.node(synset["id"], dot_label(synset), shape="box")
    for rel_ili in synset["relations"]:
        # print(synset["relations"][rel_ili])
        rel_type = synset["relations"][rel_ili]
        edge_color = "black"
        if rel_type[0] == "-":
            edge_color = "red"
            rel_type = rel_type[1:]
        elif rel_type[0] == "~":
            edge_color = "blue"
            rel_type = rel_type[1:]
        elif rel_type[0] == "+":
            edge_color = "green3"
            rel_type = rel_type[1:]
        if rel_ili not in synsets or rel_type == "hyponym":
            continue
        if rel_type == "hypernym":
            dot_build_up(gr, synsets[rel_ili], in_main_tree and edge_color != "red", lvl + 1)
            if in_main_tree and edge_color != "red":
                gr.edge(rel_ili, synset["id"], color=edge_color, fontcolor=edge_color, dir="back", weight="8")
            else:
                gr.edge(rel_ili, synset["id"], color=edge_color, fontcolor=edge_color, dir="back", weight="2")
        elif rel_type in reverse.keys():
            dot_build_up(gr, synsets[rel_ili], False, lvl + 1)
            gr.edge(rel_ili, synset["id"], label=rel_type, color=edge_color, fontcolor=edge_color, dir="back", weight=str(1 + (3 if in_main_tree else 0)))
        elif rel_type in reverse.values() and lvl == 0:
            dot_build_up(gr, synsets[rel_ili], False, lvl + 1)

for synset in synsets.values():
    if synset["print"]:
        print_status()
        gr = gv.Digraph(f"WN-{synset['id']}-{len(synset['hypernyms'])}H", filename=f"WN-{synset['id']}-{len(synset['hypernyms'])}H.gv", strict=True, graph_attr={"bgcolor": "none"}, node_attr={"style": "filled", "fillcolor": "white"})
        used_main.clear()
        used_side.clear()
        dot_build_up(gr, synset)

        # print(gr.source)
        gr.render((sys.argv[2] if len(sys.argv) > 2 else "Graphs") + "/" + gr.filename, format="png", engine="dot")
        current_n += 1

def print_with_hypernyms(synset):
    print()
    print(f"{synset['id']} {{ {', '.join([ ':'.join(lit) for lit in synset['set'] ])} }}")
    print()
    for hypernym in synset["hypernyms"]:
        print(f"{synsets[hypernym]['id']} {{ {', '.join([ ':'.join(lit) for lit in synsets[hypernym]['set'] ])} }}")
    print()

# pprint(synsets)
# for synset in synsets.values():
#     if synset["print"]:
#         print_with_hypernyms(synset)
#         # print(synset['id'])
