"""
glfw_cube06.py
Author: dalong10
Description: Draw 4 Cube, learning OPENGL 
"""
import common.glutils as glutils   #Common OpenGL utilities,see glutils.py
import sys, random, math
import OpenGL
from OpenGL.GL import *
from OpenGL.GL.shaders import *
import numpy 
import numpy as np
import glfw

strVS = """
#version 330 core
layout(location = 0) in vec3 position;
layout (location = 1) in vec2 inTexcoord;
out vec2 outTexcoord;
uniform mat4 uMVMatrix;
uniform mat4 uPMatrix;
uniform float a;
uniform float b;
uniform float c;
uniform float scale;
uniform float theta;

void main(){
	mat4 rot1=mat4(vec4(1.0, 0.0,0.0,0),
				vec4(0.0, 1.0,0.0,0),
				vec4(0.0,0.0,1.0,0.0),
				vec4(a,b,c,1.0));
	mat4 rot2=mat4(vec4(scale, 0.0,0.0,0.0),
					vec4(0.0, scale,0.0,0.0),
					vec4(0.0,0.0,scale,0.0),
					vec4(0.0,0.0,0.0,1.0));
	mat4 rot3=mat4( vec4(0.5+0.5*cos(theta),  0.5-0.5*cos(theta), -0.707106781*sin(theta), 0),
				   vec4(0.5-0.5*cos(theta),0.5+0.5*cos(theta), 0.707106781*sin(theta),0),
				vec4(0.707106781*sin(theta), -0.707106781*sin(theta),cos(theta), 0.0),
				vec4(0.0,         0.0,0.0, 1.0));
	gl_Position=uPMatrix * uMVMatrix * rot2 *rot1 *rot3 * vec4(position.x, position.y, position.z, 1.0);
    outTexcoord = inTexcoord;
	}
"""

strFS = """
#version 330 core
out vec4 FragColor;
in vec2 outTexcoord;
uniform sampler2D texture1;
void main(){
    FragColor = texture(texture1, outTexcoord);
	}
"""

class FirstCube:
    def __init__(self, side):
        self.side = side

        # load shaders
        self.program = glutils.loadShaders(strVS, strFS)
        glUseProgram(self.program)
        # attributes
        self.vertIndex = glGetAttribLocation(self.program, b"position")
        self.texIndex = glGetAttribLocation(self.program, b"inTexcoord")
        
        s = side/2.0
        cube_vertices = [
            -s, -s, -s, 
             s, -s, -s,
             s, s, -s,
             s, s, -s,
             -s, s, -s,
             -s, -s, -s,
             
             -s, -s, s, 
             s, -s, s,
             s, s, s,
             s, s, s,
             -s, s, s,
             -s, -s, s,

             -s, s, s, 
             -s, s, -s,
             -s, -s, -s,
             -s, -s, -s,
             -s, -s, s,
             -s, s, s,

             s, s, s, 
             s, s, -s,
             s, -s, -s,
             s, -s, -s,
             s, -s, s,
             s, s, s,

             -s, -s, -s, 
             s, -s, -s,
             s, -s, s,
             s, -s, s,
             -s, -s, s,
             -s, -s, -s,

             -s, s, -s, 
             s, s,-s,
             s, s, s,
             s, s, s,
             -s, s, s,
             -s, s,-s
             ]
        # texture coords
        t=1.0
        quadT = [
            0,0, t,0, t,t, t,t, 0,t, 0,0, 
            0,0, t,0, t,t, t,t, 0,t, 0,0, 
            t,0, t,t, 0,t, 0,t, 0,0, t,0, 
            t,0, t,t, 0,t, 0,t, 0,0, t,0,  
            0,t, t,t, t,0, t,0, 0,0, 0,t, 
            0,t, t,t, t,0, t,0, 0,0, 0,t
            ]               
        # set up vertex array object (VAO)
        self.vao = glGenVertexArrays(1)
        glBindVertexArray(self.vao)
            
        # set up VBOs
        vertexData = numpy.array(cube_vertices, numpy.float32)
        self.vertexBuffer = glGenBuffers(1)
        glBindBuffer(GL_ARRAY_BUFFER, self.vertexBuffer)
        glBufferData(GL_ARRAY_BUFFER, 4*len(vertexData), vertexData, GL_STATIC_DRAW)
        
        tcData = numpy.array(quadT, numpy.float32)
        self.tcBuffer = glGenBuffers(1)
        glBindBuffer(GL_ARRAY_BUFFER, self.tcBuffer)
        glBufferData(GL_ARRAY_BUFFER, 4*len(tcData), tcData,GL_STATIC_DRAW)
        # enable arrays
        glEnableVertexAttribArray(self.vertIndex)
        glEnableVertexAttribArray(self.texIndex)
        # Position attribute
        glBindBuffer(GL_ARRAY_BUFFER, self.vertexBuffer)
        glVertexAttribPointer(self.vertIndex, 3, GL_FLOAT, GL_FALSE, 0,None)
        
        # TexCoord attribute
        glBindBuffer(GL_ARRAY_BUFFER, self.tcBuffer)        
        glVertexAttribPointer(self.texIndex, 2, GL_FLOAT, GL_FALSE, 0,None)
        
        # unbind VAO
        glBindVertexArray(0)
        glBindBuffer(GL_ARRAY_BUFFER, 0)    

    def render(self,pMatrix,mvMatrix,texid,a,b,c,scale,r):       
        self.texid = texid
        # enable texture
        glActiveTexture(GL_TEXTURE0)
        glBindTexture(GL_TEXTURE_2D, self.texid)
        # use shader
        # set proj matrix
        glUniformMatrix4fv(glGetUniformLocation(self.program, 'uPMatrix'), 
                          1, GL_FALSE, pMatrix)       
        # set modelview matrix
        glUniformMatrix4fv(glGetUniformLocation(self.program, 'uMVMatrix'), 
                          1, GL_FALSE, mvMatrix)
        glUseProgram(self.program)
        glUniform1f(glGetUniformLocation(self.program, "a"), a)
        glUniform1f(glGetUniformLocation(self.program, "b"), b)
        glUniform1f(glGetUniformLocation(self.program, "c"), c)
        glUniform1f(glGetUniformLocation(self.program, "scale"), scale)
        theta = r*PI/180.0
        glUniform1f(glGetUniformLocation(self.program, "theta"), theta)
        # bind VAO
        glBindVertexArray(self.vao)
        glEnable(GL_DEPTH_TEST)
        # draw
        glDrawArrays(GL_TRIANGLES, 0, 36)
        # unbind VAO
        glBindVertexArray(0)

#Is called whenever a key is pressed/released via GLFW
def on_key(window, key, scancode, action, mods):
    if key == glfw.KEY_ESCAPE and action == glfw.PRESS:
        glfw.set_window_should_close(window,1)
    elif key >0  and key<1024 :
        if action == glfw.PRESS:
            keys[key]=True
        elif (action == glfw.RELEASE):
            keys[key]=False 

def do_movement():
    global cameraPos
    global cameraFront
    global cameraUp
    global deltaTime
    
    #Camera controls
    cameraSpeed = 5.0 * deltaTime
    if (keys[glfw.KEY_W]):
        cameraPos += cameraSpeed * cameraFront
        print(cameraPos)
    if (keys[glfw.KEY_S]):
        cameraPos -= cameraSpeed * cameraFront
    if (keys[glfw.KEY_A]):
        # normalize up vector
        norm = numpy.linalg.norm(cameraFront)
        cameraFront /= norm
        norm = np.linalg.norm(cameraUp)
        cameraUp /= norm
        # Side = forward x up 
        side = np.cross(cameraFront, cameraUp)
        cameraPos -= cameraSpeed * side
    if (keys[glfw.KEY_D]):
        # normalize up vector
        norm = numpy.linalg.norm(cameraFront)
        cameraFront /= norm
        norm = np.linalg.norm(cameraUp)
        cameraUp /= norm
        # Side = forward x up 
        side = np.cross(cameraFront, cameraUp)
        cameraPos += cameraSpeed * side
        
def mouse_callback(window, xpos, ypos):
    global cameraFront
    global firstMouse
    global lastX
    global lastY
    global yaw
    global pitch
    #print('mouse button: ', window, xpos, ypos)
    if (firstMouse==True):
        lastX = xpos
        lastY = ypos
        firstMouse = False
    xoffset = xpos - lastX
    yoffset = lastY - ypos
    lastX = xpos
    lastY = ypos
    #camera.ProcessMouseMovement(xoffset, yoffset)
    sensitivity = 0.05
    xoffset *= sensitivity
    yoffset *= sensitivity
    yaw   += xoffset
    pitch += yoffset
    if(pitch > 89.0):
        pitch = 89.0
    if(pitch < -89.0):
        pitch = -89.0
    cameraFront=[math.cos(math.radians(yaw)) * math.cos(math.radians(pitch)),
                math.sin(math.radians(pitch)),
                math.sin(math.radians(yaw))* math.cos(math.radians(pitch)) ]    
    norm = numpy.linalg.norm(cameraFront)
    cameraFront /= norm
    
def scroll_callback(window, xoffset, yoffset):
    global aspect
    if(aspect >= 1.0 and aspect <= 45.0):
        aspect -= yoffset
    if(aspect <= 1.0):
        aspect=1.0
    if(aspect >= 45.0):
        aspect=45.0
    print('aspect=',aspect)

if __name__ == '__main__':
    import sys
    import glfw
    import OpenGL.GL as gl
    global cameraPos
    global cameraFront
    global cameraUp
    global deltaTime
    global firstMouse
    global lastX
    global lastY
    global yaw
    global pitch
    global aspect
    
    keys=numpy.zeros(1024)
    deltaTime = 0.0
    lastFrame = 0.0   # Time of last frame
    firstMouse = True
    lastX= 400
    lastY = 300
    yaw   = -90.0
    pitch =   0.0
    aspect=45.0
    
    camera = glutils.Camera([0.0, 0.0, 5.0],
                             [0.0, 0.0, 0.0],
                             [0.0, 1.0, 0.0])
    cameraPos  =numpy.array([0,0,3.0], numpy.float32)                        
    cameraFront=numpy.array([0,0,-1.0], numpy.float32)        
    cameraUp   =numpy.array([0,1.0,0], numpy.float32)        
            

    # Initialize the library
    if not glfw.init():
        sys.exit()

    # Create a windowed mode window and its OpenGL context
    window = glfw.create_window(800, 600, "draw Cube ", None, None)
    if not window:
        glfw.terminate()
        sys.exit()

    # Make the window's context current
    glfw.make_context_current(window)
    # Install a key handler
    glfw.set_key_callback(window, on_key)
    # set window  mouse callbacks
    glfw.set_cursor_pos_callback(window,  mouse_callback)
    glfw.set_scroll_callback(window,  scroll_callback)
    
    PI = 3.14159265358979323846264
    texid = glutils.loadTexture("container2.png")
    # Loop until the user closes the window
    a=0
    firstCube0 = FirstCube(1.0)
    while not glfw.window_should_close(window):
        currentFrame = glfw.get_time()
        deltaTime = currentFrame - lastFrame       
        lastFrame = currentFrame
        glfw.poll_events()
        do_movement()
        # Render here
        width, height = glfw.get_framebuffer_size(window)
        ratio = width / float(height)
        gl.glViewport(0, 0, width, height)
        gl.glClear(gl.GL_COLOR_BUFFER_BIT | gl.GL_DEPTH_BUFFER_BIT)
        gl.glMatrixMode(gl.GL_PROJECTION)
        gl.glLoadIdentity()
        gl.glOrtho(-ratio, ratio, -1, 1, 1, -1)
        gl.glMatrixMode(gl.GL_MODELVIEW)
        gl.glLoadIdentity()
        gl.glClearColor(0.0,0.0,4.0,0.0)                
        i=a 
        camera.eye=[5*math.sin(glfw.get_time()), 0 , 5* math.cos(glfw.get_time()) ]
        # modelview matrix
        mvMatrix = glutils.lookAt(cameraPos, cameraPos+cameraFront, cameraUp)
        pMatrix = glutils.perspective(aspect, ratio, 0.1, 100.0)
        glBindTexture(GL_TEXTURE_2D, texid)              
        firstCube0.render(pMatrix, mvMatrix,texid,0.0,1,0,0.4,i)
        firstCube0.render(pMatrix, mvMatrix,texid,1.0,0,0.4,0.5,i+30)
        firstCube0.render(pMatrix, mvMatrix,texid,0.0,-1,-0.5,0.3,i+60)
        firstCube0.render(pMatrix, mvMatrix,texid,-1.0,0,0.2,0.2,i+120)
                 
        # Swap front and back buffers
        glfw.swap_buffers(window)       
        # Poll for and process events
        glfw.poll_events()

    glfw.terminate()
