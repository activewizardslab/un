import json
import pandas as pd

a = pd.read_csv('data/Journals_Categories_count.csv')
nodes = list(set(a['0']))+list(set(a['1']))
map_nodes = {v:i for i,v in enumerate(nodes)}


with open('Journals_Categories_count.json', 'w') as outfile:
    data = {
        "nodes": [{"name":i} for i in nodes], 
        "links":  [{"source": map_nodes[i[0]], "target": map_nodes[i[1]], "value": i[2]} for i in a.values]
    }
    json.dump(data, outfile)


t = pd.read_csv('static/data/Persentage_of_relation.csv')

res  = [{"key": key, "color": "", "values": [{"label": i, "value":j} for i,j in zip(t[t.columns[0]],t[key])]} for key in t.columns[1:]]

with open('static/data/Persentage_of_relation.json', 'w') as outfile:
    json.dump(res, outfile)