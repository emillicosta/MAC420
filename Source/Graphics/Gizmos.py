import numpy as np
from PyQt5.QtGui import QVector3D

from OpenGL import GL
from Source.Graphics.Actor import Actor

class Gizmos(Actor):

    ## initialization
    def __init__(self, scene, **kwargs):
        """Initialize actor."""
        super(Gizmos, self).__init__(scene, type=Actor.RenderType.Overlay, **kwargs)

        self.size = kwargs.get("size", 1.0)
        self.center = kwargs.get("center", QVector3D(0.0, 0.0, 0.0))
        self.eixo = kwargs.get("eixo", None)

        ## register shaders
        self.setSolidShader(self.shaderCollection.attributeColorShader())
        self.setSolidFlatShader(self.shaderCollection.attributeColorShader())
        self.setNoLightSolidShader(self.shaderCollection.attributeColorShader())
        self.setWireframeShader(self.shaderCollection.attributeColorShader())
        self.setNoLightWireframeShader(self.shaderCollection.attributeColorShader())

        self._vertices = None

        ## create actor
        self.initialize()


    def generateGeometry(self):
        """Generate vertices"""
        self._vertices = np.array([
            self.center.x(), self.center.y(), self.center.z(),
            self.center.x() + self.size, self.center.y(), self.center.z(),
            self.center.x(), self.center.y(), self.center.z(),
            self.center.x(), self.center.y() + self.size, self.center.z(),
            self.center.x(), self.center.y(), self.center.z(),
            self.center.x(), self.center.y(), self.center.z() + self.size
        ], dtype=np.float32)
    
        if self.eixo in ("x", "X"):
            self._colors = np.array([
                1.0, 0.0, 0.0,
                1.0, 0.0, 0.0,
                0.5, 0.5, 0.5,
                0.5, 0.5, 0.5,
                0.5, 0.5, 0.5,
                0.5, 0.5, 0.5,
            ], dtype=np.float32)
        elif self.eixo in ("y", "Y"):
            self._colors = np.array([
                0.5, 0.5, 0.5,
                0.5, 0.5, 0.5,
                0.0, 1.0, 0.0,
                0.0, 1.0, 0.0,
                0.5, 0.5, 0.5,
                0.5, 0.5, 0.5,
            ], dtype=np.float32)
        elif self.eixo in ("z", "Z"):
            self._colors = np.array([
                0.5, 0.5, 0.5,
                0.5, 0.5, 0.5,
                0.5, 0.5, 0.5,
                0.5, 0.5, 0.5,
                0.0, 0.0, 1.0,
                0.0, 0.0, 1.0,
            ], dtype=np.float32)
        else:
            self._colors = np.array([
                1.0, 0.0, 0.0,
                1.0, 0.0, 0.0,
                0.0, 1.0, 0.0,
                0.0, 1.0, 0.0,
                0.0, 0.0, 1.0,
                0.0, 0.0, 1.0,
            ], dtype=np.float32)


    def initialize(self):
        """Creates Gizmos"""
        if self._vertices is None:
            self.generateGeometry()

        ## create object
        self.create(self._vertices, colors=self._colors)


    def render(self):
        """Render grid"""
        GL.glDrawArrays(GL.GL_LINES, 0, 6)



    