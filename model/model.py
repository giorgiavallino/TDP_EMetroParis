from database.DAO import DAO
import networkx as nx

class Model:

    def __init__(self):
        self._fermate = DAO.getAllFermate()
        self._grafo = nx.DiGraph() # viene creato una volta per tutte, quindi va bene crearlo nell'__init__
        self._idMapFermate = {}
        for fermata in self._fermate:
            self._idMapFermate[fermata.id_fermata] = fermata # questa mappa associa all'id_fermata la fermata (oggetto)

    def buildGraph(self):
        self._grafo.clear()
        # Aggiungere i nodi
        self._grafo.add_nodes_from(self._fermate)
        self.addEdges_03()

    def buildGraphPesato(self):
        self._grafo.clear()
        self._grafo.add_nodes_from(self._fermate)
        self.addEdgesPesati_01()

    def addEdges_01(self):
        # Aggiungere gli archi
        for u in self._fermate:
            for v in self._fermate:
                if DAO.hasConnessione(u, v): # bisognerebbe aggiungere nell'if che i due nodi non siano uguali
                # (per un codice più pulito e preciso)
                    self._grafo.add_edge(u, v)
    # Questo metodo è corretto, ma facendo due cicli for il sistema impiega molto tempo nel determinare gli archi

    def addEdges_02(self):
        for u in self._fermate:
            for con in DAO.getVicini(u):
                v = self._idMapFermate[con.id_stazA]
                self._grafo.add_edge(u, v)

    def addEdges_03(self):
        for connessione in DAO.getAllEdges():
            u = self._idMapFermate[connessione.id_stazA]
            v = self._idMapFermate[connessione.id_stazP]
            self._grafo.add_edge(u, v)

    def addEdgesPesati_01(self):
        for connessione in DAO.getAllEdges():
            u = self._idMapFermate[connessione.id_stazA]
            v = self._idMapFermate[connessione.id_stazP]
            if self._grafo.has_edge(u, v):
                self._grafo[u][v]["weight"] += 1
            else:
                self._grafo.add_edge(u, v, weight=1)

    # L'alternativa a questo metodo potrebbe essere cambiare la query (sfruttando la funzionalità GROUP BY) (vedere DAO)

    def addEdgesPesati_02(self):
        allEdgesPesati = DAO.getAllEdgesPesati()
        for edge in allEdgesPesati:
            self._grafo.add_edge(self._idMapFermate[edge[0]],
                                 self._idMapFermate[edge[1]],
                                 weight = edge[2])

    def getArchiPesoMaggiore(self):
        edges = self._grafo.edges(data=True)
        result = []
        for edge in edges:
            if self._grafo.get_edge_data(edge[0], edge[1])["weight"] > 1:
                result.append(edge)
        return result

    def getNumNodi(self):
        return len(self._grafo.nodes)

    def getNumArchi(self):
        return len(self._grafo.edges)

    def getBFSNodesTree(self, source):
        tree = nx.bfs_tree(self._grafo, source)
        nodi = list(tree.nodes())
        return nodi[1:] # si aggiunge ciò per evitare di restituire anche il nodo sorgente

    def getDFSNodesTree(self, source):
        tree = nx.dfs_tree(self._grafo, source)
        nodi = list(tree.nodes())
        return nodi[1:]

    def getBFSNodesFromEdges(self, source):
        archi = nx.bfs_edges(self._grafo, source)
        result = []
        for u, v in archi:
            result.append(v)
        return result
    # Questo metodo genera un cammino

    @property
    def fermate(self):
        return self._fermate