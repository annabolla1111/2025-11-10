import copy

import networkx as nx

from database.DAO import DAO


class Model:
    def __init__(self):
        self._graph = nx.DiGraph()
        self._ordini = []
        self._idMapOrdini = {}

    def getAllStores(self):
        return DAO.getAllStores()

    def buildGraph(self, store, k):
        self._graph.clear()
        self._ordini = DAO.getAllNodes(store)
        for o in self._ordini:
            self._idMapOrdini[o.order_id]= o

        self._graph.add_nodes_from(self._ordini)

        allEdges = DAO.getAllEdges(store,k, self._idMapOrdini)
        for e in allEdges:
            self._graph.add_edge(e[0], e[1], weight=e[2])


    def getGraphDetails(self):
        return len(self._graph.nodes), len(self._graph.edges)

    def getAllNodes(self):
        return list(self._graph.nodes)

    def getTop5Edges(self):
        return sorted(self._graph.edges(data=True), key=lambda e: e[2]["weight"], reverse=True)[:5]

    def getCammino(self, nodoPartenza):
        source = self._idMapOrdini[int(nodoPartenza)]
        lp = [] #longest path

        #for source in self._graph.nodes:
        tree = nx.dfs_tree(self._graph, source)
        nodi = list(tree.nodes())

        for node in nodi:
            tmp = [node]  #nodo di arrivo

            while tmp[0] != source:
                pred = nx.predecessor(tree, source, tmp[0])
                tmp.insert(0, pred[0])

            if len(tmp) > len(lp):
                lp = copy.deepcopy(tmp)

        return lp


    def bestPath(self, startStr):
        self._bestPath = []
        self._bestScore = 0

        start = self._idMapOrdini[int(startStr)]

        parziale = [start]

        vicini = self._graph.neighbors(start)
        for v in vicini:
            parziale.append(v)
            self._ricorsione(parziale)
            parziale.pop()

        return self._bestPath, self._bestScore


    def _ricorsione(self, parziale):
            if self.getScore(parziale) > self._bestScore:
                self._bestScore = self.getScore(parziale)
                self._bestPath = copy.deepcopy(parziale)

            for v in self._graph.neighbors(parziale[-1]):
                if (v not in parziale and  # check if not in parziale
                        self._graph[parziale[-2]][parziale[-1]]["weight"] >
                        self._graph[parziale[-1]][v]["weight"]):  # check if peso nuovo arco è minore del precedente
                    parziale.append(v)
                    self._ricorsione(parziale)
                    parziale.pop()

    def getScore(self, listOfNodes):
        tot = 0
        for i in range(len(listOfNodes) - 1):
            tot += self._graph[listOfNodes[i]][listOfNodes[i + 1]]["weight"]

        return tot