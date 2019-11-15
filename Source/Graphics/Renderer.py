import math
import numpy as np

from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

from OpenGL import GL
from Source.Graphics.Trackball import Trackball
from Source.Graphics.Light import Light
from Source.Graphics.Camera import Camera
from Source.Graphics.Material import Material
from Source.Graphics.Scene import Scene
from Source.Graphics.Actor import Actor
from Source.Graphics.Group import Group
from Source.Graphics.Gnomon import Gnomon
from Source.Graphics.World import World
from Source.Graphics.Shaders import Shaders

# import actors
from Source.Graphics.Cone import Cone
from Source.Graphics.Cube import Cube
from Source.Graphics.Cylinder import Cylinder
from Source.Graphics.Icosahedron import Icosahedron
from Source.Graphics.Floor import Floor
from Source.Graphics.Sphere import Sphere
from Source.Graphics.SphereTessellation import SphereTessellation
from Source.Graphics.Obj import Obj
from Source.Graphics.Gizmos import Gizmos
import Source.Graphics.PyramidOne as PyramidOne
import Source.Graphics.PyramidTwo as PyramidTwo


from Source.Graphics.GizmosScale import GizmosScale 
from Source.Graphics.GizmosTranslate import GizmosTranslate 
from Source.Graphics.GizmosRotate import GizmosRotate

from enum import IntEnum

class Renderer(QOpenGLWidget):

    class ActorType(IntEnum):
        OBJ1 = 0,
        OBJ2 = 1,
        OBJ3 = 2,
        OBJ4 = 3,
        OBJ5 = 4,
        OBJ6 = 5,
        OBJ7 = 6,
        OBJ8 = 7,
        OBJ9 = 8,
        OBJ10 = 9,
        OBJ11 = 10,
        OBJ12 = 11,
        OBJ13 = 12,
        OBJ14 = 13
        

    ## initialization
    def __init__(self, parent=None, **kwargs):
        """Initialize OpenGL version profile."""
        super(Renderer, self).__init__(parent)

        self.setFocusPolicy(Qt.StrongFocus)

        self._parent = parent

        ## deal with options
        self._lighting = kwargs.get("lighting", True)
        self._antialiasing = kwargs.get("antialiasing", False)
        self._statistics = kwargs.get("statistics", True)

        ## define home orientation
        self._home_rotation = QQuaternion.fromAxisAndAngle(QVector3D(1.0, 0.0, 0.0), 25.0) * QQuaternion.fromAxisAndAngle(QVector3D(0.0, 1.0, 0.0), -50.0)

        ## define scene trackball
        self._trackball = Trackball(velocity=0.05, axis=QVector3D(0.0, 1.0, 0.0), mode=Trackball.TrackballMode.Planar, rotation=self._home_rotation, paused=True)

        ## define actor trackball
        self._actor_rotation = QQuaternion.fromAxisAndAngle(QVector3D(0.0, 1.0, 0.0), 1.0)  * QQuaternion.fromAxisAndAngle(QVector3D(0.0, 0.0, 1.0), -1.0) 
        self._trackball_actor = Trackball(velocity=0.01, axis=QVector3D(0.0, 1.0, 0.0), paused=True)
        
        ## create main scene
        self._world = World(self, home_position=QVector3D(0, 0, 3.5))

        ## do not animate
        self._animating = True

        ## not yet initialized
        self._initialized = False

        self.setAutoFillBackground(False)

        self.currentActor_ = None

        self._transform = None
        self._eixo = None
        self._gizmos = None


    def printOpenGLInformation(self, format, verbosity=0):
        print("\n*** OpenGL context information ***")
        print("Vendor: {}".format(GL.glGetString(GL.GL_VENDOR).decode('UTF-8')))
        print("Renderer: {}".format(GL.glGetString(GL.GL_RENDERER).decode('UTF-8')))
        print("OpenGL version: {}".format(GL.glGetString(GL.GL_VERSION).decode('UTF-8')))
        print("Shader version: {}".format(GL.glGetString(GL.GL_SHADING_LANGUAGE_VERSION).decode('UTF-8')))
        print("Maximum samples: {}".format(GL.glGetInteger(GL.GL_MAX_SAMPLES)))
        print("\n*** QSurfaceFormat from context ***")
        print("Depth buffer size: {}".format(format.depthBufferSize()))
        print("Stencil buffer size: {}".format(format.stencilBufferSize()))
        print("Samples: {}".format(format.samples()))
        print("Red buffer size: {}".format(format.redBufferSize()))
        print("Green buffer size: {}".format(format.greenBufferSize()))
        print("Blue buffer size: {}".format(format.blueBufferSize()))
        print("Alpha buffer size: {}".format(format.alphaBufferSize()))
            #print("\nAvailable extensions:")
            #for k in range(0, GL.glGetIntegerv(GL.GL_NUM_EXTENSIONS)-1):
            #    print("{},".format(GL.glGetStringi(GL.GL_EXTENSIONS, k).decode('UTF-8')))
            #print("{}".format(GL.glGetStringi(GL.GL_EXTENSIONS, k+1).decode('UTF-8')))


    def initializeGL(self):
        """Apply OpenGL version profile and initialize OpenGL functions.""" 	
        if not self._initialized:
            self.printOpenGLInformation(self.context().format())
        
            ## create gnomon
            self._gnomon = Gnomon(self)
            
            ## update cameras
            self._world.camera.setRotation(self._trackball.rotation().inverted())
            self._gnomon.camera.setRotation(self._trackball.rotation().inverted())

  
            GL.glEnable(GL.GL_DEPTH_TEST)
            GL.glEnable(GL.GL_DEPTH_CLAMP)
            #GL.glEnable(GL.GL_CULL_FACE)
            GL.glEnable(GL.GL_MULTISAMPLE)
            GL.glEnable(GL.GL_FRAMEBUFFER_SRGB)
            
            ## attempt at line antialising
            if self._antialiasing:
        
                GL.glEnable(GL.GL_POLYGON_SMOOTH)
                GL.glEnable(GL.GL_BLEND)

                GL.glBlendFunc(GL.GL_SRC_ALPHA, GL.GL_ONE_MINUS_SRC_ALPHA)
                GL.glHint(GL.GL_LINE_SMOOTH_HINT, GL.GL_NICEST)
                GL.glHint(GL.GL_POLYGON_SMOOTH_HINT, GL.GL_NICEST)

                GL.glPointSize(5)
                GL.glLineWidth(1)

            ## clear color
            GL.glClearColor(0.75, 0.76, 0.76, 0.0)

            ## initialize scene
            self._world.initialize()

            ## initialize gnomon
            self._gnomon.initialize()

            ## timer for immediate update
            self._timer = QTimer(self)
            self._timer.setTimerType(Qt.PreciseTimer)
            self._timer.timeout.connect(self.updateScene)
            self._timer.start()

            ## timer for measuring elapsed time
            self._elapsed_timer = QElapsedTimer()
            self._elapsed_timer.restart()
            self._frameElapsed = 0
            self._gpuElapsed = 0

            self._initialized = True

            ###
            ### Add an object to the scene
            ###
            self.currentActor_ = Obj(self._world)
            self._world.addActor(self.currentActor_)
            self._sub = 1
            self._radius = 1.0
            self._v = 10
            self._h = 10
            self._indexActor = 0
            ###


        else:
            
            ## initialize scene
            self._world.initialize()

            ## initialize gnomon
            self._gnomon.initialize()

        ## initialize OpenGL timer
        self._query = GL.glGenQueries(1)


    def clear(self):
        """Clear scene"""
        self._world.clear()
        self.update()


    def renderTimeEstimates(self):
        return [self._frameElapsed, self._gpuElapsed]


    @property
    def lighting(self):
        return self._lighting


    def setDrawStyle(self, style):
        self._draw_style = style


    def activeSceneCamera(self):
        """Returns main scene camera"""
        return self._world.camera


    def setAnimating(self, value):
        """Sets continuous update"""
        self._animating = value


    def isAnimating(self):
        """Returns whether continous update is active"""
        return self._animating


    def updateScene(self):
        """Schedule an update to the scene"""
        if self.isAnimating():
            self.update()


    def renderScene(self):
        """Draw main scene"""

        ## set scene rotation
        self._world.camera.setRotation(self._trackball.rotation().inverted())
        self._gnomon.camera.setRotation(self._trackball.rotation().inverted())

        self._world.render()

        ## render gnomon
        self._gnomon.render()

    
    def paintGL(self):
        """Draw scene"""

        ## record render time statistics
        if self._statistics:

            ## begin GPU time query
            GL.glBeginQuery(GL.GL_TIME_ELAPSED, self._query)

            ## render scene
            self.renderScene()

            ## finish GPU time query
            GL.glEndQuery(GL.GL_TIME_ELAPSED)

            ## record render time statistics, need to stall the CPU a bit
            ready = False 
            while not ready:
                ready = GL.glGetQueryObjectiv(self._query, GL.GL_QUERY_RESULT_AVAILABLE)
            self._gpuElapsed = GL.glGetQueryObjectuiv(self._query, GL.GL_QUERY_RESULT ) / 1000000.0

            ## delete query object
            #GL.glDeleteQueries( self._query )

        else:

            ## render scene
            self.renderScene()

        self._frameElapsed = self._elapsed_timer.restart()


    def resizeGL(self, width, height):
        """ Called by the Qt libraries whenever the window is resized"""
        self._world.camera.setAspectRatio(width / float(height if height > 0.0 else 1.0))


    def pan(self, point, state='start'):
        """Move camera according to mouse move"""
        if state == 'start':
            self._lastPanningPos = point
        elif state == 'move':
            delta = QLineF(self._lastPanningPos, point)
            self._lastPanningPos = point
            direction = QVector3D(-delta.dx(), -delta.dy(), 0.0).normalized()
            newpos = self._world.camera.position + delta.length()*2.0 * direction
            self._world.camera.setPosition(newpos)



    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Escape:
            self._world.selectActor(None)
            self._world.highlightActor(None)
            self._transform = None
            self._eixo = None
            if self._gizmos is not None:
                self._world.removeActor(self._gizmos)
                self._gizmos = None
        
        new_actor = self._world.selectedActor()
        if new_actor is not None:
            if event.key() == Qt.Key_Delete:
                    self.removeSelected(new_actor)
            if self._transform is None:
                if event.text() in ("x", "X"):
                    self.removeSelected(new_actor)
                             
            elif event.text() in ("x", "X", "y", "Y", "z", "Z"):
                self._eixo = event.text()
                self.gizmosUpdate(new_actor)

            if event.text() in ("s", "S") and new_actor is not None:
                self._transform = event.text()
                self._eixo = None
                self.gizmosUpdate(new_actor)

            elif event.text() in ("t", "T") and new_actor is not None:
                self._transform = event.text()
                self._eixo = None
                self.gizmosUpdate(new_actor)

            elif event.text() in ("r", "R") and new_actor is not None:
                self._transform = event.text()
                self._eixo = None
                self.gizmosUpdate(new_actor)

    def removeSelected(self,new_actor):
        self._world.selectActor(None)
        self._world.highlightActor(None)
        self._transform = None
        self._eixo = None
        self._world.removeActor(new_actor)
        if self._gizmos is not None:
            self._world.removeActor(self._gizmos)
            self._gizmos = None

    def gizmosUpdate(self, new_actor):
        if self._gizmos is not None:
            self._world.removeActor(self._gizmos)
            self._gizmos = None 
        size = new_actor.size()/2 +  QVector3D(1.0,1.0,1.0)
        center = new_actor.center()
        transf = new_actor.transform()
        eixo = self._eixo
        if self._transform in ("R", "r"):
            eixo = None
            

        self.makeCurrent()
        if self._transform in ("s", "S"):
            self._gizmos = GizmosScale(self._world, transform=transf, center=center, size=size, eixo=eixo)
            self._world.addActor(self._gizmos)
        elif self._transform in ("t", "T"):
            self._gizmos = GizmosTranslate(self._world, transform=transf, center=center, size=size, eixo= eixo)
            self._world.addActor(self._gizmos)
        elif self._transform in ("r", "R"):
            self._gizmos = GizmosRotate(self._world, transform=transf, center=center, size=size, eixo= eixo)
            self._world.addActor(self._gizmos)
        


    def mousePressEvent(self, event):
        """ Called by the Qt libraries whenever the window receives a mouse click."""
        super(Renderer, self).mousePressEvent(event)
        
        if event.buttons() == Qt.LeftButton:
            point = self._pixelPosToViewPos(event.localPos())
            new_actor = self._world.pick(point)[0]

            if new_actor == None:
                self._world.selectActor(new_actor)
                self._world.highlightActor(new_actor)    
                self._transform = None
                self._eixo = None 
                if self._gizmos is not None:
                    self.makeCurrent()
                    self._world.removeActor(self._gizmos)
                    self._gizmos = None                         


        if event.buttons()== Qt.LeftButton and QApplication.keyboardModifiers() == Qt.ShiftModifier:
            point = self._pixelPosToViewPos(event.localPos())
            new_actor = self._world.pick(point)[0]

            self._world.selectActor(new_actor)
            self._world.highlightActor(new_actor)
                

        if self._world.selectedActor() is None:
            if event.isAccepted():
                return

            if event.buttons() & Qt.LeftButton:
                self._trackball.press(self._pixelPosToViewPos(event.localPos()), QQuaternion())
                self._trackball.start()
                event.accept()
                if not self.isAnimating():
                    self.update()

            elif event.buttons() & Qt.RightButton:
                self.pan(self._pixelPosToViewPos(event.localPos()), state='start')
                self.update()
        else:
            if self._transform in ("r", "R"):
                self._trackball_actor.press(self._pixelPosToViewPos(event.localPos()), QQuaternion())
                self._trackball_actor.start()
                event.accept()
                xform = QMatrix4x4()
                quaternion = self._trackball_actor.rotation()
                xform.rotate(quaternion)
                actor = self._world.selectedActor() 
                xform = actor.transform() * xform
                actor.update(transform=xform)
                self.gizmosUpdate(actor)


    def mouseMoveEvent(self, event):
        """Called by the Qt libraries whenever the window receives a mouse move/drag event."""
        super(Renderer, self).mouseMoveEvent(event)
        if self._world.selectedActor() is None:
            if event.isAccepted():
                return

            if event.buttons() & Qt.LeftButton:
                self._trackball.move(self._pixelPosToViewPos(event.localPos()), QQuaternion())
                event.accept()
                if not self.isAnimating():
                    self.update()

            elif event.buttons() & Qt.RightButton:
                self.pan(self._pixelPosToViewPos(event.localPos()), state='move')
                self.update()
        else: 
            if event.buttons() & Qt.LeftButton:
                actor = self._world.selectedActor()
                xform = actor.transform()
                if self._transform in ("T", "t") and self._eixo is not None:
                    point = self._pixelPosToViewPos(event.localPos())
                    if self._eixo in ("x", "X"):
                        xform.translate(point.x(), 0, 0)
                    elif self._eixo in ("y", "Y"):
                        xform.translate(0, point.y(), 0)
                    else:
                        xform.translate(0, 0, -point.x())
                    actor.update(transform=xform)
                    self.gizmosUpdate(actor)
                elif self._transform in ("r", "R"):
                    self._trackball_actor.move(self._pixelPosToViewPos(event.localPos()), QQuaternion())
                    event.accept()
                    quaternion = self._trackball_actor.rotation()
                    xform.rotate(quaternion)
                    actor.update(transform=xform)
                    self.gizmosUpdate(actor)


    def mouseReleaseEvent(self, event):
        """ Called by the Qt libraries whenever the window receives a mouse release."""
        super(Renderer, self).mouseReleaseEvent(event)
        if self._world.selectedActor() is None:
            if event.isAccepted():
                return

            if event.button() == Qt.LeftButton:
                self._trackball.release(self._pixelPosToViewPos(event.localPos()), QQuaternion())
                event.accept()
                if not self.isAnimating():
                    self._trackball.stop()
                    self.update()
        else:
            if self._transform in ("r", "R"):
                self._trackball_actor.release(self._pixelPosToViewPos(event.localPos()), QQuaternion())
                event.accept()
                xform = QMatrix4x4()
                quaternion = self._trackball_actor.rotation()
                xform.rotate(quaternion)
                actor = self._world.selectedActor() 
                xform = actor.transform() * xform
                actor.update(transform=xform)
                self.gizmosUpdate(actor)
        
        

    def wheelEvent(self, event):
        """Process mouse wheel movements"""
        super(Renderer, self).wheelEvent(event)
        if self._world.selectedActor() is None:
            self.zoom(-event.angleDelta().y() / 950.0)
            event.accept()
            ## scene is dirty, please update
            self.update()
        else:
            if self._transform in ("s", "S"):
                actor = self._world.selectedActor()
                xform = QMatrix4x4() 
                factorscale =  math.exp(-event.angleDelta().y() / 950.0)
                if self._eixo is None:
                    xform.scale(factorscale)
                elif self._eixo in ("x", "X"):
                    xform.scale(factorscale, 1, 1)
                elif self._eixo in ("y", "Y"):
                    xform.scale(1, factorscale, 1)
                elif self._eixo in ("z", "Z"):
                    xform.scale(1, 1, factorscale)
                xform = actor.transform() * xform
                actor.update(transform=xform)
                self.gizmosUpdate(actor)


    def zoom(self, diffvalue):
        """Zooms in/out the active camera"""
        multiplicator = math.exp(diffvalue)

        ## get a hold of the current active camera
        camera = self._world.camera
        
        if camera.lens == Camera.Lens.Orthographic:
            # Since there's no perspective, "zooming" in the original sense
            # of the word won't have any visible effect. So we just increase
            # or decrease the field-of-view values of the camera instead, to
            # "shrink" the projection size of the model / scene.
            camera.scaleHeight(multiplicator)

        else:
        
            old_focal_dist = camera.focalDistance
            new_focal_dist = old_focal_dist * multiplicator

            direction = camera.orientation * QVector3D(0.0, 0.0, -1.0)
            newpos = camera.position + (new_focal_dist - old_focal_dist) * -direction

            camera.setPosition(newpos)
            camera.setFocalDistance(new_focal_dist)


    def viewFront(self):
        """Make camera face the front side of the scene"""
        self._trackball.reset(QQuaternion())
        self.update()
        

    def viewBack(self):
        """Make camera face the back side of the scene"""
        self._trackball.reset(QQuaternion.fromAxisAndAngle(QVector3D(0.0, 1.0, 0.0), 180.0))
        self.update()


    def viewLeft(self):
        """Make camera face the left side of the scene"""
        self._trackball.reset(QQuaternion.fromAxisAndAngle(QVector3D(0.0, 1.0, 0.0), -90.0))
        self.update()


    def viewRight(self):
        """Make camera face the right side of the scene"""
        self._trackball.reset(QQuaternion.fromAxisAndAngle(QVector3D(0.0, 1.0, 0.0), 90.0))
        self.update()


    def viewTop(self):
        """Make camera face the top side of the scene"""
        self._trackball.reset(QQuaternion.fromAxisAndAngle(QVector3D(1.0, 0.0, 0.0), 90.0))
        self.update()


    def viewBottom(self):
        """Make camera face the bottom side of the scene"""
        self._trackball.reset(QQuaternion.fromAxisAndAngle(QVector3D(1.0, 0.0, 0.0), -90.0))
        self.update()

    
    def createGridLines(self):
        """Set gridlines"""
        self.makeCurrent()
        self._world.createGridLines()
        self.doneCurrent()


    def cameraLensChanged(self, lens):
        """Switch world's. camera lens"""
        self._world.setCameraLens(lens)
        self._gnomon.setCameraLens(lens)
        self.update()


    def storeCamera(self):
        """Store world's camera parameters"""
        self._world.storeCamera()


    def recallCamera(self):
        """Recall camera parameters"""
        self._world.recallCamera()
        self._trackball.reset(self._world.camera.rotation.inverted())
        self.update()


    def resetCamera(self):
        """Reset world's camera parameters"""
        self._world.resetCamera()
        self._trackball.reset(self._home_rotation)
        self.update()


    def drawStyleChanged(self, index):
        self._world.setDrawStyle(Scene.DrawStyle.Styles[index])
        self.update()


    def lightingChanged(self, state):
        self._world.setLighting(state)
        self.update()

    
    def shadingChanged(self, index):
        self._world.setShading(Scene.Shading.Types[index])
        self.update()


    def headLightChanged(self, state):
        self._world.light.setHeadLight(state)
        self.update()


    def directionalLightChanged(self, state):
        self._world.light.setDirectional(state)
        self.update()

    
    def enableProfiling(self, enable):
        self._statistics = enable


    def enableAnimation(self, enable):
        self.setAnimating(enable)
        if not enable:
            self._trackball.stop()

    def _pixelPosToViewPos(self, point):
        return QPointF(2.0 * float(point.x()) / self.width() - 1.0, 1.0 - 2.0 * float(point.y()) / self.height())

    def setSubvisionLevel(self, val):
        self._sub = val
        self.makeCurrent()
        self.currentActor_.setSubdivisionLevel(val)
        self.update()

    def setRadius(self, val):
        self._radius = val
        self.changeActor(self._indexActor)

    def setH(self, val):
        self._h = val
        self.changeActor(self._indexActor)

    def setV(self, val):
        self._v = val
        self.changeActor(self._indexActor)

    def changeActor(self, index):
        self._indexActor = index
        self.makeCurrent()
        
        if index == Renderer.ActorType.OBJ1:
            self.currentActor_ = Obj(self._world, filename="obj-models/buildings/1.obj")
        elif index == Renderer.ActorType.OBJ2:
            self.currentActor_ = Obj(self._world, filename="obj-models/buildings/2.obj")
        elif index == Renderer.ActorType.OBJ3:
            self.currentActor_ = Obj(self._world, filename="obj-models/buildings/3.obj")
        elif index == Renderer.ActorType.OBJ4:
            self.currentActor_ = Obj(self._world, filename="obj-models/buildings/4.obj")
        elif index == Renderer.ActorType.OBJ5:
            self.currentActor_ = Obj(self._world, filename="obj-models/buildings/5.obj")
        elif index == Renderer.ActorType.OBJ6:
            self.currentActor_ = Obj(self._world, filename="obj-models/buildings/6.obj")
        elif index == Renderer.ActorType.OBJ7:
            self.currentActor_ = Obj(self._world, filename="obj-models/buildings/7.obj")
        elif index == Renderer.ActorType.OBJ8:
            self.currentActor_ = Obj(self._world, filename="obj-models/buildings/8.obj")
        elif index == Renderer.ActorType.OBJ9:
            self.currentActor_ = Obj(self._world, filename="obj-models/buildings/9.obj")
        elif index == Renderer.ActorType.OBJ10:
            self.currentActor_ = Obj(self._world, filename="obj-models/buildings/10.obj")
        elif index == Renderer.ActorType.OBJ11:
            self.currentActor_ = Obj(self._world, filename="obj-models/buildings/11.obj")
        elif index == Renderer.ActorType.OBJ12:
            self.currentActor_ = Obj(self._world, filename="obj-models/buildings/12.obj")
        elif index == Renderer.ActorType.OBJ13:
            self.currentActor_ = Obj(self._world, filename="obj-models/buildings/13.obj")
        elif index == Renderer.ActorType.OBJ14:
            self.currentActor_ = Obj(self._world, filename="obj-models/low-poly-mill/low-poly-mill.obj")


        self._world.addActor(self.currentActor_)
        

