from pyrr import matrix44 as mat4

class Scene:
    def __init__(self):
        self.Objs = []
        self.view = mat4.create_identity()
        self.projection = mat4.create_identity()
        self.light = []
    def add(self, object, lis):
        lis.append(object)
    
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
        