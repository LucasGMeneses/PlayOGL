from pyrr import matrix44 as mat4

class Scene:
    def __init__(self):
        self.objs = []
        self.view = mat4.create_identity()
        self.projection = mat4.create_orthogonal_projection(-2, 2, -2, 2, -2, 2)
        self.lights = []
        self.camPos = [0.0, 0.0, 0.0]
        self.camLookAt = [0.0, 0.0, -1.0]
        self.shader = None
    def createView(self):
        self.view = mat4.create_look_at(self.camPos, self.camLookAt, [0.0, 1.0, 0.0])

    #procura pelo nome do objeto
    def search(self, name, lis):
        n = len(lis)

        for i in range(n):
            if lis[i].name == name:
                return i
        
        return -1
    def remove(self, name, lis):
        i = self.search(name, lis)
        if i != -1:
            del(lis[i])
        else:
            print('object not found')
        