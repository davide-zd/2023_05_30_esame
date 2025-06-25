import networkx as nx

from database.DAO import DAO


class Model:
    def __init__(self):
        self._grafo = nx.Graph()
        self._idMap = {}

    def fillDD_Anni(self):
        return DAO.getAnni()

    def fillDD_Nazioni(self):
        return DAO.getNazioni()

    def creaGrafo(self, nazione, numero, anno):
        # pulisco il grafo
        self._grafo.clear()

        # creo i nodi e li aggiungo
        lista_nodi = DAO.getNodes(nazione)
        for l in lista_nodi:
            self._grafo.add_node(l)
            self._idMap[l.id] = l

        # creo gli archi (grafo non orientato)
        lista_archi = DAO.getEdges(nazione, numero, anno)
        for a in lista_archi:
            self._grafo.add_edge(self._idMap[a[0]], self._idMap[a[1]], weight=a[2])

    def graphDetails(self):
        return len(self._grafo.nodes), len(self._grafo.edges)

    def getArchiOrdinati(self):
        lista_archi = list(self._grafo.edges(data=True)) # con data=true prendo oltre all'arco anche gli attributi (peso)
        lista_ordinata = sorted(lista_archi, key=lambda x: x[2]['weight'])
        return lista_ordinata

    def fillDD_Retailer(self):
        return self._grafo.nodes

    def getCompConnessa(self, nodo):
        componente = nx.node_connected_component(self._grafo, nodo)

        # trovare la somma totale dei pesi degli archi connessi
        somma_peso = 0
        for i in componente:
            for l in componente:
                if i.id > l.id:
                    if self._grafo.has_edge(i, l):
                        somma_peso += self._grafo.edges[i, l]['weight']

        return len(componente), somma_peso