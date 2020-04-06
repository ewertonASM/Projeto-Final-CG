from OpenGLContext import testingcontext
BaseContext = testingcontext.getInteractive()
from OpenGL.GL import *
from OpenGL.arrays import vbo
from OpenGLContext.arrays import *
from OpenGL.GL import shaders
from OpenGLContext.scenegraph.basenodes import Sphere
class TestContext( BaseContext ):
    """Demonstrates use of attribute types in GLSL
    """
    LIGHT_COUNT = 3
    LIGHT_SIZE = 5
    def OnInit( self ):
        """Initialize the context"""