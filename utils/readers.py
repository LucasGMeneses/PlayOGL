import pywavefront as pwf
import sys
import numpy as np

# le os .obj
# gera um array com os pontos e as normais
def readObj(name):
    scene = pwf.Wavefront('obj/' + name + '.obj')
    scene.parse()

    for name, material in scene.materials.items():
            return np.array(material.vertices, dtype='f')

# faz a leitura do shader
def readShaderFile(filename):
	with open('shader/' + filename, 'r') as myfile:
		return myfile.read()

