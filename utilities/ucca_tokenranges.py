import json
import sys
import itertools
from tqdm import tqdm

def extract_anchor(j):
    return (j["from"], j["to"])

def extract_all_anchors(j):
    if "anchors" in j:
        return [extract_anchor(a) for a in j["anchors"]]
    else:
        return []


# collect token ranges in companion data

companion_tokens = {}

with open("data_ucca/udpipe.mrp", "r") as f:
    for line in tqdm(f):
        j = json.loads(line)
        id = j["id"]
        anchors = [[extract_anchor(a) for a in b["anchors"]] for b in j["nodes"]]
        companion_tokens[id] = set(itertools.chain(*anchors))



# collect token ranges in UCCA MRP graphs
ucca_mrp_files = ["data_ucca/ucca/ewt.mrp", "data_ucca/ucca/wiki.mrp", "data_ucca/ucca/wsj.mrp"]
num_missing_tr = 0
num_total_tr = 0

for file in ucca_mrp_files:
    print(f"Analyzing {file}...")

    with open(file, "r") as f:
        for line in tqdm(f):
            j = json.loads(line)
            id = j["id"]
            companion_anchors = companion_tokens[id]

            anchors = [extract_all_anchors(b) for b in j["nodes"]]

            for anch in itertools.chain(*anchors):
                num_total_tr += 1

                if not anch in companion_anchors:
                    print(f"[{id}] mismatched anchor: {anch}")
                    num_missing_tr += 1

print(f"{num_missing_tr} anchors mismatched out of {num_total_tr} ({100*num_missing_tr/num_total_tr:.2f}%)")
