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
        # Aggiungere i nodi
        self._grafo.add_nodes_from(self._fermate)
        self.addEdges_03()

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

    def getNumNodi(self):
        return len(self._grafo.nodes)

    def getNumArchi(self):
        return len(self._grafo.edges)

    @property
    def fermate(self):
        return self._fermate