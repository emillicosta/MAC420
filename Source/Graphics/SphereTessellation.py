import math
import numpy as np
from OpenGL import GL
from Source.Graphics.Actor import Actor

class SphereTessellation(Actor):

    ## initialization
    def __init__(self, renderer,  **kwargs):
        """Initialize actor."""
        super(SphereTessellation, self).__init__(renderer, **kwargs)

        self._level = kwargs.get("level", 30)
        self._radius = kwargs.get("radius", 1.0)
        self._rgb_colors = kwargs.get("colors", False)

        ## register shaders
        if self._rgb_colors:
            self.setSolidShader(self.shaderCollection.attributeColorPhongShader())
            self.setSolidFlatShader(self.shaderCollection.attributeColorPhongFlatShader())
            self.setNoLightSolidShader(self.shaderCollection.attributeColorShader())
            self.setWireframeShader(self.shaderCollection.uniformMaterialShader())
        else:
            self.setSolidShader(self.shaderCollection.uniformMaterialPhongShader())
            self.setSolidFlatShader(self.shaderCollection.uniformMaterialPhongFlatShader())
            self.setNoLightSolidShader(self.shaderCollection.uniformMaterialShader())
            self.setWireframeShader(self.shaderCollection.uniformMaterialPhongShader())

        #self.shaderProgram_.setUniformValue("innerSubdivisionLevel", self._level)
        #self.shaderProgram_.setUniformValue("outerSubdivisionLevel", self._level)
        self._vertices = None

        ## create actor
        self.initialize()


    def addVertex(self, v, vertices):
        """Add a vertex into the array"""
        vn = v / np.linalg.norm(v) * self._radius
        vertices += [[vn[0], vn[1], vn[2]]]
        return len(vertices)-1


    def generateGeometry(self):
        """Generate vertices"""
        vertices = []
        indices = []
        middlePointIndexCache = dict()

        t = (1.0 + math.sqrt(5.0)) / 2.0

        self.addVertex(np.array((-1.0,  t,  0)), vertices)
        self.addVertex(np.array(( 1.0,  t,  0)), vertices)
        self.addVertex(np.array((-1.0, -t,  0)), vertices)
        self.addVertex(np.array(( 1.0, -t,  0)), vertices)

        self.addVertex(np.array(( 0, -1.0,  t)), vertices)
        self.addVertex(np.array(( 0,  1.0,  t)), vertices)
        self.addVertex(np.array(( 0, -1.0, -t)), vertices)
        self.addVertex(np.array(( 0,  1.0, -t)), vertices)

        self.addVertex(np.array(( t,  0, -1.0)), vertices)
        self.addVertex(np.array(( t,  0,  1.0)), vertices)
        self.addVertex(np.array((-t,  0, -1.0)), vertices)
        self.addVertex(np.array((-t,  0,  1.0)), vertices)

        ## 5 faces around point 0
        indices += [[0, 11, 5]]
        indices += [[0, 11, 5]]
        indices += [[0, 5, 1]]
        indices += [[0, 1, 7]]
        indices += [[0, 7, 10]]
        indices += [[0, 10, 11]]

        ## 5 adjacent faces 
        indices += [[1, 5, 9]]
        indices += [[5, 11, 4]]
        indices += [[11, 10, 2]]
        indices += [[10, 7, 6]]
        indices += [[7, 1, 8]]

        ## 5 faces around point 3
        indices += [[3, 9, 4]]
        indices += [[3, 4, 2]]
        indices += [[3, 2, 6]]
        indices += [[3, 6, 8]]
        indices += [[3, 8, 9]]

        ## 5 adjacent faces 
        indices += [[4, 9, 5]]
        indices += [[2, 4, 11]]
        indices += [[6, 2, 10]]
        indices += [[8, 6, 7]]
        indices += [[9, 8, 1]]

        
        self._vertices = np.array(vertices, dtype=np.float32)
        if self._rgb_colors:
            self._colors = np.abs(np.array(vertices, dtype=np.float32))
        self._normals = np.array(vertices, dtype=np.float32)
        self._indices = np.array(indices, dtype=np.uint32)


    def initialize(self):
        """Creates SphereTessellation geometry"""
        if self._vertices is None:
            self.generateGeometry()

        ## create object
        self.create(self._vertices, colors=self._colors if self._rgb_colors else None,
            normals=self._normals,
            indices=self._indices)
            

    def render(self):
        """Render SphereTessellation"""
        GL.glDrawElements(self._render_mode, self.numberOfIndices, GL.GL_UNSIGNED_INT, None)

    