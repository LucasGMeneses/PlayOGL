import pywavefront as pwf
import sys

# le os .obj
# gera um array com os pontos e as normais
def readObj(name):
    scene = pwf.Wavefront('obj/' + name + '.obj')
    scene.parse()

    for name, material in scene.materials.items():
            return material.vertices

# faz a leitura dos shaders
def readShaderFile(filename):
	with open('shader/' + filename, 'r') as myfile:
		return myfile.read()

# le as entradas fornecidas pelo usuario
def readInput():
	with open(sys.argv[1], 'r') as myfile:
		return myfile.read()