from collections import deque

def topsort(g):
    data = {
        "graph": g,
        "state": {k: "NOT_VISITED" for k in g},
        "d":     {k: 0 for k in g},
        "f":     {k: 0 for k in g},
        "time":  0,
        "list":  deque()
    }
    for k in g:
        if data["state"][k] == "NOT_VISITED":
            _visit(data, k)
    print(*list(data["list"]))

def _visit(data, k):
    data["state"][k] = "VISITED"
    data["time"] += 1
    data["d"][k]  = data["time"]
    for adj in data["graph"][k]:
        if data["state"][adj] == "NOT_VISITED":
            _visit(data, adj)
    data["state"][k] = "FINISHED"
    data["time"] += 1
    data["f"][k]  = data["time"]
    data["list"].appendleft(k)