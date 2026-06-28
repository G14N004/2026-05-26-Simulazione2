import networkx as nx

from database.DAO import DAO


class Model:
    def __init__(self):
        self._grafo = nx.Graph()
        self._idMap={}
        pass

    def getRatings(self):
        return DAO.getRating()

    def getNumNodi(self):
        return len(self._grafo.nodes())

    def getNumArchi(self):
        return len(self._grafo.edges())

    def getNodi(self,avg1,avg2):
        return DAO.getNodi(avg1,avg2)

    def buildGrafo(self,avg1,avg2):
        self._grafo.clear()
        for nodo in self.getNodi(avg1,avg2):
            self._grafo.add_node(nodo)
            self._idMap[nodo.id]=nodo

        archi = DAO.getArchi(avg1,avg2,self._idMap)
        for arco in archi:
            self._grafo.add_edge(arco.nodo1,arco.nodo2,weight=arco.peso)


    def getTop5ArchiPeso(self):
        archi = sorted(self._grafo.edges(data=True),key=lambda x: x[2]["weight"],reverse=True)
        return archi[:5]


    def getCompConnessa(self):
        # 2. Otteniamo tutte le componenti connesse
        # nx.connected_components restituisce un generatore di insiemi (set) di nodi
        componenti = list(nx.connected_components(self._grafo))

        # --- NUMERO DI COMPONENTI CONNESSE ---
        num_componenti = len(componenti)
        #print(f"Numero di componenti connesse: {num_componenti}")

        # --- LISTA DELLA COMPONENTE PIÙ GRANDE ---
        # Usiamo max() basandoci sulla lunghezza (len) di ogni componente
        componente_piu_grande = max(componenti, key=len)

        # Convertiamo il set in una lista (opzionale, ma utile se devi manipolarla)
        lista_componente_grande = list(componente_piu_grande)
        return num_componenti, lista_componente_grande



