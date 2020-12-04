from numpy import array
import utils.readers as rd
from pyrr import matrix44 as mat4

# classe um objeto generico
class Object3d:
    def __init__(self, name, color, nVet):
        self.name = name        #  nome
        self.color = color # cor
        self.model = mat4.create_identity() # matrix model
        self.nVet = nVet

    # imprime as informações do objeto
    def printInfo(self):
        print('Name:', self.name)
        print('Nº vert:\n', self.nVet)
        print('color:', self.color)
        print('Model:\n', self.model)


# cubo
class Cube(Object3d):
    def __init__(self, name, vao, vbo, color=[1.0,1.0,1.0]):
        super().__init__(name, color, 42)
        self.vao = vao
        self.vbo = vbo

# torus
class Torus(Object3d):
    def __init__(self, name, vao, vbo, color=[1.0,1.0,1.0]):
        super().__init__(name, color, 3462)
        self.vao = vao
        self.vbo = vbo


# cone
class Cone(Object3d):
    def __init__(self, name, vao, vbo, color=[1.0,1.0,1.0]):
        super().__init__(name, color, 276)
        self.vao = vao
        self.vbo = vbo
        

# ico
class Ico(Object3d):
    def __init__(self, name, vao, vbo, color=[1.0,1.0,1.0]):
        super().__init__(name, color, 15363)
        self.vao = vao
        self.vbo = vbo

'''
    aux.append(Cube(txt)) 
    aux.append(Ico(txt))
    aux.append(Torus(txt))
    aux.append(Cone(txt))

42
15363
3462
276
'''