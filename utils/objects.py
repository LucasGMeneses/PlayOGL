from numpy import array
import utils.readers as rd
from pyrr import matrix44 as mat4

# classe um objeto generico
class Object3d:
    def __init__(self, name, vertices, color):
        self.name = name        #  nome
        self.vertices = vertices # vertices 
        self.color = color # cor
        self.model = mat4.create_identity() # matrix model
        self.nVet = len(vertices) // 6 # numero de vertices
        self.vao = None
    
    # imprime as informações do objeto
    def printInfo(self):
        print('Name:', self.name)
        print('Vertices:\n', self.vertices)
        print('color:', self.color)
        print('Model:\n', self.model)


# cubo
class Cube(Object3d):
    def __init__(self, name, color=[0.0,1.0,0.0]):
        vertices = array(rd.readObj('cube'), dtype='f')
        super().__init__(name, vertices, color)

# torus
class Torus(Object3d):
    def __init__(self, name, color=[0.0,1.0,0.0]):
        vertices = array(rd.readObj('torus'), dtype='f')
        super().__init__(name, vertices, color)

# cone
class Cone(Object3d):
    def __init__(self, name, color=[0.0,1.0,0.0]):
        vertices = array(rd.readObj('cone'), dtype='f')
        super().__init__(name, vertices, color)

# ico
class Ico(Object3d):
    def __init__(self, name, color=[0.0,1.0,0.0]):
        vertices = array(rd.readObj('ico'), dtype='f')
        super().__init__(name, vertices, color)

