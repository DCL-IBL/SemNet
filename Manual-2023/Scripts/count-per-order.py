import pickle
from pprint import pprint
import sys


if len(sys.argv) < 2:
    exit

with open(sys.argv[1], "rb") as picklejar:
    synsets: dict = pickle.load(picklejar)

counts = {}

for ili in synsets:
    count = len(synsets[ili]["hypernyms"])
    if count not in counts:
        counts[count] = 1
    else:
        counts[count] += 1

for count in counts:
    print(str(count) + " " + str(counts[count]))