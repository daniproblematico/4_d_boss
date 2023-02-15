import json

with open("project.geom", "r") as f:
    datos = json.load(f)


class Lvl:
    def __init__(self, lvl_id, H, cols, beams):
        self.lvl_id = lvl_id
        self.H = H
        self.cols = cols
        self.beams = beams

class Beam:
    def __init__(self, lvl_id, beam_id, node_i, node_f):
        self.lvl_id = lvl_id
        self.beam_id = beam_id
        self.node_i = node_i
        self.node_f = node_f

class Column:
    def __init__(self,lvl_id,column_id,node_b,node_t):
        self.lvl_id = lvl_id
        self.column_id = column_id
        self.node_b = node_b
        self.node_t = node_t

class Node:
    def __init__(self,lvl_id,node_id, x_dim, y_dim, z_dim):
        self.lvl_id=lvl_id
        self.x_dim=x_dim
        self.y_dim=y_dim
        self.z_dim=z_dim
        self.node_id=node_id

#este método crea los objetos piso y los agrupa en una lista
pisos=[]
h=0
for lvl_id in reversed(datos["pisos"]):

    h = datos["pisos"][lvl_id]+h
    col = list(datos["col_piso"][lvl_id].keys())
    beam = list(datos["vig_piso"][lvl_id].keys())
    piso = Lvl(lvl_id, h, col, beam)
    pisos.append(piso)


#este método crea los objetos viga en cada piso y los agrupa en una lista
vigas = []
for n in pisos:
    for b in n.beams:  # b es una viga perteneciente al piso n
        nodoi = datos["vigas"][b][0]
        nodod = datos["vigas"][b][1]
        viga = Beam(n.lvl_id, b, nodoi, nodod)
        vigas.append(viga)

#este método crea los objetos columna para cada piso y los agrupa en una lista
columnas=[]
for n in pisos:
    for b in n.cols:
        nodob = datos["columnas"][b][0]
        nodot = datos["columnas"][b][1]
        columna = Column(n.lvl_id, b, nodob, nodot)
        columnas.append(columna)
#parámetros de un objeto columna específico
#print(columnas[1].__dict__)


#este método crea los objetos nodo para cada piso y los agrupa en una lista

obnodos=[]
for n in pisos:
    z=n.H
    nodos=[]
    for b in n.beams:    
        nodos.append(datos["vigas"][b][0])
        nodos.append(datos["vigas"][b][1])
    for b in n.cols:
        nodos.append(datos["columnas"][b][0])
        nodos.append(datos["columnas"][b][1])
    res = []
    [res.append(x) for x in nodos if x not in res]
    for nodox in res:
        x=datos["nodos"][nodox][0]
        y=datos["nodos"][nodox][1]
        nodo=Node(n.lvl_id,nodox,x,y,z)
        #visualiza la creación de objetos nodo
        #print(nodo)
        obnodos.append(nodo)
        print(nodox)

#número de nodos creados, número de nodos en el archivo .geom
print(len(obnodos),len(datos["nodos"]))
#parámetros de un nodo específico
print(obnodos[0].__dict__)
            

