import os
import math
import numpy as np
from PyQt5.QtGui import QVector3D

from OpenGL import GL
from Source.Graphics.Actor import Actor

def getMaterial(filename, mat):
    arq = open(filename + ".mtl", "r")
    kd = [0.5,0.5,0]
    mat_ = ""
    for line in arq:
        if line.startswith('#'):
            continue
        values = line.split()
        if not values:
            continue
        if values[0] == 'newmtl':
            mat_ = values[1]
        if values[0] == 'Kd' and mat_ == mat:
            kd = []
            for v in values[1:]:
                kd.append(float(v))
            
            return kd
    return kd

class Obj(Actor):

    ## initialization
    def __init__(self, scene,  **kwargs):
        """Initialize actor."""
        super(Obj, self).__init__(scene, mode=Actor.RenderMode.Triangles, **kwargs)
        self._filename = kwargs.get("filename", "obj-models/buildings/2.obj")
        fn = self._filename.split('.')
        self._filename = fn[0]

        self._vertices = None
        self._normals = None
        self._texcoords = None
        self._colors = None
        self._rgb_colors = True

        if self._rgb_colors:
            self.setSolidShader(self.shaderCollection.attributeColorPhongShader())
            self.setSolidFlatShader(self.shaderCollection.attributeColorPhongFlatShader())
            self.setNoLightSolidShader(self.shaderCollection.attributeColorShader())
            self.setWireframeShader(self.shaderCollection.attributeColorPhongShader())

        ## create actor
        self.initialize()


    @classmethod
    def isSelectable(self):
        """Returns true if actor is selectable"""
        return True


    def generateGeometry(self):
        v_ = []
        pointMin_x = math.inf
        pointMin_y = math.inf
        pointMin_z = math.inf
        pointMax_x = -math.inf
        pointMax_y = -math.inf
        pointMax_z = -math.inf
        arq = open(self._filename + ".obj", "r")
        for line in arq:
            if line.startswith('#'):
                continue
            values = line.split()
            if not values:
                continue
            if values[0] != 'v':
                continue
            else:
                v_.append([float(values[1]), float(values[2]), float(values[3])])
                if float(values[1]) < pointMin_x:
                    pointMin_x = float(values[1])
                if float(values[2]) < pointMin_y:
                    pointMin_y = float(values[2])
                if float(values[3]) < pointMin_z:
                    pointMin_z = float(values[3])

                if float(values[1]) > pointMax_x:
                    pointMax_x = float(values[1])
                if float(values[2]) > pointMax_y:
                    pointMax_y = float(values[2])
                if float(values[3]) > pointMax_z:
                    pointMax_z = float(values[3])
        arq.close()
        self.setPointMin(QVector3D(pointMin_x, pointMin_y, pointMin_z))
        self.setPointMax(QVector3D(pointMax_x, pointMax_y, pointMax_z))
        self.setCenter()
        self.setSize()

        vertices = []
        n = []
        t = []
        normals = []
        texture = []
        colors = []
        arq = open(self._filename + ".obj", "r")
        
        for line in arq:
            if line.startswith('#'):
                continue
            values = line.split()
            if not values:
                continue
            if values[0] == 'mtllib':
                self.mtl = values[1]
            elif values[0] == 'v':
                continue
            elif values[0] == 'vn':
                n.append([float(values[1]), float(values[2]), float(values[3])])
            elif values[0] == 'vt':
                t.append([float(values[1]), float(values[2])])
            elif values[0] in ('usemtl', 'usemat'):
                color = getMaterial(self._filename, values[1])
            elif values[0] == 'f':
                face = []
                if len(values[1:]) == 4:
                    for v in values[1:]:
                        w = v.split('/')
                        face.append(int(w[0])-1)
                        colors[int(w[0])-1] = color
                        if len(w) >= 2 and len(w[1]) > 0:
                            texture[int(w[0])-1] = t[int(w[1]) -1]
                        if len(w) >= 3 and len(w[2]) > 0:
                            normals[int(w[0])-1] = n[int(w[2])-1]
                    vertices.append(v_[face[0]])
                    vertices.append(v_[face[1]]) 
                    vertices.append(v_[face[2]])
                    vertices.append(v_[face[2]]) 
                    vertices.append(v_[face[3]]) 
                    vertices.append(v_[face[0]])
                    #falta ver as normais
                else:
                    for v in values[1:]:
                        w = v.split('/')
                        vertices.append(v_[int(w[0])-1])
                        colors.append(color)
                        if len(w) >= 2 and len(w[1]) > 0:
                            texture.append(t[int(w[1]) -1])
                        if len(w) >= 3 and len(w[2]) > 0:
                            normals.append(n[int(w[2])-1])
                        else:
                            normals.append(n[33])
        arq.close()

        self._vertices = np.array(vertices, dtype=np.float32)
        self._normals = np.array(normals, dtype=np.float32)
        self._texcoords = np.array(texture, dtype=np.float32)
        self._colors = np.array(colors, dtype=np.float32)


    def initialize(self):
        """Creates Obj's geometry"""
        if self._vertices is None:
            self.generateGeometry()

        ## create object
        self.create(vertices=self._vertices, 
            colors=self._colors,
            normals=self._normals,
            texcoords=self._texcoords)


    def render(self):
        """Render Obj"""
        GL.glDrawArrays(self._render_mode, 0, len(self._vertices))

    
