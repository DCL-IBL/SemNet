import pickle
from pprint import pprint
import sys
import pandas as pd


if len(sys.argv) == 1:
    exit

with open(sys.argv[1], "rb") as picklejar:
    synsets: dict = pickle.load(picklejar)

rels = {
    "characteristic": "has_characteristic",
    "form": "has_form",
    "function": "has_function",
    "holo_member": "holo_member",
    "holo_part": "holo_part",
    "holo_portion": "holo_portion",
    "instance_hyperonym": "instance_hyperonym",
    "origin": "has_origin",
    "purpose": "has_purpose",
    "used for": "has_uses",
    "hypernym": "hypernym"
}
rev_rels = {
    "form of": "has_form",
    "mero_part": "holo_part",
    "mero_portion": "holo_portion",
    "uses": "has_uses"
}

sheet_multiples = pd.read_excel(sys.argv[2], sheet_name="Multiples")
cur_ili = ""

for i, row in sheet_multiples.iterrows():
    if row["New type"] == "synset":
        cur_ili = row["ILI"]
    elif row["Original type"] == "hypernym" and row["New type"] != "hypernym":
        synsets[cur_ili]["hypernyms"].remove(row["ILI"])
        synsets[row["ILI"]]["hyponyms"].remove(cur_ili)
        if not pd.isnull(row["New type"]):
            del synsets[cur_ili]["relations"][row["ILI"]]
            if row["New type"] in rels:
                synsets[cur_ili]["relations"][row["ILI"]] = "~" + rels[row["New type"]]
            elif row["New type"] in rev_rels:
                synsets[row["ILI"]]["relations"][cur_ili] = "~" + rev_rels[row["New type"]]
        else:
            synsets[cur_ili]["relations"][row["ILI"]] = "-hypernym"
    elif row["New type"] == "hypernym" and pd.isnull(row["Original type"]):
        synsets[cur_ili]["hypernyms"].append(row["ILI"])
        synsets[row["ILI"]]["hyponyms"].append(cur_ili)
        synsets[cur_ili]["relations"][row["ILI"]] = "+hypernym"

sheet_other = pd.read_excel(sys.argv[2], sheet_name="Other")

for i, row in sheet_other.iterrows():
    if not pd.isnull(row["Original relation"]):
        synsets[row["Synset from"]]["relations"][row["Synset to"]] = "-" + synsets[row["Synset from"]]["relations"][row["Synset to"]]
        if row["Original relation"] == "hypernym":
            synsets[row["Synset from"]]["hypernyms"].remove(row["Synset to"])
            synsets[row["Synset to"]]["hyponyms"].remove(row["Synset from"])
    if not pd.isnull(row["New relation"]):
        if not pd.isnull(row["Original relation"]):
            synsets[row["Synset from"]]["relations"][row["Synset to"]] = "~" + rels[row["New relation"]]
        else:
            synsets[row["Synset from"]]["relations"][row["Synset to"]] = "+" + rels[row["New relation"]]
        if row["New relation"] == "hypernym":
            synsets[row["Synset from"]]["hypernyms"].append(row["Synset to"])
            synsets[row["Synset to"]]["hyponyms"].append(row["Synset from"])

if len(sys.argv) > 3:
    with open(sys.argv[3], "wb") as picklejar:
        pickle.dump(synsets, picklejar)

pprint(synsets)
