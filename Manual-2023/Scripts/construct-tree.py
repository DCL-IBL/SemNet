import pickle
import string
from sys import argv
import sys
import xml.etree.ElementTree as et
from pprint import pprint


if len(sys.argv) == 1:
    exit

wn_tree = et.parse(sys.argv[1])
synsets = {}
types = set()

for ss_el in wn_tree.getroot().findall("SYNSET"):
    ss_id = ss_el.findtext("ID")
    ss_set = [
        (ss_lit.findtext("VAL"), ss_lit.findtext("SENSE")) for ss_lit in ss_el.find("SYNONYM").findall("LITERAL")
    ]
    ss_hypernyms = [
        ilr_el.findtext("VAL") for ilr_el in ss_el.findall("ILR") if ilr_el.findtext("TYPE") == "hypernym"
    ]
    ss_relations = {
        ilr_el.findtext("VAL"):ilr_el.findtext("TYPE") for ilr_el in ss_el.findall("ILR") if ilr_el.findtext("TYPE") == "hypernym"
    }
    ss_cpa = [
        cpa_el.text for cpa_el in ss_el.findall("CPA")
    ]
    ss_def = ss_el.findtext("DEF")
    synsets[ss_id] = {
        "id": ss_id,
        "set": ss_set,
        "hypernyms": ss_hypernyms,
        "cpa": ss_cpa,
        "hyponyms": [],
        "def": ss_def,
        "relations": ss_relations,
        "print": len(ss_hypernyms) > 1
    }

for synset in synsets.values():
    for hypernym in synset["hypernyms"]:
        if hypernym in synsets:
            synsets[hypernym]["hyponyms"].append(synset["id"])
        else:
            print(f"Hypernym {hypernym} not in set")

if len(sys.argv) > 2:
    with open(sys.argv[2], "wb") as picklejar:
        pickle.dump(synsets, picklejar)

pprint(synsets)
