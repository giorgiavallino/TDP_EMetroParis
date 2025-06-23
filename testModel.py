# File per testare il modello

from model.fermata import Fermata
from model.model import Model

model = Model()

model.buildGraphPesato()
print(f"Numero nodi: {model.getNumNodi()}")
print(f"Numero archi: {model.getNumArchi()}")

fermata = Fermata(2, "Abbesses", 2.33855, 48.8843)
nodesBFS = model.getBFSNodesTree(fermata)
for nodo in nodesBFS:
    print(nodo)

archiMaggiori = model.getArchiPesoMaggiore()
for arco in archiMaggiori:
    print(arco)