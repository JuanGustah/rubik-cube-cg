import glfw
from OpenGL.GL import *
import OpenGL.GL.shaders as gls
from OpenGL.GLU import *
from rubik_state import State

if not glfw.init():
    raise Exception("Falha ao inicializar GLFW")

# variaveis globais 
width, height = 1000, 800
zoom_factor = 1.0
zoom_sensitivity = 0.05
CUBE_SIZE = 3
cube_state = State(CUBE_SIZE)

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

colors = (
    (0.0, 0.0, 1.0),     # 0: Azul (face frontal)
    (0.0, 1.0, 0.0),     # 1: Verde (face traseira)
    (1.0, 1.0, 1.0),     # 2: Branco (face superior)
    (1.0, 1.0, 0.0),     # 3: Amarelo (face inferior)
    (1.0, 0.5, 0.0),     # 4: Laranja (face esquerda)
    (1.0, 0.0, 0.0)      # 5: Vermelho (face direita)
)

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
        # gira a face frontal
        elif key == glfw.KEY_F:
            if mods & glfw.MOD_SHIFT:
                    cube_state.front_clock()
            else:
                    cube_state.front_anticlock()
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
    x, y, z = cube
    
    is_front = (z == CUBE_SIZE - 1)
    is_back = (z == 0)
    is_top = (y == CUBE_SIZE - 1)
    is_bottom = (y == 0)
    is_left = (x == 0)
    is_right = (x == CUBE_SIZE - 1)
    
    glPushMatrix()
    glMultMatrixf(transformMat(cube))
    
    glPolygonMode(GL_FRONT_AND_BACK, GL_FILL)
    glBegin(GL_QUADS)
    for i in range(len(faces)):
        if i == 0 and is_front:  # Face frontal
            color_index = cube_state.faces[0, y, x]
        elif i == 1 and is_back:  # Face traseira
            color_index = cube_state.faces[1, y, CUBE_SIZE-1-x]
        elif i == 2 and is_top:  # Face superior
            color_index = cube_state.faces[2, CUBE_SIZE-1-z, x]
        elif i == 3 and is_bottom:  # Face inferior
            color_index = cube_state.faces[3, z, x]
        elif i == 4 and is_left:  # Face esquerda
            color_index = cube_state.faces[4, y, CUBE_SIZE-1-z]
        elif i == 5 and is_right:  # Face direita
            color_index = cube_state.faces[5, y, z]
        else:
            color_index = i  
        
        glColor3fv(colors[color_index])
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
        gluLookAt(8, 5, -18,  # Posição da câmera
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