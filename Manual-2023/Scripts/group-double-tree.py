import pickle
from pprint import pprint
import sys
import xlsxwriter


if len(sys.argv) < 3:
    exit

with open(sys.argv[1], "rb") as picklejar:
    synsets: dict = pickle.load(picklejar)

pprint(synsets)

groups = {ili: set([hyponym for hyponym in synsets[ili]["hyponyms"] if len(synsets[hyponym]["hypernyms"]) > 1]) for ili in synsets}
groups = dict(filter(lambda item: len(item[1]) > 0, groups.items()))
# groups = dict(sorted(groups.items(), key=lambda item: len(item[1]), reverse=True))

dgroups = {}
for group1_ili in groups:
    for group2_ili in groups:
        if group1_ili == group2_ili or (group2_ili, group1_ili) in dgroups:
            continue
        dgroup = groups[group1_ili] & groups[group2_ili]
        if len(dgroup) > 0:
            dgroups[(group1_ili, group2_ili)] = dgroup

pprint(dgroups, sort_dicts=False)

def literals(ili):
    return ", ".join([":".join(lit) for lit in synsets[ili]["set"]])

def cpa(ili):
    return ", ".join(synsets[ili]["cpa"])

def rowset(type, ili):
    return [type, type, ili, literals(ili), cpa(ili), synsets[ili]["def"]]

for (group1_ili, group2_ili) in dgroups:
    dgroup = dgroups[(group1_ili, group2_ili)]
    dgroup_ili = group1_ili[:15] + "-" + group2_ili[7:]
    with xlsxwriter.Workbook(sys.argv[2] + "/" + "{:>02}".format(str(len(dgroup))) + "-" + dgroup_ili + ".xlsx") as workbook:
        worksheet = workbook.add_worksheet(dgroup_ili)
        worksheet.write_row(0, 0, ["DH type", "SK type", "ili", "literals", "cpa", "def"])
        worksheet.write_row(1, 0, rowset("group", group1_ili))
        worksheet.write_row(2, 0, rowset("group", group2_ili))

        row = 4
        for hyponym in dgroup:
            worksheet.write_row(row, 0, rowset("synset", hyponym)); row += 1
            for hypernym in synsets[hyponym]["hypernyms"]:
                worksheet.write_row(row, 0, rowset("hypernym", hypernym)); row += 1
            row += 1
