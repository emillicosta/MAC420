from PyQt5.QtGui import QMatrix4x4, QVector3D, QVector4D

from OpenGL import GL
from Source.Graphics.Actor import Actor
from Source.Graphics.Group import Group
from Source.Graphics.Material import Material
from Source.Graphics.Cone import Cone
from Source.Graphics.Cube import Cube
from Source.Graphics.Cylinder import Cylinder
from Source.Graphics.Icosahedron import Icosahedron
from Source.Graphics.Gizmos import Gizmos

##  The orientation marker
class GizmosTranslate(Group):

    ## initialization
    def __init__(self, scene, **kwargs):
        """Initialize actor."""
        super(GizmosTranslate, self).__init__(scene, **kwargs)

        self._resolution = kwargs.get("resolution", 12)
        self._colorx = kwargs.get("xcolor", QVector3D(1.0, 0.0, 0.0))
        self._colory = kwargs.get("ycolor", QVector3D(0.0, 1.0, 0.0))
        self._colorz = kwargs.get("zcolor", QVector3D(0.0, 0.0, 1.0))
        self._transform = kwargs.get("transform", QMatrix4x4())
        self.size = kwargs.get("size", QVector3D(1.0,1.0,1.0))
        self.center = kwargs.get("center", QVector3D(0.0, 0.0, 0.0))
        self.eixo = kwargs.get("eixo", None)

        self.setPickable(False)
        self.setName("GizmosTranslate")

        if self.eixo in ("X", "x"):
            self._colorx = QVector3D(1.0, 0, 0)
            self._colory = QVector3D(0.5, 0.5, 0.5)
            self._colorz = QVector3D(0.5, 0.5, 0.5)
        elif self.eixo in ("Y", "y"):
            self._colory = QVector3D(0.0, 1.0, 0)
            self._colorx = QVector3D(0.5, 0.5, 0.5)
            self._colorz = QVector3D(0.5, 0.5, 0.5)
        elif self.eixo in ("z", "Z"):
            self._colorz = QVector3D(0.0, 0, 1.0)
            self._colory = QVector3D(0.5, 0.5, 0.5)
            self._colorx = QVector3D(0.5, 0.5, 0.5)
        else:
            self._colorx = QVector3D(1.0, 0, 0)
            self._colory = QVector3D(0.0, 1.0, 0)
            self._colorz = QVector3D(0.0, 0, 1.0)
       
        ## create lines
        xform = QMatrix4x4()
        xform.translate(self.center.x(), self.center.y(), self.center.z())
        xform.scale(self.size.x(), self.size.y(), self.size.z())
        transf = self._transform * xform
        self.addPart(Gizmos(self.scene, transform=transf, eixo=self.eixo))

        ## x axis cone
        xform = QMatrix4x4()
        xform.translate(self.center.x() + self.size.x(), self.center.y(), self.center.z())
        xform.scale(0.05, 0.05, 0.05)
        xform.scale(self.size.x(), self.size.y(), self.size.z())
        xform.rotate(-90.0, QVector3D(0.0, 0.0, 1.0))
        transf = self._transform * xform
        self.addPart(Cone(self.scene, name="xaxis", material=Material(diffuse=self._colorx, specular=QVector3D(0.5, 0.5, 0.5), 
            shininess=76.8), transform=transf))


        ## y axis cone
        xform = QMatrix4x4()
        xform.translate(self.center.x(), self.center.y() + self.size.y(), self.center.z())
        xform.scale(0.05, 0.05, 0.05)
        xform.scale(self.size.x(), self.size.y(), self.size.z())
        transf = self._transform * xform
        self.addPart(Cone(self.scene, name="yaxis", material=Material(diffuse=self._colory, specular=QVector3D(0.5, 0.5, 0.5), 
            shininess=76.8), transform=transf))

        ## z axis cone
        xform = QMatrix4x4()
        xform.translate(self.center.x(), self.center.y(), self.center.z() + self.size.z())
        xform.scale(0.05, 0.05, 0.05)
        xform.scale(self.size.x(), self.size.y(), self.size.z())
        xform.rotate(90.0, QVector3D(1.0, 0.0, 0.0))
        transf = self._transform * xform
        self.addPart(Cone(self.scene, name="zaxis", material=Material(diffuse=self._colorz, specular=QVector3D(0.5, 0.5, 0.5), 
            shininess=76.8), transform=transf))