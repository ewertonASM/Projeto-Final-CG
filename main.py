import glfw
from OpenGL.GL import *
from OpenGL.GL.shaders import compileProgram, compileShader
import pyrr
from TextureLoader import load_texture
from ObjLoader import ObjLoader

from camera import Camera

cam = Camera()
WIDTH, HEIGHT = 1280, 720
lastX, lastY = WIDTH / 2, HEIGHT / 2
first_mouse = True
left, right, forward, backward = False, False, False, False


# Retorno de chamada do teclado
def key_input_clb(window, key, scancode, action, mode):
    global left, right, forward, backward
    if key == glfw.KEY_ESCAPE and action == glfw.PRESS:
        glfw.set_window_should_close(window, True)

    if key == glfw.KEY_W and action == glfw.PRESS:
        forward = True
    elif key == glfw.KEY_W and action == glfw.RELEASE:
        forward = False
    if key == glfw.KEY_S and action == glfw.PRESS:
        backward = True
    elif key == glfw.KEY_S and action == glfw.RELEASE:
        backward = False
    if key == glfw.KEY_A and action == glfw.PRESS:
        left = True
    elif key == glfw.KEY_A and action == glfw.RELEASE:
        left = False
    if key == glfw.KEY_D and action == glfw.PRESS:
        right = True
    elif key == glfw.KEY_D and action == glfw.RELEASE:
        right = False

# Função de movimento 
def do_movement():
    if left:
        cam.process_keyboard("LEFT", 0.1)
    if right:
        cam.process_keyboard("RIGHT", 0.1)
    if forward:
        cam.process_keyboard("FORWARD", 0.1)
    if backward:
        cam.process_keyboard("BACKWARD", 0.1)


# Função de retorno de chamada na posição do mouse
def mouse_look_clb(window, xpos, ypos):
    global first_mouse, lastX, lastY

    if first_mouse:
        lastX = xpos
        lastY = ypos
        first_mouse = False

    xoffset = xpos - lastX
    yoffset = lastY - ypos

    lastX = xpos
    lastY = ypos

    cam.process_mouse_movement(xoffset, yoffset)


vertex_src = """
# version 330

layout(location = 0) in vec3 a_position;
layout(location = 1) in vec2 a_texture;
layout(location = 2) in vec3 a_normal;

uniform mat4 model;
uniform mat4 projection;
uniform mat4 view;

out vec2 v_texture;

void main()
{
    gl_Position = projection * view * model * vec4(a_position, 1.0);
    v_texture = a_texture;
}
"""

fragment_src = """
# version 330

in vec2 v_texture;

out vec4 out_color;

uniform sampler2D s_texture;

void main()
{
    out_color = texture(s_texture, v_texture);
}
"""


# Janela redimensiona a função de retorno de chamada
def window_resize_clb(window, width, height):
    glViewport(0, 0, width, height)
    projection = pyrr.matrix44.create_perspective_projection_matrix(45, width / height, 0.1, 100)
    glUniformMatrix4fv(proj_loc, 1, GL_FALSE, projection)


# iniciando biblioteca glfw
if not glfw.init():
    raise Exception("glfw can not be initialized!")

# criando janela
window = glfw.create_window(WIDTH, HEIGHT, "My OpenGL window", None, None)

# checando se janela foi criada
if not window:
    glfw.terminate()
    raise Exception("glfw window can not be created!")

# definindo posição da janela
glfw.set_window_pos(window, 400, 200)

# definindo a função de retorno de chamada para redimensionar a janela
glfw.set_window_size_callback(window, window_resize_clb)
# definindo o retorno de chamada da posição do mouse
glfw.set_cursor_pos_callback(window, mouse_look_clb)
# definindo o retorno de chamada da entrada do teclado
glfw.set_key_callback(window, key_input_clb)
# capturar o cursor do mouse
glfw.set_input_mode(window, glfw.CURSOR, glfw.CURSOR_DISABLED)


glfw.make_context_current(window)

# Carregando objetos 3d
walled_indices, walled_buffer = ObjLoader.load_model("meshes/wooden-wall3.obj")
trees_indices, trees_buffer = ObjLoader.load_model("meshes/outono.obj")
tower_indices, tower_buffer = ObjLoader.load_model("meshes/wallcastle2.obj")
floor_indices, floor_buffer = ObjLoader.load_model("meshes/floor.obj")

shader = compileProgram(compileShader(vertex_src, GL_VERTEX_SHADER), compileShader(fragment_src, GL_FRAGMENT_SHADER))

# VAO e VBO
VAO = glGenVertexArrays(4)
VBO = glGenBuffers(4)


# walled VAO
glBindVertexArray(VAO[0])
# walled Vertex Buffer Object
glBindBuffer(GL_ARRAY_BUFFER, VBO[0])
glBufferData(GL_ARRAY_BUFFER, walled_buffer.nbytes, walled_buffer, GL_STATIC_DRAW)

# walled vertices
glEnableVertexAttribArray(0)
glVertexAttribPointer(0, 3, GL_FLOAT, GL_FALSE, walled_buffer.itemsize * 8, ctypes.c_void_p(0))
# walled textures
glEnableVertexAttribArray(1)
glVertexAttribPointer(1, 2, GL_FLOAT, GL_FALSE, walled_buffer.itemsize * 8, ctypes.c_void_p(12))
# walled normals
glVertexAttribPointer(2, 3, GL_FLOAT, GL_FALSE, walled_buffer.itemsize * 8, ctypes.c_void_p(20))
glEnableVertexAttribArray(2)

# trees VAO
glBindVertexArray(VAO[1])
# trees Vertex Buffer Object
glBindBuffer(GL_ARRAY_BUFFER, VBO[1])
glBufferData(GL_ARRAY_BUFFER, trees_buffer.nbytes, trees_buffer, GL_STATIC_DRAW)

# trees vertices
glEnableVertexAttribArray(0)
glVertexAttribPointer(0, 3, GL_FLOAT, GL_FALSE, trees_buffer.itemsize * 8, ctypes.c_void_p(0))
# trees textures
glEnableVertexAttribArray(1)
glVertexAttribPointer(1, 2, GL_FLOAT, GL_FALSE, trees_buffer.itemsize * 8, ctypes.c_void_p(12))
# trees normals
glVertexAttribPointer(2, 3, GL_FLOAT, GL_FALSE, trees_buffer.itemsize * 8, ctypes.c_void_p(20))
glEnableVertexAttribArray(2)

# floor VAO
glBindVertexArray(VAO[2])
# floor Vertex Buffer Object
glBindBuffer(GL_ARRAY_BUFFER, VBO[2])
glBufferData(GL_ARRAY_BUFFER, floor_buffer.nbytes, floor_buffer, GL_STATIC_DRAW)

# floor vertices
glEnableVertexAttribArray(0)
glVertexAttribPointer(0, 3, GL_FLOAT, GL_FALSE, floor_buffer.itemsize * 8, ctypes.c_void_p(0))
# floor textures
glEnableVertexAttribArray(1)
glVertexAttribPointer(1, 2, GL_FLOAT, GL_FALSE, floor_buffer.itemsize * 8, ctypes.c_void_p(12))
# floor normals
glVertexAttribPointer(2, 3, GL_FLOAT, GL_FALSE, floor_buffer.itemsize * 8, ctypes.c_void_p(20))
glEnableVertexAttribArray(2)

# tower VAO
glBindVertexArray(VAO[3])
# tower Vertex Buffer Object
glBindBuffer(GL_ARRAY_BUFFER, VBO[3])
glBufferData(GL_ARRAY_BUFFER, tower_buffer.nbytes, tower_buffer, GL_STATIC_DRAW)

# tower vertices
glEnableVertexAttribArray(0)
glVertexAttribPointer(0, 3, GL_FLOAT, GL_FALSE, tower_buffer.itemsize * 8, ctypes.c_void_p(0))
# tower textures
glEnableVertexAttribArray(1)
glVertexAttribPointer(1, 2, GL_FLOAT, GL_FALSE, tower_buffer.itemsize * 8, ctypes.c_void_p(12))
# tower normals
glVertexAttribPointer(2, 3, GL_FLOAT, GL_FALSE, tower_buffer.itemsize * 8, ctypes.c_void_p(20))
glEnableVertexAttribArray(2)




textures = glGenTextures(4)
load_texture("meshes/outono.jpg", textures[0])
load_texture("meshes/outono.jpg", textures[1])
load_texture("meshes/solo.jpg", textures[2])
load_texture("meshes/towertex.jpg", textures[3])

glUseProgram(shader)
glClearColor(0, 0.1, 0.1, 1)
glEnable(GL_DEPTH_TEST)
glEnable(GL_BLEND)
glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)

projection = pyrr.matrix44.create_perspective_projection_matrix(45, WIDTH / HEIGHT, 0.1, 100)
walled_pos = pyrr.matrix44.create_from_translation(pyrr.Vector3([0, 0, 0]))
trees_pos = pyrr.matrix44.create_from_translation(pyrr.Vector3([0, 0, 0]))
floor_pos = pyrr.matrix44.create_from_translation(pyrr.Vector3([0, 0, 0]))
tower_pos = pyrr.matrix44.create_from_translation(pyrr.Vector3([0, 0, 0]))

model_loc = glGetUniformLocation(shader, "model")
proj_loc = glGetUniformLocation(shader, "projection")
view_loc = glGetUniformLocation(shader, "view")

glUniformMatrix4fv(proj_loc, 1, GL_FALSE, projection)



while not glfw.window_should_close(window):
    glfw.poll_events()
    do_movement()

    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

    view = cam.get_view_matrix()
    glUniformMatrix4fv(view_loc, 1, GL_FALSE, view)

    glBindVertexArray(VAO[0])
    glBindTexture(GL_TEXTURE_2D, textures[0])
    glUniformMatrix4fv(model_loc, 1, GL_FALSE, trees_pos)
    glDrawArrays(GL_TRIANGLES, 0, len(trees_indices))

    glBindVertexArray(VAO[1])
    glBindTexture(GL_TEXTURE_2D, textures[1])
    glUniformMatrix4fv(model_loc, 1, GL_FALSE, trees_pos)
    glDrawArrays(GL_TRIANGLES, 0, len(trees_indices))

    # draw the trees
    glBindVertexArray(VAO[3])
    glBindTexture(GL_TEXTURE_2D, textures[3])
    glUniformMatrix4fv(model_loc, 1, GL_FALSE, tower_pos)
    glDrawArrays(GL_TRIANGLES, 0, len(tower_indices))


    # draw the floor
    glBindVertexArray(VAO[2])
    glBindTexture(GL_TEXTURE_2D, textures[2])
    glUniformMatrix4fv(model_loc, 1, GL_FALSE, floor_pos)
    glDrawArrays(GL_TRIANGLES, 0, len(floor_indices))

    glfw.swap_buffers(window)



# terminate glfw, free up allocated resources
glfw.terminate()
