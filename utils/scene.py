from pyrr import matrix44 as mat4

class Scene:
    # construtor
    def __init__(self):
        self.objs = []
        self.view = mat4.create_identity() # matriz view
        self.projection = mat4.create_orthogonal_projection(-2, 2, -2, 2, -2, 2) # matriz projection
        self.lights = []
        self.camPos = [0.0, 0.0, 0.0]
        self.camLookAt = [0.0, 0.0, -1.0]
        
        self.shader = None
        self.diffuse = 0.2
        self.ambient = 0.2
        self.specular = 0.2
    
    # cria a matriz view baseada na posicao da camera e do lookat
    def createView(self):
        self.view = mat4.create_look_at(self.camPos, self.camLookAt, [0.0, 1.0, 0.0])

    # procura o objeto / luz pelo nome
    def search(self, name, lis):
        n = len(lis)

        for i in range(n):
            if lis[i].name == name:
                return i
        
        return -1
    
    # remove o objeto / luz pelo nome
    def remove(self, name, lis):
        i = self.search(name, lis)
        if i != -1:
            del(lis[i])
        else:
            print('object not found')
        