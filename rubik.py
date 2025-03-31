import glfw
from OpenGL.GL import *
import OpenGL.GL.shaders as gls
from OpenGL.GLU import *
from rubik_state import State

if not glfw.init():
    raise Exception("Falha ao inicializar GLFW")

# Variáveis globais
width, height = 1000, 800
zoom_factor = 1.0
zoom_sensitivity = 0.05
CUBE_SIZE = 3
cube_state = State(CUBE_SIZE)

cubes = []

def read_off(file_path):
    with open(file_path, 'r') as file:
        lines = file.readlines()
    
    assert lines[0].strip() == "OFF", "Formato inválido"
    
    num_vertices, num_faces, _ = map(int, lines[1].split())
    
    vertices = [tuple(map(float, line.split())) for line in lines[2:2+num_vertices]]
    faces = []
    colors = []
    
    for line in lines[2+num_vertices:2+num_vertices+num_faces]:
        data = list(map(float, line.split()))
        faces.append(tuple(map(int, data[1:5])))
        colors.append(tuple(data[5:]))  
    
    return vertices, faces, colors

vertices, faces, colors = read_off('rubik.off')

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
        elif key == glfw.KEY_W:
            if mods & glfw.MOD_SHIFT:
                cube_state.up_anticlock()
            else:
                cube_state.up_clock()
        elif key == glfw.KEY_S:
            if mods & glfw.MOD_SHIFT:
                cube_state.down_anticlock()
            else:
                cube_state.down_clock()
        elif key == glfw.KEY_A:
            if mods & glfw.MOD_SHIFT:
                cube_state.left_anticlock()
            else:
                cube_state.left_clock()
        elif key == glfw.KEY_D:
            if mods & glfw.MOD_SHIFT:
                cube_state.right_anticlock()
            else:
                cube_state.right_clock()
        elif key == glfw.KEY_F:
            if mods & glfw.MOD_SHIFT:
                cube_state.front_anticlock()
            else:
                cube_state.front_clock()
        elif key == glfw.KEY_B:
            if mods & glfw.MOD_SHIFT:
                cube_state.back_anticlock()
            else:
                cube_state.back_clock()
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
    for comp in coord:
        translationArr.append((comp-2/2)*2.05) 

    matrixTransformationMatricesNeeded = [identityMatrix[0], identityMatrix[1], identityMatrix[2], translationArr]
    matrixTransformation = []

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
        if i == 0 and is_front:
            color_index = cube_state.faces[0, y, x]
        elif i == 1 and is_back:
            color_index = cube_state.faces[1, y, CUBE_SIZE-1-x]
        elif i == 2 and is_top:
            color_index = cube_state.faces[2, CUBE_SIZE-1-z, x]
        elif i == 3 and is_bottom:
            color_index = cube_state.faces[3, z, x]
        elif i == 4 and is_left:
            color_index = cube_state.faces[4, y, CUBE_SIZE-1-z]
        elif i == 5 and is_right:
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