import networkx as nx

from database.DAO import DAO


class Model:
    def __init__(self):
        self._grafo=nx.Graph()
        self.idMap={}


    def getAllYear(self):
        return DAO.getAllYear()

    def getAllNazioni(self):
        return DAO.getAllNazioni()

    def creaGrafo(self,nazione,anno):
        # cancello il grafo precedente
        self._grafo.clear()
        #creo i nodi e la mappa
        nodes = DAO.getNodes(nazione)
        for n in nodes:
            self._grafo.add_node(n)
            self.idMap[n.Retailer_code]=n

        #creo gli archi
        archi = DAO.getEdges(nazione,anno)
        for a in archi:
            self._grafo.add_edge(self.idMap[a[0]],self.idMap[a[1]], weight=a[2])




    def getGraphDetails(self):
            return len(self._grafo.nodes), len(self._grafo.edges)


    def volume(self,nodo):
        peso=0
        for n in self._grafo.neighbors(nodo):
            peso+=self._grafo.edges[nodo,n]['weight']
        return peso