import os, json
import pandas as pd

a = pd.read_csv('data/Relationship_category_count.csv')
nodes = list(set(a['0']))+list(set(a['1']))
map_nodes = {v:i for i,v in enumerate(nodes)}


with open('file.json', 'w') as outfile:
    data = {
        "nodes": [{"name":i} for i in nodes], 
        "links":  [{"source": map_nodes[i[0]], "target": map_nodes[i[1]], "value": i[2]} for i in a.values]
    }
    json.dump(data, outfile)