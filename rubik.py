import glfw
from OpenGL.GL import *
import OpenGL.GL.shaders as gls
from OpenGL.GLU import *

if not glfw.init():
    raise Exception("Falha ao inicializar GLFW")

width, height = 1000, 800
zoom_factor = 1.0
zoom_sensitivity = 0.05

#GPT cantou aqui, mas gera um cubo basico
vertices = [
    (-1, -1, -1),  # Vértice 0
    ( 1, -1, -1),  # Vértice 1
    ( 1,  1, -1),  # Vértice 2
    (-1,  1, -1),  # Vértice 3
    (-1, -1,  1),  # Vértice 4
    ( 1, -1,  1),  # Vértice 5
    ( 1,  1,  1),  # Vértice 6
    (-1,  1,  1)   # Vértice 7
]

faces = [
    (4, 5, 6, 7),  # Face frontal
    (0, 1, 2, 3),  # Face traseira
    (3, 2, 6, 7),  # Face superior
    (0, 1, 5, 4),  # Face inferior
    (0, 3, 7, 4),  # Face esquerda
    (1, 2, 6, 5)   # Face direita
]

colors = ((1, 0, 0), (0, 1, 0), (1, 0.5, 0), (1, 1, 0), (1, 1, 1), (0, 0, 1))

cubes = []

def key_callback(window, key, scancode, action, mods):
    global rotCubeIn
    if action == glfw.PRESS:
        if key == glfw.KEY_LEFT:
            rotCubeIn = (0, -1)
        elif key == glfw.KEY_RIGHT:
            rotCubeIn = (0, 1)
        elif key == glfw.KEY_UP:
            rotCubeIn = (-1, 0)
        elif key == glfw.KEY_DOWN:
            rotCubeIn = (1, 0)
    elif action == glfw.RELEASE:
        rotCubeIn = (0, 0)

window = glfw.create_window(width, height, "Rubik cube", None, None)

if not window:
    glfw.terminate()
    raise Exception("Falha ao criar a window GLFW")

def scroll_callback(window, xoffset, yoffset):
    global zoom_factor
    
    if yoffset > 0:
        zoom_factor *= (1.0 + zoom_sensitivity)  
    else:
        zoom_factor *= (1.0 - zoom_sensitivity) 
        
    zoom_factor = max(0.1, min(zoom_factor, 5.0))

glfw.make_context_current(window)
glfw.set_key_callback(window, key_callback)
glfw.set_scroll_callback(window, scroll_callback)

identityMatrix = [[1 if i==j else 0 for i in range(3)] for j in range(3)]
rotCubeIn = (0,0)

def init():
    glClearColor(0,0,0,1)
    glEnable(GL_DEPTH_TEST) 

    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluPerspective(45, (width/height), 0.1, 50.0)
    glMatrixMode(GL_MODELVIEW)

    glLineWidth(8)

    for i in range(3):
        for j in range(3):
            for k in range(3):
                cubes.append([i,j,k])

def transformMat(coord):
    translationArr = []

    #ajusta o lugar do cubinho dentro do cubo magico
    for comp in coord:
        translationArr.append((comp-2/2)*2.05) 

    matrixTransformationMatricesNeeded = [identityMatrix[0], identityMatrix[1], identityMatrix[2], translationArr]
    matrixTransformation = []

    # [ r1 r2 r3 0]
    # [ r1 r2 r3 0]  rotação por hora é 0
    # [ r1 r2 r3 0]
    # [ t1 t2 t3 1]
    for i in range(len(matrixTransformationMatricesNeeded)):
        matrix = matrixTransformationMatricesNeeded[i]

        for j in range(3):
            matrixTransformation.append(matrix[j])
        
        if i < 3:
            matrixTransformation.append(0)
        else:
            matrixTransformation.append(1)

    return matrixTransformation

def drawCube(cube):
    glPushMatrix()

    glMultMatrixf(transformMat(cube))
    
    glPolygonMode(GL_FRONT_AND_BACK, GL_FILL)
    glBegin(GL_QUADS)
    for i in range(len(faces)):
        glColor3fv(colors[i])
        for vertexIdx in faces[i]:
            glVertex3fv(vertices[vertexIdx])
    glEnd()

    glPolygonMode(GL_FRONT_AND_BACK, GL_LINE)
    glBegin(GL_QUADS)
    for i in range(len(faces)):
        glColor3f(0,0,0)
        for vertexIdx in faces[i]:
            glVertex3fv(vertices[vertexIdx])
    glEnd()

    glPopMatrix()

def render():
    init()

    anglX = 0
    anglY = 0

    while not glfw.window_should_close(window):
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

        glLoadIdentity()
        gluLookAt(8, 5, 18,  # Posição da câmera
                0, 0, 0,  # Para onde a câmera olha
                0, 1, 0)  # Vetor "up" (para cima)
        
        anglX += rotCubeIn[0]*2
        anglY += rotCubeIn[1]*2

        glRotatef(anglY, 0, 1, 0)
        glRotatef(anglX, 1, 0, 0)

        glScalef(zoom_factor, zoom_factor, zoom_factor)
        
        for cube in cubes:
            drawCube(cube)

        glfw.swap_buffers(window)
        glfw.poll_events()

    
    glfw.terminate()

render()