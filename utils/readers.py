import pywavefront as pwf

def readObj(name):
    scene = pwf.Wavefront('obj/' + name + '.obj')
    scene.parse()

    for name, material in scene.materials.items():
            return material.vertices

def readShaderFile(filename):
	with open('shader/' + filename, 'r') as myfile:
		return myfile.read()