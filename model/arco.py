from dataclasses import dataclass

from model.regista import Regista


@dataclass
class Arco:
    nodo1:Regista
    nodo2:Regista
    peso:int