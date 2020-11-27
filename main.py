import sys
import numpy as np
from OpenGL.GL import *
from OpenGL.GL import shaders
from OpenGL.GLUT import *

from utils.objects import *
from utils.readers import readShaderFile
vao = None
vbo = None

shaderProgram = None
cube = Cube('cn1',[1.0,0.0,1.0])

def init():
	global shaderProgram
	global vao
	global vbo
	
	glClearColor(0, 0, 0, 0)
	
	vertex_code = readShaderFile('default.vp')
	fragment_code = readShaderFile('default.fp')

	# compile shaders and program
	vertexShader = shaders.compileShader(vertex_code, GL_VERTEX_SHADER)
	fragmentShader = shaders.compileShader(fragment_code, GL_FRAGMENT_SHADER)
	shaderProgram = shaders.compileProgram(vertexShader, fragmentShader)
	
	# Create and bind the Vertex Array Object
	vao = GLuint(0)
	glGenVertexArrays(1, vao)
	glBindVertexArray(vao)
	
	# Create and bind the Vertex Buffer Object
	
	vertices =  cube.vertices
	
	vbo = glGenBuffers(1)
	glBindBuffer(GL_ARRAY_BUFFER, vbo)
	glBufferData(GL_ARRAY_BUFFER, vertices, GL_STATIC_DRAW)
	glVertexAttribPointer(0, 3, GL_FLOAT, False, 6 * sizeof(GLfloat), ctypes.c_void_p(3*sizeof(GLfloat)))  # vertices
	glVertexAttribPointer(1, 3, GL_FLOAT, False, 6 * sizeof(GLfloat), ctypes.c_void_p(0))  # vertores normais

	glEnableVertexAttribArray(0);  # 0=location do atributo, tem que ativar todos os atributos inicialmente sao desabilitados por padrao
	glEnableVertexAttribArray(1);  # 1=location do atributo, tem que ativar todos os atributos inicialmente sao desabilitados por padrao
	
	# Note that this is allowed, the call to glVertexAttribPointer registered VBO
	# as the currently bound vertex buffer object so afterwards we can safely unbind
	glBindBuffer(GL_ARRAY_BUFFER, 0)
	# Unbind VAO (it's always a good thing to unbind any buffer/array to prevent strange bugs)
	glBindVertexArray(0)

def display():
	global shaderProgram
	global vao
	
	glEnable(GL_DEPTH_TEST)

	glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
	# load everthing back
	glUseProgram(shaderProgram)
	glBindVertexArray(vao)
	glBindBuffer(GL_ARRAY_BUFFER, vbo)
	id = glGetUniformLocation(shaderProgram, 'fColor')
	glUniform3fv(id,1, cube.color)
	# glDrawArrays( mode , first, count)
	glDrawArrays(GL_TRIANGLE_STRIP, 0, cube.nVet)

	#clean things up
	glBindBuffer(GL_ARRAY_BUFFER, 0)
	glBindVertexArray(0)
	glUseProgram(0)
	
	glutSwapBuffers()  # necessario para windows!

def reshape(width, height):
	glViewport(0, 0, width, height)

def readInput():
	with open(sys.argv[1], 'r') as myfile:
		return myfile.read()
	
if __name__ == '__main__':
	glutInit(sys.argv[0])

	glutInitContextVersion(3, 0)
	glutInitContextProfile(GLUT_CORE_PROFILE)
	glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGB | GLUT_DEPTH)
	
	glutInitWindowSize(640, 640)
	glutCreateWindow(b'PlayOGL')
	
	glutReshapeFunc(reshape)
	glutDisplayFunc(display)
	glutIdleFunc(display)
	init()
	
	glutMainLoop()
