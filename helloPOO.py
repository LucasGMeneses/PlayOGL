import sys
import numpy as np

from OpenGL.GL import *
from OpenGL.GL import shaders
from OpenGL.GLUT import *


class Frame:
	def __init__(self, title='Frame', width=640, height=640):
		self.vao = None
		self.vbo = None
		self.shaderProgram = None

		glutInit(sys.argv)
		glutInitContextVersion(3, 0)
		glutInitContextProfile(GLUT_CORE_PROFILE);
		glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGB | GLUT_DEPTH)
	
		glutInitWindowSize(width, height)
		glutCreateWindow(title)
	
		glutReshapeFunc(self.reshape)
		glutDisplayFunc(self.display)
		self.init()
		glutMainLoop()


	def readShaderFile(self, filename):
		with open('shader/' + filename, 'r') as myfile:
			return myfile.read()

	def init(self):

		glClearColor(0, 0, 0, 0)
		
		vertex_code = self.readShaderFile('hello.vp')
		fragment_code = self.readShaderFile('hello.fp')

		# compile shaders and program
		vertexShader = shaders.compileShader(vertex_code, GL_VERTEX_SHADER)
		fragmentShader = shaders.compileShader(fragment_code, GL_FRAGMENT_SHADER)
		self.shaderProgram = shaders.compileProgram(vertexShader, fragmentShader)
		
		# Create and bind the Vertex Array Object
		self.vao = GLuint(0)
		glGenVertexArrays(1, self.vao)
		glBindVertexArray(self.vao)

		# Create and bind the Vertex Buffer Object
		vertices = np.array([[0, 1, 0, 0, 0, 1], [-1, -1, 0, 1, 1, 0], [1, -1, 0, 0, 1, 0]], dtype='f')
		self.vbo = glGenBuffers(1)
		glBindBuffer(GL_ARRAY_BUFFER, self.vbo)
		glBufferData(GL_ARRAY_BUFFER, vertices, GL_STATIC_DRAW)
		glVertexAttribPointer(0, 3, GL_FLOAT, False, 6 * sizeof(GLfloat), ctypes.c_void_p(0))  # first 0 is the location in shader
		glVertexAttribPointer(1, 3, GL_FLOAT, False, 6 * sizeof(GLfloat), ctypes.c_void_p(3*sizeof(GLfloat)))  # first 0 is the location in shader

		glEnableVertexAttribArray(0);  # 0=location do atributo, tem que ativar todos os atributos inicialmente sao desabilitados por padrao
		glEnableVertexAttribArray(1);  # 1=location do atributo, tem que ativar todos os atributos inicialmente sao desabilitados por padrao
		
		# Note that this is allowed, the call to glVertexAttribPointer registered VBO
		# as the currently bound vertex buffer object so afterwards we can safely unbind
		glBindBuffer(GL_ARRAY_BUFFER, 0)
		# Unbind VAO (it's always a good thing to unbind any buffer/array to prevent strange bugs)
		glBindVertexArray(0)

	def display(self):
		
		glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
		
		# load everthing back
		glUseProgram(self.shaderProgram)
		glBindVertexArray(self.vao)
		glBindBuffer(GL_ARRAY_BUFFER, self.vbo)
		
		# glDrawArrays( mode , first, count)
		glDrawArrays(GL_TRIANGLES, 0, 3)

		#clean things up
		glBindBuffer(GL_ARRAY_BUFFER, 0)
		glBindVertexArray(0)
		glUseProgram(0)
		
		glutSwapBuffers()  # necessario para windows!

	def reshape(self, width, height):
		glViewport(0, 0, width, height)

fr = Frame('PlayOGL')