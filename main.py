import sys
import numpy as np
import math

from OpenGL.GL import *
from OpenGL.GL import shaders
from OpenGL.GLUT import *
from PIL import Image

from utils.objects import *
from utils.readers import *
from utils.scene import Scene

window = None
vao = []
vbo = []

shaderProgram = []
axis = False
wire = False
lights = False

def axisDraw():
	pass
def execComands(scene):
	global axis
	global wire
	global lights

	file = open(sys.argv[1])
	for line in file:
		if line != '\n':
			cmd = line.replace('\n','').split(' ')
			# visualização dos eixos xyz
			if cmd[0]  == 'axis_on':
				axis = True
			elif cmd[0] == 'axis_off':
				axis = False

			# visao wireframe
			elif cmd[0] == 'wire_on':
				wire = True
			elif cmd[0] == 'wire_off':
				wire = False

			# manipula objetos
			elif cmd[0] == 'add_shape':
				obj = None
				if cmd[1] == 'cube':
					obj = Cube(cmd[2], vao[0], vbo[0])
				if cmd[1] == 'torus':
					obj = Torus(cmd[2], vao[1], vbo[1])
				if cmd[1] == 'cone':
					obj = Cone(cmd[2], vao[2], vbo[2])
				if cmd[1] == 'sphere':
					obj = Ico(cmd[2], vao[3], vbo[3])
				
				if obj != None:
					scene.objs.append(obj)
			
			elif cmd[0] == 'remove_shape':
				scene.remove(cmd[1], scene.objs)
			
			# manipula pts de luz
			elif cmd[0] == 'add_light':
				pos = [float(cmd[2]),float(cmd[3]),float(cmd[4])]
				light = Light(cmd[1], pos)
				scene.lights.append(light)

			elif cmd[0] == 'remove_light':
				scene.remove(cmd[1], scene.lights)
			
			elif cmd[0] == 'light_on':
				lights = True
			elif cmd[0] == 'light_off':
				lights = False
			
			# reflexao
			elif cmd[0] == 'reflection_on':
				print(cmd[0])
			elif cmd[0] == 'reflection_off':
				print(cmd[0])
			
			# cores
			elif cmd[0] == 'shading':
				print(cmd[0])
			elif cmd[0] == 'color':
				index = scene.search(cmd[1],scene.objs)
				newColor = [float(cmd[2]),float(cmd[3]),float(cmd[4])]
				scene.objs[index].color = newColor

			# transformacoes
			elif cmd[0] == 'translate':
				index = scene.search(cmd[1],scene.objs)
				pos = [float(cmd[2]),float(cmd[3]),float(cmd[4])]
				scene.objs[index].translate(pos)
			elif cmd[0] == 'rotate':
				index = scene.search(cmd[1],scene.objs)
				ang = math.radians(float(cmd[2]))
				vect = [float(cmd[3]),float(cmd[4]),float(cmd[5])]
				scene.objs[index].rotate(ang, vect)
			elif cmd[0] == 'scale':
				index = scene.search(cmd[1],scene.objs)
				scale = [float(cmd[2]),float(cmd[3]),float(cmd[4])]
				scene.objs[index].scale(scale)
			
			elif cmd[0] == 'shear':
				print(cmd[0])
			
			# camera configs
			elif cmd[0] == 'lookat':
				look = [float(cmd[1]),float(cmd[2]),float(cmd[3])]
				scene.camLookAt = look
			elif cmd[0] == 'cam':
				pos = [float(cmd[1]),float(cmd[2]),float(cmd[3])]
				scene.camPos = pos
			
			# opcoes extras
			elif cmd[0] == 'save':
				glPixelStorei(GL_PACK_ALIGNMENT,1)
				data = glReadPixels(0, 0, 640, 640, GL_RGBA, GL_UNSIGNED_BYTE)
				image = Image.frombytes("RGBA", (640,640), data)
				image.save(cmd[1]+'.png','png')

			elif cmd[0] == 'quit':
				glutLeaveMainLoop(window)
				glutDestroyWindow(window)
			else:
				print('ERROR')
	file.close()

def init():
	global shaderProgram
	global vao
	global vbo
	
	glClearColor(0, 0, 0, 0)
	
	
	shader = ['none','axis', 'lights']
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
	
	objetos = ['cube', 'torus', 'cone', 'ico']
	# Create and bind the Vertex Array Object
	for i in range(len(objetos)):
		
		vao.append(GLuint(0))
		glGenVertexArrays(1,vao[i])
		glBindVertexArray(vao[i])
		# Create and bind the Vertex Buffer Object
		vertices =  readObj(objetos[i])
		vbo.append(glGenBuffers(1))
		glBindBuffer(GL_ARRAY_BUFFER, vbo[i])
		glBufferData(GL_ARRAY_BUFFER, vertices, GL_STATIC_DRAW)
		
		glVertexAttribPointer(0, 3, GL_FLOAT, False, 6 * sizeof(GLfloat), ctypes.c_void_p(3*sizeof(GLfloat)))  # vertices
		glVertexAttribPointer(1, 3, GL_FLOAT, False, 6 * sizeof(GLfloat), ctypes.c_void_p(0))  # vertores normais
		glEnableVertexAttribArray(0) 
		glEnableVertexAttribArray(1)
	
	print(readObj(objetos[0]))
	
	# axis vao e vbo
	vao.append(GLuint(0))
	glGenVertexArrays(1,vao[4])
	glBindVertexArray(vao[4])
	# Create and bind the Vertex Buffer Object
	vertices =  np.array([[-3, 0, 0, 1, 0, 0], [3, 0, 0, 1, 0, 0], # x
						[0, -3, 0, 0, 1, 0],[0, 3, 0, 0, 1, 0],	   # Y
						[0, 0, -3, 0, 0, 1],[0, 0, 3, 0, 0, 1]],   # Z
						dtype='f')
	vbo.append(glGenBuffers(1))
	glBindBuffer(GL_ARRAY_BUFFER, vbo[4])
	glBufferData(GL_ARRAY_BUFFER, vertices, GL_STATIC_DRAW)
		
	glVertexAttribPointer(1, 3, GL_FLOAT, False, 6 * sizeof(GLfloat), ctypes.c_void_p(3*sizeof(GLfloat)))  # vertices
	glVertexAttribPointer(0, 3, GL_FLOAT, False, 6 * sizeof(GLfloat), ctypes.c_void_p(0))  # vertores normais
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
	global axis
	global wire

	scene = Scene()
	scene.shader = shaderProgram[0]
	glEnable(GL_DEPTH_TEST)
	glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
	
	execComands(scene)
	scene.createView()
	# load everthing back
	for obj in scene.objs:
		glUseProgram(scene.shader)
		glBindVertexArray(obj.vao)
		glBindBuffer(GL_ARRAY_BUFFER, obj.vbo)
		#obj.printInfo()
		id = glGetUniformLocation(scene.shader, 'fColor')
		glUniform3fv(id, 1, obj.color)
		
		id = glGetUniformLocation(scene.shader, 'model')
		glUniformMatrix4fv(id, 1, GL_FALSE, obj.model)

		id = glGetUniformLocation(scene.shader, 'view')
		glUniformMatrix4fv(id, 1, GL_FALSE, scene.view)
		
		id = glGetUniformLocation(scene.shader, 'projection')
		glUniformMatrix4fv(id, 1, GL_FALSE, scene.projection)
		
		if wire == True:
			glDrawArrays(GL_LINE_LOOP, 0, obj.nVet)
			wire == False
		else:
			glDrawArrays(GL_TRIANGLE_STRIP, 0, obj.nVet)
	if lights == True:
		for light in scene.lights:
			glUseProgram(shaderProgram[2])

			id = glGetUniformLocation(shaderProgram[2], 'vPos')
			glUniform3fv(id, 1, light.position)

			id = glGetUniformLocation(scene.shader, 'view')
			glUniformMatrix4fv(id, 1, GL_FALSE, scene.view)
			
			id = glGetUniformLocation(scene.shader, 'projection')
			glUniformMatrix4fv(id, 1, GL_FALSE, scene.projection)
			glPointSize(10)
			glDrawArrays(GL_POINTS, 0, 1)
	
	if axis == True:
		glUseProgram(shaderProgram[1])
		glBindVertexArray(vao[4])
		glBindBuffer(GL_ARRAY_BUFFER, vbo[4])
		
		id = glGetUniformLocation(shaderProgram[1], 'view')
		glUniformMatrix4fv(id, 1, GL_FALSE, scene.view)
		id = glGetUniformLocation(shaderProgram[1], 'projection')
		glUniformMatrix4fv(id, 1, GL_FALSE, scene.projection)

		glDrawArrays(GL_LINES, 0, 6)

		axis = False
	
	#clean things up
	glBindBuffer(GL_ARRAY_BUFFER, 0)
	glBindVertexArray(0)
	glUseProgram(0)
	
	glutSwapBuffers()  # necessario para windows!
	glReadBuffer(GL_FRONT)

def reshape(width, height):
	glViewport(0, 0, width, height)

	
if __name__ == '__main__':
	glutInit(sys.argv[0])

	glutInitContextVersion(3, 0)
	glutInitContextProfile(GLUT_CORE_PROFILE)
	glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGB | GLUT_DEPTH)
	
	glutInitWindowSize(640, 640)
	window =glutCreateWindow(b'PlayOGL')
	
	glutReshapeFunc(reshape)
	glutDisplayFunc(display)
	glutIdleFunc(display)
	init()
	
	glutMainLoop()
