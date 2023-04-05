import pickle
from pprint import pprint
import sys
import pandas as pd


if len(sys.argv) == 1:
    exit

with open(sys.argv[1], "rb") as picklejar:
    synsets: dict = pickle.load(picklejar)

multiplesxls = pd.read_excel(sys.argv[2])
print(multiplesxls)
curili = ""
typesynsets = {}
for i, row in multiplesxls.iterrows():
    if row["New type"] == "synset":
        curili = row["ILI"]
    elif row["New type"] == sys.argv[3]:
        typesynsets[curili] = synsets[curili]

leaves = []
mids = []

for ili in typesynsets:
    if len(synsets[ili]["hypernyms"]) > 1:
        if "hyponyms" in synsets[ili] and len(synsets[ili]["hyponyms"]) > 0:
            mids.append(ili)
        else:
            leaves.append(ili)

print(f"{len(leaves)} leaves: {leaves}")
print(f"{len(mids)} mids: {mids}")
