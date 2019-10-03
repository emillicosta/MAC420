import math
import numpy as np
from OpenGL import GL
from Source.Graphics.Actor import Actor

class Sphere(Actor):

    ## initialization
    def __init__(self, renderer,  **kwargs):
        """Initialize actor."""
        super(Sphere, self).__init__(renderer, **kwargs)

        self._radius = kwargs.get("radius", 1.0)
        self._v = kwargs.get("v", 30)
        self._h = kwargs.get("h", 30)
        self._rgb_colors = kwargs.get("colors", False)

        self._hStep = 2 * math.pi / self._h
        self._vStep = math.pi / self._v;

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

        self._vertices = None

        ## create actor
        self.initialize()



    def generateGeometry(self):
        """Generate vertices"""
        vertices = []
        indices = []
        normals = []
        texture = []

        for i in range(self._v+1):
            
            theta = math.pi / 2 - i * self._vStep

            #indices
            if i != self._v:
                k1 = i * (self._h + 1)
                k2 = k1 + self._h + 1

            for j in range(self._h+1):
                phi = j * self._hStep

                x = self._radius * math.cos(theta) * math.sin(phi)
                y = self._radius * math.sin(theta)
                z = self._radius * math.cos(theta) * math.cos(phi)
                
                vertices.append([x, y, z])
                

                if i != self._v and j != self._h:
                    if i != 0:
                        indices.append([k1,k2,k1+1])
                    if i != self._v -1 :
                        indices.append([k1 + 1, k2, k2+1])
                    k1 = k1+1
                    k2 = k2+1
                
                #normais e coord de textura
                normal = [x/self._radius,y/self._radius,z/self._radius]
                normals.append(normal)
                s = j / self._h
                t = i / self._v
                texture.append([s, t])

        self._vertices = np.array(vertices, dtype=np.float32)
        if self._rgb_colors:
            self._colors = np.abs(np.array(vertices, dtype=np.float32))
        self._normals = np.array(normals, dtype=np.float32)
        self._indices = np.array(indices, dtype=np.uint32)
        self._texcoords = np.array(texture, dtype=np.uint32)


    def initialize(self):
        """Creates Sphere geometry"""
        if self._vertices is None:
            self.generateGeometry()

        ## create object
        self.create(self._vertices, colors=self._colors if self._rgb_colors else None,
            normals=self._normals,
            texcoords=self._texcoords,
            indices=self._indices)
            

    def render(self):
        """Render Sphere"""
        GL.glDrawElements(self._render_mode, self.numberOfIndices, GL.GL_UNSIGNED_INT, None)

    