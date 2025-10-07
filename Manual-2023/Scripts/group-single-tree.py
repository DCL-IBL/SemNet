import pickle
from pprint import pprint
import sys
import xlsxwriter


if len(sys.argv) < 3:
    exit

with open(sys.argv[1], "rb") as picklejar:
    synsets: dict = pickle.load(picklejar)

pprint(synsets)

groups = {ili: [hyponym for hyponym in synsets[ili]["hyponyms"] if len(synsets[hyponym]["hypernyms"]) > 1] for ili in synsets}
groups = dict(filter(lambda item: len(item[1]) > 0, groups.items()))
groups = dict(sorted(groups.items(), key=lambda item: len(item[1]), reverse=True))
pprint(groups, sort_dicts=False)

def literals(ili):
    return ", ".join([":".join(lit) for lit in synsets[ili]["set"]])

def cpa(ili):
    return ", ".join(synsets[ili]["cpa"])

def rowset(type, ili):
    return [type, type, ili, literals(ili), cpa(ili), synsets[ili]["def"]]

print(groups)

for group_ili in groups:
    with xlsxwriter.Workbook(sys.argv[2] + "/" + "{:>02}".format(str(len(groups[group_ili]))) + "-" + group_ili + ".xlsx") as workbook:
        worksheet = workbook.add_worksheet(group_ili)
        worksheet.write_row(0, 0, ["DH type", "SK type", "ili", "literals", "cpa", "def"])
        worksheet.write_row(1, 0, rowset("group", group_ili))

        row = 3
        for hyponym in groups[group_ili]:
            worksheet.write_row(row, 0, rowset("synset", hyponym)); row += 1
            for hypernym in synsets[hyponym]["hypernyms"]:
                worksheet.write_row(row, 0, rowset("hypernym", hypernym)); row += 1
            row += 1
