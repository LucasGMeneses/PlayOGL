import sys
import numpy as np
from OpenGL.GL import *
from OpenGL.GL import shaders
from OpenGL.GLUT import *

from utils.objects import *
from utils.readers import *
from utils.scene import Scene
vao = None
vbo = None

shaderProgram = []
data = readObj('cube')
cube = Cube('oi')
def execComands():

	file = open(sys.argv[1])
	for line in file:
		if line != '\n':
			cmd = line.replace('\n','').split(' ')
			# visualização dos eixos xyz
			if cmd[0]  == 'axis_on':
				print('eixos ligados')
			elif cmd[0] == 'axis_off':
				print(cmd[0])

			# visao wireframe
			elif cmd[0] == 'wire_on':
				print(cmd[0])
			elif cmd[0] == 'wire_off':
				print(cmd[0])

			# manipula objetos
			elif cmd[0] == 'add_shape':
				print(cmd[0])
			elif cmd[0] == 'remove_shape':
				print(cmd[0])
			
			# manipula pts de luz
			elif cmd[0] == 'add_light':
				print(cmd[0])
			elif cmd[0] == 'remove_light':
				print(cmd[0])
			elif cmd[0] == 'light_on':
				print(cmd[0])
			elif cmd[0] == 'light_off':
				print(cmd[0])
			
			# reflexao
			elif cmd[0] == 'reflection_on':
				print(cmd[0])
			elif cmd[0] == 'reflection_off':
				print(cmd[0])
			
			# cores
			elif cmd[0] == 'shading':
				print(cmd[0])
			elif cmd[0] == 'color':
				print(cmd[0])

			# transformacoes
			elif cmd[0] == 'translate':
				print(cmd[0])
			elif cmd[0] == 'rotate':
				print(cmd[0])
			elif cmd[0] == 'scale':
				print(cmd[0])
			elif cmd[0] == 'shear':
				print(cmd[0])
			
			# camera configs
			elif cmd[0] == 'lookat':
				print(cmd[0])
			elif cmd[0] == 'cam':
				print(cmd[0])
			
			# opcoes extras
			elif cmd[0] == 'save':
				print('NOT IMPLEMENTED')
			elif cmd[0] == 'quit':
				print('NOT IMPLEMENTED')
			else:
				print('ERROR')
	file.close()

def init():
	global shaderProgram
	global vao
	global vbo
	
	glClearColor(0, 0, 0, 0)
	
	
	shader = ['default']
	# compila todos os shaders disponiveis na lista a cima
	n = len(shader)
	for i in range(n):
		vertex_code = readShaderFile(shader[i] +'.vp')
		fragment_code = readShaderFile(shader[i] + '.fp')

		# compile shaders and program
		vertexShader = shaders.compileShader(vertex_code, GL_VERTEX_SHADER)
		fragmentShader = shaders.compileShader(fragment_code, GL_FRAGMENT_SHADER)
		aux = shaders.compileProgram(vertexShader, fragmentShader)
		shaderProgram.append(aux)
	
	# Create and bind the Vertex Array Object
	vao = GLuint(0)
	vao = glGenVertexArrays(1)
	glBindVertexArray(vao)
	# Create and bind the Vertex Buffer Object
	vertices =  data
	#print(data)
	vbo = glGenBuffers(1)
	
	glBindBuffer(GL_ARRAY_BUFFER, vbo)
	glBufferData(GL_ARRAY_BUFFER, vertices, GL_STATIC_DRAW)
	

	glVertexAttribPointer(0, 3, GL_FLOAT, False, 6 * sizeof(GLfloat), ctypes.c_void_p(3*sizeof(GLfloat)))  # vertices
	glVertexAttribPointer(1, 3, GL_FLOAT, False, 6 * sizeof(GLfloat), ctypes.c_void_p(0))  # vertores normais

	glEnableVertexAttribArray(0) 
	glEnableVertexAttribArray(1)
	
	# Note that this is allowed, the call to glVertexAttribPointer registered VBO
	# as the currently bound vertex buffer object so afterwards we can safely unbind
	glBindBuffer(GL_ARRAY_BUFFER, 0)
	#Unbind VAO (it's always a good thing to unbind any buffer/array to prevent strange bugs)
	glBindVertexArray(0)

def display():
	global shaderProgram
	global vao
	scene = Scene()
	glEnable(GL_DEPTH_TEST)
	glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
	execComands()

	# load everthing back
	glUseProgram(shaderProgram[0])
	glBindVertexArray(vao)
	glBindBuffer(GL_ARRAY_BUFFER, vbo)
	id = glGetUniformLocation(shaderProgram[0], 'fColor')
	glUniform3fv(id,1, cube.color)
	glDrawArrays(GL_TRIANGLE_STRIP, 0, cube.nVet)
	
	#clean things up
	glBindBuffer(GL_ARRAY_BUFFER, 0)
	glBindVertexArray(0)
	glUseProgram(0)
	
	glutSwapBuffers()  # necessario para windows!
def reshape(width, height):
	glViewport(0, 0, width, height)

	
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
