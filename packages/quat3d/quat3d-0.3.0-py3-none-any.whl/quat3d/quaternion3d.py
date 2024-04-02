import os
import logging

import numpy as np
import stl

from PyQt6.QtCore import QThread, pyqtSignal
from PyQt6.QtGui import QColor, QPixmap, QIcon, QAction, QQuaternion
from PyQt6.QtWidgets import QApplication, QMenu
from PyQt6.QtWidgets import QMainWindow, QMessageBox, QColorDialog
import pyqtgraph.opengl as gl

import genlib.udp as udp


XNODE_CODE="""import time
from pop.core  import Uart
from pop.ext import IMU

imu = IMU()

imu.init()
    
while True:
    w, x, y, z = imu.read(IMU.QUATERNION)
    data = "{} {} {} {}".format(w, x, y, z)
    Uart.write(data, slip=True)
    
    # This is an optimized value for 
    # visualizations up to 65 frames.
    time.sleep_ms(20)
"""

ABOUT = "Version: 1.0.0\n\nPySide6: 6.6.2\nPyOpenGL: 3.1.7\npyqtgraph: 0.13.4\n\n@PlanX Labs. 2024"


class ReadThread(QThread):
    readSignal = pyqtSignal(object)
    
    def __init__(self, mainWindow, group, iport, mcast, log_name):
        super().__init__()
        
        mainWindow.closeSignal.connect(self.onClose)
                
        if mcast:
            self.__socket = udp.MulticastReceiver(group=group, port=iport)
        else:
            self.__socket = udp.UDPServer(port=iport)

        self.__is_run = True
        self.__log_name = log_name  
        
    def onClose(self):
        self.__is_run = False
                
    def run(self):
        while self.__is_run:
            message = self.__socket.recvFrom(unpickling=True, timeout=0.001)
            if message:                
                data = [float(n) for n in message.payload.replace(',', ' ').split(' ')]
                self.readSignal.emit(data[:4])

            self.usleep(100)

class Quaternion3D(QMainWindow):
    SPHERE = 0
    JET_AIRPLANE = 1
    
    closeSignal = pyqtSignal()
    
    def __init__(self, group, iport, mcast, clipboard, log_name):
        super().__init__()
        
        self.readThread = ReadThread(self, group, iport, mcast, log_name)
        self.readThread.readSignal.connect(self.onDraw)
        self.readThread.start()
        self.clipboard = clipboard
        self.__log_name = log_name
        
        self.initGUI()

    def closeEvent(self, event):
        self.closeSignal.emit()
          
    def __change_object(self, object):
        self.object = object

        if object == self.SPHERE:
            self.gl_view.setCameraPosition(distance=3)
            mesh_data = self.sphere_mesh_data
        elif object == self.JET_AIRPLANE:
            self.gl_view.setCameraPosition(distance=150, elevation=0)
            mesh_data = self.air_plane_mesh_data
        else:
            return 

        self.mesh_item.setMeshData(meshdata=mesh_data, smooth=False, shader="normalColor")

    def onSphere(self):
        if self.object != self.SPHERE:
            self.__change_object(self.SPHERE)
            self.jet_airplane_action.setCheckable(False)
            self.sphere_action.setCheckable(True)

        self.sphere_action.setChecked(True)  
        
    def onJetAirPlane(self):
        if self.object != self.JET_AIRPLANE:
            self.__change_object(self.JET_AIRPLANE)
            self.sphere_action.setCheckable(False)
            self.jet_airplane_action.setCheckable(True)
        
        self.jet_airplane_action.setChecked(True)
    
    def onBgColor(self):
        dlg = QColorDialog(self)
        dlg.setOption(QColorDialog.ColorDialogOption.ShowAlphaChannel, on=True)
        dlg.setCurrentColor(self.bg_color)
        dlg.currentColorChanged.connect(lambda: self.gl_view.setBackgroundColor(dlg.currentColor()))
        dlg.rejected.connect(lambda: self.gl_view.setBackgroundColor(self.bg_color))

        if dlg.exec():
            self.bg_color = dlg.currentColor()

    def onXnodeCode(self):
        msgbox = QMessageBox(self)        
        msgbox.setIconPixmap(QPixmap(os.path.join(os.path.dirname(__file__), "quat_xnode_code.png")))
        msgbox.setWindowTitle("The code below needs to be run on XNode.")
        copy_bt = msgbox.addButton("Copy", QMessageBox.ButtonRole.YesRole)
        copy_bt.clicked.connect(lambda : self.clipboard.setText(XNODE_CODE))
        msgbox.addButton("Ok", QMessageBox.ButtonRole.YesRole)        
        msgbox.exec()

    def onDraw(self, quat):    
        if self.old_quat == quat:
            return
                
        self.old_quat = quat
        
        q = QQuaternion(*quat).normalized()
        axis, angle = q.getAxisAndAngle()
                
        logging.getLogger(self.__log_name).info(f"{axis=}, {angle=}")    

        self.mesh_item.resetTransform()
        self.mesh_item.rotate(angle, axis.x(), axis.y(), axis.z())
        
    def initGUI(self):
        self.setWindowTitle("Quaternion 3D Viewer")
        self.resize(800, 600)
        self.setWindowIcon(QIcon(os.path.join(os.path.dirname(__file__), "quat.png")))
        
        self.initMenu()
            
        self.old_quat = (0.0, 0,0, 0,0, 0,0)        
        self.bg_color = QColor(0, 33, 50, 255) #RGBA
        self.object = self.SPHERE

        self.glView()       

    def initMenu(self):
        menubar = self.menuBar()
        file_menu = menubar.addMenu("&File")
        help_menu = menubar.addMenu("&Help")
        
        self.sphere_action = QAction("S&phere", self)
        self.sphere_action.setCheckable(True)
        self.sphere_action.setChecked(True)
        self.sphere_action.triggered.connect(self.onSphere)
        self.jet_airplane_action = QAction("&Jet AirPlane", self)
        self.jet_airplane_action.triggered.connect(self.onJetAirPlane)        
        change_bg_action = QAction("&Background Color", self)
        change_bg_action.triggered.connect(self.onBgColor)        
        exit_action = QAction("E&xit", self)
        exit_action.triggered.connect(QApplication.quit)
        
        xnode_code_action = QAction("XNode &Code", self)
        xnode_code_action.triggered.connect(self.onXnodeCode)        
        about_action = QAction("&About", self)
        about_action.triggered.connect(lambda: QMessageBox().information(self, "Quaternion 3D Viewer", ABOUT))

        object_menu = QMenu("&Object", self)
        file_menu.addMenu(object_menu)
        object_menu.addAction(self.sphere_action)
        object_menu.addAction(self.jet_airplane_action)
        
        file_menu.addAction(change_bg_action)
        file_menu.addAction(exit_action)
        help_menu.addAction(xnode_code_action)
        help_menu.addAction(about_action)

    def glView(self):
        self.gl_view = gl.GLViewWidget(self)
        self.setCentralWidget(self.gl_view)
        self.gl_view.setBackgroundColor(self.bg_color)
        
        self.sphere_mesh_data = gl.MeshData.sphere(rows=10, cols=20)

        stl_mesh = stl.mesh.Mesh.from_file(os.path.join(os.path.dirname(__file__), "jet.stl"))
        stl_mesh.translate([80, 25, -10]) 
        points = stl_mesh.points.reshape(-1, 3)
        faces = np.arange(points.shape[0]).reshape(-1, 3)
        self.air_plane_mesh_data = gl.MeshData(vertexes=points, faces=faces)

        self.gl_view.setCameraPosition(distance=3)
        mesh_data = self.sphere_mesh_data
        self.mesh_item = gl.GLMeshItem(meshdata=mesh_data, smooth=False, shader="normalColor")
        self.gl_view.addItem(self.mesh_item)