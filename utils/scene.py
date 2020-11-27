from pyrr import matrix44 as mat4

class scene:
    def __init__(self):
        
        self.view = mat4.create_identity()
        self.projection = mat4.create_identity()