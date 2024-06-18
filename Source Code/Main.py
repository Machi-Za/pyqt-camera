import cv2
import os
from datetime import datetime
from Main_Designer import Ui_Main
from PyQt5 import QtWidgets,QtCore, QtGui

class Main(QtWidgets.QMainWindow, Ui_Main):
    def __init__(main, parent=None):
        super(Main, main).__init__(parent)
        main.setupUi(main)

        main.cap = None
        main.camera = 0
        main.capture = 0
        main.id = 0

        def time():
            now = datetime.now()
            Y = now.strftime("%y")
            M = now.month
            D = now.day
            H = now.hour
            E = now.minute
            S = now.second
            times = f"{Y}{M}{D}_{H}{E}{S}"
            return times
    
        def Camera():
            cap = cv2.VideoCapture(main.id)
            while (cap.isOpened()):
                ret, frame = cap.read()
                if ret == True:
                    rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                    bgr = cv2.cvtColor(rgb, cv2.COLOR_RGB2BGR)

                    h, w, ch = rgb.shape
                    fps = ch * w
                    image = QtGui.QImage(rgb.data, w, h, fps, QtGui.QImage.Format_RGB888)
                    images= QtGui.QPixmap.fromImage(image)
                    main.Cam_View.setPixmap(images.scaled(main.Cam_View.width(), main.Cam_View.height(), QtCore.Qt.KeepAspectRatio))

                    if cv2.waitKey(1) and main.capture == 1:
                        main.Cam_Preview.clear()
                        filename = '{}.jpg'.format(time())
                        directory= "Pictures/"
                        cv2.imwrite(directory + filename, bgr)
                        
                        saved_image = QtGui.QImage(rgb.data, rgb.shape[1], rgb.shape[0],rgb.shape[1] * rgb.shape[2], QtGui.QImage.Format_RGB888)
                        saved_pixmap = QtGui.QPixmap.fromImage(saved_image)
                        main.Cam_Preview.setPixmap(saved_pixmap.scaled(main.Cam_Preview.width(), main.Cam_Preview.height(),QtCore.Qt.KeepAspectRatio))
                                                    
                        main.capture = 0
                    
                    if cv2.waitKey(1) and main.camera == 0:
                        main.Cam_View.clear()
                        main.Cam_Preview.clear()
                        main.Cam_View.setText("No Device")
                        cap.release()
                        break
                else:
                    main.Cam_View.clear()
                    main.Cam_Preview.clear()
                    main.Cam_View.setText("No Device")                    
                    cap.release()
                    break
            cv2.destroyAllWindows()

        def List_Camera():
            main.Cbx_Camera.clear()
            index = 0
            while True:
                cap = cv2.VideoCapture(index, cv2.CAP_DSHOW)
                if cap.isOpened():
                    main.Cbx_Camera.addItem(f"Camera {index}")
                elif not cap.isOpened():
                    break
                cap.release()
                index += 1

        def Main_Load():
            folder = "Pictures"
            if not os.path.exists(folder):
                os.makedirs(folder)
            List_Camera()
        Main_Load()

        main.Btn_Refresh.clicked.connect(lambda: Btn_Refresh_Click())
        def Btn_Refresh_Click():
            List_Camera()

        main.Btn_CameraOn.clicked.connect(lambda: Btn_CameraOn_Click())
        def Btn_CameraOn_Click():
            main.Btn_CameraOn.hide()
            main.Btn_CameraOff.show()
            main.camera = 1
            main.id = main.Cbx_Camera.currentIndex()
            Camera()

        main.Btn_CameraOff.clicked.connect(lambda: Btn_CameraOff_Click())
        def Btn_CameraOff_Click():
            main.Btn_CameraOff.hide()
            main.Btn_CameraOn.show()
            main.camera = 0

        main.Btn_Capture.clicked.connect(lambda: Btn_Capture_Click())
        def Btn_Capture_Click():
            if main.camera == 1:
                main.capture = 1