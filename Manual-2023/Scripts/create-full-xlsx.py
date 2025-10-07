import pickle
from pprint import pprint
import sys
import xlsxwriter


if len(sys.argv) < 3:
    exit

with open(sys.argv[1], "rb") as picklejar:
    synsets: dict = pickle.load(picklejar)

# pprint(synsets)

def literals(ili):
    return ", ".join([":".join(lit) for lit in synsets[ili]["set"]])

def cpa(ili):
    return ", ".join(synsets[ili]["cpa"])

def rowset(filter_code, type, ili):
    return [filter_code, "", type, type, ili, literals(ili), cpa(ili), synsets[ili]["def"]]

with xlsxwriter.Workbook(sys.argv[2]) as workbook:
    worksheet = workbook.add_worksheet("Multiples")
    worksheet.write_row(0, 0, ["Filter code", "New CPA", "Original type", "New type", "ILI", "Literals", "Automatic CPA", "Definition"])

    row = 1
    for hyponym in synsets:
        if len(synsets[hyponym]["hypernyms"]) < 2:
            continue
        
        filter_code = "-".join([hili[7:15] for hili in synsets[hyponym]["hypernyms"]])
        worksheet.write_row(row, 0, rowset(filter_code, "synset", hyponym)); row += 1
        for hypernym in synsets[hyponym]["hypernyms"]:
            worksheet.write_row(row, 0, rowset(filter_code, "hypernym", hypernym)); row += 1
        worksheet.write_row(row, 0, [filter_code]); row += 1
