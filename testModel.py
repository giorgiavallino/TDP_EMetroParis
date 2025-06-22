# File per testare il modello

from model.model import Model

model = Model()
model.buildGraph()
print(f"Numero nodi: {model.getNumNodi()}")
print(f"Numero archi: {model.getNumArchi()}")