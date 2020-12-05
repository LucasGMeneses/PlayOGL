from numpy import array
import utils.readers as rd
from pyrr import matrix44 as mat4

# classe um objeto generico
class Object3d:
    def __init__(self, name, color, nVet, vao, vbo):
        self.name = name        #  nome
        self.color = color # cor
        self.model = mat4.create_identity() # matrix model
        self.nVet = nVet
        self.vao = vao
        self.vbo = vbo

    def translate(self, position):
        translate = mat4.create_from_translation(position,dtype='f')
        self.model = mat4.multiply(self.model, translate)
    def scale(self, scale):
        scale = mat4.create_from_scale(scale,dtype='f')
        self.model = mat4.multiply(self.model, scale)

    def rotate(self, ang, vect):
        rotate = mat4.create_from_axis_rotation(vect, ang)
        self.model = mat4.multiply(self.model, rotate)
    
    # imprime as informações do objeto
    def printInfo(self):
        print('Name:', self.name)
        print('Nº vert:\n', self.nVet)
        print('color:', self.color)
        print('Model:\n', self.model)
        print('VAO:\n', self.vao)
        print('VBO:\n', self.vbo)
        print('%%%%%%%%%%%%%%%%%%%%%%%%')


# cubo
class Cube(Object3d):
    def __init__(self, name, vao, vbo, color=[1.0,1.0,1.0]):
        super().__init__(name, color, 42, vao, vbo)
        

# torus
class Torus(Object3d):
    def __init__(self, name, vao, vbo, color=[1.0,1.0,1.0]):
        super().__init__(name, color, 3462, vao, vbo)



# cone
class Cone(Object3d):
    def __init__(self, name, vao, vbo, color=[1.0,1.0,1.0]):
        super().__init__(name, color, 276, vao, vbo)
        

# ico
class Ico(Object3d):
    def __init__(self, name, vao, vbo, color=[1.0,1.0,1.0]):
        super().__init__(name, color, 15363, vao, vbo)

class Light:
    def __init__(self, name, position):
        self.name = name
        self.position = position
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